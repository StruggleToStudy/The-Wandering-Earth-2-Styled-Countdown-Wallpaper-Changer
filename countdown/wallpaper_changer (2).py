import ctypes
import datetime#获取时间

from PIL import ImageFont,Image,ImageDraw#编辑图片
from os.path import join,abspath,dirname,exists#获取路径
from os import mkdir
from apscheduler.schedulers.background import BackgroundScheduler#定时任务

from components import Countdown,Explanation
from screen import Screen
from screens import Screens
from images import Images

class WallPaperChanger:
	def __init__(self,path=abspath(join(dirname(__file__),'files'))):
		#路径
		self.path = path
		self.path_font = join(self.path,'fonts')
		self.path_images = join(self.path,'images')

		if not exists(self.path):
			mkdir(self.path)



		self.Screens = Screens(duration = '1m')

		#测试代码
		event_name = ['测试倒计时','test countdown']
		event_day = "2023-04-04 14:20:0"
		#创建屏幕实例
		self.lib = Images([self.path,self.path_images],pics = ['掠过木星.jpg'])

		Screen1 = Screen(self.path,self.lib)
		Screen1.add_components(Countdown([self.path,self.path_font],
						[['高考危机','college entrance examination crisis'],'2023-06-07'],
						datetrans = ['d',{'wtd':-1,'dth':3,'htm':1,'mts':3}],
						loc = (500,500)
						))
		Screen1.add_components(Explanation([self.path,self.path_font],
                                                ['测试文字','test word'],
                                                (100,100)))

		Screen2 = Screen(self.path,self.lib)
		screen2.add_components(Countdown([self.path,self.path_font],
						[event_name,event_day],
						datetrans = ['h',{'wtd':-1,'dth':3,'htm':1,'mts':3}]
						))

		self.Screens.add_screen(Screen1)
		self.Screens.add_screen(Screen2)
		
		
	def _prepare_scheduler(self):
		self.scheduler = BackgroundScheduler()
		self.scheduler.start()
		
	def change_wallpaper(self):
		'''更换壁纸'''
		ctypes.windll.user32.SystemParametersInfoW(20,0,self.screen_curr.image,0)

	def update_wallpaper(self):
		#更新选定的屏幕并更换桌面
		self.Screens.screen_curr.update()
		#self.change_wallpaper()
		#如果有更新任务，就设置最近的
		update_dates = self.Screens.screen_curr.update_dates[:]
		switch_screen_date = self.Screens.next_update_time
		if len(update_dates) > 0:
			update_date = update_dates[0]
			if update_dates < switch_screen_date:
				self.scheduler.add_job(self.update_wallpaper,'date',
						       run_date = update_date)
			else:
				pass#更换当前屏幕
			
			
	def change_curr_screen(self):
		pass
		
	def start(self):
		self._prepare_scheduler()
		self.Screens.start()
		self.update_wallpaper()
			
if __name__ == '__main__':
	app = WallPaperChanger()
	app.start()
	
