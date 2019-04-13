import os
import zipfile

cwdpath = os.getcwd()
subdirs = os.listdir(cwdpath)
for i in subdirs:
    path_subdir = os.path.join(cwdpath, i)
    if os.path.isdir(path_subdir):
       print ('compressing', i)
       zip_name = path_subdir + ".zip"
       zip = zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED)
       for j in os.listdir(path_subdir):
           filename = os.path.join(path_subdir, j)
           zip.write(filename, j)
       zip.close()
       print ('compressing finished')
