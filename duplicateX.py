import os
import csv

reading_dir = "restaurants" # 중복을 제거할 파일들이 있는 디렉토리
targetArea = "광진구"
# 잠실 -> 송파구 , 건대 -> 광진구 , 홍대 -> 마포구 , 강남 -> 강남구
dupX = set()
newData = []
fileList = os.listdir(reading_dir)

for file in fileList:

    fileName = file

    f = open(reading_dir + '/'  + fileName , 'r')
    reader = csv.reader(f)

    i = 0

    for line in reader:
        restaurant_id = line[5]
        if restaurant_id in dupX or targetArea not in line[6]:
            continue
        else:
            dupX.add(restaurant_id)
            newData.append(line)

        i += 1

nf = open('final.csv'  , 'w')
writer = csv.writer(nf)

for line in newData:
    writer.writerow(line)

f.close()
nf.close()
