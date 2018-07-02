#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame,sys,time,random,math,json
from pygame.locals import *


def sorting(y):
	'''寻路的函数'''
	location_list=y
	#先找头和尾
	sorted_list_B_E=[]
	for x in location_list:
		y=0
		if [x[0],x[1]+1] in location_list:
			y+=1
		if [x[0],x[1]-1] in location_list:
			y+=1
		if [x[0]-1,x[1]] in location_list:
			y+=1
		if [x[0]+1,x[1]] in location_list:
			y+=1
		if y==1:
			sorted_list_B_E.append(x) #头和尾找到了
	#哪个是头哪个是尾
	list_B=sorted_list_B_E[0]
	for x in sorted_list_B_E:
		if sum(x)<sum(list_B):
			list_B=x #头找到了
	list_E=sorted_list_B_E[-1]
	
	for x in sorted_list_B_E:
		if sum(x)>sum(list_E):
			list_E=x #尾找到了
	#开始排序
	sorted_list=[]
	sorted_list.append(list_B)
	location_list.remove(list_B)
	location_list.remove(list_E) #location_list中移除了起点和终点
	current_point=list_B
	while True:
		if [current_point[0],current_point[1]+1] in location_list:
			sorted_list.append([current_point[0],current_point[1]+1])
			location_list.remove([current_point[0],current_point[1]+1])
			current_point=[current_point[0],current_point[1]+1]
		
		if [current_point[0],current_point[1]-1] in location_list:
			sorted_list.append([current_point[0],current_point[1]-1])
			location_list.remove([current_point[0],current_point[1]-1])
			current_point=[current_point[0],current_point[1]-1]
		
		if [current_point[0]+1,current_point[1]] in location_list:
			sorted_list.append([current_point[0]+1,current_point[1]])
			location_list.remove([current_point[0]+1,current_point[1]])
			current_point=[current_point[0]+1,current_point[1]]
		
		if [current_point[0]-1,current_point[1]] in location_list:
			sorted_list.append([current_point[0]-1,current_point[1]])
			location_list.remove([current_point[0]-1,current_point[1]])
			current_point=[current_point[0]-1,current_point[1]]
		
		if len(location_list)==0:
			break
	sorted_list.append(list_E)
	return sorted_list

def adding(Y,x):
	'''在两个路径点之间添加若干个路径点的函数'''
	y=Y[:]
	a=[]
	for i in range(len(Y)-1):
		a.append(y[i])
		if y[i][0]==y[i+1][0]:
			distance=y[i+1][1]-y[i][1]
			unit_distance=distance/(x+1)
			for j in range(1,x+1):
				a.append([y[i][0],y[i][1]+j*unit_distance])
		elif y[i][1]==y[i+1][1]:
			distance=y[i+1][0]-y[i][0]
			unit_distance=distance/(x+1)
			for j in range(1,x+1):
				a.append([y[i][0]+j*unit_distance,y[i][1]])
	a.append(y[-1])
	return a

def route(file_path,current_sheet,m):
	'''基于前两个函数的方法，根据json文件中的信息创建密集度可控的路径，以坐标集的形式表现出来'''
	unit_length=70
	message=[]
	route=[]
	line=[]
	#由json读取地图信息
	filename=file_path+str(current_sheet)+'.json'
	with open(filename) as f:
		messages=json.load(f)
	columns=len(messages)
	rows=len(messages[0])
	for i in range(0,columns):
		for j in range(0,rows):
			if messages[i][j]==1:
				route.append([j+1,i+1])
	route=sorting(route)
	for i in route:
			line.append((int(i[0]*unit_length-0.5*unit_length),int(i[1]*unit_length-0.5*unit_length)))
	line=adding(line,m)
	return line

def print_text(font, x, y, text, color=(255,255,255), shadow=False):
	if shadow:
		imgText = font.render(text, True, (0,0,0))
		screen.blit(imgText, (x-2,y-2))
	imgText = font.render(text, True, color)
	screen.blit(imgText, (x,y))

def wrap_angle(angle):
	return abs(angle % 360)

def target_angle(x1,y1,x2,y2):
	delta_x = x2 - x1
	delta_y = y2 - y1
	angle_radians = math.atan2(delta_y,delta_x)
	angle_degrees = math.degrees(angle_radians)
	return angle_degrees

class Point(object):
	def __init__(self, x, y):
		self.__x = x
		self.__y = y

	#X property
	def getx(self): return self.__x
	def setx(self, x): self.__x = x
	x = property(getx, setx)

	#Y property
	def gety(self): return self.__y
	def sety(self, y): self.__y = y
	y = property(gety, sety)

	def __str__(self):
		return "{X:" + "{:.0f}".format(self.__x) + \
			",Y:" + "{:.0f}".format(self.__y) + "}"

class Map(object):
	'''在屏幕上生成地图和信息栏'''
	def __init__(self,file_path,sheet_number):
		self.image_ground=pygame.image.load('images/background/ground.png').convert_alpha()
		self.image_cube1=pygame.image.load('images/map/cube1.png').convert_alpha()
		self.image_cube2=pygame.image.load('images/map/cube2.png').convert_alpha()
		self.unit_length=70
		self.messages1=[]
		self.messages2=[]
		
		self.rows=0 #行长度
		self.columns=0 #列长度
		
		self.rows2=0 #行长度
		self.columns2=0 #列长度
		
		self.hight=0
		self.width=0
		self.current_sheet=sheet_number
		self.filename1=file_path
		
		
		#由json读取地图信息
		filename=file_path+str(sheet_number)+'.json'
		with open(filename) as f:
			self.messages1=json.load(f)
		self.columns=len(self.messages1)
		self.rows=len(self.messages1[0])
		self.lujing=route(file_path,sheet_number,2)
		self.interface_buttons=[]
		#添加第一个按钮
		self.interface_buttons.append(False)
# 		self.interface_button=False
		#添加第二个按钮
		self.interface_buttons.append(False)
# 		self.interface_button2=False
		#添加第三个按钮
		self.interface_buttons.append(False)
		self.interface_button3=False
		#铲除按钮
		self.interface_shovel=False
		
		#鼠标交互
		self.mouse_x=0
		self.mouse_y=0
		self.mouse_down_x=0
		self.mouse_down_y=0
		#所有按钮的位置
		self.addbutton_pos=[]
		self.inaddbutton_pos=[]
		#左下角添加按钮
# 		self.addbutton_pos=(0,self.unit_length*self.columns)
# 		self.inaddbutton_pos=False
		self.addbutton_pos.append((0,self.unit_length*self.columns))
		self.inaddbutton_pos.append(False)
		
		#第二个按钮
# 		self.addbutton_pos2=(self.unit_length,self.unit_length*self.columns)
# 		self.inaddbutton_pos2=False
		self.addbutton_pos.append((self.unit_length,self.unit_length*self.columns))
		self.inaddbutton_pos.append(False)
		
		#第三个按钮
