
import os
import numpy as np
from PIL import Image

image_dir = "VOCdevkit/VOC2007/JPEGImages"
mask_dir = "VOCdevkit/VOC2007/SegmentationClass"

images = {
    os.path.splitext(f)[0]
    for f in os.listdir(image_dir)
    if f.lower().endswith((".jpg", ".jpeg", ".png"))
}

masks = {
    os.path.splitext(f)[0]
    for f in os.listdir(mask_dir)
    if f.lower().endswith(".png")
}

print("原始图片数量：", len(images))
print("标签图片数量：", len(masks))

print("缺少标签的图片：", sorted(images - masks)[:20])
print("缺少原图的标签：", sorted(masks - images)[:20])

bad_size = []
pixel_values = set()

for name in sorted(images & masks):
    image_path = os.path.join(image_dir, name + ".jpg")
    mask_path = os.path.join(mask_dir, name + ".png")

    # 同时兼容 jpg/jpeg/png 原图
    if not os.path.exists(image_path):
        for ext in [".jpeg", ".png"]:
            candidate = os.path.join(image_dir, name + ext)
            if os.path.exists(candidate):
                image_path = candidate
                break

    img = Image.open(image_path)
    mask = Image.open(mask_path)

    if img.size != (512, 512) or mask.size != (512, 512):
        bad_size.append((name, img.size, mask.size))

    arr = np.array(mask)
    pixel_values.update(np.unique(arr).tolist())

print("尺寸不正确的图片：", bad_size[:20])
print("标签像素值：", sorted(pixel_values))
print("检查完成！")
