#coding=utf-8
'''
Created on 2016年3月4日

@author: admin
'''
from fabric.api import *
from fabric.contrib.console import confirm
import readfile as f
import os

#env.user="root"
env.host_string='root@119.39.48.91:10002'
env.password='JiaDe~!234'

def getfile(localpath,remotepath):
    with settings(warn_only=True):
        result=get(remotepath,localpath)
    if result.failed and not confirm("get file failed,continue[Y/N]"):
        abort("Aborting file get task!")
def putfile(localpath,remotepath):
    with settings(warn_only=True):
        result=put(localpath,remotepath)
    if result.failed and not confirm("get file failed,continue[Y/N]"):
        abort("Aborting file get task!")
    else:
        print "put file ok!"    
def check_file(localpath,remotepath):
    with settings(warn_only=True):
        lmd5=local("certutil -hashfile %s MD5" % localpath,capture=True).split("\r\n")[1].replace(' ','')
        rmd5=run("md5sum %s" % remotepath).split(' ')[0]
        print "lmd5_value:%s" % lmd5
        print "Rmd5_value:%s" % rmd5
    if lmd5==rmd5:
        print "check over"
    else:
        print "check fail"
"""def untar(remotepath):
    pathlable=os.path.split(remotepath)
    dname=os.path.splitext(pathlable[1])[0]
    #with cd(pathlable[0]):
    runs=run("unzip " + remotepath+" -d "+ pathlable[0])
        run("cp -rf "+ dname+"/* "+"tester/")
    with cd(pathlable[0]+"tester/"):
        run("ll")"""

def main():
    fabdict=dict(f.readfile("fabtest.csv"))
    localpath=fabdict['localpath']
    remotepath=fabdict['remotepath']
    #putfile(localpath,remotepath)
    #check_file(localpath,remotepath)
    
    untar(remotepath)

    
if __name__=="__main__":
    main()

    