# 		self.addbutton_pos3=(self.unit_length*2,self.unit_length*self.columns)
# 		self.inaddbutton_pos3=False
		self.addbutton_pos.append((self.unit_length*2,self.unit_length*self.columns))
		self.inaddbutton_pos.append(False)
		#右下角拆除按钮
		self.minusbutton_pos=(70*14,self.unit_length*self.columns)
		self.inminusbutton_pos=False
		
		#金币数量
		self.money=400
		#被保护物血量
		self.treasure_blood=1000
		self.blood=1000
		#防护塔底座
		self.dizuo=[]

	def reload(self):
		xls_data1=get_data(self.filename1)
		self.messages1=xls_data1[str(self.current_sheet)]
		self.columns=len(self.messages1)
		self.rows=len(self.messages1[0])
		self.lujing=route(self.filename1,self.current_sheet,3)

	def draw_map(self):
		#画路
		screen.blit(self.image_ground,(0,0))
		for pos in self.lujing:
			x=int(pos[0])
			y=int(pos[1])
			pos=x,y
			pygame.draw.circle(screen,yellow1,pos,3,0)
		#画阴影
		for i in range(0,self.columns):
			for j in range(0,self.rows):
				x_location=j*self.unit_length
				y_location=i*self.unit_length
				
				if self.messages1[i][j]!=1:
					pos=x_location+2,y_location+2,self.unit_length,self.unit_length
					color=black
					pygame.draw.rect(screen,color,pos,0)
		#画土地
		for i in range(0,self.columns):
			for j in range(0,self.rows):
				x_location=j*self.unit_length
				y_location=i*self.unit_length
					
				if self.messages1[i][j]==0:
					pos=(x_location,y_location)
					if (i+j)%2==0:
						screen.blit(self.image_cube1,pos)
					else:
						screen.blit(self.image_cube2,pos)

				
		#画树和房子		
		for i in range(0,self.columns):
			for j in range(0,self.rows):
				x_location=j*self.unit_length
				y_location=i*self.unit_length
				if self.messages1[i][j]==2:
					pos=(x_location,y_location)
					image1=pygame.image.load('images/map/cherry.png').convert_alpha()
					screen.blit(image1,pos)
				if self.messages1[i][j]==3:
					pos=(x_location,y_location)
					image2=pygame.image.load('images/map/apple.png').convert_alpha()
					screen.blit(image2,pos)
				if self.messages1[i][j]==4:
					pos=(x_location,y_location)
					image3=pygame.image.load('images/map/草莓.png').convert_alpha()
					screen.blit(image3,pos)
		#画防御塔底座
		for dizuo in self.dizuo:
			dizuo.construct(screen)
# 			screen.blit(dizuo[0],dizuo[1])
					
		#画底部菜单栏和按钮
		pos=(0,self.columns*self.unit_length)
		image4=pygame.image.load('images/map/菜单栏.png').convert_alpha()
		screen.blit(image4,pos)
		
		image5=pygame.image.load('images/buttons/按钮_添加.png').convert_alpha()
		image6=pygame.image.load('images/buttons/按钮_添加_红.png').convert_alpha()
		
		image7=pygame.image.load('images/buttons/按钮_暂停.png').convert_alpha()
		image8=pygame.image.load('images/buttons/按钮_暂停_红.png').convert_alpha()
		shovelImage=pygame.image.load('images/buttons/按钮_减去.png').convert_alpha()
		shovelImage1=pygame.image.load('images/buttons/按钮_减去_红.png').convert_alpha()
		screen.blit(image7,(15*70,8*70))
		screen.blit(shovelImage,(14*70,8*70))
		
		#如果鼠标在按钮上，就将按钮变红
		addbuttonIndex=0
		while addbuttonIndex<len(self.addbutton_pos):
			if self.inaddbutton_pos[addbuttonIndex]:
				screen.blit(image6,self.addbutton_pos[addbuttonIndex])
			else:
				screen.blit(image5,self.addbutton_pos[addbuttonIndex])
			addbuttonIndex+=1

			
		if self.inminusbutton_pos:
			screen.blit(shovelImage1,self.minusbutton_pos)
		else:
			screen.blit(shovelImage,self.minusbutton_pos)
		
		#显示金钱
		text='$='+str(self.money)
		print_text(font1,200,self.columns*self.unit_length+10,text,yellow2,True)
		text1='life='+str(self.treasure_blood)
		print_text(font1,400,self.columns*self.unit_length+10,text1,yellow2,True)
		text2='剩余数量:'+str(len(a))
		print_text(font1,200,self.columns*self.unit_length+70,text2,yellow2,True)
		
	def interactPos(self,imageName):#图片与地图互动的方法
		for i in range(0,self.columns):
				for j in range(0,self.rows):
					left=j*self.unit_length
					right=(j+1)*self.unit_length
					up=i*self.unit_length
					down=(i+1)*self.unit_length
					if self.mouse_x>=left and\
					 self.mouse_x<right and\
					  self.mouse_y>=up and\
					   self.mouse_y<down and\
					    self.messages1[i][j]==0:
						pos=j*self.unit_length-2,i*self.unit_length-2,self.unit_length+4,self.unit_length+4
						pygame.draw.rect(screen,black,pos,2)
						image=pygame.image.load(imageName).convert_alpha()
						screen.blit(image,(j*self.unit_length,i*self.unit_length))

	def interface(self,mouse_x,mouse_y):
		self.mouse_x=mouse_x
		self.mouse_y=mouse_y
		image8=pygame.image.load('images/buttons/按钮_暂停_红.png').convert_alpha()
		if self.mouse_x>=15*self.unit_length and\
		 self.mouse_x<16*self.unit_length and\
		 self.mouse_y>8*70 and self.mouse_y<9*70:
			screen.blit(image8,(15*70,8*70))
			
		#第一个按钮
		if self.interface_buttons[0]: #当self.interface_buttons[0]的值为True时，鼠标移到土地上会有交互的效果
			self.interactPos('images/towers/防御塔1.png')#进行互动
		#判断鼠标是否在第一个按钮上
		if self.mouse_x>0 and\
		 self.mouse_x<self.unit_length and\
		  self.mouse_y>self.columns*self.unit_length and\
		   self.mouse_y<(self.columns+1)*self.unit_length:
			self.inaddbutton_pos[0]=True
		else:
			self.inaddbutton_pos[0]=False
		
		
		#第二个按钮
		if self.interface_buttons[1]: #当self.interface_buttons[1]的值为True时，鼠标移到土地上会有交互的效果
			self.interactPos('images/towers/防御塔2.png')
		#判断鼠标是否在第二个按钮上
		if self.mouse_x>self.unit_length and\
		 self.mouse_x<self.unit_length*2 and\
		  self.mouse_y>self.columns*self.unit_length and\
		   self.mouse_y<(self.columns+1)*self.unit_length:
			self.inaddbutton_pos[1]=True
		else:
			self.inaddbutton_pos[1]=False
		#第三个按钮
		if self.interface_buttons[2]: #当self.interface_buttons[2]的值为True时，鼠标移到土地上会有交互的效果
			self.interactPos('images/towers/防御塔3.png')
		#判断鼠标是否在第三个按钮上
		if self.mouse_x>self.unit_length*2 and\
		 self.mouse_x<self.unit_length*3 and\
		  self.mouse_y>self.columns*self.unit_length and\
		   self.mouse_y<(self.columns+1)*self.unit_length:
			self.inaddbutton_pos[2]=True
		else:
			self.inaddbutton_pos[2]=False
		
		
		#判断鼠标是否在拆除按钮上
		if self.mouse_x>70*14 and\
		 self.mouse_x<70*15 and\
		  self.mouse_y>self.columns*self.unit_length and\
		   self.mouse_y<(self.columns+1)*self.unit_length:
			self.inminusbutton_pos=True
		else:
			self.inminusbutton_pos=False
			
		#铲子与地图的交互
		if self.interface_shovel: #当self.interface_shovel的值为True时，鼠标移到土地上会有交互的效果
			for i in range(0,self.columns):
				for j in range(0,self.rows):
					left=j*self.unit_length
					right=(j+1)*self.unit_length
					up=i*self.unit_length
					down=(i+1)*self.unit_length
					if self.mouse_x>=left and\
					 self.mouse_x<right and\
					  self.mouse_y>=up and\
					   self.mouse_y<down and\
					    self.messages1[i][j]==0:
						pos=j*self.unit_length-2,i*self.unit_length-2,self.unit_length+4,self.unit_length+4
						pygame.draw.rect(screen,yellow1,pos,4)

						
		#再画一遍各种装饰物		
		for i in range(0,self.columns):
			for j in range(0,self.rows):
				x_location=j*self.unit_length
				y_location=i*self.unit_length
				if self.messages1[i][j]==2:
					pos=(x_location,y_location)
					image1=pygame.image.load('images/map/cherry.png').convert_alpha()
					screen.blit(image1,pos)
				if self.messages1[i][j]==3:
					pos=(x_location,y_location)
					image2=pygame.image.load('images/map/apple.png').convert_alpha()
					screen.blit(image2,pos)
				if self.messages1[i][j]==4:
					pos=(x_location,y_location)
					image3=pygame.image.load('images/map/草莓.png').convert_alpha()
					screen.blit(image3,pos)
				
	#建造塔的方法	
	def buildTower(self,towerIndex,target,turrentImage,dizuoImage,width,height,columns,value,atk,rangee,coldDown,attackType):
		#要建造的塔的类型的索引大于或等于类型数
		if towerIndex>=len(self.interface_buttons):
			#直接结束
			return False
		#按照输入的参数建造塔
		if self.interface_buttons[towerIndex]==True:
			index=0
			while index<len(self.interface_buttons):
				if index!=towerIndex:
					self.interface_buttons[index]=False
				index+=1
			#重置铲子
			self.interface_shovel=False
			#有足够的钱
			if self.money>=value:
				if self.mouse_down_x>=0 and\
				 self.mouse_down_x<self.unit_length*self.rows and\
				  self.mouse_down_y>=0 and\
				   self.mouse_down_y<(self.columns)*self.unit_length: 
					for i in range(0,self.columns):
						for j in range(0,self.rows):
							left=j*self.unit_length
							right=(j+1)*self.unit_length
							up=i*self.unit_length
							down=(i+1)*self.unit_length
							if self.mouse_down_x>left and\
							 self.mouse_down_x<right and\
							  self.mouse_down_y>up and\
							   self.mouse_down_y<down and self.messages1[i][j]==0:
								if len(towers)>0:
									for tower in towers:
										if tower.X==left and tower.Y==up:
											self.interface_buttons[towerIndex]=False
											return
								#建造底座
								self.dizuo.append(Dizuo(dizuoImage,left,up))
								#添加塔
								towers.add(MyTower(target,turrentImage,width,height,columns,left,up,value,atk,rangee,coldDown,attackType))
								self.money-=value
					#建造完成后重置按钮
					self.interface_buttons[towerIndex]=False
			else:
				moreMineral.play(loops=0)
				self.interface_buttons[towerIndex]=False	
		
	def mouse_down(self,mouse_down_x,mouse_down_y):
		self.mouse_down_x=mouse_down_x
		self.mouse_down_y=mouse_down_y
		
		#判断鼠标是否点击在添加按钮上
		buttonIndex=0
		while buttonIndex<len(self.interface_buttons):
			if self.interface_buttons[buttonIndex]==False:
				if self.mouse_down_x>=self.unit_length*buttonIndex and\
				 self.mouse_down_x<self.unit_length*(buttonIndex+1) and\
				  self.mouse_down_y>=self.columns*self.unit_length and\
				   self.mouse_down_y<(self.columns+1)*self.unit_length: 
					self.interface_buttons[buttonIndex]=True 
			buttonIndex+=1
			
		#建造第一座塔
		self.buildTower(0,screen,'images\\towers\\turret2.png','images\\towers\\底座.png',70,70,4,120,180,1.5,50,"bullets")
		
		#建造第二座塔
		self.buildTower(1,screen,'images\\towers\\turret3.png','images\\towers\\底座2.png',70,70,4,80,1.5,2,0,"laser")

		#第三座塔——加特林
		self.buildTower(2,screen,'images\\towers\\加特林.png','images\\towers\\加特林底座.png',70,70,4,100,3,1.25,1,"machineGun")

		#铲除
		if self.interface_shovel:
			self.interface_buttons[1]=False
			self.interface_buttons[0]=False
			#鼠标点在格子里
			if self.mouse_down_x>=0 and\
				 self.mouse_down_x<self.unit_length*self.rows and\
				  self.mouse_down_y>=0 and\
				   self.mouse_down_y<(self.columns)*self.unit_length: 
					for i in range(0,self.columns):
							for j in range(0,self.rows):
								left=j*self.unit_length
								right=(j+1)*self.unit_length
								up=i*self.unit_length
								down=(i+1)*self.unit_length
								if self.mouse_down_x>=left and\
								 self.mouse_down_x<right and\
								  self.mouse_down_y>=up and\
								   self.mouse_down_y<down and\
								    self.messages1[i][j]==0:
									for tower in towers:
										#如果这个格子有塔，那就将它嘿嘿嘿……
										if tower.X==left and tower.Y==up:
											self.money+=int(tower.value/40)*10
											tower.kill()
									i=0
									#拆底座
									while i<len(self.dizuo):
										if self.dizuo[i].left==left and\
										 self.dizuo[i].up==up:
											del self.dizuo[i]
											i-=1
										i+=1
					#铲子用一次之后就归位
					self.interface_shovel=False
			
