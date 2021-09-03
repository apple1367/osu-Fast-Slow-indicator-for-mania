import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtGui import QPixmap
from PyQt5 import QtCore
import requests

GOSU_URL = 'http://127.0.0.1:24050/json'
session = requests.Session()
TRESHOLD = 16
xywh = [900,400,120,50]

class MyApp(QWidget):

	def __init__(self):
		super().__init__()
		self.initUI()

	def initUI(self):
		self.early = QPixmap()
		self.late = QPixmap()
		self.perfect = QPixmap()
		self.early.load('fast.png')
		self.late.load('slow.png')
		self.perfect.load('perfect.png')
		self.imagelabel = QLabel(self)
		self.imagelabel.setAlignment(QtCore.Qt.AlignCenter)	
		self.imagelabel.setPixmap(self.late)	
		self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
		self.setAttribute(QtCore.Qt.WA_NoSystemBackground, True)
		self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
		self.move(xywh[0], xywh[1])
		self.resize(xywh[2], xywh[3])
		self.show()

	def updatelate(self):
		self.imagelabel.setPixmap(self.late)
		self.imagelabel.repaint()
	def updateperfect(self):
		self.imagelabel.setPixmap(self.perfect)
		self.imagelabel.repaint()
	def updateearly(self):
		self.imagelabel.setPixmap(self.early)
		self.imagelabel.repaint()
	def update(self):
		self.response = session.get(GOSU_URL)
		self.data = self.response.json()
		self.hit_errors = self.data['gameplay']['hits']['hitErrorArray']
		if not self.hit_errors:
			print("플레이 대기중")
			QtCore.QTimer.singleShot(100,self.update)
			return
		if len(self.hit_errors) == 1:
			QtCore.QTimer.singleShot(10,self.update)
			return
		self.last_error = self.hit_errors[-1] + 0.3 * self.hit_errors[-2]
		if self.last_error < -TRESHOLD:
			self.updateearly()
		elif self.last_error > TRESHOLD:
			self.updatelate()
		else:
			self.updateperfect()
		QtCore.QTimer.singleShot(1,self.update)


if __name__ == '__main__':
   app = QApplication(sys.argv)
   ex = MyApp()
   ex.updateperfect()
   ex.update()
   sys.exit(app.exec_())