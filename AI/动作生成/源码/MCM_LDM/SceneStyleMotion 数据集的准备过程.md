# SceneStyleMotion 数据集的准备过程

# 一、爬取数据+录制视频

略，主要是关键词检索，去网上搜索对应场景下的动作视频，保存为mp4格式，供VIBE识别和后面的管线的处理。



# 二、数据处理

整体的流程结构如下：

```python
关键是mp4视频->

​	VIBE估计出3D姿态，相机位姿等->

​		利用脚本对齐，估计相机位姿，平滑抖动+Foot相关处理，转为AMASS类似的数据格式->

​			打标签，和HumanML3D的处理方式类似，转换为网络支持的输入格式。
```

在这一部分中，会介绍VIBE估计姿态的环境配置、数据处理等过程，关键脚本在机器上，以及网盘当中。

## 1.配置VIBE相关的环境

VIBE的主页：https://github.com/mkocabas/VIBE

对应的指令分别如下（注意，在4090的AutoDL机器上，不用按照Github的安装步骤，按照下面这个即可,先在base环境下）：

```bash
git clone https://github.com/mkocabas/VIBE.git
pip install git+https://github.com/giacaglia/pytube.git --upgrade
pip install git+https://github.com/mattloper/chumpy.git
pip install git+https://github.com/mkocabas/yolov3-pytorch.git
pip install git+https://github.com/mkocabas/multi-person-tracker.git
pip install opencv-python
pip install numba
pip install --upgrade contourpy
pip install filterpy
```

然后下载对应的VIBE的权重数据：

```bash
./BaiduPCS-Go-v3.9.7-linux-amd64/BaiduPCS-Go download /AIFiles/VIBE/vibe_data.zip --saveto /root/autodl-tmp/VIBE/VIBE/data
```

以及我们的数据集数据（mp4格式），通过批处理脚本下载到指定路径下面：

