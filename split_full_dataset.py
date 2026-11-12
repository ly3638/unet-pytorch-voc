
import os
import random
import shutil
from datetime import datetime

base_dir = "VOCdevkit/VOC2007"

mask_dir = os.path.join(base_dir, "SegmentationClass")
split_dir = os.path.join(
    base_dir, "ImageSets", "Segmentation"
)

train_file = os.path.join(split_dir, "train.txt")
val_file = os.path.join(split_dir, "val.txt")
trainval_file = os.path.join(split_dir, "trainval.txt")
test_file = os.path.join(split_dir, "test.txt")

# 1. 读取旧的训练集和验证集名单
def read_list(path):
    with open(path, "r", encoding="utf-8") as f:
        return set(line.strip() for line in f if line.strip())

old_train = read_list(train_file)
old_val = read_list(val_file)
old_used = old_train | old_val

# 2. 读取完整标签名单
all_images = {
    os.path.splitext(f)[0]
    for f in os.listdir(mask_dir)
    if f.lower().endswith(".png")
}

# 3. 检查旧名单是否都存在
missing = old_used - all_images

if missing:
    raise ValueError(
        f"旧名单中有图片不存在：{sorted(missing)}"
    )

print("完整图片数量：", len(all_images))
print("旧训练图片：", len(old_train))
print("旧验证图片：", len(old_val))
print("旧名单合计：", len(old_used))

# 4. 备份旧划分文件
backup_dir = os.path.join(
    split_dir,
    "backup_" + datetime.now().strftime("%Y%m%d_%H%M%S")
)
os.makedirs(backup_dir, exist_ok=True)

for path in [train_file, val_file, trainval_file, test_file]:
    if os.path.exists(path):
        shutil.copy2(
            path,
            os.path.join(backup_dir, os.path.basename(path))
        )

# 5. 旧训练、验证图片全部放进新训练集
new_train = set(old_used)

# 6. 其余图片随机划分
remaining = sorted(all_images - old_used)

random.seed(42)
random.shuffle(remaining)

val_count = round(len(remaining) * 0.1)

new_val = set(remaining[:val_count])
new_train.update(remaining[val_count:])

# 7. 写入新的名单
def save_list(path, names):
    with open(path, "w", encoding="utf-8") as f:
        for name in sorted(names):
            f.write(name + "\n")

save_list(train_file, new_train)
save_list(val_file, new_val)
save_list(trainval_file, all_images)

# 暂时不单独设置测试集
save_list(test_file, set())

# 8. 输出结果
print("\n新数据集划分完成！")
print("训练集数量：", len(new_train))
print("验证集数量：", len(new_val))
print("总数量：", len(new_train) + len(new_val))
print("旧图片进入新验证集数量：", len(old_used & new_val))
print("备份目录：", backup_dir)
