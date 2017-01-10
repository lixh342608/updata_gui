#coding=utf-8
'''
Created on 2016年10月18日

@author: pc
'''
#更新
from Tkinter import *
import tkMessageBox
from fabric.api import *
from fabric.contrib.console import confirm
from tk_msginput import *
from xltest import xl_red,xl_write
import os,xlrd
from tkFileDialog  import asksaveasfilename
#读取待更新文件路径列表（row_num+cal行，第五列）
"""def readf(row_num,cal):
    filelist=[]
    cell=xl_red(row_num,cal)
    upfilelist=cell[2].split("\n")
    for file in upfilelist:
        if file:
            filelist.append(file)
    return filelist   """
#下载文件
def getfile(localpath,remotepath):
    with settings(warn_only=True):
        result=get(remotepath,localpath)
    #if result.failed and not confirm("get file failed,continue[Y/N]"):
        #abort("Aborting file get task!")

#上传文件
def putfile(localpath,remotepath):
    with settings(warn_only=True):
        result=put(localpath,remotepath)
    #if result.failed: and not confirm("get file failed,continue[Y/N]"):
        #abort("Aborting file get task!")
    #else:
        #print "put file ok!" 
#根据MD5校验上传文件是否正确   
def check_file(localpath,remotepath):
    with settings(warn_only=True):
        lmd5=local("certutil -hashfile %s MD5" % localpath,capture=True).split("\r\n")[1].replace(' ','')
        rmd5=run("md5sum %s" % remotepath).split(' ')[0]
    if lmd5==rmd5:
        return 1
    else:
        return 0
def back_file(file,packgename,backdir="/opt/back"):
    backfile=backdir+"/"+str(packgename)+file
    file_backpath=os.path.split(backfile)[0]
    run("install -d %s" % file_backpath)
    return backfile
