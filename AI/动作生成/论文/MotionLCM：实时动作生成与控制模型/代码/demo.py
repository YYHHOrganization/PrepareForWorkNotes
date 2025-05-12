# 导入基础库
import os
import pickle
import sys
import datetime
import logging
import os.path as osp

# 配置管理
from omegaconf import OmegaConf  # 用于管理YAML配置文件

# PyTorch相关
import torch

# 项目内部模块
from mld.config import parse_args          # 配置文件解析
from mld.data.get_data import get_dataset  # 数据加载器
from mld.models.modeltype.mld import MLD   # 主模型类
from mld.models.modeltype.vae import VAE   # 变分自编码器基类
from mld.utils.utils import set_seed, move_batch_to_device  # 工具函数
from mld.data.humanml.utils.plot_script import plot_3d_motion  # 可视化
from mld.utils.temos_utils import remove_padding  # 数据后处理

# 环境设置
os.environ["TOKENIZERS_PARALLELISM"] = "false"  # 禁用tokenizer并行

def load_example_hint_input(text_path: str) -> tuple:
    """加载控制提示输入（用于ControlNet模式）
    Args:
        text_path: 控制提示文件路径
    Returns:
        (帧数列表, 控制类型ID列表, 提示ID列表)
    """
    # 文件格式示例：
    # 120 1 3  # 120帧，控制类型1，提示3
    # 60 2 5   # 60帧，控制类型2，提示5
    with open(text_path, "r") as f:
        lines = f.readlines()

    n_frames, control_type_ids, control_hint_ids = [], [], []
    for line in lines:
        s = line.strip()
        n_frame, control_type_id, control_hint_id = s.split(' ')
        n_frames.append(int(n_frame))
        control_type_ids.append(int(control_type_id))
        control_hint_ids.append(int(control_hint_id))

    return n_frames, control_type_ids, control_hint_ids

def load_example_input(text_path: str) -> tuple:
    """加载普通文本输入
    Args:
        text_path: 输入文本文件路径  
    Returns:
        (文本列表, 长度列表)
    """
    # 文件格式示例：
    # 120 A person is walking slowly  # 120帧对应文本
    # 60 Jumping twice                 # 60帧对应文本
    with open(text_path, "r") as f:
        lines = f.readlines()

    texts, lens = [], []
    for line in lines:
        s = line.strip()
        s_l = s.split(" ")[0]    # 提取帧数
        s_t = s[(len(s_l) + 1):] # 提取文本
        lens.append(int(s_l))
        texts.append(s_t)
    return texts, lens

