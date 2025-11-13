from PIL import Image
from os.path import join,exists,basename
import datetime
from apscheduler.schedulers.background import BackgroundScheduler#定时任务

class Screen:
	'''管理单个屏幕上所有元素绘制的类'''
	def __init__(self,path,image_lib = None,mode = 'none'):
		self.path = path
		self.components = []
		self.mode = mode#切换方式

		self.scheduler = BackgroundScheduler()

		self.image_lib = image_lib#选定图库
		if self.image_lib == None:#若没有指定图库
			self.pic = join(self.path,'background.jpg')#
		else:
			self.pic = self.image_lib.image

	def add_components(self,component):
		'''添加一个部件'''
		self.components.append(component)
	
	def prepare_background(self):
		'''生成加工原图'''
		if not exists(self.pic):#如果图片不存在
			self.pic = join(self.path,'background_today.jpg')
			#调整大小
			image = Image.new('RGB',(3840,2160),color = 'black')#创建新背景
			image.save(self.pic)#保存在默认位置
		else:
			#生成加工图
			image = Image.open(self.pic)
		
			#如果比例不合适就进行加工
			
			image.save(join(self.path,'background_today.jpg'))
		self.image = join(self.path,'background_today.jpg')#加工图

	def update(self):
		#更新背景
		if self.image_lib != None:
			if datetime.datetime.now() >= self.image_lib.sync():
				self.image_lib.select_image()
				self.pic = self.image_lib.image
		#绘制背景
		self.prepare_background()
		#计算所有部件的更新时间

		
		self.update_dates = []#为主程序提供任务时间
		for i in self.components:
			i.draw(self.image)
			next_update = i.sync()
			if next_update != -1:
				self.update_dates.append(next_update)
		#计算图库更换时间
		if self.image_lib != None:
			lib_update = self.image_lib.sync()
			if lib_update != -1:
				self.update_dates.append(lib_update)

		self.update_dates.sort()#排序
	
	def start(self):
		self.scheduler.start()
		self.update()
	
	def stop(self):
		self.scheduler.shutdown()		