```bash
#!/bin/bash

# BaiduPCS-Go 程序路径 (如果不在当前目录或PATH中，请修改)
PCS_GO_EXEC="./BaiduPCS-Go-v3.9.7-linux-amd64/BaiduPCS-Go"

# 定义日志文件路径
LOG_FILE="$(dirname "$0")/download_vibe_ourdataset.log"

# BDUSS (请替换为你的有效BDUSS)
# 强烈建议不要将 BDUSS 硬编码在脚本中，而是通过环境变量或其他安全方式传入
# 例如: export BDUSS="你的BDUSS值" 然后在脚本中 BDUSS_VALUE="${BDUSS}"
# 或者在运行脚本时作为参数传入
# 为简单起见，这里暂时硬编码，但请注意安全风险
BDUSS_VALUE="xxxxxxxxx"

# 远程目录
REMOTE_DATA_DIR="/AIFiles/VIBE/ourdataset/"
# 本地目标目录
LOCAL_TARGET_DIR="/root/autodl-tmp/VIBE/VIBE/ourdataset"


# 函数：记录日志并输出到终端
log() {
    local message="$1"
    echo "$(date '+%Y-%m-%d %H:%M:%S') - ${message}" | tee -a "$LOG_FILE"
}

# 1. 登录百度网盘账号
login_baidu() {
    local bduss_to_use="$1"
    if [ -z "${bduss_to_use}" ]; then
        log "错误：BDUSS 未提供。"
        return 1
    fi

    log "开始登录百度网盘账号..."
    # 捕获标准错误和标准输出
    login_output=$("${PCS_GO_EXEC}" login -bduss="${bduss_to_use}" 2>&1)

    if echo "${login_output}" | grep -q "登录成功"; then
        log "百度网盘登录成功"
        return 0
    else
        log "百度网盘登录失败"
        log "登录命令输出: ${login_output}"
        return 1
    fi
}

# 2. 下载指定远程目录下的所有文件
download_all_files_from_remote_dir() {
    local remote_dir="$1"
    local local_dir="$2"

    log "开始从远程目录 ${remote_dir} 下载所有文件到 ${local_dir}"

    # 确保本地目录存在
    mkdir -p "${local_dir}"
    if [ $? -ne 0 ]; then
        log "错误：无法创建本地目录 ${local_dir}"
        return 1
    fi

    log "正在执行: ${PCS_GO_EXEC} ls ${remote_dir}"
    file_list_output=$("${PCS_GO_EXEC}" ls "${remote_dir}" 2>&1)

    if [ $? -ne 0 ] || echo "${file_list_output}" | grep -qi "错误"; then
        log "错误：执行 ls 命令失败或返回错误。"
        log "ls 命令输出: ${file_list_output}"
        return 1
    fi

    log "BaiduPCS-Go ls 命令原始输出:"
    printf '%s\n' "${file_list_output}" | while IFS= read -r outline; do log "  ${outline}"; done

    # 解析文件名
    # 假设：
    # - 第一行是表头或无用信息，如 "当前目录: ..." 或 "----"
    # - 第二行是列名表头，如 "# 文件大小 修改日期 文件(目录)"
    # - 实际文件列表从第三行开始
    # - 文件名在第五列 (索引, 大小, 日期, 时间, 文件名)
    # *** 请务必根据你的实际 `BaiduPCS-Go ls "${remote_dir}"` 输出调整此 awk 命令 ***
    file_list=$(echo "${file_list_output}" | awk '
        NR > 2 && $1 ~ /^[0-9]+$/ { # 跳过前两行表头，并确保第一列是数字索引
            # 收集从第五个字段到最后一个字段的所有内容作为文件名（处理文件名中可能包含空格的情况）
            name="";
            for (i=5; i<=NF; i++) {
                name = name (name=="" ? "" : " ") $i;
            }
            if (name != "") print name;
        }
    ')
    # 如果文件名保证不含空格，且确定在第5列，可以简化为：
    # file_list=$(echo "${file_list_output}" | awk 'NR > 2 && $1 ~ /^[0-9]+$/ {print $5}')


    if [ -z "${file_list}" ]; then
        log "警告：未能从 ls 输出中解析出有效的文件名列表，或远程目录 ${remote_dir} 为空。"
        log "用于解析的 ls 命令原始输出（再次显示以供调试）:"
        printf '%s\n' "${file_list_output}" | while IFS= read -r outline; do log "  ${outline}"; done
        return 0 # 目录为空或无法解析，但不是致命错误，脚本可以继续
    fi

    log "解析后，找到以下文件需要下载:"
    printf '%s\n' "${file_list}" | while IFS= read -r line; do log "  - ${line}"; done

    local all_downloads_successful=true

    printf '%s\n' "${file_list}" | while IFS= read -r file_to_download; do
        if [ -z "${file_to_download}" ]; then
            continue
        fi

        # BaiduPCS-Go ls 列出的是文件名，不含父路径
        remote_file_path="${remote_dir}${file_to_download}"
        # 本地文件路径（BaiduPCS-Go --saveto 会处理在目录下创建同名文件）
        # local_file_full_path="${local_dir}/${file_to_download}"

        log "开始下载文件: ${remote_file_path} 到 ${local_dir}"

        # 检查本地文件是否已存在 (简单的跳过逻辑，可选)
        # if [ -f "${local_dir}/${file_to_download}" ]; then
        # log "本地文件 ${local_dir}/${file_to_download} 已存在，跳过下载。"
        # continue
        # fi

        download_command="${PCS_GO_EXEC} download \"${remote_file_path}\" --saveto \"${local_dir}\""
        log "执行下载命令: ${download_command}"

        # 直接执行命令，使其输出（包括进度条）直接显示在终端和日志中
        if "${PCS_GO_EXEC}" download "${remote_file_path}" --saveto "${local_dir}"; then
            log "文件 \"${file_to_download}\" 下载成功 (退出码 $?)"
        else
            local exit_code=$?
            log "文件 \"${file_to_download}\" 下载失败 (退出码 ${exit_code})"
            all_downloads_successful=false # 标记至少有一个下载失败
            # return 1 # 如果希望任何一个文件下载失败都中止整个脚本
        fi
        log "-----------------------------------------------------" # 文件下载分隔符
    done

    if ${all_downloads_successful}; then
        log "所有已识别文件的下载尝试均成功完成。"
        return 0
    else
        log "部分或全部文件下载失败。"
        return 1 # 返回错误码，表示下载过程并非完全成功
    fi
}

# 主执行逻辑
main() {
    # 初始化日志文件
    mkdir -p "$(dirname "$LOG_FILE")"
    >"$LOG_FILE"

    log "批处理脚本 download_vibe_ourdataset.bash 开始执行"
    log "远程目录: ${REMOTE_DATA_DIR}"
    log "本地目录: ${LOCAL_TARGET_DIR}"

    # 1. 登录
    if ! login_baidu "${BDUSS_VALUE}"; then
        log "百度网盘登录失败，脚本终止。"
        exit 1
    fi

    # 2. 下载文件
    log "开始下载文件..."
    if download_all_files_from_remote_dir "${REMOTE_DATA_DIR}" "${LOCAL_TARGET_DIR}"; then
        log "文件下载过程完成。"
    else
        log "文件下载过程中出现一个或多个错误。"
        # 根据需要决定是否在这里退出
        # exit 1
    fi

    log "批处理脚本 download_vibe_ourdataset.bash 执行完毕"
}

# 执行主函数
main
```



