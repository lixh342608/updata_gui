#coding=utf-8
'''
Created on 2015年12月25日

@author: admin
'''

from Tkinter import *
import tkMessageBox
from xltest import xl_red
import pickle,shutil,re
from updata_gui import *
from fabric.api import *
from test.test_tarfile import tarname
import smtplib  
from email.mime.text import MIMEText
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )
  


#读取配置文件
def loadcol():
    try:
        with open("collocation.pic","r") as f:
            col=pickle.load(f)   
            return col     
    except IOError:
        return 0
#生成配置文件 
def writcol(col):
    with open("collocation.pic","w") as f:
        pickle.dump(col, f)
class tk_Msginput:
    #初始化TKINTER对像形状
    def __init__(self):
        self.root=Tk()
        #self.puttype=0#非分润模式：0分润模式1
        self.root.title("预设参数")
        
        width_n=self.root.winfo_screenwidth()/2-350
        height_n=self.root.winfo_screenheight()/2-300
        #background_image = PhotoImage(file='./image/bg.gif')
        #self.fram=Frame(self.root)
        #self.fram.grid()
        self.pack=0
        #self.textlist=[]
        self.textdict={}
        self.row_list=[]
        self.root.geometry('750x450+%s+%s' % (width_n,height_n))
        #self.background_label = Label(self.root, image=background_image)
        #self.background_label.place(x=0, y=0, relwidth=1, relheight=1)
        self.col=loadcol()

    #如果读取配置文件返回值为0，则弹出提示，并初始化配置信息为“”
    def send_mail(self,mail_text,username,userpw,developers=[]):
        receiver=['xjh@51cul.com','zj@51cul.com','LXH@51cul.com','lrh@51cul.com','cjk@51cul.com']
        for developer in developers:
            if developer=="" or self.col["oper_link"][developer] in receiver:
                pass
            else: 
                receiver.append(self.col["oper_link"][developer])
                #print self.col["oper_link"][developer]
        subject = '功能上线通知'  
        html_msg= '<html><h2>本邮件由工具代发，无需回复</h2><br><h4>%s</h4></html>' % mail_text   
        msg = MIMEText(html_msg,'html','utf-8')  
         
        msg['Subject'] = subject  
        msg['From'] = 'auto_test'
        msg['To'] = "dwb@51cul.com"   
        smtp = smtplib.SMTP()  
        smtp.connect('smtp.exmail.qq.com')  
        smtp.login(username, userpw)  
        smtp.sendmail(username, receiver, msg.as_string())  
        smtp.quit()
    def colback(self):
        if self.col==0:
            tkMessageBox.showinfo("提示：","没有找到可用配置文件，请手动设置相关参数！")
            #self.col=dict.fromkeys(("motecom","pwd","localpath","motepath","moteuser","cal","update_num","backdir"),"")
            self.col=dict.fromkeys(("localpath","cal","update_num","backdir","mailuser","mailpw"),"")
            self.col["puttype"]=self.col["nocake"]=0
            self.col["cake"]=1
            self.col["connext_set"]=[["","","",""],["","","",""]]
            self.col["oper_link"]={u"张建":"zj@51cul.com",
                                  u"王奔":"wangb@51cul.com",
                                  u"姚子丹":"yzd@51cul.com",
                                  u"麦博浪":"mbl@51cul.com",
                                  u"叶国正":"ygz@51cul.com",
                                  u"周树全":"zsq@51cul.com"}
    #初始化控件
    def tk_input(self):
        self.colback()
        #设置文件路径
        self.lab1=Label(self.root,text="请在下方输入远程主机信息（格式：root@192.168.1.5:22）",font = 'Helvetica -15 bold').grid(row=0,column=0,columnspan=3)
    
        motecom_var=StringVar()
    
        e1=Entry(self.root,textvariable=motecom_var).grid(row=1,column=1)
    
        motecom_var.set(self.col["connext_set"][self.col["nocake"]][0])
        cake_motecom_var=StringVar()
    
        cake_e1=Entry(self.root,textvariable=cake_motecom_var).grid(row=3,column=1)
    
        cake_motecom_var.set(self.col["connext_set"][self.col["cake"]][0])
        
        #设置新数据库地址
        #lab2=Label(self.root,text="请在下方输入远程主机密码").grid(row=2,column=0,columnspan=3)
    
        pwd_var=StringVar()
    
        e2=Entry(self.root,textvariable=pwd_var,show="*").grid(row=1,column=4)
    
        pwd_var.set(self.col["connext_set"][self.col["nocake"]][1])
        cake_pwd_var=StringVar()
    
        cake_e2=Entry(self.root,textvariable=cake_pwd_var,show="*").grid(row=3,column=4)
    
        cake_pwd_var.set(self.col["connext_set"][self.col["cake"]][1])

        
        #设置新域名
        lab3=Label(self.root,text="公共设置",font = 'Helvetica -15 bold').grid(row=6,column=0)
    
        localpath_var=StringVar()
    
        e3=Entry(self.root,textvariable=localpath_var).grid(row=7,column=1)
    
        localpath_var.set(self.col["localpath"])
        
        #设置远程主机IP
        #lab4=Label(self.root,text="请在下方输入远程目录地址").grid(row=6,column=0,columnspan=3)
    
        motepath_var=StringVar()
    
        e4=Entry(self.root,textvariable=motepath_var).grid(row=2,column=1)
    
        motepath_var.set(self.col["connext_set"][self.col["nocake"]][2])
        cake_motepath_var=StringVar()
    
        cake_e4=Entry(self.root,textvariable=cake_motepath_var).grid(row=4,column=1)
    
        cake_motepath_var.set(self.col["connext_set"][self.col["cake"]][2])
        
        #设置远程主机端口
        #lab5=Label(self.root,text="请选择上传文件列表").grid(row=10,column=0,columnspan=3)
    
        update_var=StringVar()
    
        e5=Entry(self.root,textvariable=update_var).grid(row=7,column=4)
    
        update_var.set("")
        
        #设置远程主机用户名
        #lab6=Label(self.root,text="请在下方输入程序执行角色（格式：user:group）").grid(row=8,column=0,columnspan=3)
    
        moteuser_var=StringVar()
    
        e6=Entry(self.root,textvariable=moteuser_var).grid(row=2,column=4)
    
        moteuser_var.set(self.col["connext_set"][self.col["nocake"]][3])
        cake_moteuser_var=StringVar()
    
        cake_e6=Entry(self.root,textvariable=cake_moteuser_var).grid(row=4,column=4)
    
        cake_moteuser_var.set(self.col["connext_set"][self.col["cake"]][3])
        cal_var=StringVar()
        e7=Entry(self.root,textvariable=cal_var).grid(row=8,column=1)
        try: 
            if self.col["cal"]:
                cal_var.set(self.col["cal"])
            else:
                cal_var.set(2)    
        except:
            cal_var.set(2)
        back_dir_var=StringVar()
        e8=Entry(self.root,textvariable=back_dir_var).grid(row=8,column=4)
        try: 
            if self.col["backdir"]:
                back_dir_var.set(self.col["backdir"])
            else:
                back_dir_var.set("")    
        except:
            back_dir_var.set("")
        mailuser_var=StringVar()
    
        e9=Entry(self.root,textvariable=mailuser_var,state=DISABLED)
        e9.grid(row=12,column=1)
        try:
            mailuser_var.set(self.col["mailuser"])
        except:
            mailuser_var.set("")
        mailpw_var=StringVar()
    
        e10=Entry(self.root,textvariable=mailpw_var,state=DISABLED,show="*")
        e10.grid(row=12,column=4)
        try:
            mailpw_var.set(self.col["mailpw"])
        except:
            mailpw_var.set("") 
        #back_dir_var.set(self.col["backdir"])
        Label(self.root,text="主服务器信息").grid(row=1,column=0)
        Label(self.root,text="cake服务器主机信息").grid(row=3,column=0)
        Label(self.root,text="主服务器连接密码").grid(row=1,column=3)
        Label(self.root,text="cake服务器连接密码").grid(row=3,column=3)
        Label(self.root,text="源文件地址").grid(row=7,column=0)
        Label(self.root,text="远程地址").grid(row=2,column=0)
        Label(self.root,text="cake远程地址").grid(row=4,column=0)
        Label(self.root,text="更新序号").grid(row=7,column=3)
        Label(self.root,text="用户身份").grid(row=2,column=3)
        Label(self.root,text="cake用户身份").grid(row=4,column=3)
        Label(self.root,text="请确认更新信息后点击右上角绿色按钮进行更新操作").grid(row=9,column=0,columnspan=3)
        Label(self.root,text="校准值").grid(row=8,column=0)
        Label(self.root,text="备份文件目录").grid(row=8,column=3)
        Label(self.root,text="邮箱帐户").grid(row=12,column=0)
        Label(self.root,text="邮箱密码").grid(row=12,column=3)
        for i in range(0,5):
            canv=Canvas(self.root,width=100,height=10)
            canv.grid(row=5,column=i)
            canv.create_rectangle(1,10,100,1,fill="blue")
        def topmsge(master,title,logs):
            
            toproot=Toplevel(master)
            toproot.title(title)
            width_n=toproot.winfo_screenwidth()/2-350
            height_n=toproot.winfo_screenheight()/2-300
            toproot.geometry('750x450+%s+%s' % (width_n,height_n))
            toproot.attributes("-topmost", 1)
            sbar=Scrollbar(toproot)
            sbar.pack(side=RIGHT,fill=Y)
            txt=Text(toproot,width=300,height=30,font = ("Arial, 10"),yscrollcommand=sbar.set)
            txt.pack()
            txt.insert(INSERT,logs)
            sbar.config(command=txt.yview)
            Button(toproot,text="确定",command=(lambda:top_quit()),width=15).pack(side=BOTTOM)
            def top_quit():
                b1["state"]=NORMAL
                toproot.destroy()
                
        #定义按钮动作（继续动作）
        def click_on():
            if self.textdict == {} or self.row_list == []:
                tkMessageBox.showinfo("提示：","请先核对更新信息！")
            else:           
                self.col["connext_set"][self.col["nocake"]][0]=motecom_var.get()
                self.col["connext_set"][self.col["cake"]][0]=cake_motecom_var.get()
                self.col["connext_set"][self.col["nocake"]][1]=pwd_var.get()
                self.col["connext_set"][self.col["cake"]][1]=cake_pwd_var.get()
                self.col["localpath"]=localpath_var.get()
                self.col["connext_set"][self.col["nocake"]][2]=motepath_var.get()
                self.col["connext_set"][self.col["cake"]][2]=cake_motepath_var.get()
                self.col["update_num"]=update_var.get()
                self.col["connext_set"][self.col["nocake"]][3]=moteuser_var.get()
                self.col["connext_set"][self.col["cake"]][3]=cake_moteuser_var.get()
                self.col["cal"]=cal_var.get()
                self.col["backdir"]=back_dir_var.get()
                for item in self.col.values():
                    if item !="":
                        pass
                    else:
                        tkMessageBox.showinfo("提示：","以上所有项不可为空！")
                        break
                else:
                    writcol(self.col)
                    self.pack=1
                    self.root.destroy()
        def read_cell():
            self.textdict.clear()
            update_num=update_var.get()
            if "-" in update_num:
                start_num=int(update_num.split("-")[0])
                stop_num=int(update_num.split("-")[1])+1
                self.row_list=xrange(start_num,stop_num)
            else:
                self.row_list=update_var.get().split(",")
            #print self.row_list
            cal=cal_var.get()
            text=""
            oper=[]
            try:
                for row_num in self.row_list:
                    textlist=[]
                    if row_num:
                        try:
                            cell=xl_red(int(row_num),int(cal))
                        except IndexError:
                            tkMessageBox.showinfo("提示：","更新码%s超出范围，请核对！" % row_num)
                            return "out"
                        items=[["更新代号:",0],
                               ["开发人员:",4],
                               ["SVN版本号:",3],
                               ["\n更新功能:\n",1],
                               ["\n文件列表:\n",2]]
                        text+="\n"
                        for item in items:
                            text+=("*"+item[0]+str(cell[item[1]]))
                            
                            if item[1]==2:
                                filelist=cell[2].split("\n")
                                
                                for file in filelist:
                                    if file:
                                        textlist.append(file)
                                
                                self.textdict[row_num]=textlist
                        oper.append(cell[4])                  
                        if int(row_num)==cell[0]:
                            text+=("\n更新码校验正确，请继续更新!\n"+"*"*30+"我是分割线"+"*"*30+"\n")
                            
                        else:
                            text+=("\n更新码核对不正确，请重查证\n")
                
                return text,oper
            except EXCEPTION as e:
                tkMessageBox.showinfo("提示：",e)
                return "out"
        #定义按钮动作（获取版本号信息）
        def select_on():
                text,oper=read_cell()
                if text=="out":
                    pass
                elif text:
                    topmsge(self.root,"日志详情",text)
                else:
                    tkMessageBox.showinfo("提示：","请正确输入更新码")        
                    
        #定义打包函数
        def remote_set():
            self.col["backdir"]=back_dir_var.get()
            writcol(self.col)
            env.host_string=motecom_var.get()
            env.password=pwd_var.get()
        def bale():
            remote_set()
            upnum_list=update_var.get().split(",")
            text=""
            with cd(self.col["backdir"]):
                for upnum in upnum_list: 
                    if upnum:
                        tarname=upnum+".tar.gz"
                        try:
                            run("tar -zcvf %s %s" % (tarname,upnum))
                            newtext="%s打包成功\n" % tarname
                            text=text+newtext
                        except:
                            newtext="%s打包失败（未找到对应文件或目录！）\n" % tarname
                            
                            text=text+newtext
                            continue
                if text:     
                    tkMessageBox.showinfo("提示：",text)
                else:
                    tkMessageBox.showinfo("提示：","请输入正确的更新码！")
        def del_tar():
            remote_set()
            with cd(self.col["backdir"]):
                try:
                    run("rm -rf ./*.gz")
                    tkMessageBox.showinfo("提示：","删除压缩文件成功！")
                except:
                    tkMessageBox.showinfo("提示：","删除压缩文件失败！")
        def del_all():
            remote_set()
            with cd(self.col["backdir"]):
                try:
                    run("rm -rf ./*")
                    tkMessageBox.showinfo("提示：","清空目录成功！")
                except:
                    tkMessageBox.showinfo("提示：","清空目录失败！")
        #本地临时目录准备
        def checkdir(localdir='f:/test'):
            if not os.path.exists(localdir):
                os.mkdir(localdir)
            else:
                shutil.rmtree(localdir)
                os.mkdir(localdir)
        #返回本地及远程文件路径
        def return_filepath(item,localdir='f:/test'):
            if item=="biz" or item=="admin": 
                remotepath=self.col["connext_set"][self.col["nocake"]][2]+"/"+item+"/"+item+".php"
                print remotepath
                localpath=localdir+"/"+item+".php"
                
            elif item=="mapi":
                remotepath=self.col["connext_set"][self.col["nocake"]][2]+"/mapi/system/config.php"
                localpath=localdir+"/config.php"
            elif "cake" in item:
                remotepath=self.col["connext_set"][self.col["cake"]][2]+"/"+item+"/src/Public/index.php"
                localpath=localdir+"/index.php"
            else:
                remotepath=self.col["connext_set"][self.col["nocake"]][2]+"/"+item+"/src/Public/index.php"
                localpath=localdir+"/index.php"
            return localpath,remotepath
            
        #定义修改文件函数
        def strchange(file,reg,newstr):
            #读取文件
            #try:
            ng=open(file,'r')
            #except Exception as e:
                
            text=ng.read()
            ng.close()
            #以写入方式打开
            ng=open(file,'w')
            #编译传入的正则表达式
            reg=re.compile(reg)
            reg=re.findall(reg,text)
            print "文件%s共找出%d处匹配更改项" % (file,len(reg))
            #循环修改文件内容
            for i in reg:    
                text=re.sub(i,newstr,text)
            ng.write(text)
            ng.close()
        def change_main(localpath,remotepath,item,reg,newstr):
            checkdir()
            try:
                getfile(localpath,remotepath)
            except:
                tkMessageBox.showinfo("提示：","找不到项目%s配置文件" % item)
                return False
            if check_file(localpath,remotepath)==1:
                pass
            else:
                tkMessageBox.showinfo("提示：","%s下载配置文件核对失败" % item)
                return False
            strchange(localpath, reg, newstr)
            putfile(localpath, remotepath)
            if check_file(localpath,remotepath)==1:
                return True
            else:
                tkMessageBox.showinfo("提示：","%s上传配置文件核对失败" % item)
                return False
        #定义修改配置文件主函数
        def change_seting():
            change_text=""
            items=["biz","admin","mapi","huilaapi","cake","cakeapi"]
            reg="define\('PRODUCT','(.+?)'\)"
            newstr="TEST"
            for item in items:
                if "cake" in item:
                    env.host_string=self.col["connext_set"][self.col["cake"]][0]
                    env.password=self.col["connext_set"][self.col["cake"]][1]
                else:
                    env.host_string=self.col["connext_set"][self.col["nocake"]][0]
                    env.password=self.col["connext_set"][self.col["nocake"]][1]
                localpath,remotepath=return_filepath(item)
                if change_main(localpath,remotepath,item,reg,newstr)==False:
                    change_text+=item+"\n"
                    continue
            if change_text != "":
                tkMessageBox.showinfo("提示：", "修改配置文件失败的项目\n%s" % change_text)
            else:
                tkMessageBox.showinfo("提示：", "修改配置文件完成")
        def set_but():
            if check_var.get()==0:
                b4["state"]=DISABLED
                b7["state"]=DISABLED
            else:
                b4["state"]=NORMAL
                b7["state"]=NORMAL
        def send_updatamail():
            
            #developer="dwb@51cul.com"
            text,developers=read_cell()
            
            #print text
            if text=="out":
                pass
            elif text:
                try:
                    self.send_mail(text, self.col["mailuser"], self.col["mailpw"], developers)
                    tkMessageBox.showinfo("提示：","邮件发送成功")
                except:
                    tkMessageBox.showerror("提示：","邮件发送失败")
            else:
                tkMessageBox.show("提示：","请正确输入更新码")
        def set_mail():
            if b8_text_var.get()==u"设置邮箱信息":
                e9["state"]=NORMAL
                e10["state"]=NORMAL
                b8_text_var.set("确定")
            else:
                self.col["mailuser"]=mailuser_var.get()
                self.col["mailpw"]=mailpw_var.get()
                writcol(self.col)
                e9["state"]=DISABLED
                e10["state"]=DISABLED
                b8_text_var.set("设置邮箱信息")
        try: 
        #b1_image = Image.open("./image/open.jpg")
            b2_photo=PhotoImage(file="./image/open.gif")
            b1_photo=PhotoImage(file="./image/start.gif")
            b4_photo=PhotoImage(file="./image/send.gif")
        
            b1=Button(self.root,image=b1_photo,command=click_on,overrelief=FLAT,state=DISABLED)
            b1.grid(row=10,column=4)
            b2=Button(self.root,image=b2_photo,command=select_on,overrelief=FLAT).grid(row=7,column=5)
            #b3=Button(self.root,text="更新码代码打包",command=bale,bd=3,overrelief=FLAT,fg="blue",width=18,height=2).grid(row=10,column=1)
            b4=Button(self.root,image=b4_photo,command=send_updatamail,state=DISABLED,overrelief=FLAT)
            b4.grid(row=10,column=1)
            #b5=Button(self.root,text="清空备份目录",command=del_all,bd=3,overrelief=FLAT,fg="blue",width=18,height=2).grid(row=12,column=1)
            b6=Button(self.root,text="退出程序",command=(lambda x=self.root:x.destroy()),bd=3,overrelief=FLAT,fg="blue",width=16,height=2).grid(row=11,column=4)
            check_var=IntVar()
            cbut1=Checkbutton(self.root,text="开启配置和邮件功能",variable=check_var,command=set_but).grid(row=11,column=2)
            b7=Button(self.root,text="重置环境配置",command=change_seting,bd=3,width=18,height=2,state=DISABLED,fg="blue")
            b7.grid(row=11,column=1)
            b8_text_var=StringVar()
            b8=Button(self.root,textvariable=b8_text_var,command=set_mail,bg="yellow",fg="blue")
            b8_text_var.set("设置邮箱信息")
            b8.grid(row=12,column=2)
        except:
            tkMessageBox.showerror("提示：","找不到需要的图片素材，退出程序！")
            self.root.destroy()
        self.root.mainloop()
        return self.pack,self.textdict,self.row_list
if __name__=="__main__":
    #定义更新主函数
    def main():
        act=tk_Msginput()
        pack,textdict,row_list=act.tk_input()
        if pack==0:
            pass
        else:
            col=loadcol()
            #print col
            put=updata_list(col,textdict,row_list)
            pack=put.updata_File()
            if pack==1:
                main()
    #try:
    main()
    #except Exception as e:
        #tkMessageBox.showinfo("错误提示：",e)