# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

import os
from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import *
from PyQt4.QtCore import *
#import pyaudio
import speech_recognition as sr

try:
	_fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
	def _fromUtf8(s):
		return s

try:
	_encoding = QtGui.QApplication.UnicodeUTF8
	def _translate(context, text, disambig):
		return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
	def _translate(context, text, disambig):
		return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
	def setupUi(self, MainWindow):
		MainWindow.setObjectName(_fromUtf8("MainWindow"))
		MainWindow.resize(543, 402)
		self.centralwidget = QtGui.QWidget(MainWindow)
		self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
		self.label = QtGui.QLabel(self.centralwidget)
		self.label.setEnabled(False)
		self.label.setGeometry(QtCore.QRect(31, 20, 480, 245))
		self.label.setText(_fromUtf8(""))
		self.label.setObjectName(_fromUtf8("label"))


		self.pushButton = QtGui.QPushButton(self.centralwidget)
		self.pushButton.setGeometry(QtCore.QRect(460, 300, 51, 41))
		self.pushButton.setText(_fromUtf8(""))
		self.pushButton.setObjectName(_fromUtf8("pushButton"))
		self.pushButton.setIcon(QIcon(QPixmap("mic.png")))
		self.pushButton.setIconSize(QtCore.QSize(35, 35))
		self.pushButton.clicked.connect(self.voiceInput)


		self.lineEdit = QtGui.QLineEdit(self.centralwidget)
		self.lineEdit.setGeometry(QtCore.QRect(30, 300, 361, 41))
		self.lineEdit.setText(_fromUtf8(""))
		self.lineEdit.setObjectName(_fromUtf8("lineEdit"))


		self.pushButton_2 = QtGui.QPushButton(self.centralwidget)
		self.pushButton_2.setGeometry(QtCore.QRect(390, 300, 71, 41))
		self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
		self.pushButton_2.clicked.connect(self.gettingText)


		MainWindow.setCentralWidget(self.centralwidget)
		self.menubar = QtGui.QMenuBar(MainWindow)
		self.menubar.setGeometry(QtCore.QRect(0, 0, 543, 25))
		self.menubar.setObjectName(_fromUtf8("menubar"))
		MainWindow.setMenuBar(self.menubar)

		self.statusbar = QtGui.QStatusBar(MainWindow)
		self.statusbar.setObjectName(_fromUtf8("statusbar"))
		MainWindow.setStatusBar(self.statusbar)
		self.statusbar.showMessage("Welcome to Sign Me")

		self.retranslateUi(MainWindow)
		QtCore.QMetaObject.connectSlotsByName(MainWindow)

	def voiceInput(self):
		sample_rate = 48000
		chunk_size = 2048
		r = sr.Recognizer()

		with sr.Microphone(device_index = 0, sample_rate = sample_rate,
							chunk_size = chunk_size) as source:
			#wait for a second to let the recognizer adjust the
			#energy threshold based on the surrounding noise levestatusTextl
			r.adjust_for_ambient_noise(source)
			self.statusText()
			message = 'Say Something'
			print(message)

			#listens for the user's input
			audio = r.listen(source)

			try:
				self.speech = r.recognize_google(audio)
				#fileName = name+'.gif'
				print(self.speech)

			#error occurs when google could not understand what was said

			except sr.UnknownValueError:
				print("Google Speech Recognition could not understand audio")

			except sr.RequestError as e:
				print("Could not request results from Google Speech Recognition service; {0}".format(e))

		self.gettingText()



	def gettingText(self):
		#self.label_3.setText("Hello World !")
		#self.label_3.setFont(QtGui.QFont("Times", 20, QtGui.QFont.Bold))

		if (self.lineEdit.text()):
			name = self.lineEdit.text().lower()
			o = name.split(' ')
		else:
			o = self.speech.split(' ')

		gif_files = filter(lambda x: x.endswith('.gif'), os.listdir())
		print(gif_files)
		F = []
		for i in gif_files:
			F.append(i.split('.gif')[0])
		print (F)

		output = []
		for i in range(len(o)):
			try:
				if o[i] in F:
					output.append(o[i])
				elif o[i]+' '+o[i+1] in F:
					output.append(o[i]+' '+o[i+1])
				elif o[i]+' '+o[i+1]+' '+o[i+2] in F:
					output.append(o[i]+' '+o[i+1]+' '+o[i+2])
				elif o[i]+' '+o[i+1]+' '+o[i+2]+' '+o[i+3] in F:
					output.append(o[i]+' '+o[i+1]+' '+o[i+2]+' '+o[i+3])
				elif o[i]+' '+o[i+1]+' '+o[i+2]+' '+o[i+3]+' '+o[i+4] in F:
					output.append(o[i]+' '+o[i+1]+' '+o[i+2]+' '+o[i+3]+' '+o[i+4])
				elif o[i]+' '+o[i+1]+' '+o[i+2]+' '+o[i+3]+' '+o[i+4]+' '+o[i+5] in F:
					output.append(o[i]+' '+o[i+1]+' '+o[i+2]+' '+o[i+3]+' '+o[i+4]+' '+o[i+5])
				else:
					print("nothing")
			except:
				pass

		print(output)
		self.lineEdit.setText("")
		self.movie_names = output
		self.start()

	def start(self):
		self.load_the_nex_file()
		self.system_timer = QtCore.QTimer()
		self.system_timer.timeout.connect(self.hello_ali)
		self.system_timer.start(1500)

	def hello_ali(self):
		self.load_the_nex_file()

	def load_the_nex_file(self):
		if len(self.movie_names):
			print("get the next one")
			file_name = self.movie_names.pop(0)
			self.movie = QMovie(file_name , QByteArray(), self.label)
			self.movie.setCacheMode(QMovie.CacheAll)
			self.movie.setSpeed(100)
			self.label.setMovie(self.movie)
			self.movie.start()
		else:
			print("stop")
			self.movie.stop()
			self.system_timer.stop()

	def statusText(self):
		self.statusbar.showMessage('Say Something')

	def retranslateUi(self, MainWindow):
		MainWindow.setWindowTitle(_translate("MainWindow", "Sign Me", None))
		self.pushButton_2.setText(_translate("MainWindow", "Submit", None))


if __name__ == "__main__":
	import sys
	app = QtGui.QApplication(sys.argv)
	MainWindow = QtGui.QMainWindow()
	ui = Ui_MainWindow()
	ui.setupUi(MainWindow)
	MainWindow.show()
	sys.exit(app.exec_())