测试VIBE的输出结果：
```python
python demo.py --vid_file "/root/autodl-tmp/VIBE/VIBE/ourdataset/000 Cliffside Walk (Female).mp4" --output_folder output/ --sideview
```

可能有各种包的冲突问题，正常解决即可，最终`VIBE_prepareDataset`这台机器当中保存VIBE的运行环境，正常运行即可。



## 2.VIBE->AMASS，同时解决抖动问题

经过测试，VIBE生成的结果2D还可以，3D的话对于姿态的估计问题很大，经常对于深度的估计出现错误，人体也会一直抖动。接下来我希望能把三个启发式算法引入进来：

- （1）整体平滑的操作：显然，正常人应该保持整体躯干平稳，最起码不应该有频繁的抖动，因此应该有一个lerp的过程，保留历史姿态，类似于TAA这样，同时保持主要骨骼不要来回抖动；
- （2）由于VIBE要转到AMASS数据集的类似格式，这里需要考虑相机位姿到世界空间的转换，之前的脚本虽然做了简化，但看VIBE的效果还是需要处理一下的，这里可以做一些假设，因为我们的数据集是比较专业的，因此可以指定待转换的对象是否是侧向的，如果是的话，可以认为沿着直线行走，不要有太大的变化幅度。
- （3）对于脚来说，可以假定把脚尽量放在地面上，可以以前面一些帧的平均值作为脚的位置，好加IK进去么？

请你依据我接下来提供的脚本，给出修改之后的脚本，尽可能地解决我刚才提出的问题，我们的目标是让VIBE输出的充满噪声的抖动3D结果变得平滑，且相对比较优质。



## 3.Train

> ```
> python demo_transfer.py --cfg ./configs/config_mld_humanml3d.yaml --cfg_assets ./configs/assets.yaml --style_motion_dir demo/style_motion --content_motion_dir demo/content_motion --scale 2.5
> ```

跑这个：

python demo_transfer.py --cfg ./configs/config_test_our_train.yaml --cfg_assets ./configs/assets.yaml --style_motion_dir demo/style_motion --content_motion_dir demo/content_motion --scale 2.5



python demo_transfer.py --cfg ./configs/config_test_our_train.yaml --cfg_assets ./configs/assets0529.yaml --style_motion_dir demo/style_motion --content_motion_dir demo/content_motion --scale 2.5



/root/autodl-tmp/MCM-LDM/configs/assets0529.yaml



train的代码：

```python
python -m train --cfg /root/autodl-tmp/MCM-LDM/configs/config_train_denoiser.yaml --cfg_assets configs/assets.yaml --batch_size 128 --nodebug
```

目前的train的代码：

```python
python -m train_my --cfg /root/autodl-tmp/MCM-LDM/configs/config_train_denoiser.yaml --cfg_assets /root/autodl-tmp/MCM-LDM/configs/assets0529.yaml --batch_size 128 --nodebug
```

