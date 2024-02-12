import requests
import csv
import os

motors = []

with open("C:/Users/khanh/code/DATA_SCIENCE/data/fill-blank.csv", encoding='utf8') as file_name:
    file_read = csv.reader(file_name)
    motors = list(file_read)
motors = motors[1:]
# download images

data_path = 'C:/Users/khanh/code/DATA_SCIENCE/data/motor_image/'
count = 0
for motor in motors:
    for link in motor[5][2:-2].split('","'):
        # if count<=55033:
        #     count+=1
        #     continue
        file_name = data_path + 'images/' + str(count) + '.jpg'
        with open(file_name, 'wb') as f:
            image = requests.get(link)
            f.write(image.content)
        file_name = data_path + 'labels/' + str(count) + '.txt'
        with open(file_name, 'w', encoding='utf8') as f:
            f.write(motor[12])
        file_name = data_path + 'links/' + str(count) + '.txt'
        with open(file_name, 'w', encoding='utf8') as f:
            f.write(link)
            print(count)
            count+=1

