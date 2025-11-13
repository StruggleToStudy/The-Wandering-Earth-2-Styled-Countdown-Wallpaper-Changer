import datetime
from os.path import join,basename
from PIL import ImageFont,Image,ImageDraw

from os.path import join,basename


class Component:
	def __init__(self):
		pass
	def draw(self):
		pass
	def sync(self):
		pass


class Countdown(Component):
	'''流浪地球2风格的倒计时'''
	def __init__(self,path,event,loc=None,datetrans = ['d',{'wtd':-1,'dth':3,'htm':1,'mts':3}]):
		#路径
		self.path_save = path[0]
		self.path_font = path[1]
		#事件名称
		self.event_name = event[0]#
		self.event_day = event[1]#
		#处理简写的时间格式（没有时分秒）
		if len(self.event_day) <= 11:
			self.event_day = self.event_day.strip() + ' 00:00:00'
		
		self.date_format_default = datetrans[0]#默认日期格式
		self.date_format_change = datetrans[1]#决定什么时候切换日期格式
		
		self.loc = loc

		self.days = '??'
		self.event_day_date = datetime.datetime.strptime(self.event_day,"%Y-%m-%d %H:%M:%S")#
		self.unit = ''
		
		self._prepare_fonts()

	def _prepare_fonts(self):
		#字体文件
		self.font_loc = join(self.path_font,'字魂59号-创粗黑.ttf')
		self.font_loc2 = join(self.path_font,'DIN-1451-Mittelschrift.ttf')#字体
                #颜色
		self.font_num_color = 'red'
		self.font_cn_color = 'white'
		self.font_en_color = 'white'
	
	def get_time(self):
		'''计算今日与目标日期的间隔并以适当的单位返回'''
		#获取时间
		curr_date = datetime.datetime.now()
		
		date_formats = {'w':['周','weeks'],'d':['天','days'],'h':['小时','hours'],'m':['分','minutes'],'s':['秒','seconds']}
		date_format = date_formats[self.date_format_default]#
		if curr_date > self.event_day_date:#超过预定日期
			return ["还剩",'in'],0,date_format
		else:
			#计算时间间隔
			date_gap = self.event_day_date - curr_date
			days,seconds = date_gap.days,date_gap.seconds
			durations = {'w':days // 7,
				'd':days,
				'h':days * 24 + seconds // 3600,
				'm':days * 24 * 60 + seconds // 60,
				's':days * 24 * 3600 + seconds}

			units = ['w','d','h','m','s']
			flag = False
			duration = durations['w']

			for i in range(1,len(units)):
				unit = units[i]
				if flag:
					if duration < self.date_format_change[f'{units[i-1]}t{unit}']:
						date_format = date_formats[unit]
						duration = durations[unit]
					else:
						break
				elif self.date_format_default == unit and not flag:
					date_format = date_formats[unit]
					duration = durations[unit]
					flag = True

		#if duration == 0:
		#	return ["不足",'in less than'],1,date_format

		return ["还剩",'in'],duration + 1,date_format

	def trans_fonts(self):
		#字体大小
		self.font_size = 200
		self.font_size_small = int(self.font_size / 2)
		self.font_size_tiny = int(self.font_size / 4)
		#准备字体
		self.font_num = ImageFont.truetype(self.font_loc2,self.font_size)
		self.font_cn = ImageFont.truetype(self.font_loc,self.font_size_small)
		self.font_en = ImageFont.truetype(self.font_loc2,self.font_size_tiny)

			
	def draw(self,background):
		'''在图片上绘制倒计时的整体'''
		#打开图片
		image = Image.open(background)
		draw = ImageDraw.Draw(image)
		
		if self.loc != None:
			x,y = self.loc
		else:
			x,y = image.size[0] / 2 ,image.size[1] / 2
		
		#准备文字
		crisis = f"距{self.event_name[0]}"
		crisis_en = f"THE {self.event_name[1].upper()}"
		remain,self.days,self.unit = self.get_time()#还剩/不足 XX 单位 更换名字
		days = str(self.days)
		
		#准备文字文件
		self.trans_fonts()

		#计算文字的长度
		crisis_length = draw.textsize(crisis,self.font_cn)[0]
		crisis_en_length = draw.textsize(crisis_en,self.font_en)[0]
		days_length = draw.textsize(days,self.font_num)[0]
		
		#添加红色矩形
		draw.rectangle([x-int(self.font_size_small / 10) * 3,y,x-int(self.font_size_small / 10) * 2,y+self.font_size],fill = 'red',outline = None)
		
		#添加文字
		#中文
		draw.text((x-crisis_length+self.font_size_small*2,y-self.font_size_small),crisis,font = self.font_cn,fill = self.font_cn_color)
		draw.text((x,y),remain[0],font = self.font_cn,fill = self.font_cn_color)
		draw.text((x+self.font_size_small*2+days_length,y),self.unit[0],font = self.font_cn,fill = self.font_cn_color)
		#英文
		draw.text((x,y+self.font_size_small),crisis_en,font = self.font_en,fill = self.font_en_color)
		draw.text((x,y+self.font_size_small+self.font_size_tiny),f"{remain[1].upper()} {days} {self.unit[1].upper()}",font = self.font_en,fill = self.font_en_color)
		
		#添加倒计时数字
		draw.text((x+2*self.font_size_small,y-self.font_size_small),days,font = self.font_num,fill = self.font_num_color)
		
		#保存
		image.save(join(self.path_save,basename(background)))#改为图片路径

	def sync(self):
		'''计算到下一次更新需要多久'''
		a,self.days,self.unit = self.get_time()
		day = self.days - 1#
		unit = self.unit[1][0]#

		if day < 0:
			return -1
		
		if unit == 'w':
			duration = datetime.timedelta(days = 7)
		elif unit == 'd':
			duration = datetime.timedelta(days = 1)
		elif unit == 'h':
			duration = datetime.timedelta(seconds = 3600)
		elif unit == 'm':
			duration = datetime.timedelta(seconds = 60)
		elif unit == 's':
			duration = datetime.timedelta(seconds = 1)
		else:#没有计算过天数
			return -1
		return self.event_day_date - duration * day



