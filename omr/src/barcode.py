# -*- coding: utf-8 -*-
import subprocess as sp
import glob

zbar=["C:\\Program Files (x86)\\ZBar\\bin\\zbarimg","-q",""]
files=glob.glob("folha.jpg")
print files
for fn in files:
    zbar[-1]=fn
    code=sp.check_output(zbar)
    print code.split(':')[1][:-1]
