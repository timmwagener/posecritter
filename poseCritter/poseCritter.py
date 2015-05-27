
'''
poseCritter
==========================================

A database driven pose library.

To use it execute the following script in your Maya
Script Editor.

.. code::

    from poseCritter import poseCritter
    poseCritter.poseCritter()

Current Status
-----------------------
Please note that currently i do not have the time to continue support for this little script.
It has basically been abandonded since 2012, and many things i would do differently today.
It might never the less work fine for you, but keep in mind that there might be newer, better
solutions.

Dependencies
-----------------------
PyQT4

Contact
-----------------------
**Author:** `Timm Wagener <mailto:wagenertimm@gmail.com>`_
'''


#Imports
#------------------------------------------------------------------
from PyQt4 import QtGui, QtCore, uic
import sys, os
import functools
import maya.OpenMayaUI as openMayaUi
import sip

#Reload boolean
doReload = False

from lib import FlowLayout
if(doReload): reload(FlowLayout)

from lib import PoseButton
if(doReload): reload(PoseButton)

from lib import DbFunctions
if(doReload): reload(DbFunctions)

from lib import MayaFunctionality
if(doReload): reload(MayaFunctionality)


#Get Maya QMAinWindow as Parent
#-------------------------------------------------------
def getMayaQMainWindow():
	ptr = openMayaUi.MQtUtil.mainWindow()
	return sip.wrapinstance(long(ptr), QtCore.QObject)


#Get ui file classes
#------------------------------------------------------------------
#Add path of ressource_rc.py
ressourceFilePath = os.path.join(os.path.dirname(__file__), 'media')
sys.path.append(ressourceFilePath)
uiFilePath = os.path.join(os.path.dirname(__file__), 'media\\poseCritterUi.ui')
uiClassesList = uic.loadUiType(uiFilePath)


