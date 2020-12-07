from PySide2.QtWidgets import QApplication, QMainWindow, QPushButton, QPlainTextEdit,QLabel,QWidget
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QFile,QSize,QTimer
from PySide2.QtGui import QImage, QPixmap
import cv2
import serial
import serial.tools.list_ports
#def handleCalc ():
	#print('按钮被点击了')

#app = QApplication([])

#window = QMainWindow()
#window.resize(500, 400)
#window.move(300, 310)
#window.setWindowTitle('薪资统计')


#textEdit = QPlainTextEdit(window)
#textEdit.setPlaceholderText("请输入薪资表")
#textEdit.move(10,25)
#textEdit.resize(300,350)

#button = QPushButton('统计', window)
#button.move(380,80)
#button.clicked.connect(handleCalc)

#window.show()


#app.exec_()
class CalVar:
	def __init__(self):
		# 从文件中加载UI定义
		qfile_CalVar= QFile('D:/program/pyui/CalulateRealTimeVideoVariance.ui')
		qfile_CalVar.open(QFile.ReadOnly)
		qfile_CalVar.close()
		
		plist = list(serial.tools.list_ports.comports())
		



        # 从 UI 定义中动态 创建一个相应的窗口对象
        # 注意：里面的控件对象也成为窗口对象的属性了
        # 比如 self.ui.button , self.ui.textEdit
		self.ui = QUiLoader().load(qfile_CalVar)
		
		self.ui.OpenCamera.clicked.connect(self.btnopen_click)
		self.ui.ButtonUp.clicked.connect(self.btnUp_click)
		self.ui.ButtonStop.clicked.connect(self.btnStop_click)
		self.ui.ButtonDown.clicked.connect(self.btnDown_click)
		'''
		串口初始化部分
		'''
		self.serial1=False
		if len(plist) <= 0:
			print ("The Serial port can't find!")
			self.ui.serialNamelabel.setText('Don\'t have serial')
		else:#表示已经连接了有串口
			plist_0 =list(plist[0])
			serialName = plist_0[0]
			self.serial1 = serial.Serial(serialName, 9600, timeout=1) 
			print ("check which port was really used >",self.serial1.name)
			self.ui.serialNamelabel.setText('serialName:'+self.serial1.name)


	'''
	点击open button的事件处理
	'''
	def btnopen_click(self):
		#img = cv2.imread('C:/Users/59872/Desktop/DIP/AllLena.jpg', 0)
		#(means,stddev)=cv2.meanStdDev(img)#先计算，因为下面格式转换了
		#img=cv2.cvtColor(img,cv2.COLOR_BGR2BGRA)#先将图片转换成BGRA格式
		#qtimg = QImage(img,img.shape[1], img.shape[0],
        #               QImage.Format_RGB32)#再按RGB32格式转换成QImage即可,
											#img.shape[0]读入的时图片的高度height
											#img.shape[1]读入的时图片的宽度weight
		#self.ui.Cameralabel.resize(QSize(img.shape[1], img.shape[0]))#重新修改CameraLabel的大小
		#self.ui.Cameralabel.setPixmap(QPixmap.fromImage(qtimg))
		#self.ui.variancelabel.setText(str(stddev[0][0]**2))#计算方差
		self.capture = cv2.VideoCapture(0)#选择调用哪个摄像头的
		self.capture.set(cv2.CAP_PROP_FRAME_WIDTH , self.ui.Cameralabel.width())
		self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, self.ui.Cameralabel.height())

		self.timer = QTimer()
		self.timer.timeout.connect(self.display_gray_video_stream)
		self.timer.start(30)

	def display_gray_video_stream(self):

		_, frame = self.capture.read(0)
		'''
		cap.read()是按帧读取，返回两个值：ret,frame
    	ret是布尔值，如果读取帧是正确的则返回True，如果文件读取到结尾，它的返回值就为False；
    	后面的frame该帧图像的三维矩阵BGR形式。
		'''

		(means,stddev)=cv2.meanStdDev(frame)
		self.ui.variancelabel.setText(str(stddev[0][0]**2))


        #frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
		frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
		frame = cv2.flip(frame, 1)#使图像进行翻转,1水平翻转，0垂直翻转，-1水平垂直翻转
        #image = QImage(frame, frame.shape[1], frame.shape[0],
         #              frame.strides[0], QImage.Format_RGB888)
		image = QImage(frame, frame.shape[1], frame.shape[0],
                       frame.strides[0], QImage.Format_Indexed8)
		self.ui.Cameralabel.setPixmap(QPixmap.fromImage(image))

	def btnUp_click(self):
		if self.serial1:
			self.move('FF010010003F50')#速度63 全速
		else:
			print('当前没有插入端口')
	def btnStop_click(self):
		if self.serial1:
			self.move('FF010000000001')#停止
		else:
			print('当前没有插入端口')
	def btnDown_click(self):
		if self.serial1:
			self.move('FF010008003F48')#下降速度63 全速
		else:
			print('当前没有插入端口')
			
	

	def move(self,send_data):
		if self.serial1.is_open:
			print("port open success")
			#send_data = send_data.decode('hex')    # 发送数据转换为b'\xff\x01\x00U\x00\x00V'
			send_data = bytes.fromhex(send_data)
			self.serial1.write(send_data)
		else:
			print("port open failed")




app = QApplication([])
calvar = CalVar()
calvar.ui.show()
app.exec_()
