#coding=utf-8
'''
Created on 2015年12月31日

@author: admin
'''
import paramiko,sys

class parftp:
    def __init__(self,ip,port,user,pwd):
        self.tp = paramiko.Transport((ip,port))
        self.tp.connect(username=user,password=pwd)
        self.sftp = paramiko.SFTPClient.from_transport(self.tp)
    def filesize(self,filename):
        attr=self.sftp.stat(filename)
        return attr.st_size
    def callback(self,a,b):
        sys.stdout.write('Data Transmission %10d [%3.2f%%]\r' %(a,a*100./int(b)))
        sys.stdout.flush()
    def get_ftp(self,localpath,motepath):
        try:
            self.sftp.get(motepath,localpath,self.callback)
        
        except Exception as e:
            print e
            self.tp.close()
    def put_ftp(self,localpath,motepath):
        try:
            self.sftp.put(localpath,motepath)
        
        except Exception as e:
            print e
            self.tp.close()
    def quit(self):
        self.tp.close()
    
            
if __name__=="__main__":
    ftp=parftp("119.39.48.91",10002,"root","JiaDe~!234")
    try:
        size=ftp.filesize("/www/svn_temp/aaa")
        print size
    except:
        print "filedir not exsixt"
    #attr=ftp.filesize("/opt/WEB.tar.gz")
    #print attr
    #print attr.st_size
    #remotepath='/home/hisuwms/tomcat.tar.gz'
    #localpath='c:/test/tomcat.tar.gz'
    #ftp.get_ftp(localpath, remotepath)
    #ftp.quit()