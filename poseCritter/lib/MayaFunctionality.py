

#MayaFunctionality
#------------------------------------------------------------------
'''
Maya Functionality:
Implements all the functionality for Maya using PyMel
'''

'''
ToDo:
1 - getSelectedManipList
'''


#Import
#------------------------------------------------------------------
import pymel.core as pm
import maya.OpenMayaUI as openMayaUi
import maya.OpenMaya as openMaya
import sip
import maya.cmds as cmds
from PyQt4 import QtGui, QtCore
import os



	
#Functions
#------------------------------------------------------------------	



#Namespace
#------------------------------------------------------------------	
#getNamespaces
def getNamespaces():
	namespacesList = []
	
	#Check if current namespace is root else set to scene root
	if not(pm.namespaceInfo(isRootNamespace = True)):
		
		#store current namespace
		currentNamespace = pm.namespaceInfo(currentNamespace = True)
		#Set to rootnamespace
		pm.namespace(setNamespace = ':')
		#Query namespaceList
		namespacesList = pm.namespaceInfo(listOnlyNamespaces = True, r = True)
		#Set back to old namespace
		pm.namespace(setNamespace = currentNamespace)
	
	#If namespace is root namespace
	else:
		#Query namespaceList
		namespacesList = pm.namespaceInfo(listOnlyNamespaces = True, r = False)
		
	#Rebuild namespaceList without UI and shared
	namespacesListTmp = []
	
	for namespaceItem in namespacesList:
		if not(namespaceItem == 'UI' or namespaceItem == 'shared'): namespacesListTmp.append(namespaceItem)
	
	namespacesList = namespacesListTmp
	
	#Append root namespace
	namespacesList.append('root')
	#Reverse List to have root as first item
	namespacesList.reverse()
	
	return namespacesList
	

	

	
#SelectedObjects
#------------------------------------------------------------------

#getSelectedList
def getSelectedList():
	
	#Get current Selection of Nodes
	selectedList = pm.ls(sl = True, fl = True)
	
	return selectedList
	
#getSelectedObjectsFromTagList
def getSelectedObjectsFromTagList(tagList):
	
	#Get current Selection of Nodes
	selectedList = pm.ls(tagList)
	
	return selectedList
	

	
#buildSelectedItemsDictionary
def buildSelectedItemsDictionary(selectedList):
	
	dbInsertString = ''
	dbInsertDict = {}
	attrList = []
	
	
	#Iterate items of selectedList and get list of not all Attrs != Hidden or locked
	for selectedItem in selectedList:
		attrList.append(pm.listAttr(selectedItem, k = True, u = True))
	
			
	#buildDbInsertDict
	#for item in selectedList
	for selectedListIndex in range(0, len(selectedList)):
		
		#for attrList in attrList
		#build attrAndValueDict
		attrAndValueDict = {}
		for attribute in attrList[selectedListIndex]:
			attrAndValueDict[attribute] = pm.getAttr(selectedList[selectedListIndex].name() +'.' +attribute)
		
		
		#if len of namespace is >1 that means there is a namespace
		#else just get item[0]
		if(len(selectedList[selectedListIndex].name().split(':')) > 1):
			
			#get list of names splitted at ':'
			selectedItemNameList = selectedList[selectedListIndex].name().split(':')
			#Remove first item
			selectedItemNameList.pop(0)
			
			#Iterate selectedItemNameList and concatenate to final string
			selectedItemName = ''
			for splitResult in selectedItemNameList:
				selectedItemName += splitResult
				#Append : sign if splitResult is not last entry of selectedItemNameList
				if not (splitResult == selectedItemNameList[-1]): 
					selectedItemName += ':'
			
		#Else just take item[0]
		else: selectedItemName = selectedList[selectedListIndex].name().split(':')[0]
			
		
		#Add dict of attrs and values to dbInsertDict
		dbInsertDict[selectedItemName] = attrAndValueDict
	
	
	return dbInsertDict
	

	
