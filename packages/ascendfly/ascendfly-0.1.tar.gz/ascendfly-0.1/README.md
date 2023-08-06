[TOC]

# 1 简介

## 1.1 背景

该项目通过Ascend Compute Language Python(pyACL) API实现Ascendfly目标分类检测推理框架，封装了一系列易用的python接口，目的是简化用户使用pyACL开发流程，加速算法迁移部署。以下对ascendfly相关接口功能、依赖安装和使用进行简要说明。

## 1.2 主要功能

本软件提供以下功能：

1. 封装了Context、Memory资源类，简化资源调度与分配。
2. 封装了AscendArray类，类似numpy.ndrray在device上进行图片和tensor管理，实现数据统一性。
3. 封装了VideoCapture和VideoWriter类，获取实时H264（MAIN LEVEL without B frame）协议的RTSP/RTMP码流，并通过Ascend310芯片硬解码，或逐帧把图片编码为264/265码流。
4. 封装了Image类，实现图片解码、缩放、剪切、padding等图像处理功能。
5. 封装了Model类执行模型推理功能。
6. 封装了Profiling类，方便进行模型性能调优。
7. 其他如单算子调用，后处理等功能。

## 1.3 程序架构

Ascendfly系统级封装主要包括以下模块。

1. 资源管理（resource）:

   resource资源包括内存模块（mem）、context和线程/进程资源（thread/multi-process）, 由各自文件进行管理。

2. 基础模块（base）：

   主要包括数据预处理模块（dvpp），模型推理模块（model）和视频拉流模块（stream_puller）

3. 公共模块（common）：

   涉及到常量模块（const），日志模块（log），配置和命令解析模块（config_paser 和 cmd_paser）。

4. 流程模块（workflow）：提供一个流程串接样例，来实现上述各模块的调用和流水线拼接。workflow里面包含pre_process（调用dvpp的一些方法，实现预处理）、post_process(实现了yolov3的后处理)、inference（调用model，实现模型推理）和work_flow（流程拼接，实现端到端功能）

5. 主函数（main）：用于启动demo

整体系统设计如下图所示：