#-------------------------------------------------------------------------------



class Explanation(Component):
	'''流浪地球2风格的注释'''
	def __init__(self,path,word,loc=None):
		#路径
		self.path_save = path[0]
		self.path_font = path[1]

		self.word_cn = str(word[0])
		self.word_en = str(word[1]).upper()

		self.loc = loc


		self._prepare_fonts()

	def _prepare_fonts(self):
		#字体文件
		self.font_loc = join(self.path_font,'Font.ttf')#中文字体
		self.font_loc2 = join(self.path_font,'Rajdhani Medium.otf')#英文字体
                #颜色
		self.font_cn_color = 'white'
		self.font_en_color = 'white'

	def trans_fonts(self):
		#字体大小
		self.font_size = 200
		self.font_size_tiny = int(self.font_size / 4)
		#准备字体
		self.font_cn = ImageFont.truetype(self.font_loc,self.font_size)
		self.font_en = ImageFont.truetype(self.font_loc2,self.font_size_tiny)

	def draw(self,background):
		'''在图片上绘制注释的整体'''
		#打开图片
		image = Image.open(background)
		draw = ImageDraw.Draw(image)

		if self.loc != None:
			x,y = self.loc
		else:
			x,y = image.size[0] / 2 ,image.size[1] / 2

		#准备文字文件
		self.trans_fonts()
		
		#添加红色矩形
		draw.rectangle([x-int(int(self.font_size / 2) / 10) * 3,y,x-int(int(self.font_size / 2) / 10) * 2,y+self.font_size+self.font_size_tiny],fill = 'red',outline = None)

		#添加字
		#中文#
		draw.text((x,y),self.word_cn,font = self.font_cn,fill = self.font_cn_color)
		#英文
		draw.text((x,y+self.font_size),self.word_en,font = self.font_en,fill = self.font_en_color)

		#保存
		image.save(join(self.path_save,basename(background)))#改为图片路径

	def sync(self):
		return -1



#-------------------------------------------------------------------------------



class Quotes(Component):
	def __init__(self):
		pass

