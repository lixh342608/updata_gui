#coding=utf-8
'''
Created on 2015年12月25日

@author: admin
'''
 
import smtplib  
from email.mime.text import MIMEText  
  
sender = 'LXH@51cul.com'
receiver=[]  
receiver.append('dwb@51cul.com')
receiver.append('LXH@51cul.com')
subject = 'python email test'  
smtpserver = 'smtp.exmail.qq.com'  
username = 'LXH@51cul.com'  
password = 'Abc123..'     
msg = MIMEText('<html><h1>你好</h1></html>','html','utf-8')  
 
msg['Subject'] = subject  
msg['From'] = sender
msg['To'] = "dwb@51cul.com"   
smtp = smtplib.SMTP()  
smtp.connect(smtpserver)  
smtp.login(username, password)  
smtp.sendmail(sender, receiver, msg.as_string())  
smtp.quit()
print "send ok!"  




"""import smtplib
from email.mime.text import MIMEText
 
SMTPserver = 'smtp.exmail.qq.com'
sender = 'LXH@51cul.com'
password = "Abc123.."

message = '不简单呀. 你好'
msg = MIMEText(message,"utf-8")
 
msg['Subject'] = 'Test Email by Python'
msg['From'] = sender
msg['To'] = "dwb@51cul.com"

mailserver = smtplib.SMTP(SMTPserver, 25)

mailserver.login(sender, password)

mailserver.sendmail(sender, [sender,"dwb@51cul.com"], msg.as_string())

mailserver.close()
print 'send email success'"""

"""root = Tk()                                                     # explicit root
    
trees = [('The Larch!',          'light blue'),
         ('The Pine!',           'light green'),
         ('The Giant Redwood!', 'red')]
    
for (tree, color) in trees:
    win = Toplevel(root)                                        # new window
    win.title('Sing...')                                        # set border
    win.protocol('WM_DELETE_WINDOW', lambda:0)                  # ignore close
    #win.iconbitmap('py-blue-trans-out.ico')                     # not red Tk
    
    msg = Button(win, text=tree, command=win.destroy)           # kills one win
    msg.pack(expand=YES, fill=BOTH)
    msg.config(padx=10, pady=10, bd=10, relief=RAISED)
    msg.config(bg='black', fg=color, font=('times', 30, 'bold italic'))
    
root.title('Lumberjack demo')
Label(root, text='Main window', width=30).pack()
Button(root, text='Quit All', command=root.quit).pack()         # kills all app
root.mainloop()"""

"""from Tkinter import *
 
def btn_click():
  b2['text'] = 'clicked'
  evalue = e.get()
  print 'btn Click and Entry value is %s' % evalue 
 
def btn_click_bind(event):
  print 'enter b2'
 
def show_toplevel():
  top = Toplevel()
  top.title('2号窗口')
  Label(top, text='这是2号窗口').pack()
 
root = Tk()
root.title('1号窗口')
# 显示内置图片
# x = Label(root, bitmap='warning')
l = Label(root, fg='red', bg='blue',text='wangwei', width=34, height=10)
l.pack()
 
# command 指定按钮调用的函数
b = Button(root, text='clickme', command=btn_click)
b['width'] = 10
b['height'] = 2
b.pack()
# 使用bind 方式关联按钮和函数
b2 = Button(root, text = 'clickme2')
b2.configure(width = 10, height = 2, state = 'disabled')
b2.bind("<Enter>", btn_click_bind)
b2.pack()
# 弹出Toplevel窗口
b3 = Button(root, text = 'showToplevel', command=show_toplevel)
b3.pack()
 
# 输入框
e = Entry(root, text = 'input your name')
e.pack()
# 密码框
epwd = Entry(root, text = 'input your pwd', show = '*')
epwd.pack()
 
# 菜单
def menu_click():
  print 'I am menu'
 
xmenu = Menu(root)
submenu = Menu(xmenu, tearoff = 0)
for item in ['java', 'cpp', 'c', 'php']:
  xmenu.add_command(label = item, command = menu_click)
   
for item in ['think in java', 'java web', 'android']:
  submenu.add_command(label = item, command = menu_click)
xmenu.add_cascade(label = 'progame', menu = submenu)
 
# 弹出菜单
def pop(event):
  submenu.post(event.x_root, event.y_root)
 
# 获取鼠标左键点击的坐标
def get_clickpoint(event):
  print event.x, event.y
 
# frame
for x in ['red', 'blue', 'yellow']:
  Frame(height = 20, width = 20, bg = x).pack()
 
root['menu'] = xmenu
root.bind('<Button-3>', pop)
root.bind('<Button-1>', get_clickpoint)
root.mainloop()"""






"""from Tkinter import *
import tkMessageBox

msg=tkMessageBox.showinfo("提示：","没有找到可用配置文件，请手动设置相关参数！")
root=Tk()
sb = Scrollbar(root)
sb.pack(side=RIGHT, fill=Y)"""

"""from tkinter import *

root = Tk()

sb = Scrollbar(root)
sb.pack(side=RIGHT, fill=Y)

lb = Listbox(root, yscrollcommand=sb.set)

for i in range(1000):
&nbsp; &nbsp; lb.insert(END, str(i))

lb.pack(side=LEFT, fill=BOTH)

sb.config(command=lb.yview)

mainloop()"""