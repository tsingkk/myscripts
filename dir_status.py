# 分析目录内的文件变化

import os
import json
import time

# 获取目录下所有文件的相对路径列表及最后修改时间字典
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
        print('>>>>>>当前目录已存在文件修改记录日志kkklog.json，读取成功。')
    else:
        print('>>>>>>当前目录未发现文件修改记录日志kkklog.json，将创建。')
        a = {}
    nowstrTime = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
    a[nowstrTime] = f_mtime
    a['last_version'] = nowstrTime
    with open(log_path, 'w') as f:
        json.dump(a, f, ensure_ascii=False)
    print('>>>>>>文件修改记录已保存进日志。')


def printarray(a_array):
    thenum = 0
    for i in a_array:
        thenum += 1
        print('[%d] %s' % (thenum, i))


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
    mklog(workpath, f_mtime_now)
    return f_added, f_edited, f_deleted, flist_now, f_mtime_now


if __name__=='__main__':
    workpath = os.getcwd()
    # 设置需要忽略的文件名列表
    f_ignored = ['kkklog.json']
    f_added, f_edited, f_deleted, flist_now, f_mtime_now = dirstatus(workpath, f_ignored)
    print('='*20+'新增的文件'+'='*20)
    printarray(f_added)
    print('='*20+'修改的文件'+'='*20)
    printarray(f_edited)
    print('='*20+'删除的文件'+'='*20)
    printarray(f_deleted)


    
