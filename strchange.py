#coding=utf-8
'''
Created on 2015年12月25日

@author: admin
'''
import re,os,shutil,paramiko,parftp
import tk_msginput as tk

class strChange:
    def __init__(self,file_path,newstr):
        self.file_path=file_path
        self.newstr=newstr
    
    #转换远程文件路径
    def motevar(self,path):
        return self.file_path+path
    
    def checkdir(self):
        if not os.path.exists("f:/test"):
            os.mkdir('f:/test')
        else:
            shutil.rmtree('f:/test')
            os.mkdir('f:/test')
        
    def strchange(self,file,reg,newstr):
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
        #循环修改文件内容
        for i in reg:    
            text=re.sub(i,newstr,text)
        ng.write(text)
        ng.close()
        
    
    def test_main(self,motepath,reg,newstr,ftp):
        
        self.checkdir()
        motefile=self.motevar(motepath)
        filename=motefile.split("/")
        localfile="C:/Users/admin/Desktop/test/"+filename[-1]
        ftp.get_ftp(localfile, motefile)
        
        reg='docBase="(.+?)/webapp/shop" debug="0"'
        self.strchange(localfile,reg,newstr)
        ftp.put_ftp(localfile, motefile)
        
if __name__=="__main__":
    """#接收参数
    inp=tk.tk_Msginput()
    lst=inp.tk_input()
    term=["file_path","newdb","newurl","moteip","moteport","moteuser","motepwd"]
    perfer=dict(zip(term,lst))
    print perfer
    print perfer["newdb"]
    sc=strChange(perfer["file_path"],perfer["newurl"],perfer["newdb"])
    #建立远程连接
    tp=parftp.parftp(perfer['moteip'],int(perfer['moteport']),perfer["moteuser"],perfer["motepwd"])
    """
    #检查文件夹是否存在
    regs=['docBase="(.+?)/webapp/shop" debug="0"',
          'url="jdbc:oracle:thin:@(.+?)"',
          'path="(.+?)/webapp/shop/WEB-INF/index" searchinterval="10"',
          'docBase="(.+?)/webapp/supplier" debug="0"',
          '"imageUrlPrefix": "http://(.+?)/product"',
          'docBase="(.+?)/webapp/erp" debug="0"',
          'path="(.+?)/webapp/shop/WEB-INF/index" searchinterval="10"']
    files=["/soft/tomcat-xmt-shop/conf/server.xml",
           "/webapp/shop/WEB-INF/classes/Database.xml",
           "/webapp/shop/WEB-INF/classes/LuceneConfig.xml",
           "/soft/tomcat-xmt-sp/conf/server.xml",
           "/webapp/supplier/WEB-INF/classes/Database.xml",
           "/webapp/supplier/editor/ueditor/jsp/config.json",
           "/soft/tomcat-xmt-erp/conf/server.xml",
           "/webapp/erp/WEB-INF/classes/Database.xml",
           "/webapp/thread/thread-order/Database.xml",
           "/webapp/thread/thread-other/Database.xml",
           "/webapp/thread/thread-user/Database.xml",
           "/webapp/thread/thread-order/LuceneConfig.xml",
           "/webapp/thread/thread-other/LuceneConfig.xml",
           "/webapp/thread/thread-user/LuceneConfig.xml"]
    
    """for i in regs:
        for j in files:
            #for k in [perfer["file_path"],perfer["newurl"],perfer["newdb"]]:
            k=""
            if "docBase" in i:
                k=perfer["file_path"]
            elif "path" in i:
                k=perfer["file_path"]
            elif i=='url="jdbc:oracle:thin:@(.+?)"':
                k=perfer["newdb"]
            elif i=='"imageUrlPrefix": "http://(.+?)/product"':
                k=perfer["newurl"]
            else:
                print regs
                print "error"
                
                    
            
            sc.test_main(j,i,k,tp)
            print i + " "+"完成"
            
    
    tp.quit()"""
    
    inp=tk.tk_Msginput()
    lst=inp.tk_input()
    term=["file_path","newdb","newurl","moteip","moteport","moteuser","motepwd"]
    perfer=dict(zip(term,lst))
    sc=strChange(perfer["file_path"],perfer["newurl"],perfer["newdb"])
    
    tp=parftp.parftp(perfer['moteip'],int(perfer['moteport']),perfer["moteuser"],perfer["motepwd"])

    
    sc.checkdir()
    motefile=sc.motevar("/soft/tomcat-xmt-shop/conf/server.xml")
    localfile="C:/Users/admin/Desktop/test/server.xml"
    tp.get_ftp(localfile, motefile)
    
    reg='docBase="(.+?)/webapp/shop" debug="0"'
    sc.strchange(localfile,reg,sc.file_path)
    tp.put_ftp(localfile, motefile)
    print motefile+"已完成"    
    #修改第二个文件
    sc.checkdir()
    motefile=sc.motevar("/webapp/shop/WEB-INF/classes/Database.xml")
    localfile="C:/Users/admin/Desktop/test/Database.xml"
    tp.get_ftp(localfile, motefile)
    reg='url="jdbc:oracle:thin:@(.+?)"'
    sc.strchange(localfile,reg,sc.newdb)
    tp.put_ftp(localfile, motefile)
    print motefile+"已完成"  
    
    #修改第三个文件
    sc.checkdir()
    motefile=sc.motevar("/webapp/shop/WEB-INF/classes/LuceneConfig.xml")
    localfile="C:/Users/admin/Desktop/test/LuceneConfig.xml"
    tp.get_ftp(localfile, motefile)
    reg='path="(.+?)/webapp/shop/WEB-INF/index" searchinterval="10"'
    sc.strchange(localfile,reg,sc.file_path)
    tp.put_ftp(localfile, motefile)
    print motefile+"已完成"  
    #修改第四个文件
    sc.checkdir()
    motefile=sc.motevar("/soft/tomcat-xmt-sp/conf/server.xml")
    localfile="C:/Users/admin/Desktop/test/server.xml"
    tp.get_ftp(localfile, motefile)
    reg='docBase="(.+?)/webapp/supplier" debug="0"'
    sc.strchange(localfile,reg,sc.file_path)
    tp.put_ftp(localfile, motefile)
    print motefile+"已完成"  
    
    #修改第五个文件
    sc.checkdir()
    motefile=sc.motevar("/webapp/supplier/WEB-INF/classes/Database.xml")
    localfile="C:/Users/admin/Desktop/test/Database.xml"
    tp.get_ftp(localfile, motefile)
    reg='url="jdbc:oracle:thin:@(.+?)"'
    sc.strchange(localfile,reg,sc.newdb)
    tp.put_ftp(localfile, motefile)
    print motefile+"已完成"  
    
    #修改第六个文件
    sc.checkdir()
    motefile=sc.motevar("/webapp/supplier/editor/ueditor/jsp/config.json")
    localfile="C:/Users/admin/Desktop/test/config.json"
    tp.get_ftp(localfile, motefile)
    reg='"imageUrlPrefix": "http://(.+?)/product"'
    sc.strchange(localfile,reg,sc.newurl)
    tp.put_ftp(localfile, motefile)
    print motefile+"已完成"  
    #修改第七文件
    sc.checkdir()
    motefile=sc.motevar("/soft/tomcat-xmt-erp/conf/server.xml")
    localfile="C:/Users/admin/Desktop/test/server.xml"
    tp.get_ftp(localfile, motefile)
    reg='docBase="(.+?)/webapp/erp" debug="0"'
    sc.strchange(localfile,reg,sc.file_path)
    tp.put_ftp(localfile, motefile)
    print motefile+"已完成"  
    #修改第八个文件
    sc.checkdir()
    motefile=sc.motevar("/webapp/erp/WEB-INF/classes/Database.xml")
    localfile="C:/Users/admin/Desktop/test/Database.xml"
    tp.get_ftp(localfile, motefile)
    reg='url="jdbc:oracle:thin:@(.+?)"'
    sc.strchange(localfile,reg,sc.newdb)
    tp.put_ftp(localfile, motefile)
    print motefile+"已完成"  
    #同步线程配置
    #修改第一个文件
    sc.checkdir()
    motefile=sc.motevar("/webapp/thread/thread-order/Database.xml")
    localfile="C:/Users/admin/Desktop/test/Database.xml"
    tp.get_ftp(localfile, motefile)
    reg='url="jdbc:oracle:thin:@(.+?)"'
    sc.strchange(localfile,reg,sc.newdb)
    tp.put_ftp(localfile, motefile)
    print motefile+"已完成"  
    #修改第二个文件
    sc.checkdir()
    motefile=sc.motevar("/webapp/thread/thread-other/Database.xml")
    localfile="C:/Users/admin/Desktop/test/Database.xml"
    tp.get_ftp(localfile, motefile)
    reg='url="jdbc:oracle:thin:@(.+?)"'
    sc.strchange(localfile,reg,sc.newdb)
    tp.put_ftp(localfile, motefile)
    print motefile+"已完成"  
    
    #修改第三个文件
    sc.checkdir()
    motefile=sc.motevar("/webapp/thread/thread-user/Database.xml")
    localfile="C:/Users/admin/Desktop/test/Database.xml"
    tp.get_ftp(localfile, motefile)
    reg='url="jdbc:oracle:thin:@(.+?)"'
    sc.strchange(localfile,reg,sc.newdb)
    tp.put_ftp(localfile, motefile)
    print motefile+"已完成"  
    #修改第四个文件
    sc.checkdir()
    motefile=sc.motevar("/webapp/thread/thread-order/LuceneConfig.xml")
    localfile="C:/Users/admin/Desktop/test/LuceneConfig.xml"
    tp.get_ftp(localfile, motefile)
    reg='path="(.+?)/webapp/shop/WEB-INF/index" searchinterval="10"'
    sc.strchange(localfile,reg,sc.file_path)
    tp.put_ftp(localfile, motefile)
    print motefile+"已完成"  
    #修改第五个文件
    sc.checkdir()
    motefile=sc.motevar("/webapp/thread/thread-other/LuceneConfig.xml")
    localfile="C:/Users/admin/Desktop/test/LuceneConfig.xml"
    tp.get_ftp(localfile, motefile)
    reg='path="(.+?)/webapp/shop/WEB-INF/index" searchinterval="10"'
    sc.strchange(localfile,reg,sc.file_path)
    tp.put_ftp(localfile, motefile)
    print motefile+"已完成"  
    #修改第六个文件
    sc.checkdir()
    motefile=sc.motevar("/webapp/thread/thread-user/LuceneConfig.xml")
    localfile="C:/Users/admin/Desktop/test/LuceneConfig.xml"
    tp.get_ftp(localfile, motefile)
    reg='path="(.+?)/webapp/shop/WEB-INF/index" searchinterval="10"'
    sc.strchange(localfile,reg,sc.file_path)
    tp.put_ftp(localfile, motefile)
    print motefile+"已完成" 