import face_recognition
import pickle
import os
import sys


def printarray(a_array):
    thenum = 0
    for i in a_array:
        thenum += 1
        print('[%d] %s' % (thenum, i))

def face_compare():
    if not os.path.exists('face_lib.pkl'):
        print('>>>>>>当前目录中不存在人脸编码库文件<face_lib.pkl>，需创建。')
        sys.exit()
    a_imgpath = input('输入用于人脸对比的图片绝对路径（图片中仅能有一个人脸）：')
    a_tolerance = input('输入容差，数值越小识别结果相似性越大（取值0~1，默认0.4）：')
    a_tolerance = float(a_tolerance or '0.4')
    image = face_recognition.load_image_file(a_imgpath)
    unknwon_face_encodings = face_recognition.face_encodings(image)
    unknwon_face_encoding = unknwon_face_encodings[0]
    with open('face_lib.pkl', 'rb') as f:
        face_encodings = pickle.load(f)
    match_faces = []
    for i in face_encodings.keys():
        matches = face_recognition.compare_faces(
            [face_encodings[i]],
            unknwon_face_encoding,
            tolerance=a_tolerance
        )
        print(matches)
        if matches[0] == True:
            match_faces.append(i)
    if len(match_faces) == 0:
        print('>>>>>>人脸库中没有找到相似人脸。')
    else:
        print('>>>>>>该人脸与以下人脸相似：')
        printarray(match_faces)


if __name__=='__main__':
    face_compare()
    print('>>>>>>人脸识别完毕。')