class MoreInterface(object):
	'''处理游戏中的菜单页'''
	def __init__(self):
		self.image_background=pygame.image.load('images/background/深色背景.png').convert_alpha()
		self.image_title=pygame.image.load('images/background/游戏大标题.png').convert_alpha()
		self.image_creater=pygame.image.load('images/background/作者信息.png').convert_alpha()

		self.image_newgame=pygame.image.load('images/buttons/按钮_新游戏.png').convert_alpha()
		self.image_newgame1=pygame.image.load('images/buttons/按钮_新游戏_红.png').convert_alpha()

		self.image_choose=pygame.image.load('images/buttons/按钮_选择关卡.png').convert_alpha()
		self.image_choose1=pygame.image.load('images/buttons/按钮_选择关卡_红.png').convert_alpha()

		self.image_about=pygame.image.load('images/buttons/按钮_关于.png').convert_alpha()
		self.image_about1=pygame.image.load('images/buttons/按钮_关于_红.png').convert_alpha()
		
		self.image_return=pygame.image.load('images/buttons/按钮_返回.png').convert_alpha()
		self.image_return1=pygame.image.load('images/buttons/按钮_返回_红.png').convert_alpha()
		
		self.image_game_win=pygame.image.load('images/background/赢了.png').convert_alpha()
		self.image_game_lost=pygame.image.load('images/background/输了.png').convert_alpha()
		
		self.image_again=pygame.image.load('images/buttons/按钮_再来一局.png').convert_alpha()
		self.image_again1=pygame.image.load('images/buttons/按钮_再来一局_红.png').convert_alpha()
		self.image_next=pygame.image.load('images/buttons/按钮_下一关.png').convert_alpha()
		self.image_next1=pygame.image.load('images/buttons/按钮_下一关_红.png').convert_alpha()
		
		self.image_finish=pygame.image.load('images/background/finished.png').convert_alpha()
		self.image_return_begin=pygame.image.load('images/buttons/按钮_返回首页.png').convert_alpha()
		self.image_return_begin1=pygame.image.load('images/buttons/按钮_返回首页_红.png').convert_alpha()
		
		self.image_exit=pygame.image.load('images/buttons/按钮_退出.png').convert_alpha()
		self.image_exit1=pygame.image.load('images/buttons/按钮_退出_红.png').convert_alpha()
		
		self.image_continue=pygame.image.load('images/buttons/按钮_继续.png').convert_alpha()
		self.image_continue1=pygame.image.load('images/buttons/按钮_继续_红.png').convert_alpha()
		
		self.image_1=pygame.image.load('images/buttons/按钮_1.png').convert_alpha()
		self.image_2=pygame.image.load('images/buttons/按钮_2.png').convert_alpha()
		self.image_3=pygame.image.load('images/buttons/按钮_3.png').convert_alpha()
		self.image_4=pygame.image.load('images/buttons/按钮_4.png').convert_alpha()
		self.image_5=pygame.image.load('images/buttons/按钮_5.png').convert_alpha()
		self.image_6=pygame.image.load('images/buttons/按钮_6.png').convert_alpha()
		
		self.image_1_1=pygame.image.load('images/buttons/按钮_1_红.png').convert_alpha()
		self.image_2_1=pygame.image.load('images/buttons/按钮_2_红.png').convert_alpha()
		self.image_3_1=pygame.image.load('images/buttons/按钮_3_红.png').convert_alpha()
		self.image_4_1=pygame.image.load('images/buttons/按钮_4_红.png').convert_alpha()
		self.image_5_1=pygame.image.load('images/buttons/按钮_5_红.png').convert_alpha()
		self.image_6_1=pygame.image.load('images/buttons/按钮_6_红.png').convert_alpha()
		
		self.image_of_num=[self.image_1,self.image_2,self.image_3,self.image_4,self.image_5,self.image_6]
		self.image_of_num_1=[self.image_1_1,self.image_2_1,self.image_3_1,self.image_4_1,self.image_5_1,self.image_6_1]
		self.num_pos=[(500,300),(550,300),(600,300),(500,350),(550,350),(600,350)]

		self.mouse_x=0
		self.mouse_y=0
		self.mouse_down_x=0
		self.mouse_down_y=0
		
		self.open_page=True
		self.continue_page=False
		self.about_page=False
		self.choosing_page=False
		
		self.game_begin=False
		
		self.game_win=False
		
		self.game_on=False
		
		self.game_over=True
	
	def init(self):

		self.mouse_down_x=0
		self.mouse_down_y=0
		
		self.open_page=True
		self.continue_page=False
		self.about_page=False
		self.choosing_page=False
		
		self.game_begin=False
		
		self.game_win=False
		
		self.game_on=False
		
		self.game_over=True
		
	def draw_open_page(self):
		if self.open_page==True:
			screen.blit(self.image_background,(0,0))
			screen.blit(self.image_title,(0,0))
			screen.blit(self.image_newgame,(800,120))
			screen.blit(self.image_choose,(800,250))
			screen.blit(self.image_about,(800,380))
			
			if self.mouse_x>=800 and self.mouse_x<=800+240 and self.mouse_y>=120 and self.mouse_y<=120+92:
				screen.blit(self.image_newgame1,(800,120))
			if self.mouse_x>=800 and self.mouse_x<=800+240 and self.mouse_y>=250 and self.mouse_y<=250+92:
				screen.blit(self.image_choose1,(800,250))
			if self.mouse_x>=800 and self.mouse_x<=800+240 and self.mouse_y>=380 and self.mouse_y<=380+92:
				screen.blit(self.image_about1,(800,380))
			
			#点击新游戏
			if self.mouse_down_x>=800 and self.mouse_down_x<=800+240 and self.mouse_down_y>=120 and self.mouse_down_y<=120+92:
				time.sleep(0.3)
				print_text(font1,430,600,'loading.',white,False)
				pygame.display.update()
				time.sleep(0.5)
				print_text(font1,430,600,'loading..',white,False)
				pygame.display.update()
				time.sleep(0.5)
				print_text(font1,430,600,'loading...',white,False)
				pygame.display.update()
				time.sleep(0.5)
				self.game_begin=True
			#点击关于
			if self.mouse_down_x>=800 and self.mouse_down_x<=800+240 and self.mouse_down_y>=380 and self.mouse_down_y<=380+92:
				self.about_page=True
			#点击选择关卡
			if self.mouse_down_x>=800 and self.mouse_down_x<=800+240 and self.mouse_down_y>=250 and self.mouse_down_y<=250+92:
				self.choosing_page=True
		
		#关于页面
		if self.about_page==True:
			screen.blit(self.image_background,(0,0))
			screen.blit(self.image_return,(70*16-240,0))
			screen.blit(self.image_creater,(0,0))
			
			if self.mouse_x>=70*16-240+43 and self.mouse_x<=70*16-43 and self.mouse_y>=20 and self.mouse_y<=92-20:
				screen.blit(self.image_return1,(70*16-240,0))
			
			if self.mouse_down_x>=70*16-240+43 and self.mouse_down_x<=70*16-43 and self.mouse_down_y>=20 and self.mouse_down_y<=92-20:
				self.about_page=False
		
		#选关页面
		if self.choosing_page==True:
			screen.blit(self.image_background,(0,0))
			screen.blit(self.image_return,(70*16-240,0))
			for i in range(0,6):
				screen.blit(self.image_of_num[i],self.num_pos[i])
			for i in range(0,6):
				if self.mouse_x>=self.num_pos[i][0] and\
				 self.mouse_x<self.num_pos[i][0]+40 and\
				  self.mouse_y>=self.num_pos[i][1] and\
				   self.mouse_y<self.num_pos[i][1]+40:
					screen.blit(self.image_of_num_1[i],self.num_pos[i])
			for i in range(0,6):
				if self.mouse_down_x>=self.num_pos[i][0] and\
				 self.mouse_down_x<self.num_pos[i][0]+40 and\
				  self.mouse_down_y>=self.num_pos[i][1] and\
				   self.mouse_down_y<self.num_pos[i][1]+40:
					global current_level
					current_level=i+1
					self.game_begin=True
					
			if self.mouse_x>=70*16-240+43 and\
			 self.mouse_x<=70*16-43 and\
			  self.mouse_y>=20 and\
			   self.mouse_y<=92-20:
				screen.blit(self.image_return1,(70*16-240,0))
				
			
			if self.mouse_down_x>=70*16-240+43 and self.mouse_down_x<=70*16-43 and self.mouse_down_y>=20 and self.mouse_down_y<=92-20:
				self.choosing_page=False

	def draw_transition_page(self):
		self.game_on=False
		if self.game_win==True:
			screen.blit(self.image_game_win,(0,0))
		elif self.game_win==False:
			screen.blit(self.image_game_lost,(0,0))
		if self.game_win==True:
			screen.blit(self.image_next,(400,300))
			if self.mouse_x>=400 and self.mouse_x<400+239 and self.mouse_y>=300 and self.mouse_y<=300+92:
				screen.blit(self.image_next1,(400,300))
		screen.blit(self.image_again,(400,400))
		screen.blit(self.image_return_begin,(400,500))
		if self.mouse_x>=400 and self.mouse_x<400+239 and self.mouse_y>=400 and self.mouse_y<=400+92:
			screen.blit(self.image_again1,(400,400))
		if self.mouse_x>=400 and self.mouse_x<=400+239 and self.mouse_y>=500 and self.mouse_y<=500+92:
			screen.blit(self.image_return_begin1,(400,500))
		if self.game_win==True:
			if self.mouse_down_x>=400 and self.mouse_down_x<=400+239 and self.mouse_down_y>=300 and self.mouse_down_y<=300+92:
				time.sleep(0.3)
				print_text(font1,760,400,'loading.',white,False)
				pygame.display.update()
				time.sleep(0.5)
				print_text(font1,760,400,'loading..',white,False)
				pygame.display.update()
				time.sleep(0.5)
				print_text(font1,760,400,'loading...',white,False)
				pygame.display.update()
				time.sleep(0.5)
				self.game_on=True
				
		if self.mouse_down_x>=400 and self.mouse_down_x<=400+239 and self.mouse_down_y>=400 and self.mouse_down_y<=400+92:
			time.sleep(0.3)
			print_text(font1,760,400,'loading.',white,False)
			pygame.display.update()
			time.sleep(0.5)
			print_text(font1,760,400,'loading..',white,False)
			pygame.display.update()
			time.sleep(0.5)
			print_text(font1,760,400,'loading...',white,False)
			pygame.display.update()
			time.sleep(0.5)
			global current_level
			current_level=current_level-1
			self.game_on=True
		if self.mouse_down_x>=400 and self.mouse_down_x<=400+239 and self.mouse_down_y>=500 and self.mouse_down_y<=500+92:
			self.__init__()
			global game_begin
			game_begin=False
			global game_over
			game_over=False
	
	def draw_finished_page(self):
		screen.blit(self.image_finish,(0,0))
		screen.blit(self.image_return_begin,(400,400))
		screen.blit(self.image_exit,(400,500))
		if self.mouse_x>=400 and self.mouse_x<=400+239 and self.mouse_y>=400 and self.mouse_y<=400+92:
			screen.blit(self.image_return_begin1,(400,400))
		if self.mouse_x>=400 and self.mouse_x<=400+239 and self.mouse_y>=500 and self.mouse_y<=500+92:
			screen.blit(self.image_exit1,(400,500))
		if self.mouse_down_x>=400 and self.mouse_down_x<=400+239 and self.mouse_down_y>=400 and self.mouse_down_y<=400+92:
			self.game_begin=False
			self.game_over=False
		if self.mouse_down_x>=400 and self.mouse_down_x<=400+239 and self.mouse_down_y>=500 and self.mouse_down_y<=500+92:
			sys.exit()

	def draw_pause_page(self):
		screen.blit(self.image_background,(0,0))
		screen.blit(self.image_continue,(400,300))
		screen.blit(self.image_return_begin,(400,400))
		if self.mouse_x>=400 and self.mouse_x<=400+239 and self.mouse_y>=300 and self.mouse_y<=300+92:
			screen.blit(self.image_continue1,(400,300))
		if self.mouse_x>=400 and self.mouse_x<=400+239 and self.mouse_y>=400 and self.mouse_y<=400+92:
			screen.blit(self.image_return_begin1,(400,400))
		if self.mouse_down_x>=400 and self.mouse_down_x<=400+239 and self.mouse_down_y>=300 and self.mouse_down_y<=300+92:
			global game_pause
			game_pause=False
			self.init()
		elif self.mouse_down_x>=400 and self.mouse_down_x<=400+239 and self.mouse_down_y>=400 and self.mouse_down_y<=400+92:
			global game_begin,game_over
			game_begin=False
			game_over=False
			game_pause=False

