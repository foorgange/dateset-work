import os
import cv2
import numpy as np
from glob import glob
from tqdm import tqdm

# 裁剪窗口大小（单位：像素）
tile_size = 512

# === 1. 设置输入路径 ===
image_dir = 'data/vaihingen/image'    # 原始图像（彩色 .tif）
label_dir = 'data/vaihingen/label'    # 标签图像（灰度 .tif）

# === 2. 设置输出路径 ===
out_img_dir = 'result/new_vaihingen/new_image'  # 裁剪后的图像保存路径
out_lbl_dir = 'result/new_vaihingen/new_label'  # 裁剪后的标签保存路径

# 自动创建输出目录（如果不存在）
os.makedirs(out_img_dir, exist_ok=True)
os.makedirs(out_lbl_dir, exist_ok=True)

# === 3. 获取所有图像路径 ===
image_paths = sorted(glob(os.path.join(image_dir, '*.tif')))
label_paths = sorted(glob(os.path.join(label_dir, '*_noBoundary.tif')))

# 保证图像与标签一一对应
assert len(image_paths) == len(label_paths), "图像和标签数量不一致"

# === 4. 遍历每一对图像和标签 ===
for img_path, lbl_path in tqdm(zip(image_paths, label_paths), total=len(image_paths), desc='正在处理'):
    # 读取图像：彩色 (3通道)
    image = cv2.imread(img_path, cv2.IMREAD_COLOR)
    if image is None:
        print(f"[错误] 无法读取图像文件: {img_path}")
        continue

    # 读取标签：灰度图（单通道）
    label = cv2.imread(lbl_path, cv2.IMREAD_GRAYSCALE)
    if label is None:
        print(f"[错误] 无法读取标签文件: {lbl_path}")
        continue

    # 获取图像高度和宽度
    h, w = image.shape[:2]

    # 从文件名中提取如 area_1
    basename = os.path.splitext(os.path.basename(img_path))[0]  # 如 top_mosaic_09cm_area1
    area_name = "area_" + basename.split("area")[-1]  # 得到 area_1

    # 遍历图像：步长为 tile_size
    for y in range(0, h, tile_size):
        for x in range(0, w, tile_size):
            # 裁剪图像块和标签块
            tile_img = image[y:y+tile_size, x:x+tile_size]
            tile_lbl = label[y:y+tile_size, x:x+tile_size]

            # 如果 tile_lbl 是空的，跳过该块
            if tile_lbl is None or tile_lbl.size == 0:
                print(f"[警告] tile_lbl 是空的，跳过该块。坐标: ({x}, {y}) in {area_name}")
                continue

            # 判断是否需要填充（补黑边）
            if tile_img.shape[0] < tile_size or tile_img.shape[1] < tile_size:
                pad_img = np.zeros((tile_size, tile_size, 3), dtype=np.uint8)
                pad_lbl = np.zeros((tile_size, tile_size), dtype=np.uint8)

                pad_img[:tile_img.shape[0], :tile_img.shape[1]] = tile_img
                pad_lbl[:tile_lbl.shape[0], :tile_lbl.shape[1]] = tile_lbl

                tile_img = pad_img
                tile_lbl = pad_lbl

            # 生成文件名
            img_name = f"{area_name}_{y}_{x}.jpg"
            lbl_name = f"{area_name}_{y}_{x}.png"

            # 保存图像和标签
            cv2.imwrite(os.path.join(out_img_dir, img_name), tile_img)
            cv2.imwrite(os.path.join(out_lbl_dir, lbl_name), tile_lbl)
