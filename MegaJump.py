# -*- coding: cp936 -*-
from Tkinter import *
from time import *
from winsound import *
class Hero:  #定义小球类
    def __init__(self,x,y,r):
        self.set=c.create_oval(x-r,y-r,x+r,y+r,fill="blue")
        self.velocity=20
        self.acceleration=-0.5
        self.time=0

        self.xpos=x
        self.ypos=y
        self.radius=r
    def leftMove(self,event):
        c.move(self.set,-10,0)
        self.xpos-=10
        c.update()
    def rightMove(self,event):
        c.move(self.set,10,0)
        self.xpos+=10
        c.update()
    def verticalMove(self,y):
        c.move(self.set,0,y)
    def rightblinkmove(self):
        c.move(self.set,-600-self.radius,0)
        self.xpos=-self.radius
    def leftblinkmove(self):
        c.move(self.set,600+self.radius,0)
        self.xpos=600+self.radius
        
def Mes_gameover(): #是否再来一次
    top=Toplevel(height=300,width=400,bg="white")
    top.title("What a pity!")
    Label(top,text="Sorry you have failed! Would you like to try again?",\
        bg="white",fg="red",font=("Times",15,"italic"))\
        .grid(row=1,column=1,rowspan=2)
    Button(top,text="Of Course!",width=15,bg="white",command=top.destroy).grid(row=1,column=2)
    Button(top,text="I give up..QAQ",width=15,bg="white",command=root.destroy).grid(row=2,column=2)
    top.mainloop()

def menuSet(): #菜单设置
    m1=Menu(root)
    root.config(menu=m1)
    m2=Menu(m1)
    m1.add_cascade(label="Function",menu=m2)
    m2.add_command(label="Print",command=Mes_gameover)
    m2.add_separator()
    m2.add_command(label="Exit",command=root.quit)



root=Tk()
root.title("My masterpeice")
menuSet()
c=Canvas(root,bg="white",width=600,height=600)
c.pack()

Ball=Hero(300,500,5)  #建立对象
deadline=c.create_line(0,500,600,500,fill="red",width=3)

c.focus_set()    #绑定左右运动      
c.bind("<Key-a>",Ball.leftMove)
c.bind("<Key-d>",Ball.rightMove)

dt=0.005

while True:  #控制时间位置速度
    Ball.time+=dt
    dy=Ball.velocity*dt
    Ball.ypos-=dy 
    Ball.velocity+=Ball.acceleration*dt
    Ball.verticalMove(-dy)
    if Ball.xpos-Ball.radius>600:
       Ball.rightblinkmove()
    if Ball.xpos+Ball.radius<0:
       Ball.leftblinkmove() 
    c.update()
    if Ball.ypos>550:    #终止条件
        break
#Beep(600, 200)
sleep(0.1)
c.delete(Ball.set)
Mes_gameover()

