# 파일 정렬설치 
# pip install natsort 설치

# os listdir 
import os 

# 이미지가 저장된 디렉토리 경로 
img_dir = './image01_data'

# 디렉토리 내 모든 파일 목록 가져오기
file_list_temp = sorted(os.listdir(img_dir))
print(file_list_temp)
      
# 이미지 정렬하기
img_dir = './image01_data'
file_list_temp01 = sorted(os.listdir(img_dir))
print(file_list_temp01)

# glob.glob
import glob
import os
from natsort import natsort

file_list = glob.glob(os.path.join("사과", "jpg"))

# 이미지 재정렬 
from natsort import natsort
file_list_sort = natsort.natsorted(glob.glob(os.path.join("사과", "*.jpg")))
print(file_list_sort)

# os.walk 
def get_img_paths(root_path):   #하위에 있는 경로 모두 탐색
    file_paths = []
    for (path, dir, files) in os.walk(root_path):
        print("path", path)
        print("dir", dir)
        print("files", files)
        for file in files :
            file_path = os.path.join(path, file)
            print("file_path : ", file_path)
            ext = os.path.splitext(file)[-1].lower()
            print("ext", ext)
            formats_list = [".bmp", ".jpg", ".jpeg", ".png", ".tif",
                            ".dng", ".tiff"]    #이미지 형식 타입(외우기)
            if ext in formats_list:
                file_path = os.path.join(path, file)
                print("file_path :", file_path)
                file_paths.append(file_path)
        return file_paths

file_paths_temp = get_img_paths("./data/")
print(file_paths_temp)

# 이미지 정방형 만들기
# pip3 install image 설치 후 진행
# pip pip install matplotlib 설치 후 진행
from PIL import Image 
import numpy as np
import matplotlib.pyplot as plt

def expand2square(pil_img, background_color):
    width, height = pil_img.size

    #정사각형 
    if width == height:
        return pil_img
    
    # 너비가 높이보다 큰 경우 처리하는 코드 
    elif width > height:
        result = Image.new(pil_img.mode, (width, width), background_color)
        result.paste(pil_img, (0, (width - height) // 2))
        return result 
    else:
        result = Image.new(pil_img.mode, (height, height), background_color)
        result.paste(pil_img, ((height - width) // 2, 0))
        return result 
    
    def resize_with_padding(pil_img, new_size, background_color):
        img = expend2square(pil_img, background_color)
        img = img.resize((new_size[0], new_size[1], Image.ANTIALIAS))
        return img 
    
img = Image.open("./image01.jpg")
img_new = resize_with_padding(img, (300, 300), (0,0,255))

plt.imshow(img)
plt.show()

plt.imshow(img_new)
plt.show()