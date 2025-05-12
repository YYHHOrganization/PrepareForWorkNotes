import os
import sys
import logging
import datetime
import os.path as osp

from tqdm.auto import tqdm
from omegaconf import OmegaConf

import torch
import swanlab
import diffusers
import transformers
from torch.utils.tensorboard import SummaryWriter
from diffusers.optimization import get_scheduler

from mld.config import parse_args
from mld.data.get_data import get_dataset
from mld.models.modeltype.mld import MLD
from mld.utils.utils import print_table, set_seed, move_batch_to_device

os.environ["TOKENIZERS_PARALLELISM"] = "false"


def main():
    cfg = parse_args() # 解析命令行参数和配置文件
    device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
    set_seed(cfg.SEED_VALUE)

    # **** 3. 输出目录与实验记录 ***************
    name_time_str = osp.join(cfg.NAME, datetime.datetime.now().strftime("%Y-%m-%dT%H-%M-%S"))
    cfg.output_dir = osp.join(cfg.FOLDER, name_time_str)
    os.makedirs(cfg.output_dir, exist_ok=False) # 创建输出目录
    os.makedirs(f"{cfg.output_dir}/checkpoints", exist_ok=False)
    
    # 初始化可视化工具（TensorBoard/SwanLab）
    if cfg.vis == "tb":
        writer = SummaryWriter(cfg.output_dir)
    elif cfg.vis == "swanlab":
        writer = swanlab.init(project="MotionLCM",
                              experiment_name=os.path.normpath(cfg.output_dir).replace(os.path.sep, "-"),
                              suffix=None, config=dict(**cfg), logdir=cfg.output_dir)
    else:
        raise ValueError(f"Invalid vis method: {cfg.vis}")

    # ************ 4. 日志与配置文件保存 ***************
    # 配置日志记录
    stream_handler = logging.StreamHandler(sys.stdout)
    file_handler = logging.FileHandler(osp.join(cfg.output_dir, 'output.log'))
    handlers = [file_handler, stream_handler]
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
                        datefmt="%m/%d/%Y %H:%M:%S",
                        handlers=handlers)
    logger = logging.getLogger(__name__)

    OmegaConf.save(cfg, osp.join(cfg.output_dir, 'config.yaml')) # 保存配置文件

    transformers.utils.logging.set_verbosity_warning()
    diffusers.utils.logging.set_verbosity_info()

    assert cfg.model.is_controlnet, "cfg.model.is_controlnet must be true for controlling!"

    # ************ 5. 数据集加载 ***************
    dataset = get_dataset(cfg)
    train_dataloader = dataset.train_dataloader()
    val_dataloader = dataset.val_dataloader()

    # **************6. 模型初始化*********
    logger.info(f"Loading pretrained model: {cfg.TRAIN.PRETRAINED}")
    state_dict = torch.load(cfg.TRAIN.PRETRAINED, map_location="cpu")["state_dict"]
    lcm_key = 'denoiser.time_embedding.cond_proj.weight'

    # 检查是否为LCM（Latent Consistency Model）模式
    is_lcm = False
    if lcm_key in state_dict:
        is_lcm = True
        time_cond_proj_dim = state_dict[lcm_key].shape[1]
        cfg.model.denoiser.params.time_cond_proj_dim = time_cond_proj_dim
    logger.info(f'Is LCM: {is_lcm}')

    model = MLD(cfg, dataset)
    logger.info(model.load_state_dict(state_dict, strict=False))
    logger.info(model.controlnet.load_state_dict(model.denoiser.state_dict(), strict=False))

    # 冻结主模型参数，仅训练ControlNet和轨迹编码器
    model.vae.requires_grad_(False) # 冻结VAE
    model.text_encoder.requires_grad_(False)
    model.denoiser.requires_grad_(False)
    model.vae.eval() # 设置VAE为评估模式,将会影响dropout和batchnorm等层的行为
    model.text_encoder.eval()
    model.denoiser.eval()
    model.to(device)

    # ************ 7. 优化器和学习率调度器 ***************
    controlnet_params = list(model.controlnet.parameters())
    traj_encoder_params = list(model.traj_encoder.parameters())
    params = controlnet_params + traj_encoder_params
    params_to_optimize = [{'params': controlnet_params, 'lr': cfg.TRAIN.learning_rate},
                          {'params': traj_encoder_params, 'lr': cfg.TRAIN.learning_rate_spatial}]

    logger.info("learning_rate: {}, learning_rate_spatial: {}".
                format(cfg.TRAIN.learning_rate, cfg.TRAIN.learning_rate_spatial))

    optimizer = torch.optim.AdamW(
        params_to_optimize,
        betas=(cfg.TRAIN.adam_beta1, cfg.TRAIN.adam_beta2),
        weight_decay=cfg.TRAIN.adam_weight_decay,
        eps=cfg.TRAIN.adam_epsilon)

    if cfg.TRAIN.max_train_steps == -1:
        assert cfg.TRAIN.max_train_epochs != -1
        cfg.TRAIN.max_train_steps = cfg.TRAIN.max_train_epochs * len(train_dataloader)

    if cfg.TRAIN.checkpointing_steps == -1:
        assert cfg.TRAIN.checkpointing_epochs != -1
        cfg.TRAIN.checkpointing_steps = cfg.TRAIN.checkpointing_epochs * len(train_dataloader)

    if cfg.TRAIN.validation_steps == -1:
        assert cfg.TRAIN.validation_epochs != -1
        cfg.TRAIN.validation_steps = cfg.TRAIN.validation_epochs * len(train_dataloader)

    lr_scheduler = get_scheduler(
        cfg.TRAIN.lr_scheduler,
        optimizer=optimizer,
        num_warmup_steps=cfg.TRAIN.lr_warmup_steps,
        num_training_steps=cfg.TRAIN.max_train_steps)

    # Train!
    logger.info("***** Running training *****")
    logging.info(f"  Num examples = {len(train_dataloader.dataset)}")
    logging.info(f"  Num Epochs = {cfg.TRAIN.max_train_epochs}")
    logging.info(f"  Instantaneous batch size per device = {cfg.TRAIN.BATCH_SIZE}")
    logging.info(f"  Total optimization steps = {cfg.TRAIN.max_train_steps}")

    global_step = 0

    # ************ 9. 验证函数 ***************
    @torch.no_grad()
    def validation():
        model.controlnet.eval()
        model.traj_encoder.eval()
        val_loss_list = []
        for val_batch in tqdm(val_dataloader):
            val_batch = move_batch_to_device(val_batch, device)
            val_loss_dict = model.allsplit_step(split='val', batch=val_batch)
            val_loss_list.append(val_loss_dict)
        metrics = model.allsplit_epoch_end()
        for loss_k in val_loss_list[0].keys():
            metrics[f"Val/{loss_k}"] = sum([d[loss_k] for d in val_loss_list]).item() / len(val_dataloader)
        min_val_km = metrics['Metrics/kps_mean_err(m)']
        min_val_tj = metrics['Metrics/traj_fail_50cm']
        print_table(f'Validation@Step-{global_step}', metrics)
        for mk, mv in metrics.items():
            if cfg.vis == "tb":
                writer.add_scalar(mk, mv, global_step=global_step)
            elif cfg.vis == "swanlab":            
                writer.log({mk: mv}, step=global_step)
        model.controlnet.train()
        model.traj_encoder.train()
        return min_val_km, min_val_tj

    min_km, min_tj = validation()

    # ************ 8. 训练循环 ***************
    progress_bar = tqdm(range(0, cfg.TRAIN.max_train_steps), desc="Steps")
    while True:
        for step, batch in enumerate(train_dataloader):
            batch = move_batch_to_device(batch, device)
            loss_dict = model.allsplit_step('train', batch) # 前向计算损失

            diff_loss = loss_dict['diff_loss']
            cond_loss = loss_dict['cond_loss']
            rot_loss = loss_dict['rot_loss']
            loss = loss_dict['loss']
            
            # 反向传播与梯度裁剪
            loss.backward() # 反向传播
            torch.nn.utils.clip_grad_norm_(params, cfg.TRAIN.max_grad_norm) # 梯度裁剪
            optimizer.step()
            lr_scheduler.step()
            optimizer.zero_grad(set_to_none=True)

            # 记录训练指标
            progress_bar.update(1)
            global_step += 1

            # 保存检查点
            # 定期验证和保存模型
            if global_step % cfg.TRAIN.checkpointing_steps == 0:
                save_path = os.path.join(cfg.output_dir, 'checkpoints', f"checkpoint-{global_step}.ckpt")
                ckpt = dict(state_dict=model.state_dict())
                model.on_save_checkpoint(ckpt)
                torch.save(ckpt, save_path)
                logger.info(f"Saved state to {save_path}")

            # 验证与最优模型保存
            if global_step % cfg.TRAIN.validation_steps == 0:
                cur_km, cur_tj = validation() # 验证集评估
                if cur_km < min_km: # 保存最佳模型（基于关键点误差）
                    min_km = cur_km
                    save_path = os.path.join(cfg.output_dir, 'checkpoints', f"checkpoint-{global_step}-km-{round(cur_km, 3)}.ckpt")
                    ckpt = dict(state_dict=model.state_dict())
                    model.on_save_checkpoint(ckpt)
                    torch.save(ckpt, save_path)
                    logger.info(f"Saved state to {save_path} with km:{round(cur_km, 3)}")

                if cur_tj < min_tj:
                    min_tj = cur_tj
                    save_path = os.path.join(cfg.output_dir, 'checkpoints', f"checkpoint-{global_step}-tj-{round(cur_tj, 3)}.ckpt")
                    ckpt = dict(state_dict=model.state_dict())
                    model.on_save_checkpoint(ckpt)
                    torch.save(ckpt, save_path)
                    logger.info(f"Saved state to {save_path} with tj:{round(cur_tj, 3)}")

            logs = {"loss": loss.item(), "lr": lr_scheduler.get_last_lr()[0],
                    "diff_loss": diff_loss.item(), 'cond_loss': cond_loss.item(), 'rot_loss': rot_loss.item()}
            progress_bar.set_postfix(**logs)
            for k, v in logs.items():
                if cfg.vis == "tb":
                    writer.add_scalar(f"Train/{k}", v, global_step=global_step)
                elif cfg.vis == "swanlab":
                    writer.log({f"Train/{k}": v}, step=global_step)

            if global_step >= cfg.TRAIN.max_train_steps:
                save_path = os.path.join(cfg.output_dir, 'checkpoints', f"checkpoint-last.ckpt")
                ckpt = dict(state_dict=model.state_dict())
                model.on_save_checkpoint(ckpt)
                torch.save(ckpt, save_path)
                exit(0)


if __name__ == "__main__":
    main()
