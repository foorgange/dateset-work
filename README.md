# 数据集处理工具

## 项目概述

本项目是一个用于处理和准备图像分割数据集的工具集，主要包含了针对特定遥感图像数据集（如 DDXPlus 和 Vaihingen）的预处理脚本。这些脚本的核心功能是将大幅面的遥感图像及其对应的标签图，裁剪成适合深度学习模型训练的小块 (patches)。

通过将大图切分成小图，可以有效地增加训练样本数量，并使得数据能够以批次 (batch) 的形式高效地载入模型进行训练。该工具集对于从事遥感图像语义分割研究和开发的工程师与学者来说实用。

## 主要特性

*   **针对特定数据集**: 提供了专门用于处理 DDXPlus 和 Vaihingen 数据集的脚本.
*   **图像与标签同步裁剪**: 确保原始图像和其对应的标签图在相同位置被裁剪，维持数据的一致性.
*   **自定义裁剪参数**: 用户可以方便地在脚本中调整裁剪窗口的大小 (patch size) 和步长 (stride)，以适应不同模型和实验的需求.
*   **文件处理自动化**: 自动创建输出目录，并根据原始文件名对裁剪后的小块进行系统命名和保存.

## 文件结构

```
dateset-work/
├── .gitignore         # 定义了 Git 应忽略的文件和目录
├── requirements.txt   # 项目依赖的 Python 库
├── split_ddxplus.py   # 用于裁剪 DDXPlus 数据集的脚本
└── split_vaihingen.py # 用于裁剪 Vaihingen 数据集的脚本
```

## 安装

1.  **克隆代码库**:
    ```bash
    git clone https://github.com/foorgange/dateset-work.git
    cd dateset-work
    ```

2.  **创建并激活 Conda 环境 (推荐)**:
    ```bash
    conda create -n dataset-tools python=3.8
    conda activate dataset-tools
    ```

3.  **安装依赖**:
    ```bash
    pip install -r requirements.txt
    ```

## 使用方法

### 1. 数据集准备

在使用脚本之前，请确保您的数据集已按以下结构存放：

*   **Vaihingen 数据集**:
    ```
    /path/to/vaihingen/
    ├── top/         # 存放原始遥感图像 (.tif 文件)
    │   ├── top_mosaic_09cm_area1.tif
    │   └── ...
    └── dsm_gt/      # 存放对应的标签图 (.tif 文件)
        ├── top_mosaic_09cm_area1.tif
        └── ...
    ```

*   **DDXPlus 数据集**:
    (请根据 `split_ddxplus.py` 脚本中的路径设置，将数据集放置在相应位置。)

### 2. 配置脚本

打开 `split_vaihingen.py` 或 `split_ddxplus.py` 文件，根据您的实际情况修改以下变量：

*   **文件路径**: 修改指向您的原始图像和标签图的路径变量.
*   **输出路径**: 指定裁剪后的小块图像和标签的保存位置.
*   **裁剪参数**:
    *   `split_width`: 裁剪窗口的宽度.
    *   `split_height`: 裁剪窗口的高度.
    *   `stride`: 裁剪窗口滑动的步长.

### 3. 运行脚本

配置完成后，在终端中运行相应的脚本：

*   **处理 Vaihingen 数据集**:
    ```bash
    python split_vaihingen.py
    ```

*   **处理 DDXPlus 数据集**:
    ```bash
    python split_ddxplus.py
    ```

脚本执行完毕后，裁剪好的图像和标签小块将会保存在您指定的输出目录中.

## 脚本逻辑简介

以 `split_vaihingen.py` 为例，其核心工作流程如下：

1.  **定义路径**: 设置原始数据文件夹、标签文件夹以及裁剪后图像和标签的输出文件夹.
2.  **遍历图像**: 脚本会遍历原始数据文件夹中的所有 `.tif` 图像.
3.  **读取数据**: 使用 `gdal` 库读取每张大图的图像数据和地理空间信息.
4.  **滑动窗口裁剪**:
    *   通过嵌套循环，在整张大图上移动一个预设大小（例如 256x256）的窗口.
    *   移动的步长 (stride) 也是预设的，这决定了裁剪出的小块之间是否有重叠.
    *   在每个窗口位置，同时从原始图像和对应的标签图中裁剪出相应的小块.
5.  **保存结果**: 将裁剪出的图像小块和标签小块分别保存为 `.png` 或 `.tif` 格式的文件，并以系统化的方式命名（例如 `area1_1_1.png`）.

