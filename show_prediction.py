""" from PIL import Image
import numpy as np

# 读取预测结果
mask = Image.open(
    "miou_out/detection-results/image_2687.png"
)

mask = np.array(mask)

# 背景设为黑色，道路设为白色
visual = np.zeros((mask.shape[0], mask.shape[1]), dtype=np.uint8)
visual[mask == 1] = 255

# 保存可视化结果
Image.fromarray(visual).save("road_prediction_white.png")

print("道路预测可视化完成！") """
from PIL import Image
import numpy as np
import os

# 真实标签路径
gt_path = "VOCdevkit/VOC2007/SegmentationClass/image_2687.png"

# 模型预测结果路径
pred_path = "miou_out/detection-results/image_2687.png"

""" # 分别读取图片
gt = np.array(Image.open(gt_path))
pred = np.array(Image.open(pred_path))

# 转换成黑底白路
gt_visual = np.zeros(gt.shape, dtype=np.uint8)
gt_visual[gt == 1] = 255

pred_visual = np.zeros(pred.shape, dtype=np.uint8)
pred_visual[pred == 1] = 255

# 保存结果
Image.fromarray(gt_visual).save("ground_truth_white.png")
Image.fromarray(pred_visual).save("prediction_white.png")

print("真实标签和预测结果转换完成！")
 """

gt = np.array(Image.open(gt_path)) == 1
pred = np.array(Image.open(pred_path)) == 1

# RGB 三色对比图
result = np.zeros((*gt.shape, 3), dtype=np.uint8)

# 正确识别：绿色
result[gt & pred] = [0, 255, 0]

# 漏检：红色
result[gt & ~pred] = [255, 0, 0]

# 误检：蓝色
result[~gt & pred] = [0, 0, 255]

Image.fromarray(result).save("road_comparison.png")

print("对比图已保存：road_comparison.png")