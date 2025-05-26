# MCM-LDM Github环境配置的注意事项

仓库链接：https://github.com/XingliangJin/MCM-LDM



# 一、基础环境配置

先拉仓库，在AutoDL中放到数据盘里，不要放到系统盘中。

> 可能需要学术加速：
>
> ```shell
> source /etc/network_turbo
> ```

然后创建conda环境，并激活：
```bash
conda create python=3.9 --name mcmldm

conda init bash # 针对新机器，注意初始化之后要kill掉当前的terminal，然后重新开一个

conda activate mcmldm
```

```
pip install -r requirements.txt
```

这里面会出现几个问题：

- `matplotlib`这个包会出现安装错误之类的问题，需要安装下面的系统依赖：

```bash
sudo apt-get update
sudo apt-get install -y libfreetype6-dev  # 核心依赖
sudo apt-get install -y pkg-config        # 辅助工具
# 然后重新下载并编译
pip install --no-cache-dir matplotlib
```

- `blis`是高性能矩阵运算相关的包，会编译非常长的时间（估计至少有10分钟），耐心等待即可。



## 1.google drive怎么加速

先下载到本地，上传到百度网盘上（有会员），然后按照下面的步骤来：

> 在 **AutoDL 实例** 中通过百度网盘传输文件，可以通过以下 **3 种方法** 实现（无需 VPN，适配国内网络环境）：
>
> ---
>
> ### 方法 1：官方客户端 + 图形化界面（适合新手）
> #### 步骤：
> 1. **在本地电脑操作**：
>    - 将文件上传到你的百度网盘（网页版或客户端）
>    - 右键文件 → 生成分享链接（选择「有提取码」）
>
> 2. **在 AutoDL 实例中下载**：
>    ```bash
>    # 安装百度网盘官方 Linux 客户端（需桌面环境）
>    wget https://issuecdn.baidupcs.com/issue/netdisk/LinuxGuanjia/baidunetdisk_4.17.7_amd64.deb
>    sudo apt install ./baidunetdisk_4.17.7_amd64.deb
>    
>    # 启动客户端（需 VNC 或 X11 转发）
>    baidunetdisk
>    ```
>    - 登录账号 → 通过分享链接下载（需手动操作）
>
> #### 缺点：
> - 依赖图形界面，不适合纯命令行环境
> - 大文件需要会员加速
>
> ---
>
> ### 方法 2：命令行工具 `bypy`（推荐）
> #### 步骤：
> 1. **安装工具**：
>    ```bash
>    pip install bypy
>    ```
>
> 2. **授权登录**：
>    ```bash
>    bypy info
>    ```
>    - 命令行会返回一个授权链接，复制到本地浏览器打开
>    - 登录百度账号 → 复制授权码回终端
>
> 3. **下载文件**：
>    ```bash
>    # 列出网盘文件
>    bypy list
>    
>    # 下载文件（需分享链接的提取码）
>    bypy downdir /你的网盘路径 /root/autodl-tmp/
>    ```
>
> #### 优点：
> - 纯命令行操作，适合服务器环境
> - 支持断点续传
>
> #### 缺点：
> - 单线程下载，速度较慢（约 1-2MB/s）
> - 需要手动处理分享链接的提取码
>
> ---
>
> ### 方法 3：第三方解析工具（高速下载）
> #### 步骤：
> 1. **获取直链**：
>    - 在本地浏览器用 [百度网盘直链解析工具](https://pan.baidu.com/s/1... ) 生成下载直链
>    - 或使用 API 工具（如 [BaiduPCS-Go](https://github.com/qjfoidnh/BaiduPCS-Go)）
>
> 2. **在 AutoDL 中下载**：
>    ```bash
>    # 示例：通过直链下载（需替换真实 URL）
>    wget --header="User-Agent: Mozilla/5.0" "直链URL" -O /root/autodl-tmp/file.zip
>    ```
>
> #### 优点：
> - 绕过限速，速度可达 10MB/s+
> - 无需登录账号
>
> #### 缺点：
> - 直链可能失效，需要定期更新工具
> - 需手动操作本地浏览器
>
> ---
>
> ### 终极方案：分卷压缩 + 多平台接力
> 如果文件 >10GB：
> 1. **在本地电脑**：
>    ```bash
>    # 分卷压缩（每卷 2GB）
>    split -b 2G large_file.zip large_file_part_
>    ```
> 2. **上传分卷**到百度网盘 + 阿里云盘（双备份）
> 3. **在 AutoDL 中**：
>    ```bash
>    # 从不同平台并行下载分卷
>    bypy downdir /分卷路径 /root/parts/ &  # 百度网盘
>    ali-cli download 分享链接 /root/parts/ &  # 阿里云盘
>    wait
>    
>    # 合并分卷
>    cat /root/parts/large_file_part_* > large_file.zip
>    ```
>
> ---
>
> ### 注意事项：
> 1. 百度网盘对非会员有单文件下载限制（通常 ≤4GB）
> 2. 敏感文件可能被屏蔽，建议加密压缩（密码保护）
> 3. 推荐组合使用 **bypy（稳定） + 直链解析（加速）**
>
> 如果需要更具体的操作指导，可以告诉我：
> - 你的文件大小
> - 是否能在本地访问百度网盘
> - 是否需要全自动脚本方案

登录：

```
./BaiduPCS-Go-v3.9.7-linux-amd64/BaiduPCS-Go login -bduss=xxxx
```

查看目录：

```
(mcmldm) root@autodl-container-06564c8c34-2234d0a3:~/autodl-tmp# ./BaiduPCS-Go-v3.9.7-linux-amd64/BaiduPCS-Go ls /
```

下载对应的文件（提前上传到网盘当中）：

```
root@autodl-container-06564c8c34-2234d0a3:~/autodl-tmp# ./BaiduPCS-Go-v3.9.7-linux-amd64/BaiduPCS-Go download /AIFiles/t2m.tar.gz
```

==速度会比直接上传要快不少。==