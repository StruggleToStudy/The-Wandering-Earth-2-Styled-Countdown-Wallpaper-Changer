from os.path import join
from os import listdir
from random import randint
import datetime
from datetime import timedelta

class Images:
	'''存储一组源图片地址的类'''
	def __init__(self,path,mode=['none',''],pics=None):
		self.path_save = path[0]
		self.path_image = path[1]
		
		self.mode = mode[0]#切换方式
		self.duration = mode[1]#切换时间
		
		self.images = []#图片库
		if pics == 'all':#全选
			pics = listdir(self.path_image)
		#将选定的图片转换为正确的路径

		#添加更宽泛的识别
		if pics != None:
			for i in pics:
				self.images.append(join(self.path_image,i))
		else:
			self.images = [join(self.path_save,'background.jpg')]

		self.last_time = datetime.datetime.now()
		
		self.index = 0
		self.image = self.images[self.index]
		self.select_image()


	def select_image(self):
		'''根据模式选择一张图片'''
		length = len(self.images)
		mode = self.mode
		if mode == 'order':
			self.index = (self.index + 1)%length#循环选择
		elif mode == 'random':
			#不重复选择
			index = randint(0,length-1)
			while index == self.index and length > 1:
				index = randint(0,length-1)
			self.index = index
		else:
			pass
		self.image = self.images[self.index]

		self.last_time = datetime.datetime.now()#

	def calculate_next_time(self):
		pass

	def sync(self):#想办法只用在更新时计算一次
		if self.mode != 'none':
			day = int(self.duration[:-1])
			unit = self.duration[-1]
			if unit == 'd':
				duration = timedelta(days = 1)
			elif unit == 'h':
				duration = timedelta(seconds = 3600)
			elif unit == 'm':
				duration = timedelta(seconds = 60)
			else:
				return -1
			return self.last_time + duration * day#
		else:
			return -1
