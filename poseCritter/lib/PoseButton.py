
#PoseButton
#------------------------------------------------------------------
'''
Description
'''

#Imports
#------------------------------------------------------------------
from PyQt4 import QtGui, QtCore
import sys, os
import random


#PoseButton class
#------------------------------------------------------------------
class PoseButton(QtGui.QWidget):
	
	#Constructor
	def __init__(self, poseName = '', dbName = '', widthHeight = 30, parent = None):
		super(PoseButton,self).__init__(parent)
		
		#Instance Vars
		self.lytVertButtons = QtGui.QVBoxLayout()
		self.poseBtn = QtGui.QPushButton()
		self.delPoseBtn = QtGui.QPushButton()
		
		self.width = widthHeight
		self.height = widthHeight
		self.delBtnHeight = int(widthHeight/4)
		self.poseName = poseName
		self.dbName = dbName
		
		self.poseBtnStyleSheet = ''
		self.poseBtnImagePath = ''
		self.imageFileFormat = 'jpg'
		
		#setupPoseButton
		self.setPoseBtnImagePath()
		self.setPoseBtnStyleSheet()
		self.setupPoseButton()
		
		
		
		
	
	#setupPoseButton
	def setupPoseButton(self):
		
		#Buttons setup
		self.poseBtn.setObjectName(self.poseName)
		self.delPoseBtn.setObjectName('delete ' +self.poseName)
		
		self.poseBtn.setText(self.poseName)
		self.delPoseBtn.setText('delete ' +self.poseName)
		
		self.poseBtn.setMaximumSize(self.width, self.height)
		self.poseBtn.setMinimumSize(self.width, self.height)
		self.delPoseBtn.setMaximumSize(self.width, self.delBtnHeight)
		self.delPoseBtn.setMinimumSize(self.width, self.delBtnHeight)
		
		#ButtonStyleSheets
		self.poseBtn.setStyleSheet(self.poseBtnStyleSheet)
		
		#PoseButton Widget setup
		self.setFixedSize(self.width, self.height + self.delBtnHeight)
		self.setLayout(self.lytVertButtons)
		
		
		#Lyt setup
		self.lytVertButtons.setMargin(0)
		self.lytVertButtons.setSpacing(0)
		
		self.lytVertButtons.addWidget(self.poseBtn)
		self.lytVertButtons.addWidget(self.delPoseBtn)
		
		
	#getPoseName
	def getPoseName(self):
		return self.poseName
		
	#getDbName
	def getDbName(self):
		return self.dbName
		
	#setWidth
	def setWidth(self, newWidth):
		self.width = newWidth
		
	#setHeight
	def setHeight(self, newHeight):
		self.height = newHeight
		self.delBtnHeight = int(newHeight/4)
		
	#resizePoseButton
	def resizePoseButton(self, newWidth, newHeight):
		
		#Set width and height variables
		self.setWidth(newWidth)
		self.setHeight(newHeight)
		
		#Resize poseBtn and delPoseBtn
		self.poseBtn.setMaximumSize(self.width, self.height)
		self.poseBtn.setMinimumSize(self.width, self.height)
		self.delPoseBtn.setMaximumSize(self.width, self.delBtnHeight)
		self.delPoseBtn.setMinimumSize(self.width, self.delBtnHeight)
		
		#PoseButton Widget setup
		self.setFixedSize(self.width, self.height + self.delBtnHeight)
		
		
	#setPoseBtnStyleSheet
	def setPoseBtnStyleSheet(self):
		
		
		#check if image exists / if so then set background to red else random
		if(os.path.exists(self.poseBtnImagePath)):
		
			self.poseBtnStyleSheet = 'QWidget#'+str(self.getPoseName())+' {\
			border-image: url('+self.poseBtnImagePath.replace('\\', '\/')+');\
			font-weight: bold;\
			color: rgb(255,255,255);\
			font-size: 15px;\
			}'
		
		else:
			self.poseBtnStyleSheet = 'QWidget#'+str(self.getPoseName())+' {\
			background-color: rgb(255, 0,0);\
			font-weight: bold;\
			color: rgb(255,255,255);\
			font-size: 15px;\
			}'
		
		
	#setPoseBtnImagePath
	def setPoseBtnImagePath(self):
		
		#Get path that points to lib folder
		self.poseBtnImagePath = os.path.join(os.path.dirname(__file__))
		
		#Build final string
		self.poseBtnImagePath = self.poseBtnImagePath[:-4] +'\\media\\images\\' +self.getDbName() +self.getPoseName() +'.' +self.imageFileFormat
		
		
		
#Execute if not imported
#------------------------------------------------------------------
if(__name__ == '__main__'):
	app = QtGui.QApplication(sys.argv)
	poseButtonInstance = PoseButton('Heiner', 80)
	#poseButtonInstance.show()
	sys.exit(app.exec_())
		
		

		
		
		
		
		
