import os
import zipfile

zf = zipfile.ZipFile("myzipfile.zip", "w")

for dirname, subdirs, files in os.walk("./user/songdir/Bonrix_SS/Employee_1"):
    for filename in files:
        zf.write(os.path.join(dirname, filename))
zf.close()