![输入图片说明](https://images.gitee.com/uploads/images/2021/0222/151913_6ad4c066_8307159.jpeg "system.jpg")

## 1.4 设计流程

![输入图片说明](https://images.gitee.com/uploads/images/2021/0222/151932_3604f1a3_8307159.jpeg "thread.jpg")



# 2 环境依赖及安装指导

## 2.1 环境依赖

pyACL_YoloV3_Demo需要依赖**pyACL（CANN 20.1或者20.2版本）**、[pylive555](https://github.com/mosquito/pylive555)和[opencv]()。以下简要介绍相关依赖软件安装过程。

表2-1 硬件要求

| 环境要求 | 说明                                                        |
| -------- | ----------------------------------------------------------- |
| 硬件环境 | Atlas 300（型号3000 或 3010）/Atlas 800（型号3000 或 3010） |
| 操作系统 | CentOS 7.6/Ubuntu18.04                                      |

表2-2 环境依赖软件及软件版本

| 软件名称 | 软件版本                              |
| -------- | ------------------------------------- |
| pyACL  | （安装CANN 20.1 或者 20.2，会自带安装pyACL ） |
| pylive555 | - |
| opencv   | 4.4.0及以上 |



## 2.2 pylive555安装过程

pyACL_YoloV3_Demo依赖三方开源库[pylive555](https://github.com/mosquito/pylive555)进行获取H264、H265的RSTP/RTMP视频流，送给DVPP进行解码，以进行后续业务。编译和安装过程依赖[Live555]( http://www.live555.com/liveMedia/public)软件库，请先下载安装。

- **步骤 1**  下载Live555安装包

  http://www.live555.com/liveMedia/public/live555-latest.tar.gz

- **步骤 2** 解压live555安装包到任意路径下：

  ```shell
  tar -xvzf live.tar.gz
  ```

- **步骤 3** 生成makefile文件，并编译、安装：

  - 如果是x86环境，编译安装步骤参考如下：

    ```shell
    ./genMakefiles linux#注意后面这个参数是根据当前文件夹下config.<后缀>获取得到的
    export CPPFLAGS=-fPIC CFLAGS=-fPIC
    make -j8
    make install
    ```

  - 如果是arm环境，编译安装步骤参考如下：

    ```shell
    ./genMakefiles linux-64bit#注意后面这个参数是根据当前文件夹下config.<后缀>获取得到的
    export CPPFLAGS=-fPIC CFLAGS=-fPIC
    make -j8
    make install
    ```

- **步骤 4** 下载pylive555安装包：

  https://github.com/mikemccand/pylive555

- **步骤 5** pylive555编译安装，解压pylive555-master.zip到任意目录：

  ```shell
  unzip pylive555-master.zip
  ```

- **步骤 6** 修改setup.py安装脚本

  ```shell
  cd pylive555-master
  vim setup.py
  ```

  修改setup.py如下：

  ```diff
  @@ -1,11 +1,11 @@
   from distutils.core import setup, Extension
  
  -INSTALL_DIR = './live'
  +INSTALL_DIR = '/usr/local'
   module = Extension('live555',
  -                   include_dirs=['%s/%s/include' % (INSTALL_DIR, x) for x in ['liveMedia', 'BasicUsageEnvironment', 'UsageEnv
  +                   include_dirs=['%s/include/%s' % (INSTALL_DIR, x) for x in ['liveMedia', 'BasicUsageEnvironment', 'UsageEnv
                      libraries=['liveMedia', 'groupsock', 'BasicUsageEnvironment', 'UsageEnvironment'],
                      #extra_compile_args = ['-fPIC'],
  -                   library_dirs=['%s/%s' % (INSTALL_DIR, x) for x in ['liveMedia', 'UsageEnvironment', 'groupsock']],
  +                   library_dirs=['%s/lib'%INSTALL_DIR],
                      sources = ['module.cpp'])
  
   setup(name = 'live555',
  ```

- **步骤 7** 编译，然后把编译后的so文件拷贝到`/usr/local/python3.7.5/lib/python3.7/site-packages/`目录下，或把so文件加入到PYTHONPATH环境变量中。

  ```shell
  python3 setup.py build
  cp build/lib.linux-x86_64-3.7/live555.cpython-37m-x86_64-linux-gnu.so /usr/local/python3.7.5/lib/python3.7/site-packages/
  ```

  或

  ```shell
  export PYTHONPATH=$PYTHONPATH:/home/pylive555-master/build/lib.linux-x86_64-3.7/
  ```

- **步骤 8** 完成。如果import live555出现以下错误，可能是openssl库没有链接到pylive555的库文件中。

  ```shell
  Python 3.7.5 (default, Jan 15 2021, 07:19:45)
  [GCC 4.8.5 20150623 (Red Hat 4.8.5-36)] on linux
  Type "help", "copyright", "credits" or "license" for more information.
  >>> import live555
  Traceback (most recent call last):
    File "<stdin>", line 1, in <module>
  ImportError: /usr/local/lib/live555.cpython-37m-x86_64-linux-gnu.so: undefined symbol: SSL_CTX_free
  ```

  可采用以下方法强制LD_PRELOAD载入ssl库

  ```shell
  export LD_PRELOAD=/lib64/libssl.so.1.0.2k
  ```

  

## 2.3 opencv安装过程

如果是ARM平台，编译安装opencv-python前需要先安装python3.7.5

- **步骤 1** 下载opencv-python

   https://pypi.org/project/opencv-python/4.4.0.46/#files
   
- **步骤 2**  解压opencv-python

   tar -zxvf opencv-python-4.4.0.46.tar.gz && cd opencv-python-4.4.0.46
   
- **步骤 3**  编译opencv-python

   python3.7.5 setup.py install
   
   


## 2.4 CANN安装

pyACL作为用户的API编程接口，提供Device管理、Context管理、Stream管理、内存管理、模型加载与执行、算子加载与执行、媒体数据处理等python API库供用户开发应用。pyAcl_YoloV3_Demo需要在Ascend设备上运行，需要依赖pyACL提供APIs，具体环境安装方法参考[《CANN 软件安装指南》](https://support.huaweicloud.com/instg-cli-cann/atlascli_03_0001.html), 安装CANN后，进行[环境变量配置](https://support.huaweicloud.com/asdevg-python-cann/atlaspython_01_0006.html)。



# 3 使用指导

使用请先熟悉pyACL开发流程，具体请参见[《应用开发指南(Python)》](https://support.huaweicloud.com/asdevg-python-cann/atlaspython_01_0001.html)。

## 3.1 使用约束

本章节介绍pyACL_YoloV3_Demo限制约束。

表3-1 使用约束

| 名称     | 规格约束                                                     |
| -------- | ------------------------------------------------------------ |
| 进程     | 单进程                                                       |
| 线程     | python全局性解释锁（GIL）的约束，单进程中线程不易过多，根据实际需求进行测试，寻求合适线程数。当线程需求多，但是性能急剧下降，则解决方案：<br>（1）可以通过合并workflow中的模块，减少线程数；<br>（2）可以创建一个workflow对象，绑定一个device，并启用一个进程（多进程模式暂时不支持，用户可自己开发） |
| pyACL    | 总体约束请参考[《应用开发指南(Python)》中的使用约束](https://support.huaweicloud.com/asdevg-python-cann/atlaspython_01_0001.html) |
| device   | 单进程中device数目不宜过多，推荐不超过4个device（同一张atlas卡内） |
| context  | 一个context对应一个device（程序默认）                        |
| 视频拉流 | 目前只支持rtsp协议，拉取H264（去除B帧）的视频流              |
| 预处理   | 预处理模块：<br>（1）AscendDvpp仅包括：[jpeg解码](https://support.huaweicloud.com/asdevg-python-cann/atlaspython_01_0083.html)，vpc中的[resize](https://support.huaweicloud.com/asdevg-python-cann/atlaspython_01_0080.html)和[一抠一贴](https://support.huaweicloud.com/asdevg-python-cann/atlaspython_01_0078.html)功能；调用jpeg解码，需要用户自己写''数据获取''代码<br>（2）AscendVdec中的视频解码([vdec](https://support.huaweicloud.com/asdevg-python-cann/atlaspython_01_0089.html))模块支持H264和H265格式，但是拉取的流不支持265；<br>（3）针对yolov3进行的数据预处理中，要求模型对于输入数据的要求为：宽(w) 大等于高（h） |
| 推理     | AscendModel负责模型推理，当前只支持静态batch和静态resolution |



## 3.2 使用前准备

运行前，需要先进行模型的转换和配置文件修改。模型和配置文件的存放位置可自定义。

### 3.2.1 模型准备

- **步骤 1 :** 模型下载

  首先，获取以下链接中所用到的原始网络模型，对应的权重文件和aipp_cfg文件，并将其存放到开发环境普通用户下的任意目录，例如：/home/model/

  | 文件类型        | 下载链接                                                     |
  | --------------- | ------------------------------------------------------------ |
  | YOLO-v3权重文件 | [caffe模型权重下载地址](https://modelzoo-train-atc.obs.cn-north-4.myhuaweicloud.com/003_Atc_Models/AE/ATC%20Model/Yolov3/yolov3.caffemodel)|
  | YOLO-v3模型文件 | [caffe模型文件下载地址](https://modelzoo-train-atc.obs.cn-north-4.myhuaweicloud.com/003_Atc_Models/AE/ATC%20Model/Yolov3/yolov3.prototxt) |
  | aipp配置文件    | [cfg文件下载地址](https://modelzoo-train-atc.obs.cn-north-4.myhuaweicloud.com/003_Atc_Models/AE/ATC%20Model/Yolov3/aipp_nv12.cfg) |

- **步骤 2:** ATC工具环境变量设置

  当上述模型和aipp配置文件下载并存放在同一目录下后，需要应用ATC（模型转换工具），把caffe模型转成适配Ascend平台的离线推理om模型。ATC工具使用前先进行环境变量设置，具体可参考[《ATC工具使用指南》](https://support.huaweicloud.com/tg-Inference-cann/atlasatc_16_0004.html)设置环境变量。

- **步骤 3:** 模型转换前文件修改

  进入文件目录下，例如：/home/model/

  ```shell
  cd /home/model/
  ```

  根据实际码流路数修改yolov3.prototxt的输入batch_size。

  ```json
  name: "Darkent2Caffe"
  input: "data"
  input_shape {
    dim: 1 #batch_size
    dim: 3
    dim: 416
    dim: 416
  }
  input: "img_info"
  input_shape {
    dim: 1 #batch_size
    dim: 4
  }
  ```

- **步骤 4:** 模型转换

  ```shell
  atc --model=yolov3.prototxt --weight=yolov3.caffemodel --framework=0 --output=yolov3.om --soc_version=Ascend310 --insert_op_conf=aipp_nv12.cfg
  ```

  上述命令行详细参数请参考[ATC工具参数说明](https://support.huaweicloud.com/tg-Inference-cann/atlasatc_16_0007.html)

### 3.2.2 配置文件

在运行Demo前，根据实际情况，可以修改配置文件中的参数。配置文件格式如下：

```shell
[video_stream]       # 视频流section
channel_count = 2    # rtsp视频流通道的数目；例：通道为2，有两路视频流被拉取
channel_id = 0,1     # 视频流通道的id；例：2路视频流的id分别为 0 和 1
rtsp = rtsp://192.168.122.137/fujian_caishichang_00.264, rtsp://192.168.122.137/fujian_caishichang_01.264  # rtsp视频流地址(逗号隔开)；例：2路视频流地址
width = 1280         # 视频流中图像宽度； 例：宽为1280
height = 720         # 视频流中图像高度； 例：高为720
encode_type = H264   # 编码类型  例：H264编码
```



## 3.3 demo运行

进入pyACL_Yolov3_Demo的src目录下，运行main.py

```shell
python3.7.5 main.py
```

可配置命令：

| 命令                 | 解释             | 默认值            |
| -------------------- | ---------------- | ----------------- |
| --device             | 配置启用的device | 0                 |
| --model_path         | 模型文件存放位置 | ./data/model/yolov3.om |
| --batch              | 模型batch数目    | 1                 |
| --model_input_width  | 模型输入图片的宽 | 416               |
| --model_input_height | 模型输入图片的高 | 416               |
| --conf_path          | 配置文件存放路径 | ./conf/cfg.ini    |

例子：

```shell
python3.7.5 main.py --device 0 1 --model_path ./data/model/yolov3.om --batch 2 --model_input_width 416 --model_input_height 416 --conf_path ./conf/cfg.ini
```

用上述命令行，运行main.py时，启用的功能为：

1.  启用device_id为0和1的device

2.  模型和配置文件存放的位置为：./model/yolov3.om 和 ./conf/cfg.ini

3.  batch 为 2 （当设定batch为2的时候，对应的atc转换的yolov3的om模型，batch也必须为2）

4.  模型输入图片宽高：416 * 416

   

# 4 附录

## 4.1 FAQ

### 4.1.1 xxxxxx

## 