def main():
    # 1. 配置初始化
    cfg = parse_args()  # 解析命令行参数和配置文件
    device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
    set_seed(cfg.SEED_VALUE)  # 设置随机种子

    # 2. 输出目录设置
    name_time_str = osp.join(cfg.NAME, "demo_" + datetime.datetime.now().strftime("%Y-%m-%dT%H-%M-%S"))
    cfg.output_dir = osp.join(cfg.TEST_FOLDER, name_time_str)
    vis_dir = osp.join(cfg.output_dir, 'samples')
    os.makedirs(cfg.output_dir, exist_ok=False)  # 严格创建新目录
    os.makedirs(vis_dir, exist_ok=False)

    # 3. 日志配置
    steam_handler = logging.StreamHandler(sys.stdout)
    file_handler = logging.FileHandler(osp.join(cfg.output_dir, 'output.log'))
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
                        datefmt="%m/%d/%Y %H:%M:%S",
                        handlers=[steam_handler, file_handler])
    logger = logging.getLogger(__name__)

    # 保存当前配置
    OmegaConf.save(cfg, osp.join(cfg.output_dir, 'config.yaml'))

    # 4. 模型加载
    state_dict = torch.load(cfg.TEST.CHECKPOINTS, map_location="cpu")["state_dict"]
    logger.info("Loading checkpoints from {}".format(cfg.TEST.CECKPOINTS))

    # 模型类型判断（关键修改点1：此处决定模型架构）
    # --------------------------------------------------
    is_vae = False
    vae_key = 'vae.skel_embedding.weight'  # VAE特有层
    if vae_key in state_dict:
        is_vae = True
    logger.info(f'Is VAE: {is_vae}')

    is_mld = False  
    mld_key = 'denoiser.time_embedding.linear_1.weight'  # MLD特有层
    if mld_key in state_dict:
        is_mld = True
    logger.info(f'Is MLD: {is_mld}')

    is_lcm = False
    lcm_key = 'denoiser.time_embedding.cond_proj.weight'  # LCM特有层
    if lcm_key in state_dict:
        is_lcm = True
        time_cond_proj_dim = state_dict[lcm_key].shape[1]
        cfg.model.denoiser.params.time_cond_proj_dim = time_cond_proj_dim  # 动态更新配置
    logger.info(f'Is LCM: {is_lcm}')

    # ControlNet检测（关键修改点2：控制网络加载）
    cn_key = "controlnet.controlnet_cond_embedding.0.weight"
    is_controlnet = True if cn_key in state_dict else False
    cfg.model.is_controlnet = is_controlnet  # 配置更新
    logger.info(f'Is Controlnet: {is_controlnet}')

    # 模型类选择
    if is_mld or is_lcm or is_controlnet:
        target_model_class = MLD  # 主模型类
    else:
        target_model_class = VAE  # 基线模型

    # 优化器配置（关键修改点3：噪声优化开关）
    if cfg.optimize:
        assert cfg.model.get('noise_optimizer') is not None
        cfg.model.noise_optimizer.params.optimize = True
        logger.info('Optimization enabled. Set the batch size to 1.')
        logger.info(f'Original batch size: {cfg.TEST.BATCH_SIZE}')
        cfg.TEST.BATCH_SIZE = 1  # 优化时batch必须为1

    # 5. 数据加载
    dataset = get_dataset(cfg)  # 获取数据集实例
    # ！！！！【入口】
    model = target_model_class(cfg, dataset)  # 初始化模型
    model.to(device)
    model.eval()
    model.requires_grad_(False)
    logger.info(model.load_state_dict(state_dict))  # 加载权重

    # 6. 生成参数
    FPS = eval(f"cfg.DATASET.{cfg.DATASET.NAME.upper()}.FRAME_RATE")  # 帧率获取

    # 7. 生成流程（关键修改点4：两种生成模式）
    if cfg.example is not None and not is_controlnet:
        # 模式A：示例文本生成
        text, length = load_example_input(cfg.example)
        for t, l in zip(text, length):
            logger.info(f"{l}: {t}")

        batch = {"length": length, "text": text}

        for rep_i in range(cfg.replication):  # 重复生成次数
            with torch.no_grad():
                joints = model(batch)[0]  # 生成关节数据

            # 保存结果
            num_samples = len(joints)
            for i in range(num_samples):
                res = dict()
                pkl_path = osp.join(vis_dir, f"sample_id_{i}_length_{length[i]}_rep_{rep_i}.pkl")
                res['joints'] = joints[i].detach().cpu().numpy()  # 转numpy
                res['text'] = text[i]
                res['length'] = length[i]
                res['hint'] = None
                with open(pkl_path, 'wb') as f:
                    pickle.dump(res, f)  # 序列化保存
                logger.info(f"Motions are generated here:\n{pkl_path}")

                # 可视化生成
                if not cfg.no_plot:
                    plot_3d_motion(pkl_path.replace('.pkl', '.mp4'),
                                 joints[i].detach().cpu().numpy(),
                                 text[i], fps=FPS)
    else:
        # 模式B：测试集批量生成
        test_dataloader = dataset.test_dataloader()
        for rep_i in range(cfg.replication):
            for batch_id, batch in enumerate(test_dataloader):
                batch = move_batch_to_device(batch, device)
                with torch.no_grad():
                    joints, joints_ref = model(batch)  # 生成及参考关节

                # 数据处理
                num_samples = len(joints)
                text = batch['text']
                length = batch['length']
                if 'hint' in batch:  # ControlNet模式处理
                    hint, hint_mask = batch['hint'], batch['hint_mask']
                    hint = dataset.denorm_spatial(hint) * hint_mask  # 去归一化
                    hint = remove_padding(hint, lengths=length)  # 移除填充
                else:
                    hint = None

                # 保存结果
                for i in range(num_samples):
                    res = dict()
                    pkl_path = osp.join(vis_dir, f"batch_id_{batch_id}_sample_id_{i}_length_{length[i]}_rep_{rep_i}.pkl")
                    res['joints'] = joints[i].detach().cpu().numpy()
                    res['text'] = text[i]
                    res['length'] = length[i]
                    res['hint'] = hint[i].detach().cpu().numpy() if hint is not None else None
                    with open(pkl_path, 'wb') as f:
                        pickle.dump(res, f)
                    logger.info(f"Motions are generated here:\n{pkl_path}")

                    # 可视化
                    if not cfg.no_plot:
                        plot_3d_motion(pkl_path.replace('.pkl', '.mp4'),
                                     joints[i].detach().cpu().numpy(),
                                     text[i], fps=FPS,
                                     hint=hint[i].detach().cpu().numpy() if hint is not None else None)

                    # 参考数据保存（仅第一次重复）
                    if rep_i == 0:
                        res['joints'] = joints_ref[i].detach().cpu().numpy()
                        with open(pkl_path.replace('.pkl', '_ref.pkl'), 'wb') as f:
                            pickle.dump(res, f)
                        logger.info(f"Reference motions saved:\n{pkl_path.replace('.pkl', '_ref.pkl')}")
                        if not cfg.no_plot:
                            plot_3d_motion(pkl_path.replace('.pkl', '_ref.mp4'),
                                         joints_ref[i].detach().cpu().numpy(),
                                         text[i], fps=FPS,
                                         hint=hint[i].detach().cpu().numpy() if hint is not None else None)

if __name__ == "__main__":
    main()