class updata_list:
    #初始化tkinter
    def __init__(self,col,filedict,row_list):
        self.filedict=filedict
        self.row_list=row_list
        self.pack=0
        self.col=col
        self.root=Tk()
        self.root.title("文件更新")
        width_n=self.root.winfo_screenwidth()/2-200
        height_n=self.root.winfo_screenheight()/2-250
        self.root.geometry('500x500+%s+%s' % (width_n,height_n))
        self.framl=Frame(self.root,height=500,width=100,bd=10)
        strs="工具提示：本工具只适用简单上传文件，请尽量保证输入数据可用性，上传列表文件只读取第一个字符为‘/’的文件。"
        self.lab1=Label(self.framl,text=strs,wraplength = 80,justify = 'left',font = ("Arial, 14"))
        self.lab1.pack()
        self.framl.pack(side=LEFT)
        self.framt=Frame(self.root,height=100,width=425,bd=10,bg="green")
        self.ask=StringVar()
        self.lab1=Label(self.framt,textvariable=self.ask,font = ("Arial, 28"))
        self.lab1.pack()
        self.ask.set("正在准备开始！")
        self.framt.pack(side=TOP)
        self.log=Text(self.root,width=50,height=30,font = ("Arial, 10"))
        self.log.pack()
    #上传文件
    def updata_File(self):
        #定义标记文件动作
        def saved():
            for row in self.row_list:
                wrcode=xl_write(int(row),int(self.col["cal"]))
                if wrcode:
                    pass
                else:
                    tkMessageBox.showinfo("提示：","该文件已在其它程序打开，保存失败！")
                    break
            if wrcode:
                    
                tkMessageBox.showinfo("提示：","保存成功！")
            
        #定义保存日志文件到本地动作
        def asSavelocal():
            
            filename=asksaveasfilename(initialfile=u"更新日志.xls")
            for row in self.row_list:
               
                wrcode=xl_write(int(row),int(self.col["cal"]),xlfile=filename)
                if wrcode:
                    
                    tkMessageBox.showinfo("提示：","保存成功！")
                else:
                    tkMessageBox.showinfo("提示：","该文件已在其它程序打开，保存失败！")
        #定义继续更新动作，将返回值pack置为1
        def let_go():
            self.pack=1
            self.root.destroy()

        #更新本地代码库
        local("svn update "+self.col["localpath"])
        #初始化上传正确数和错误数
        num=0
        bad=0
        #需要上传更新文件总数
        count=0
        for key in self.filedict.keys():
            count+=len(self.filedict[key])
        
        #count=len(self.filelist)
        #遍历更新文件列表
        
            for file in self.filedict[key]:
                if file[1:5]=="cake":
                    self.col["puttype"]=self.col["cake"]
                else:
                    self.col["puttype"]=self.col["nocake"]
                env.host_string=self.col["connext_set"][self.col["puttype"]][0]
                env.password=self.col["connext_set"][self.col["puttype"]][1]
                file=file.strip()
                pathlist=file.split("/")
                master_dir=self.col["connext_set"][self.col["puttype"]][2]+"/"+pathlist[1]
                self.ask.set("正在上传第%d个文件%d/%s" % (num+1,num,count))
                self.log.insert(INSERT,"开始上传%s\n"% file)
                localpath=self.col["localpath"]+file
                remotepath=self.col["connext_set"][self.col["puttype"]][2]+file
                #判断本地文件是否存在
                if os.path.isfile(localpath)==False:
                    #判断本地文件是否目录
                    if os.path.isdir(localpath)==True:
                        self.log.insert(INSERT,"%s为目录\n" % localpath)
                        bad+=1
                        continue
                    else:
                        #文件不存在时同步删除服务器对应文件
                        self.log.insert(INSERT,"文件%s本地不存在\n" % localpath)
                        com="""if [ -f "%s" ]; then
                                   rm -f %s
                               fi""" % (remotepath,remotepath)
                        run(com)
                        self.log.insert(INSERT,"同步删除服务器文件%s\n" % localpath)
                        num+=1
                        continue
                filepath=os.path.split(remotepath)[0]
                self.log.insert(INSERT,localpath+"==>>"+remotepath+"\n")
                self.log.insert(INSERT,"正在创建目录"+filepath+"\n")
                run("install -d %s" % filepath)
                #给上传文件授权
                run("chmod 755 %s" % filepath)
                #给上传文件重置属主、属组
                run("chown -R %s %s" % (self.col["connext_set"][self.col["puttype"]][3],master_dir))
                self.log.insert(INSERT,"正在上传文件%s\n" % localpath)
                putfile(localpath,remotepath)
                remote_backpath=back_file(file, key,self.col["backdir"])
                putfile(localpath,remote_backpath)
                t=check_file(localpath,remotepath)
                if t==1:
                    print "文件%s上传成功" % file
                    self.log.insert(INSERT,"%s上传成功！\n" % file)
                    num+=1
                else:
                    self.log.insert(INSERT,"%s上传失败！\n" % file)
                    bad+=1
                #给上传文件授权
                run("chmod 755 %s" % remotepath)
                #给上传文件重置属主、属组
                run("chown -R %s %s" % (self.col["connext_set"][self.col["puttype"]][3],remotepath))
                self.log.insert(INSERT,"上传完成，正在删除系统缓存！\n")
                run("rm -rf %s/public/runtime/*" % master_dir)
        self.ask.set("上传完成%d/%s" % (num,count))
        #self.log.insert(INSERT,"上传完成，正在删除系统缓存！\n")
        #删除缓存
        #run("rm -rf %s/public/runtime/*" % master_dir)
        tkMessageBox.showinfo("提示：","上传完成 错误数：%s" % bad)
        Button(self.root,text="退出程序",command=(lambda x=self.root:x.destroy()),bg="red").pack(padx=10,side=RIGHT)
        Button(self.framl,text="标记日志已更新",command=saved,bg="red").pack(pady=5)
        Button(self.framl,text="另存日志到本地",command=asSavelocal,bg="red").pack(pady=5) 
        Button(self.root,text="继续更新=》",command=let_go,bg="red").pack(padx=10,side=LEFT) 
        self.root.mainloop()
        return self.pack  
if __name__=="__main__":
    """filelist=readf(2)
    print filelist
    col={"upfile":"F:/test/201610160857.txt",
         "remotecom":"root@119.39.48.91:10002 ",
         "remotepwd":"JiaDe~!234",
         "localpath":"F:/test",
         "remotepath":"/data/wwwroot/51yushtest",
         "moteuser":"root:root"
         }
    col={'motecom': 'root@119.39.48.91:10002', 
    'localpath': 'f:/svn_out', 
    'pwd': 'JiaDe~!234', 
    'motepath': '/data/wwwroot/51yushtest', 
    'moteuser': 'root:root', 
    'update_num':2}"""
    def main():
        act=tk_Msginput()
        act.colback()
        pack=act.tk_input()
        #print pack
        if pack==0:
            pass
        else:
            col=loadcol()
            #print col
            c1=updata_list(col)
            pack=c1.updata_File()
            if pack==1:
                main()
    main()
    
    
