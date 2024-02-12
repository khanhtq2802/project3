import os

images_path = "C:/Users/khanh/code/DATA_SCIENCE/data/clean_images/images/"
labels_path = "C:/Users/khanh/code/DATA_SCIENCE/data/clean_images/labels/"
links_path = "C:/Users/khanh/code/DATA_SCIENCE/data/clean_images/links/"

images_list = os.listdir(images_path)
labels_list = os.listdir(labels_path)
links_list = os.listdir(links_path)

for i in range(len(images_list)):
    images_list[i] = images_list[i].replace('jpg','txt')

remove_labels_list = list(set(labels_list).difference(set(images_list)))
remove_links_list = list(set(links_list).difference(set(images_list)))

for i in remove_labels_list:
    os.remove(labels_path+i)
for i in remove_links_list:
    os.remove(links_path+i)