#printSelectedItemsDictionary
def printSelectedItemsDictionary(selectedItemsDict):
		
	for manip in selectedItemsDict.keys():
		print('\n' +manip +'\n-----------------------')
		for attr in selectedItemsDict[manip].keys():
			
			#Get Value for attr
			value = selectedItemsDict[manip][attr]
			#Print Each Attr and value
			print(str(attr) +': ' +str(value))
			


#Tag Check
#------------------------------------------------------------------

#checkTag
def checkTag(tagList):
	
	#iterate tagList and check obj existence for each node
	for nodeName in tagList:
		try:
			pm.PyNode(nodeName)
		except:
			return False
	
	return True

			

#Set Pose
#------------------------------------------------------------------



#setPose
def setPose(poseDict, namespace):
	
	#start undo chunk
	cmds.undoInfo(openChunk=True)
	
	try:
	
		#Iterate through manips in poseDict
		for manip in poseDict.keys():
			#iterate through attributes in attrDict of manip
			for attribute in poseDict[manip].keys():
				
				#Set namespace for manip
				if(namespace == 'root'): manipName = manip
				else: manipName = namespace +':' +manip
				
				#Get Value for attr
				attrValue = poseDict[manip][attribute]
				
				#setAttr
				try:			
					pm.setAttr(manipName +'.' +str(attribute), attrValue)
				except:
					print('Error setting ' +manipName)
	
	except:
		pass
		
	finally:
		#end undo chunk
		cmds.undoInfo(closeChunk=True)
	

#Screenshot
#------------------------------------------------------------------

				
#takeScreenshotForPoseBtn
def takeScreenshotForPoseBtn(filepath, filename, filesizeW, filesizeH):
	
	defaultRenderGlobalsNode = pm.PyNode('defaultRenderGlobals')
	
	#Get Current imageFormat from renderglobals
	currentImageFormat = pm.getAttr(defaultRenderGlobalsNode.name()+'.imageFormat')
	
	#Set new imageFormat to jpg
	defaultRenderGlobalsNode.setAttr('imageFormat', 8)
	
	
	#Create Playblast image
	
	#create playblast image path
	playblastImagePath = filepath +filename + '.jpg'
	pm.playblast(cf = playblastImagePath, fr = [pm.currentTime()],wh = (filesizeW, filesizeH), fmt =  'image',o = False, orn = False, v = False, p = 100)
	
	#Reset imageFormat to old one
	defaultRenderGlobalsNode.setAttr('imageFormat', currentImageFormat)
	

#takeScreenshotForPoseBtnApi
def takeScreenshotForPoseBtnApi(filepath, filename, dbName, filesizeW, filesizeH):
	
	#construct playblast image path
	playblastImagePath = filepath +dbName + filename + '.jpg'
	
	#Grab last active 3d view
	view = openMayaUi.M3dView.active3dView()
	
	#read the color buffer from the view, and save the MImage to disk
	image = openMaya.MImage()
	view.readColorBuffer(image, True)
	image.resize(filesizeW, filesizeH, True)
	image.writeToFile(playblastImagePath, 'jpg')
	

#removeScreenshot
def removeScreenshot(completeFilepath):
	os.remove(completeFilepath)
	

	
	
#Make Dockable
#------------------------------------------------------------------

#makeDockable
def makeDockable(childWidget, areaName, width, label):
	
	slider = pm.floatSlider() #some throwaway control, feel free to delete this when you're done.
	dock = pm.dockControl(l = label, content=slider,  area = areaName, w = width ) #Returns the string path to the dock control. The control is a QDockWidget under the hood.
	dockPt = openMayaUi.MQtUtil.findControl(dock) #Find the pointer to the dock control
	dockWidget = sip.wrapinstance(long(dockPt), QtCore.QObject) #Get that pointer as a Qt widget
	childWidget.setParent(dockWidget)
	dockWidget.setWidget(childWidget) #Set the docked widget to be your custom control.




	