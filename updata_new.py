#coding=utf-8
'''
Created on 2017年1月13日

@author: pc
'''
from Tkinter import *
import tkMessageBox
from fabric.api import *
from fabric.contrib.console import confirm
from tk_msginput import *
from xltest import xl_red,xl_write
import os,xlrd,threading,time
from tkFileDialog  import asksaveasfilename
from multiprocessing import Pool

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
        self.badtxt=""
        #初始化上传正确数和错误数
        self.num=0
        self.bad=0
        #需要上传更新文件总数
        self.count=0
        self.col=col
    def gui_init(self):
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
        def select_bad():
            if self.badtxt:
                tkMessageBox.showinfo("提示：",self.badtxt)
            else:
                tkMessageBox.showinfo("提示：","没有错误信息！")
        self.root=Tk()
        self.root.title("文件更新")
        
        try:
            self.background_image = PhotoImage(file='image/bg.gif')
            self.root.iconbitmap('image/edi.ico')
        except:
            tkMessageBox.showerror("提示：","找不到需要的图片素材，退出程序！")
        w = self.background_image.width()
        h = self.background_image.height()
        width_n=self.root.winfo_screenwidth()/2-350
        height_n=self.root.winfo_screenheight()/2-300
        self.root.geometry('%dx%d+%d+%d' % (w,h,width_n,height_n))
        self.root.attributes("-alpha",0.9)
        background_label = Label(self.root, image=self.background_image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
        
        
        self.framl=Frame(self.root,height=500,width=100,bd=10)
        strs="工具提示：本工具只适用简单上传文件，请尽量保证输入数据可用性，上传列表文件只读取第一个字符为‘/’的文件。"
        self.lab1=Label(self.framl,text=strs,wraplength = 80,justify = 'left',font = ("Arial, 14"))
        self.lab1.pack()
        self.framl.pack(side=LEFT)
        self.framt=Frame(self.root,bd=10,bg="green")
        self.ask=StringVar()
        self.lab2=Label(self.framt,textvariable=self.ask,font = ("Arial, 12"))
        self.lab2.pack()
        self.ask.set("正在准备开始！")
        self.framt.pack(side=TOP)
        self.framlog=Frame(self.root)
        self.framlog.pack()
        self.sbar=Scrollbar(self.framlog)
        self.sbar.pack(side=RIGHT,fill=Y)
        self.log=Text(self.framlog,width=90,height=30,font = ("Arial, 10"),yscrollcommand=self.sbar.set,background="#B0C4DE")
        self.log.pack()
        self.sbar.config(command=self.log.yview)
        Button(self.root,text="退出程序",command=(lambda x=self.root:x.destroy()),bg="#B0C4DE").pack(padx=10,side=RIGHT)
        Button(self.framl,text="标记日志已更新",command=saved,bg="#B0C4DE").pack(pady=5)
        Button(self.framl,text="另存日志到本地",command=asSavelocal,bg="#B0C4DE").pack(pady=5)
        Button(self.framl,text="查看错误信息",command=select_bad,bg="yellow").pack(pady=5) 
        Button(self.root,text="继续更新=》",command=let_go,bg="#B0C4DE").pack(padx=10,side=LEFT) 
        self.root.mainloop()
    def log_insert(self,txt):
        try:
            self.log.insert(INSERT,txt)
            self.log.see(INSERT)
        except TclError:
            self.log.insert(INSERT,"进程阻塞，等待3秒！")
            time.sleep(3)
            self.log_insert(txt)
            
        
    #上传文件
    def updata_File(self):
        th=threading.Thread(target=self.gui_init)
        th.start()
 
        def badtxtinfo(file,typenum):
            if typenum==1:
                txt="错误%d:%s为目录！\n" % (self.bad,file)
            elif typenum==2:
                txt="警告:文件%s不存在！\n" % (file)
            else:
                txt="错误%d:%s上传失败！\n" % (self.bad,file)
            self.badtxt+=txt
            return txt
                
        #更新本地代码库
        local("svn update "+self.col["localpath"])
        
        for key in self.filedict.keys():
            self.count+=len(self.filedict[key])
        #keylist=self.filedict.keys()
        #count=len(self.filelist)
        
        #遍历更新文件列表

        for key in self.filedict.keys():
            try:
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
                    self.ask.set("正在上传第%d个文件,完成度：%d/%s 错误数：%d" % (self.num+1,self.num,self.count,self.bad))
                    self.log_insert("开始上传%s\n" % file)
                    localpath=self.col["localpath"]+file
                    remotepath=self.col["connext_set"][self.col["puttype"]][2]+file
                    #判断本地文件是否存在
                    if os.path.isfile(localpath)==False:
                        #判断本地文件是否目录
                        if os.path.isdir(localpath)==True:
                            self.bad+=1
                            txt=badtxtinfo(file, 1)
                            self.log_insert(txt)
                            
                            continue
                        else:
                            txt=badtxtinfo(file, 2)
                            #文件不存在时同步删除服务器对应文件
                            self.log_insert(txt)
                            com="""if [ -f "%s" ]; then
                                       rm -f %s
                                   fi""" % (remotepath,remotepath)
                            run(com)
                            self.log_insert("同步删除服务器文件%s\n" % localpath)
                            self.num+=1
                            continue
                    filepath=os.path.split(remotepath)[0]
                    self.log_insert("%s==>>%s\n" % (localpath,remotepath))
                    txt="正在创建目录%s\n" % (filepath)
                    self.log_insert(txt)
                    run("install -d %s" % filepath)
                    #给上传文件授权
                    run("chmod 755 %s" % filepath)
                    #给上传文件重置属主、属组
                    run("chown -R %s %s" % (self.col["connext_set"][self.col["puttype"]][3],master_dir))
                    self.log_insert("正在上传文件%s\n" % (localpath))
                    putfile(localpath,remotepath)
                    t=check_file(localpath,remotepath)
                    if t==1:
                        print "文件%s上传成功" % file
                        self.log_insert("%s上传成功！\n" % file)
                        self.num+=1
                    else:
                        self.bad+=1
                        txt=badtxtinfo(file, 3)
                        self.log_insert(txt)
                        
                    #给上传文件授权
                    run("chmod 755 %s" % remotepath)
                    #给上传文件重置属主、属组
                    run("chown -R %s %s" % (self.col["connext_set"][self.col["puttype"]][3],remotepath))
                    self.log_insert("上传完成，正在删除系统缓存！\n")
                    run("rm -rf %s/public/runtime/*" % master_dir)
                    time.sleep(2)
            except EXCEPTION:
                self.bad+=1
                self.badtxt+="错误%d:程序 出错！"
                time.sleep(3)
        self.ask.set("上传完成%d/%s 错误数：%d" % (self.num,self.count,self.bad))
        th.join()
        return self.pack



if __name__=="__main__":
    main()