#poseCritter class
#------------------------------------------------------------------
class poseCritter(uiClassesList[0], uiClassesList[1]):
	
	
	#Constructor
	#------------------------------------------------------------------	
	def __init__(self, parent = getMayaQMainWindow()):
		super(poseCritter, self).__init__(parent)
		
		#Instance Vars
		self.flowLayout = FlowLayout.FlowLayout()
		self.dbDir = os.path.join(os.path.dirname(__file__), 'database\\')
		self.dbStandard = 'poses'
		
		self.dockIt = True
		self.dockArea = 'left'
		self.version = 1
		self.label = 'poseCritter RC'
		
		
		#Startup Routine
		#------------------------------------------------------------------	
		
		#setupUi
		self.setupUi(self)
		
		#Set flowLayout
		self.scrlAreaPoseButtonsWidget.setLayout(self.flowLayout)
		
		#ConnectUi
		self.connectUi()
		
		#Set QValidators for lineInputs
		self.setPoseNameValidator()
		self.setTagValidator()
		self.setGroupNameValidator()
		
		#If not existing create dbPose
		if not(DbFunctions.checkIfDbExists(self.dbDir, self.dbStandard)): 
			DbFunctions.createDb(self.dbDir, self.dbStandard)
			
		#Set cmbbxGroups to already existing databases in the db folder
		self.setCmbbxGroups()
		
		#Create Initial Buttons from db
		self.createButtonsFromDb()
		
		#setNamespacesCombobox
		self.setNamespacesCombobox()
		
		#setLabelAuthor
		self.setLabelAuthor('poseCritter RC.' +str(self.version) +' by Timm Wagener / timmwagener.com')
		
		#makeDockable
		if(self.dockIt):
			windowWidth = self.geometry().width()
			MayaFunctionality.makeDockable(self, self.dockArea, windowWidth, self.label + ' ' + str(self.version))
		
		
		#show Ui
		self.show()
		
		
		
		
	
	
	
	#ConnectUi method
	#------------------------------------------------------------------	
		
	#ConnectUi
	def connectUi(self):
		
		#Connect btnCreateGroup
		self.btnCreateGroup.clicked.connect(self.addDb)
		
		#Connect btnDeleteGroup
		self.btnDeleteGroup.clicked.connect(self.deleteCurrentDb)
		
		#Connect cmbbxGroups
		self.cmbbxGroups.currentIndexChanged.connect(self.createButtonsFromDb)
		
		#Connect btnAdd
		self.btnAdd.clicked.connect(self.addPoseButton)
		
		#Connect btnRemoveAll
		self.btnRemoveAll.clicked.connect(self.removeAll)
		
		#Connect sldButtonSize
		self.sldButtonSize.valueChanged.connect(self.resizePoseButtons)
		
		#Connect btnRefreshNamespaces
		self.btnRefreshNamespaces.clicked.connect(self.setNamespacesCombobox)
		
		#Connect btnTagFromSelected
		self.btnTagFromSelected.clicked.connect(self.getTagFromSelected)
		
		#connect chkbxAddByTag
		self.chkbxAddByTag.toggled.connect(self.toggleTags)
		
		#Connect leFilter
		self.leFilter.textChanged.connect(self.filterPoseButtons)
		
		
		
		
	
	
	
	#PoseButton methods
	#------------------------------------------------------------------
	
	
	
	
	#addDb
	def addDb(self):
		
		#Check if leGroupName is empty
		if not (self.getDbName() == ''):
			#Get dbName
			dbName = self.getDbName()
			
			#Check if db already exists
			if not (DbFunctions.checkIfDbExists(self.dbDir, dbName)):
				
				
				#Create dB
				DbFunctions.createDb(self.dbDir, dbName)
				#Update cmbbx
				self.setCmbbxGroups()
				
				
			
			#else status: dbName already exists
			else: self.setStatus('Db %s already exists' % (dbName))
		
		#else status: dbName empty
		else: self.setStatus('Db Name empty')
		
		
	#deleteDb
	def deleteCurrentDb(self):
		
		#check if currentDb == dbStandard
		dbName = self.getCurrentDb()
		if not(dbName == self.dbStandard):
			
			#clearButtonsFromLayout before, because otherwise btns would remain
			self.clearButtonsFromLayout()
			
			#clearBtnImages from current db
			poseNameList = DbFunctions.getObjectNames(self.dbDir, dbName)
			for poseName in poseNameList:
				#Remove screenshot
				try:
					#get complete filepath
					completeFilePath = os.path.join(os.path.dirname(__file__), 'media\\images\\')
					completeFilePath += dbName
					completeFilePath += poseName
					completeFilePath += '.jpg'
					MayaFunctionality.removeScreenshot(completeFilePath)
		
				except:
					self.setStatus('Pose %s didnt have screenshot, no screen removed' % (poseName))
			
			#remove current db
			DbFunctions.removeDb(self.dbDir, dbName)
			#Update cmbbx
			self.setCmbbxGroups()
			
			
		#else setStatus: standard db cannot be deleted
		else: self.setStatus('Standard DB cannot be deleted')
	
	
	
	#filterPoseButtons
	def filterPoseButtons(self):
		
		#get filtertext
		filterText = self.getFilterText()
		
		#Check if filterText == ''
		if not(filterText == ''):
			
			#Iterate flowlyt itemList
			for QWidgetListItem in self.flowLayout.itemList:
				
				#get poseBtn widget
				poseBtn = QWidgetListItem.widget()
				
				#check if filterText in poseBtn poseName
				if(filterText in poseBtn.getPoseName()):
					#if match and item is hidden set visible
					if(poseBtn.isHidden()): poseBtn.setVisible(True)
				else: 
					#if no match and item is not hidden then hide
					if not(poseBtn.isHidden()): poseBtn.setHidden(True)
					
		
		#If filterText == '' set all visible
		else:
			#Iterate flowlyt itemList
			for QWidgetListItem in self.flowLayout.itemList:
				
				#get poseBtn widget
				poseBtn = QWidgetListItem.widget()
				poseBtn.setVisible(True)
				
	
					
	
	#removePoseButton
	def removePoseButton(self, btn):
		
		#Remove Widget
		btn.setParent(None)
		
		#Remove db entry
		dbName = self.getCurrentDb()
		DbFunctions.removePose(self.dbDir, dbName, str(btn.getPoseName()))
		
		
		#Remove screenshot
		try:
			#get complete filepath
			completeFilePath = os.path.join(os.path.dirname(__file__), 'media\\images\\')
			completeFilePath += dbName
			completeFilePath += str(btn.getPoseName())
			completeFilePath += '.jpg'
			MayaFunctionality.removeScreenshot(completeFilePath)
		
		except:
			self.setStatus('Pose %s didnt have screenshot, no screen removed' % (str(btn.getPoseName())))
	
	
	
	
	#addPoseButton
	def addPoseButton(self):
	
		#ADD POSE BY SELECTION
		#------------------------------------------------------------------
		if not(self.chkbxAddByTag.isChecked()):
			#check if there are selected objects
			if(len(MayaFunctionality.getSelectedList())):
				#Check if posename is set
				if not(self.getPoseName() == ''):
					#check against objectName list to avoid two equal names
					if not(self.getPoseName() in self.getItemListObjectNames()):
						
						
						
						
						#Create poseBtn Instance, connect Signals and add to FLyt
						#------------------------------------------------------------------
						
						#Create Screenshot for poseBtn
						try:
							imagePath = os.path.join(os.path.dirname(__file__), 'media/images/')
							imageSize = int(self.sldButtonSize.maximum())
							MayaFunctionality.takeScreenshotForPoseBtnApi(imagePath, self.getPoseName(), self.getCurrentDb(), imageSize, imageSize )
						except:
							self.setStatus('Error taking screenshot for %s' % (self.getPoseName()))
						
						
						#Create PoseButton instance
						btn = PoseButton.PoseButton(self.getPoseName(), self.getCurrentDb(), self.getPoseButtonSize())
						self.flowLayout.addWidget(btn)
						
						#Connect PoseBtn Instance
						btn.poseBtn.clicked.connect(functools.partial(self.setPose, self.getPoseName()))
						btn.delPoseBtn.clicked.connect(functools.partial(self.removePoseButton, btn))
						
						
						
						#Add pose to db
						#------------------------------------------------------------------
						
						#Get List of selected objects
						selectedObjList = MayaFunctionality.getSelectedList()
						#Convert obj list to poseDict
						poseDict = MayaFunctionality.buildSelectedItemsDictionary(selectedObjList)
						#Convert pose Dict to pickled dbString
						dbString = DbFunctions.convertDictToDbString(poseDict)
						#add poseName and dbString to DB
						dbName = self.getCurrentDb()
						DbFunctions.insertPose(self.dbDir, dbName, self.getPoseName(), dbString)
						
					
					
					
					#Else if posename twice
					else: self.setStatus('Pose already exists')
				
				#Else if no Posename is set
				else: self.setStatus('No Pose name entered')
				
			#Else if no objects are selected
			else: self.setStatus('No objects selected')
		
		
		
		
		#ADD POSE BY TAG
		#------------------------------------------------------------------
		else:
			#Check if tag is empty
			if not(self.getTag() == ''):
				
				#Get tag list
				tagList = self.getListFromTag()
				
				#Check if tag items valid
				if(MayaFunctionality.checkTag(tagList)):
					
					#Check if posename is set
					if not(self.getPoseName() == ''):
						
						#check against objectName list to avoid two equal names
						if not(self.getPoseName() in self.getItemListObjectNames()):
							
							
							
							
							#Create poseBtn Instance, connect Signals and add to FLyt
							#------------------------------------------------------------------
							
							#Create Screenshot for poseBtn
							try:
								imagePath = os.path.join(os.path.dirname(__file__), 'media/images/')
								imageSize = int(self.sldButtonSize.maximum())
								MayaFunctionality.takeScreenshotForPoseBtnApi(imagePath, self.getPoseName(), self.getCurrentDb(), imageSize, imageSize )
							except:
								self.setStatus('Error taking screenshot for %s' % (self.getPoseName()))
							
							
							#Create PoseButton instance
							btn = PoseButton.PoseButton(self.getPoseName(), self.getCurrentDb(), self.getPoseButtonSize())
							self.flowLayout.addWidget(btn)
							
							#Connect PoseBtn Instance
							btn.poseBtn.clicked.connect(functools.partial(self.setPose, self.getPoseName()))
							btn.delPoseBtn.clicked.connect(functools.partial(self.removePoseButton, btn))
							
							
							
							#Add pose to db
							#------------------------------------------------------------------
							
							#Get List of selected objects
							selectedObjList = MayaFunctionality.getSelectedObjectsFromTagList(tagList)
							#Convert obj list to poseDict
							poseDict = MayaFunctionality.buildSelectedItemsDictionary(selectedObjList)
							#Convert pose Dict to pickled dbString
							dbString = DbFunctions.convertDictToDbString(poseDict)
							#add poseName and dbString to DB
							dbName = self.getCurrentDb()
							DbFunctions.insertPose(self.dbDir, dbName, self.getPoseName(), dbString)
					
						
						
						#Else if posename twice
						else: self.setStatus('Pose already exists')
							
					#Else if no Posename is set
					else: self.setStatus('No Pose name entered')
					
				#Else if tagSelectedListWrong
				else: self.setStatus('Tag check failed - Check tag for writing errors')
			
			#Else if no Tag entered
			else: self.setStatus('No Tag entered')
		
		
	
	
	#createInitialButtonsFromDb
	def createButtonsFromDb(self):
		
		
		#Check if number of Groups is 0 and if so pass
		if(self.cmbbxGroups.count() == 0):
			pass
		
		#else rebuild buttons from cmbbx items
		else:
			#Clear lyt
			self.clearButtonsFromLayout()
			
			#Get current db
			dbName = self.getCurrentDb()
			
			#getObjectNames from Db
			objectNamesDb = DbFunctions.getObjectNames(self.dbDir, dbName)
			
			#Iterate through objectNamesFromDb and generate poseButton for each
			for name in objectNamesDb:
				
				
				#Create poseBtn Instance, connect Signals and add to FLyt
				#------------------------------------------------------------------
				
				btn = PoseButton.PoseButton(name, dbName, self.getPoseButtonSize())
				self.flowLayout.addWidget(btn)
				
				btn.poseBtn.clicked.connect(functools.partial(self.setPose, name))
				btn.delPoseBtn.clicked.connect(functools.partial(self.removePoseButton, btn))
			
	
	
	#clearButtonsFromLayout
	def clearButtonsFromLayout(self):
		
		#get List of all databases
		dbList = DbFunctions.getDatabases(self.dbDir)
		
		#for each db get all objectnames
		for dbName in dbList:
			#all objectnames for dbName
			objectNamesDb = DbFunctions.getObjectNames(self.dbDir, dbName)
		
			#Iterate through objectNamesFromDb
			for name in objectNamesDb:
			
				#Iterate objects in flowlyt itemList
				for QListWidget in self.flowLayout.itemList:
				
					#QListWidget > poseBtn widget
					poseBtn = QListWidget.widget()
				
					#If poseBtn.poseName == name
					if(str(poseBtn.getPoseName()) == name):
				
						#Remove Widget
						poseBtn.setParent(None)		
		
	
	
	
	
	#resizePoseButtons
	def resizePoseButtons(self):
		#Iterate through items in itemList and resize
		newBtnSize = self.getPoseButtonSize()
		for item in self.flowLayout.itemList:
			item.widget().resizePoseButton(newBtnSize, newBtnSize)
			
	
	
	#removeAll
	def removeAll(self):
		
		#getObjectNames from Db
		dbName = self.getCurrentDb()
		objectNamesDb = DbFunctions.getObjectNames(self.dbDir, dbName)
		
		#Iterate through objectNamesFromDb
		for name in objectNamesDb:
			
			#Iterate objects in flowlyt itemList
			for QListWidget in self.flowLayout.itemList:
				
				#QListWidget > poseBtn widget
				poseBtn = QListWidget.widget()
				
				#If poseBtn.poseName == name
				if(str(poseBtn.getPoseName()) == name):
				
					#Remove screenshot
					try:
						#get complete filepath
						completeFilePath = os.path.join(os.path.dirname(__file__), 'media\\images\\')
						completeFilePath += dbName
						completeFilePath += str(poseBtn.getPoseName())
						completeFilePath += '.jpg'
						MayaFunctionality.removeScreenshot(completeFilePath)
				
					except:
						self.setStatus('Pose %s didnt have screenshot, no screen removed' % (str(poseBtn.getPoseName())))
				
				
					#Remove Widget
					poseBtn.setParent(None)
				
		
			
		#Remove db entries
		DbFunctions.removeAll(self.dbDir, dbName)
			
			
	
	
	
	
	#Flowlayout methods
	#------------------------------------------------------------------
	
	#getItemListObjectNames
	def getItemListObjectNames(self):
		
		objectNamesList = []
		
		for item in self.flowLayout.itemList:
			objectNamesList.append(item.widget().getPoseName())
		
		return objectNamesList
	
		
	#printLayoutItems
	def printLayoutItems(self, lyt):
		for index in range(0, lyt.count()):
			print('item: %s objectName: %s' % (index, lyt.itemAt(index).widget().getPoseName()))
	
	
	
	
	
	
	#Get & set methods
	#------------------------------------------------------------------
	
	#getStatus
	def getStatus(self):
		return str(self.leStatus.text())
	
	#setStatus
	def setStatus(self, msg):
		self.leStatus.setText(msg)
		
	#getTag
	def getTag(self):
		return str(self.leTag.text())
		
	#getListFromTag
	def getListFromTag(self):
		
		#getTag string
		tagStr = self.getTag()
		
		#get tag list split by ','
		tagListTmp = tagStr.split(',')
		
		#Iterate through tagListTmp
		tagList = []
		for tagItem in tagListTmp:
			#strip whitespaces from tagItem
			tagItemStripped = tagItem.strip()
			#Check if tagItemStr is empty
			if not(tagItemStripped == ''):
				#add tagItemStripped
				tagList.append(tagItemStripped)
		
		return tagList
		
	#getTagFromSelected
	def getTagFromSelected(self):
		
		#Get selectedList
		selectedList = MayaFunctionality.getSelectedList()
		
		#Check if len(selectedList) > 0
		if not(len(selectedList)): self.setStatus('No Items selected')
		
		#if there are selected items
		else:
			#Iterate selectedList and create string
			tagStr = ''
			for index in range(0, len(selectedList)):
				tagStr += selectedList[index].name()
				
				#Append comma if item is not the last
				if not(selectedList[index] == selectedList[-1]): tagStr += ','
				
		#setTag
		self.setTag(tagStr)
		
	#setTag
	def setTag(self, tag):
		self.leTag.setText(tag)
		
	#getPoseButtonSize
	def getPoseButtonSize(self):
		return self.sldButtonSize.value()
		
	#getPoseName
	def getPoseName(self):
		return str(self.lePoseButtonName.text())
		
	#getFilterText
	def getFilterText(self):
		return str(self.leFilter.text())
		
	#setNamespacesCombobox
	def setNamespacesCombobox(self):
		
		#Get namespaceList
		namespacesList = MayaFunctionality.getNamespaces()
		
		#Clear and set cmbbxNamespace
		self.cmbbxNamespace.clear()
		self.cmbbxNamespace.addItems(namespacesList)
		
		
		
	#getNamespace
	def getNamespace(self):
		return str(self.cmbbxNamespace.currentText())
	
	
	#setPose
	def setPose(self, poseName):
		
		#Retrieve poseDictStr from DB for poseName
		dbName = self.getCurrentDb()
		poseDictStr = DbFunctions.getPoseSettings(self.dbDir, dbName, poseName)
		
		#Unpickle poseDictStr to dict
		poseDict = DbFunctions.convertDbStringToDict(poseDictStr)
		
		#Print selectedItemsDict
		#MayaFunctionality.printSelectedItemsDictionary(poseDict)
		
		#Set pose
		MayaFunctionality.setPose(poseDict, self.getNamespace())
		
	
	#setPoseNameValidator
	def setPoseNameValidator(self):
		
		#Create QRegExp object to prevent from whitespaces
		regexpNoWhitespaces = QtCore.QRegExp("^\\S+$")
		
		#Create QValidator to prevent from whitespaces in poseName
		vldtrNoWhitespaces = QtGui.QRegExpValidator()
		vldtrNoWhitespaces.setRegExp(regexpNoWhitespaces)
		
		#Set Validator for lePoseButtonName
		self.lePoseButtonName.setValidator(vldtrNoWhitespaces)
		
	#setGroupValidator
	def setGroupNameValidator(self):
		
		#Create QRegExp object to prevent from whitespaces
		regexpNoWhitespaces = QtCore.QRegExp("^\\S+$")
		
		#Create QValidator to prevent from whitespaces in poseName
		vldtrNoWhitespaces = QtGui.QRegExpValidator()
		vldtrNoWhitespaces.setRegExp(regexpNoWhitespaces)
		
		#Set Validator for leGroupName
		self.leGroupName.setValidator(vldtrNoWhitespaces)
		
	#setTagValidator
	def setTagValidator(self):
		
		#Create QRegExp object to allow only input of form word + ,
		regexpTag = QtCore.QRegExp("^((\\S)+([,]){1})*$")
		
		#Create QValidator to prevent from whitespaces in poseName
		vldtrTag = QtGui.QRegExpValidator()
		vldtrTag.setRegExp(regexpTag)
		
		#Set Validator for leTag
		self.leTag.setValidator(vldtrTag)
		
	
	
	#setCmbbxGroups
	def setCmbbxGroups(self):
		
		#clear
		self.cmbbxGroups.clear()
		
		#Get list of Databases in dbDir
		fileList = DbFunctions.getDatabases(self.dbDir)
					
		#Add fileList
		self.cmbbxGroups.addItems(fileList)
		
	
	#getCurrentDb
	def getCurrentDb(self):
		return str(self.cmbbxGroups.currentText())
	
	#getDbName
	def getDbName(self):
		return str(self.leGroupName.text())
		
	#setLabelAuthor
	def setLabelAuthor(self, msg):
		self.lblAuthor.setText(msg)
	
	
	#Tags
	#------------------------------------------------------------------
	
	#enableTags
	def toggleTags(self):
		
		#Check chkbxAddByTag state
		
		#if on
		if(self.chkbxAddByTag.isChecked()):
			#Enable leTag
			self.leTag.setEnabled(True)
			#printStatus
			self.setStatus('Tags enabled')
		
		#Else if off
		else:
			#Disable leTag
			self.leTag.setDisabled(True)
			#printStatus
			self.setStatus('Tags disabled')
			
	
	
	
	
	#TMP Methods
	#------------------------------------------------------------------
	
	#poseBtnVisToggle
	def poseBtnVisToggle(self, index):
		
		#Get poseBtn at index
		poseBtn = self.flowLayout.itemList[index].widget()
		
		#Toggle Vis
		if(poseBtn.isHidden()): poseBtn.setVisible(True)
		else: poseBtn.setHidden(True)
		


		
#Execute if not imported
#------------------------------------------------------------------
if(__name__ == '__main__'):
	app = QtGui.QApplication(sys.argv)
	poseCritterInstance = poseCritter()
	sys.exit(app.exec_())