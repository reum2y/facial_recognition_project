import cv2
import numpy as np
from PIL import Image
import os

path = 'dataset' #경로 (dataset 폴더)

recognizer = cv2.face.LBPHFaceRecognizer_create()
detector = cv2.CascadeClassifier('haarcascades/haarcascade_frontalface_default.xml')

def getImagesAndLabels(path):
    print(path)
    imagePaths = [os.path.join(path,f) for f in os.listdir(path)]
    #listdir : 해당 디렉토리 내 파일 리스트
    #path + file Name : 경로 list 만들기

    faceSamples = []
    ids = []
    print(imagePaths)
    for imagePath in imagePaths: #각 파일마다
        print(imagePath)
        image = [os.path.join(imagePath, f) for f in os.listdir(imagePath)]
        for img in image:
            print(img)
            #흑백 변환
            PIL_img = Image.open(img).convert('L') #L : 8 bit pixel, bw
            print(PIL_img)
            img_numpy = np.array(PIL_img, 'uint8')

            #user id
            id = int(os.path.split(img)[-1].split(".")[1])#마지막 index : -1
            print(id)
            #얼굴 샘플
            faces = detector.detectMultiScale(img_numpy)
            for(x,y,w,h) in faces:
                faceSamples.append(img_numpy[y:y+h,x:x+w])
                ids.append(id)

    return faceSamples, ids

def removeAllFile(filepath):
    if os.path.exists(filepath):
        for file in os.scandir(filepath):
            os.remove(file.path)
        return 'Remove .jpg Files'
    else:
        return 'Could not found Directory'


print('\n [INFO] Training faces. It will take a few seconds. Wait ...')


faces, ids = getImagesAndLabels(path)

recognizer.train(faces,np.array(ids)) #학습

recognizer.write('trainer/trainer.yml')

#print(removeAllFile('dataset'))     #학습완료된 .jpg사진삭제

print('\n [INFO] {0} faces trained. Exiting Program'.format(len(np.unique(ids))))