class Dizuo(object):
	'''底座类，因为不会动，所以没必要做成精灵'''
	def __init__(self,image,left,up):
		self.image=pygame.image.load(image).convert_alpha()
		self.left=left
		self.up=up
		
	def construct(self,surface):
		surface.blit(self.image,(self.left,self.up))

class MyMonster(pygame.sprite.Sprite):
	'''创建一个monster，主要属性：速度，血量，击杀奖励'''
	def __init__(self, target, filename, width, height, columns,excel_filename,current_sheet,m,n,x,show_up_time,sound_death,armor): #m越大，跑得越慢，n是血量,x是击杀奖励
		pygame.sprite.Sprite.__init__(self) #extend the base Sprite class
		self.master_image = None
		self.frame = 0
		self.old_frame = -1
		self.frame_width = 1
		self.frame_height = 1
		self.first_frame = 0
		self.last_frame = 0
		self.columns = 2
		self.last_time = 0
		self.money=x
		#高级精灵动画
		self.direction=0
		self.velocity=Point(0.0,0.0)
		self.master_image = pygame.image.load(filename).convert_alpha()
		self.frame_width = width
		self.frame_height = height
		self.rect = Rect(0,0,width,height)
		self.columns = columns
		#try to auto-calculate total frames
		rect = self.master_image.get_rect()
		self.last_frame = (rect.width // width) * (rect.height // height) - 1
		self.lujing=route(excel_filename,current_sheet,m)
		#血量
		self.blood=n
		self.current_blood=n
		#护甲
		self.armor=armor
		#初始点位
		self.i=0
		
		self.show_up_time=show_up_time
		#音效部分
		#死亡音效
		self.sound_death=sound_death
	#X property
	def _getx(self): return self.rect.x
	def _setx(self,value): self.rect.x = value
	X = property(_getx,_setx)

	#Y property
	def _gety(self): return self.rect.y
	def _sety(self,value): self.rect.y = value
	Y = property(_gety,_sety)

	#position property
	def _getpos(self): return self.rect.topleft
	def _setpos(self,pos): self.rect.topleft = pos
	position = property(_getpos,_setpos)
		

	def load(self, filename, width, height, columns):
		self.master_image = pygame.image.load(filename).convert_alpha()
		self.frame_width = width
		self.frame_height = height
		self.rect = Rect(0,0,width,height)
		self.columns = columns
		#try to auto-calculate total frames
		rect = self.master_image.get_rect()
		self.last_frame = (rect.width // width) * (rect.height // height) - 1

	def update(self, current_time, rate=30):
		#update animation frame number
		if current_time > self.last_time + rate:
			self.frame += 1
			if self.frame > self.last_frame:
				self.frame = self.first_frame
			self.last_time = current_time
		

		#build current frame only if it changed
		if self.frame != self.old_frame:
			frame_x = (self.frame % self.columns) * self.frame_width
			frame_y = (self.frame // self.columns) * self.frame_height
			rect = Rect(frame_x, frame_y, self.frame_width, self.frame_height)
			self.image = self.master_image.subsurface(rect)
			self.old_frame = self.frame
	#敌人被炮弹击中
	def hitByBullet(self,bullet):
		if bullet.atk-self.armor>0:
			self.current_blood-=bullet.atk-self.armor
		else:
			self.current_blood-=1
		
		
	def show_blood(self):
		if self.current_blood>4:
			pos0=self.X+8,self.Y-4,100/2+2,7
			pygame.draw.rect(screen,black,pos0,0)
			pos1=self.X+6,self.Y-6,100/2+2,7
			pygame.draw.rect(screen,white,pos1,0)
			pos2=self.X+7,self.Y-4,self.current_blood/self.blood*50,4
			if self.current_blood>=self.blood*0.5:
				pygame.draw.rect(screen,green,pos2,0)
			else:
				pygame.draw.rect(screen,red,pos2,0)
		text=str(int(self.current_blood))+'/'+str(self.blood)
		print_text(font2,self.X+5,self.Y-15,text,white)

	def __str__(self):
		return str(self.frame) + "," + str(self.first_frame) + \
			   "," + str(self.last_frame) + "," + str(self.frame_width) + \
			   "," + str(self.frame_height) + "," + str(self.columns) + \
			   "," + str(self.rect)

class Bullet(pygame.sprite.Sprite):
	#弹药类，用来生成弹药的
	def __init__(self,target,width,height,X,Y,speed,atk,direction,imagePath,life):
		pygame.sprite.Sprite.__init__(self)
		self.target=[target]
		self.width=width
		self.height=height
		self.X=X-7
		self.Y=Y-7
		self.life=life
		#rect和image是一定要有的属性
		self.rect = Rect(0,0,width,height)
# 		self.image=None
		self.image=pygame.image.load(imagePath).convert_alpha()
		self.speed=speed
		self.atk=atk
		self.position=Point(self.X,self.Y)
		self.velocity=Point(0,0)
		self.direction=direction
		self.last_time=0
		self.end_pos=(target.rect.x,target.rect.y)
		
	
	def update(self,ticks):
		#设定当前位置
		self.position.x += self.velocity.x * 10.0
		self.position.y += self.velocity.y * 10.0
		self.rect=Rect(self.position.x,self.position.y,self.width,self.height)
		self.life-=1
		
	#弹药的绘图方法
	def draw(self,surface):
		#其实炮弹就是一个圆或者一张图片
# 		pygame.draw.circle(surface, white, self.position, 5)
		surface.blit(self.image,self.position)

class MyTower(pygame.sprite.Sprite):
	'''创建防御塔，主要属性：攻速，攻击力，cd时间'''
	def __init__(self, target,filename,width,height,columns,X,Y,value,atk,rangee,coldDown,attackType):
		pygame.sprite.Sprite.__init__(self)
		self.master_image = None
		self.frame = 0
		self.old_frame = -1
		self.frame_width = 1
		self.frame_height = 1
		self.first_frame = 0
		self.last_frame = 0
		self.columns = 2
		self.last_time = 0
		self.master_image = pygame.image.load(filename).convert_alpha()
		self.frame_width = width
		self.frame_height = height
		self.rect = Rect(0,0,width,height)
		self.columns = columns
		rect = self.master_image.get_rect()
		self.last_frame = (rect.width // width) * (rect.height // height) - 1
		self.X=X
		self.Y=Y
		self.rotation=0.0
		self.old_rotation=0.0
		#用来绘制的草图
		self.scratch=None
		self.value=value
####################################
		#初始化目标为空
		self.target=[]
		#初始化攻击力
		self.atk=atk
		#射程（碰撞半径倍数）
		self.range=rangee
		#冷却时间
		self.coldDown=coldDown
		self.current_coldDown=0
		#攻击类型
		self.attackType=attackType

		
	#X property
	def _getx(self): return self.rect.x
	def _setx(self,value): self.rect.x = value
	X = property(_getx,_setx)

	#Y property
	def _gety(self): return self.rect.y
	def _sety(self,value): self.rect.y = value
	Y = property(_gety,_sety)

	#position property
	def _getpos(self): return self.rect.topleft
	def _setpos(self,pos): self.rect.topleft = pos
	position = property(_getpos,_setpos)
	

	def update(self, current_time, rate=30):
		#update animation frame number
		if current_time > self.last_time + rate:
			self.frame += 1
			if self.frame > self.last_frame:
				self.frame = self.first_frame
			self.last_time = current_time
			

		#build current frame only if it changed
		if self.frame != self.old_frame:
			frame_x = (self.frame % self.columns) * self.frame_width
			frame_y = (self.frame // self.columns) * self.frame_height
			rect = Rect(frame_x, frame_y, self.frame_width, self.frame_height)
			self.image = self.master_image.subsurface(rect)
			self.old_frame = self.frame
		#复位
		self.scratch=self.image
		#旋转草图
		if len(self.target)>0:
			self.rotation=self.rotate()
			self.scratch=pygame.transform.rotate(self.image, -self.rotation)

	def setTarget(self,target):#设定目标
		if target.current_blood>0:
			self.target.append(target)

	def attack(self):			#进行攻击
		if self.current_coldDown==0:
			if len(self.target)>0:
				#第一种攻击方式：持续型（激光），这一种没有cd时间（或者说cd时间极短）
				if self.attackType=='laser':
					for target in self.target:
						if self.atk-target.armor>1:
							target.current_blood-=self.atk-target.armor
						else:
							target.current_blood-=1
						self.current_coldDown=self.coldDown
						#攻击的起始和终结点
						# ~ begin_pos=(int(self.X+35-35*math.sin(self.rotation-90)),\
								# ~ int(self.Y+5+35*math.cos(self.rotation-90)))
						begin_pos=(int(self.X+34),int(self.Y+34))
						end_pos=(target.X+35+random.randint(-1,1),target.Y+35+random.randint(-1,1))
						#激光效果
						pygame.draw.line(screen,red,begin_pos,end_pos,4)
						pygame.draw.circle(screen,red,end_pos,4)
						pygame.draw.circle(screen,red,begin_pos,4)
						pygame.draw.line(screen,white,begin_pos,end_pos,2)
						pygame.draw.circle(screen,white,end_pos,2)
						pygame.draw.circle(screen,white,begin_pos,2)
						#爆炸效果
						random_pos1=(target.X+35+random.randint(-20,20),target.Y+35+random.randint(-20,20))
						pygame.draw.circle(screen,red,random_pos1,8)
						pygame.draw.circle(screen,white,random_pos1,6)
				#第二种攻击方式：瞬间型（炮弹）这种的cd时间存在且不可忽略
				elif self.attackType=='bullets':
					#cd还是要调整
					self.current_coldDown=self.coldDown
					#这种直接创建出一个炮弹就不管了
					bullet=Bullet(self.target[0],5,5,self.X+35,self.Y+35,2,self.atk,self.rotation,"images\\towers\\bullet2.png",50)
					#设定炮弹初速度方向
					vel=Point(0,0)
					vel.x=math.cos( math.radians(self.rotation-90) )
					vel.y=math.sin( math.radians(self.rotation-90) )
					bullet.velocity=vel
					bullets.add(bullet)
				#第三种攻击方式，和第二种差不多，不过子弹参数不一样
				elif self.attackType=='machineGun':
					#cd还是要调整
					self.current_coldDown=self.coldDown
					#这种直接创建出一个炮弹就不管了
					bullet=Bullet(self.target[0],5,5,self.X+35,self.Y+35,2,self.atk,self.rotation,"images\\towers\\机枪子弹.png",15)
					#设定炮弹初速度方向
					vel=Point(0,0)
					vel.x=math.cos( math.radians(self.rotation-90) )
					vel.y=math.sin( math.radians(self.rotation-90) )
					bullet.velocity=vel
					bullets.add(bullet)
				
					
		elif self.current_coldDown>0:
			self.current_coldDown-=1
		else:
			self.current_coldDown=0
			
	def draw(self,surface):#绘图方法
		#绘制塔的草图
		#获取草图的宽和高
		width,height = self.scratch.get_size()
		#原图的宽和高
		frame_width,frame_height=self.image.get_size()
		#修正x和y
		xFix=(width-frame_width)/2
		yFix=(height-frame_height)/2
		#在修正后的地点印刷出旋转后的图片
		surface.blit(self.scratch, (self.X-xFix,
	    self.Y-yFix))
			
	def rotate(self):#旋转炮塔
		if len(self.target)>0:
			angle=target_angle(self.X+self.frame/2, self.Y+self.frame/2,
									 self.target[0].X+self.target[0].frame, 
									 self.target[0].Y+self.target[0].frame)
			angle+=90
			angle=wrap_angle(angle)
			return angle
		else:
			return self.rotation

class MyTreasure(pygame.sprite.Sprite):
	'''被保护的目标，血量为零时游戏结束'''
	def __init__(self, target, filename, width, height, columns,file_path,current_sheet,m,n): #m越大，跑得越慢，n是血量
		#基本操作
		pygame.sprite.Sprite.__init__(self)
		self.master_image = None
		self.frame=0
		self.old_frame=-1
		self.first_frame=0
		self.last_frame=0
		self.last_time=0
		self.velocity=Point(0.0,0.0)
		self.master_image=pygame.image.load(filename).convert_alpha()
		self.frame_width=width
		self.frame_height=height
		self.rect=Rect(0,0,width,height)
		self.columns=columns
		rect=self.master_image.get_rect()
		self.last_frame=(rect.width//width)*(rect.height//height)-1
		self.lujing=route(file_path,current_sheet,m)
		#血量
		self.blood=n
		self.current_blood=n
		#点位
		self.X=self.lujing[-1][0]-35
		self.Y=self.lujing[-1][1]-35

	#X property
	def _getx(self): return self.rect.x
	def _setx(self,value): self.rect.x = value
	X = property(_getx,_setx)

	#Y property
	def _gety(self): return self.rect.y
	def _sety(self,value): self.rect.y = value
	Y = property(_gety,_sety)

	#position property
	def _getpos(self): return self.rect.topleft
	def _setpos(self,pos): self.rect.topleft = pos
	position = property(_getpos,_setpos)

	def update(self, current_time, rate=30):
		#刷新画面
		if current_time > self.last_time + rate:
			self.frame += 1
			if self.frame > self.last_frame:
				self.frame = self.first_frame
			self.last_time = current_time

		if self.frame != self.old_frame:
			frame_x = (self.frame % self.columns) * self.frame_width
			frame_y = (self.frame // self.columns) * self.frame_height
			rect = Rect(frame_x, frame_y, self.frame_width, self.frame_height)
			self.image = self.master_image.subsurface(rect)
			self.old_frame = self.frame

	def show_blood(self):
		#显示血条
		if self.current_blood>4:
			pos0=self.X+8,self.Y-4,100/2+2,7
			pygame.draw.rect(screen,black,pos0,0)
			pos1=self.X+6,self.Y-6,100/2+2,7
			pygame.draw.rect(screen,white,pos1,0)
			pos2=self.X+7,self.Y-4,self.current_blood/self.blood*50,4
			if self.current_blood>=self.blood*0.5:
				pygame.draw.rect(screen,green,pos2,0)
			else:
				pygame.draw.rect(screen,red,pos2,0)
		text=str(int(self.current_blood))+'/'+str(self.blood)
		print_text(font2,self.X+4,self.Y-18,text,white)

def createMonster(file_path,sheet_number):
	'''批量创建monster的函数，返回一个装满了monster的列表'''
	#由json读取地图信息
	filename=file_path+str(sheet_number)+'.json'
	with open(filename) as f:
		messages=json.load(f)
	#创建一个空列表
	a=[]
	#读取怪物的信息，创建一系列实例，并添加到空列表中，每个message表示一列的内容
	for message in messages:
		a.append(MyMonster(message[0],\
		message[1],message[2],message[3],\
		message[4],message[5],message[6],\
		message[7],message[8],message[9],\
		message[10],message[11],message[12]))		
	return a

#=====================创建地图============================================
current_level=1
#创建屏幕
screen_size=(1120,700)
#=====================以下为基本操作=======================================	
#初始化
pygame.init()
#创建一个screen
screen = pygame.display.set_mode(screen_size)
#设定标题栏名称
pygame.display.set_caption("Pac-Ghost Defence")
#设定几种文字样式（字形，字号）
font1 = pygame.font.Font('fonts/FZXS.TTF',50)
font2 = pygame.font.Font(None,20)
#=====================设定几种颜色的rgb值==================================
white = 255,255,255
cyan = 0,255,255
yellow1= 229,228,50
purple = 255,0,255
green = 48,188,97
red = 207,9,22
black=0,0,0
yellow2=243,243,69
brown=182,145,42
gray=120,121,106
blue=5,19,92
#=======================================================================
my_map=Map('informations\\maps\\',current_level)#没错，current_level就是1
#初始时间为零
Time=1
#创建一个framerate用于控制帧速率
framerate = pygame.time.Clock()
#创建一个储存出场怪物的group，一开始是空的，按设定时间往里添加
group = pygame.sprite.Group()
#经由Excel表格读取信息创建一堆怪物类，储存在列表a中
a=createMonster('informations\\monsters\\',current_level)
#创建一个所有防御塔的集合列表，防御塔在游戏中通过Map类中的mouse_down方法创建	
towers=pygame.sprite.Group()
#创建一个所有弹药的集合列表，弹药由瞬间型攻击创建
bullets=pygame.sprite.Group()
#=======================================================================
#创建受保护目标目标treasure
treasure=MyTreasure(screen,'images\\treasure\\treasure.png',70,70,4,'informations\\maps\\',current_level,3,1000)
treasure_group=pygame.sprite.Group()
treasure_group.add(treasure)
#=======================================================================
moreinterface=MoreInterface()
#=======================================================================
game_over=False #游戏结束
game_begin=False #游戏开始运行
game_on=True #处于游戏画面中
game_win=False
game_pause=False
#=======================================================================
#音乐
pygame.mixer.init()
pygame.mixer.music.load("sounds/BGM.mp3")
s=pygame.mixer.Sound("sounds/bgm2.ogg")
#=======================================================================
#音效
moreMineral=pygame.mixer.Sound('sounds/NeedMoreMinerals.ogg')
#=======================================================================
while True:
	
	#非暂停页
	if game_pause==False:
		
		#游戏首页
		if game_begin==False and game_over==False:
			s.set_volume(0.1)
			s.play()
			# ~ if pygame.mixer.music.get_busy()==False:
				# ~ pygame.mixer.music.set_volume(1)
				# ~ pygame.mixer.music.play()
			pygame.mixer.music.pause()
			game_over=False #游戏结束
			game_begin=False #游戏开始运行
			game_on=True #处于游戏画面中
			game_win=False
			moreinterface.mouse_down_x=0
			moreinterface.mouse_down_y=0
			screen.fill((0,0,0))
			#读取鼠标键盘输入
			moreinterface.game_begin=False
			for event in pygame.event.get():
				if event.type==QUIT:
					sys.exit()
				elif event.type == KEYUP:
					if event.key == pygame.K_ESCAPE:
						sys.exit()
				elif event.type==MOUSEMOTION:
						mouse_x,mouse_y=event.pos
				elif event.type==MOUSEBUTTONDOWN:
					moreinterface.mouse_down_x,moreinterface.mouse_down_y=event.pos
			moreinterface.mouse_x=mouse_x
			moreinterface.mouse_y=mouse_y
			moreinterface.draw_open_page()
			game_begin=moreinterface.game_begin
# 			current_level=1
			Time=0
		
		#完成游戏，finish页
		elif game_begin==False and game_over==True:
			pygame.mixer.music.stop()
			screen.fill((0,0,0))
			#读取鼠标键盘输入
			moreinterface.init()
			for event in pygame.event.get():
				if event.type==QUIT:
					sys.exit()
				elif event.type == KEYUP:
					if event.key == pygame.K_ESCAPE:
						sys.exit()
				elif event.type==MOUSEMOTION:
						moreinterface.mouse_x,moreinterface.mouse_y=event.pos
				elif event.type==MOUSEBUTTONDOWN:
					moreinterface.mouse_down_x,moreinterface.mouse_down_y=event.pos
			moreinterface.draw_finished_page()
			game_begin=moreinterface.game_begin
			game_over=moreinterface.game_over
		
		#游戏中
		elif game_begin==True and game_on==True:
			s.fadeout(1)
			pygame.mixer.music.unpause()
			if pygame.mixer.music.get_busy()==False:
				pygame.mixer.music.set_volume(1)
				pygame.mixer.music.play()
			if pygame.mixer.music.get_busy()==False:
				pygame.mixer.music.set_volume(1)
				pygame.mixer.music.play()
			if game_over==False:
				# ~ if Time==0 and current_level==1:
					# ~ a=[]
					# ~ group=None
					# ~ bullets=None
					# ~ towers=None
					# ~ treasure_group=None
				if Time==0:
					#时间清零后全部重来
					a=[]
					for value in group:
						value.kill()
					for tower in towers:
						tower.kill()
					for treasure in treasure_group:
						treasure.kill()
					for bullet in bullets:
						bullet.kill()
					treasure=MyTreasure(screen,'images\\treasure\\treasure.png',70,70,4,'informations\\maps\\',current_level,3,1000)
					treasure_group.add(treasure)
				if len(a)==0:
					a=createMonster('informations\\monsters\\',current_level)
					my_map=Map('informations\\maps\\',current_level)
					for player in a:
						player.i=0
						
				framerate.tick(120)
				ticks = pygame.time.get_ticks()
				#隔一定的时间投放一个怪物
				for i in a:
					if i.show_up_time==Time:
						group.add(i)
				screen.fill((0,0,0))
				#读取鼠标键盘输入
				for event in pygame.event.get():
					if event.type==QUIT:
						sys.exit()
					elif event.type == KEYUP:
						if event.key == pygame.K_ESCAPE:
							sys.exit()
					elif event.type==MOUSEMOTION:
						mouse_x,mouse_y=event.pos
					elif event.type==MOUSEBUTTONDOWN:
						mouse_down_x,mouse_down_y=event.pos
						my_map.mouse_down(mouse_down_x,mouse_down_y)			
				#用draw_map()方法绘制地图
				my_map.draw_map()
				#用interface()方法对鼠标位置做出交互
				my_map.interface(mouse_x,mouse_y)
				
				#点击右下角暂停游戏
				if my_map.mouse_down_x>15*70 and\
				 my_map.mouse_down_x<16*70 and\
				  my_map.mouse_down_y>8*70 and\
				   my_map.mouse_down_y<9*70:
					game_pause=True
					my_map.mouse_down_x=0
					my_map.mouse_down_y=0
				
				#点击铲子进入铲除模式，铲子的位置是(14*70,8*70)
				if my_map.mouse_down_x>14*70 and\
				 my_map.mouse_down_x<15*70 and\
				  my_map.mouse_down_y>8*70 and\
				   my_map.mouse_down_y<9*70:
					#鼠标点中铲子，就拿起铲子
					my_map.interface_shovel=True
					my_map.mouse_down_x=0
					my_map.mouse_down_y=0
				#点击一下怪物就掉100血
				for player in group:
					if my_map.mouse_down_x>player.X and\
					my_map.mouse_down_x<player.X+player.rect.width and\
					my_map.mouse_down_y>player.Y and\
					my_map.mouse_down_y<player.Y+player.rect.height:
						player.current_blood-=100
						my_map.mouse_down_x=0
						my_map.mouse_down_y=0
						break
				
				#对于位于group里的monster，根据属性值决定其位置
				for player in group:
					player.position=player.lujing[player.i][0]-30,player.lujing[player.i][1]-32
				
				
				#高级精灵动画部分，判断monster走路的方向来决定其眼睛朝那里看
				for player in group:
					if player.current_blood>=5:
						if player.lujing[player.i][0]-player.lujing[player.i-1][0]>0:
							player.direction=0
						elif player.lujing[player.i][0]-player.lujing[player.i-1][0]<0:
							player.direction=1
						elif player.lujing[player.i][1]-player.lujing[player.i-1][1]>0:
							player.direction=3
						elif player.lujing[player.i][1]-player.lujing[player.i-1][1]<0:
							player.direction=2
					else:
						player.direction=3
					player.first_frame=player.direction*player.columns
					player.last_frame=player.first_frame+1

				#绘制怪物
				group.update(ticks, 50)
				group.draw(screen)

				#绘制弹药
				bullets.update(ticks)
				bullets.draw(screen)
				#绘制treasure
				treasure_group.update(ticks,70)
				treasure_group.draw(screen)
				treasure.show_blood()
				my_map.blood=treasure.blood
				my_map.treasure_blood=treasure.current_blood

				#显示血条
				for player in group:
					player.show_blood()

				#更新点位
				for player in group:
					if player.current_blood>0:
						player.i+=1
				for player in group:
					if player.i>len(player.lujing)-1:
						treasure.current_blood-=200
						player.current_blood=0
						player.kill()
						a.remove(player)
						
				#检测冲突
				#添加目标（不超过一个）
				for tower in towers:
					if len(tower.target)==0:
						for player in group:
							if pygame.sprite.collide_circle_ratio(tower.range)(player,tower):
								tower.setTarget(player)
								break
				#移除超过射程的目标
				for tower in towers:
					for player in tower.target:
						if not pygame.sprite.collide_circle_ratio(tower.range)(player,tower):
							tower.target.remove(player)
				#移除被消灭的目标
				for tower in towers:
					for player in tower.target:
						if player.current_blood<=0:
							tower.target.remove(player)
				#检测炮弹的命中情况并移除击中目标的炮弹
				for bullet in bullets:
					for player in group:
						if pygame.sprite.collide_rect(player, bullet):
							player.hitByBullet(bullet)
							bullet.kill()
				#移除未击中炮弹
				for bullet in bullets:
					if bullet.life<=0:
						bullet.kill()
				#杀死怪物，播放音♂效
				for player in group:
					if player.current_blood<=0:
						deathSound=pygame.mixer.Sound(player.sound_death)
						deathSound.play()
						player.kill()
						a.remove(player)
						my_map.money+=player.money
				#攻击目标，绘制防御塔
				towers.update(ticks,70)
				for tower in towers:
					tower.attack()
				for tower in towers:
					tower.draw(screen)

				#时间更新
				Time+=1
				
				if treasure.current_blood<=0:
					#表示这一关没有通过
					Time=0
					game_win=False
					moreinterface.game_win=game_win
					game_begin=True
					game_on=False
					current_level+=1

				if treasure.current_blood>1 and len(a)==0:
					#表示这关已经赢了
					pygame.display.update()
					time.sleep(0.5)
					Time=0
					game_win=True
					moreinterface.game_win=game_win
					game_begin=True
					game_on=False
					current_level+=1
					if current_level==7:
						game_over=True
						game_begin=False
		
		#两个关卡之间的过渡页
		elif game_begin==True and game_on==False:
			#读取鼠标键盘输入
			moreinterface.mouse_down_x=0
			moreinterface.mouse_down_y=0
			for event in pygame.event.get():
				if event.type==QUIT:
					sys.exit()
				elif event.type == KEYUP:
					if event.key == pygame.K_ESCAPE:
						sys.exit()
				elif event.type==MOUSEMOTION:
						mouse_x,mouse_y=event.pos
				elif event.type==MOUSEBUTTONDOWN:
					moreinterface.mouse_down_x,moreinterface.mouse_down_y=event.pos
			moreinterface.mouse_x=mouse_x
			moreinterface.mouse_y=mouse_y
			moreinterface.draw_transition_page()
			game_on=moreinterface.game_on	
	
	#暂停页
	elif game_pause==True:
		#读取鼠标键盘输入
		moreinterface.init()
		for event in pygame.event.get():
			if event.type==QUIT:
				sys.exit()
			elif event.type == KEYUP:
				if event.key == pygame.K_ESCAPE:
					sys.exit()
			elif event.type==MOUSEMOTION:
					moreinterface.mouse_x,moreinterface.mouse_y=event.pos
			elif event.type==MOUSEBUTTONDOWN:
				moreinterface.mouse_down_x,moreinterface.mouse_down_y=event.pos
		moreinterface.draw_pause_page()
	
	#刷新
	pygame.display.update()
