import os
import random
import shutil

train_take_path = "C:/Users/khanh/code/DATA_SCIENCE/data/take and remove/train/take/"
train_remove_path = "C:/Users/khanh/code/DATA_SCIENCE/data/take and remove/train/remove/"

test_take_path = "C:/Users/khanh/code/DATA_SCIENCE/data/take and remove/test/take/"
test_remove_path = "C:/Users/khanh/code/DATA_SCIENCE/data/take and remove/test/remove/"

take = os.listdir(train_take_path)
remove = os.listdir(train_remove_path)

random.shuffle(take)
random.shuffle(remove)

# move 20% of the files from each source directory to the target directory
num_files = int(0.2 * len(take))
for i in range(num_files):
    shutil.move(os.path.join(train_take_path, take[i]), test_take_path)

num_files = int(0.2 * len(remove))
for i in range(num_files):
    shutil.move(os.path.join(train_remove_path, remove[i]), test_remove_path)