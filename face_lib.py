import os
import json
import time
import face_recognition
import pickle
import shutil
import random
import sys


def getallfiles(path, f_ignored):
    flist = []
    f_mtime = {}
    for root, dirs, fs in os.walk(path):
        for f in fs:
            if f not in f_ignored:
                f_fullpath = os.path.join(root, f)
                f_relativepath = f_fullpath[(len(path)+1):]
                flist.append(f_relativepath)
                mtimef = os.path.getmtime(f_fullpath)
                localTime = time.localtime(mtimef)
                strTime = time.strftime('%Y%m%d%H%M%S', localTime)
                f_mtime[f_relativepath] = strTime
    return flist, f_mtime

def mklog(workpath, f_mtime):
    log_path = os.path.join(workpath, 'kkklog.json')
    if os.path.exists(log_path):
        with open(log_path, 'r') as f:
            a = json.load(f)
        #print('>>>>>>当前目录已存在文件修改记录日志kkklog.json，读取成功。')
    else:
        #print('>>>>>>当前目录未发现文件修改记录日志kkklog.json，将创建。')
        a = {}
    nowstrTime = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
    a[nowstrTime] = f_mtime
    a['last_version'] = nowstrTime
    with open(log_path, 'w') as f:
        json.dump(a, f, ensure_ascii=False)
    #print('>>>>>>文件修改记录已保存进日志。')

def dirstatus(workpath, f_ignored):
    f_deleted = []
    f_added = []
    f_edited = []
    flist_now, f_mtime_now = getallfiles(workpath, f_ignored)
    log_path = os.path.join(workpath, 'kkklog.json')
    if os.path.exists(log_path):
        with open(log_path, 'r') as f:
            a = json.load(f)
        last_version = a['last_version']
        f_mtime_last = a[last_version]
        flist_last = set(f_mtime_last.keys())
        f_deleted = list(flist_last - set(flist_now))
        for f in flist_now:
            if f in flist_last:
                if f_mtime_now[f] != f_mtime_last[f]:
                    f_edited.append(f)
            else:
                f_added.append(f)
    else:
        f_added = flist_now
    return f_added, f_edited, f_deleted, flist_now, f_mtime_now

def get_faceencodings(imgpath):
    image = face_recognition.load_image_file(imgpath)
    knwon_face_encodings = face_recognition.face_encodings(image)
    if len(knwon_face_encodings) == 0:
        x = 0
        a = '没有识别出人脸！'
    else:
        x = 1
        a = knwon_face_encodings[0]
    return x, a

def printarray(a_array):
    thenum = 0
    for i in a_array:
        thenum += 1
        print('[%d] %s' % (thenum, i))

def getrandom(randomlength=8):
  """
  生成一个指定长度的随机字符串
  """
  digits = '0123456789'
  ascii_letters = 'abcdefghigklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
  str_list = [random.choice(digits + ascii_letters) for i in range(randomlength)]
  random_str = ''.join(str_list)
  return random_str

def face_lib():
    imgsdir = os.path.join(os.getcwd(), 'face-lib')
    if not os.path.exists(imgsdir):
        print('>>>>>>当前目录中不存在人脸图像库目录<face-lib>，需创建。')
        sys.exit()
    if os.path.exists('face_lib.pkl'):
        with open('face_lib.pkl', 'rb') as f:
            have_face = pickle.load(f)
    else:
        have_face = {}
    not_rec_face_paths_added = []
    not_rec_face_paths_edited = []
    rec_face_paths_added = []
    rec_face_paths_edited = []
    f_ignored = ['kkklog.json']
    f_added, f_edited, f_deleted, flist_now, f_mtime_now = dirstatus(imgsdir, f_ignored)
    for i in f_added:
        all_img_path = os.path.join(imgsdir, i)
        x, a_face_encoding = get_faceencodings(all_img_path)
        if x == 0:
            not_rec_face_paths_added.append(i)
        else:
            have_face[i] = a_face_encoding
            rec_face_paths_added.append(i)
    for i in f_edited:
        all_img_path = os.path.join(imgsdir, i)
        x, a_face_encoding = get_faceencodings(all_img_path)
        if x == 0:
            not_rec_face_paths_edited.append(i)
            have_face.pop(i)
        else:
            have_face[i] = a_face_encoding
            rec_face_paths_edited.append(i)
    if len(f_deleted) != 0:
        print('>>>>>>以下图像文件已不存在，将从人脸编码库中移除。')
        printarray(f_deleted)
        for i in f_deleted:
            have_face.pop(i)
        ccc = len(f_deleted) + len(not_rec_face_paths_edited)
    else:
        ccc = len(not_rec_face_paths_edited)
    with open('face_lib.pkl', 'wb') as f:
        pickle.dump(have_face, f)
    aaa = len(rec_face_paths_added)
    bbb = len(rec_face_paths_edited)
    print('='*20+'人脸编码库更新情况'+'='*20)
    print('已新增%d张人脸编码，已修改%d张人脸编码，已删除%d张人脸编码。' % (aaa,bbb,ccc))
    print('人脸编码库共有%d条数据。' % len(have_face))
    print('='*58)
    not_rec_face_paths = not_rec_face_paths_added + not_rec_face_paths_edited
    if len(not_rec_face_paths) != 0:
        print('>>>>>>以下图像未能识别出人脸，将从人脸图像库中移除。')
        printarray(not_rec_face_paths)
        not_rec_face_dir = os.path.join(os.getcwd(), 'not_rec_face')
        if not os.path.exists(not_rec_face_dir):
            os.mkdir(not_rec_face_dir)
        for i in not_rec_face_paths:
            full_img_path = os.path.join(imgsdir, i)
            #os.remove(full_img_path)
            new_name = getrandom(8) + '-' + i
            full_img_move_to = os.path.join(not_rec_face_dir, new_name)
            shutil.move(full_img_path, full_img_move_to)
            f_mtime_now.pop(i)
        ddd = len(f_deleted) + len(not_rec_face_paths_edited)
        eee = aaa
        fff = bbb
        flist_now = list(set(flist_now) - set(not_rec_face_paths))
    else:
        ddd = len(f_deleted)
        eee = len(f_added)
        fff = len(f_edited)
    print('='*20+'人脸图像库更新情况'+'='*20)
    print('已新增%d张人脸图像，已修改%d张人脸图像，已删除%d张人脸图像。' % (eee,fff,ddd))
    mklog(imgsdir, f_mtime_now)
    print('人脸图像库共有%d张图像。' % len(flist_now))
    print('='*58)


if __name__=='__main__':
    face_lib()
    print(">>>>>>人脸编码录入完成！")
    
    