import datetime
from datetime import timedelta

class Screens:
	'''存储一组屏幕的类'''
	def __init__(self,mode = 'order',duration = '1h'):
		self.mode = mode
		self.duration = duration

		self.index = -1
		self.screens = []

	def add_screen(self,screen):
		self.screens.append(screen)
		if self.index == -1:
			self.index = 0
			self.screen_curr = self.screens[0]

	def change_curr_screen(self):
		if len(self.screens) > 0:
			self.screen_curr.stop()
			self.select_screen()
			self.screen_curr.start()
			self.next_update_time = self.sync()
		else:
			print('没有背景可以更换')

	def start(self):
		if len(self.screens) > 0:
			self.screen_curr.start()
			self.next_update_time = self.sync()
		else:
			print('没有背景可以显示')

	def stop(self):
		if len(self.screens) > 0:
			self.screen_curr.stop()
		else:
			print('没有背景可以显示')
		

	def select_screen(self):
		'''根据模式选择一幅背景'''
		length = len(self.screens)
		if length > 0:
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

			self.screen_curr = self.screens[self.index]
		else:
			print('没有背景可以选择')

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
			return datetime.datetime.now() + duration * day
		else:
			return -1
