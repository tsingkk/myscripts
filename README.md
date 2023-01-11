# myscripts
some simple scripts for work and play written by myself in Python.

**RSShub_make_RSS.py**: a python3 script that converts weburl to rss feed made by RSSHub. 

**selectmovie.py**: a python3 script that helps me choose a video at random from your computer disc.

**batch_compress.py**: a python3 script that finishes batch compression of directories in the current directory.

**get_load_diatance.py**: a python3 script that acquires a batch of transportation distance between the two places from [lbs.amap.com](https://lbs.amap.com), and then saves the data in a xlsx file. The instructions of this script: [利用 Python 批量获取县镇运输距离](https://blog.3gek.cc/posts/2019/09/li-yong-pythonpi-liang-huo-qu-xian-zhen-ju-chi/)

**face_lib.py**：批量识别并采集图像中人脸编码，生成人脸编码库文件。
    - 用来识别人脸的图像，需放在当前工作目录下的子目录`face-lib`中；
    - 用来识别的人脸图像，一张图像中最好只含一张人脸，多出的人脸不会被存储编码；
    - 人脸编码被存储在当前工作目录下的文件`face_lib.pkl`中；
    - 子目录`face-lib`中无法识别出人脸的图像，会被移动到子目录`not_rec_face`中；
    - 更新子目录`face-lib`中人脸图像文件，重新运行程序会进行增量识别并更新`face_lib.pkl`。

**face_rec.py**：给一张未知人脸的图像，从`face_lib.py`生成的人脸编码库中，对比出相似人脸。
    - 未知人脸图像，最好只包含一张人脸，多余人脸不会被对比；
    - 当前工作目录中需存在人脸编码库文件`face_lib.pkl`；
    - 可设定容差参数`tolerance`，默认值0.4；
    - 识别对比后程序会给出相似人脸的文件名。

**dir_status.py**：分析并记录当前工作目录中的文件变化情况：
    - 初次运行会在当前目录下生成文件`kkklog.json`用于记录文件变化；
    - 文件是否修改，采用对比*文件名+修改时间*的方法；
    - 运行程序后会给出相对于上一次运行是当前目录内的文件变化（新增、修改、删除）情况。


