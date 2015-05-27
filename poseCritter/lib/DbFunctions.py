


#DbFunctions
#------------------------------------------------------------------
'''
Description
'''

#Imports
#------------------------------------------------------------------
import sys, os
import sqlite3
import pickle



#DbFunctions
#------------------------------------------------------------------


#checkIfDbExists
def checkIfDbExists(dbDir, dbName):
	
	#build complete db Path
	dbFileFormat = '.db'
	dbPath = dbDir + dbName + dbFileFormat
	
	return os.path.exists(dbPath)

	
#createDb
def createDb(dbDir, dbName):
	
	#build complete db Path
	dbFileFormat = '.db'
	dbPath = dbDir + dbName + dbFileFormat
	
	
	#Create db at dbPath
	connection = sqlite3.connect(dbPath)
	
	#Create cursor
	cursor = connection.cursor()
	
	#SQL Query
	sql = """
	CREATE TABLE poses
	(poseName text, manipulatorSettings text)
	"""
	
	#ExecuteQuery
	cursor.execute(sql)
	
	
	#End connection
	connection.close()
	
	


#removeDb
def removeDb(dbDir, dbName):
	
	#build complete db Path
	dbFileFormat = '.db'
	dbPath = dbDir + dbName + dbFileFormat
	
	#remove db
	os.remove(dbPath)
	
	

#insertPose
def insertPose(dbDir, dbName, poseName, manipulatorSettings):
	
	#build complete db Path
	dbFileFormat = '.db'
	dbPath = dbDir + dbName + dbFileFormat
	
	#Create db at self.dbPath
	connection = sqlite3.connect(dbPath)
		
	#Create cursor
	cursor = connection.cursor()
		
	#SQL Query
	sql = """
	INSERT INTO poses
	VALUES (?,?)
	"""
		
	#ExecuteQuery
	cursor.execute(sql, [poseName, manipulatorSettings])
		
	#Connection commit
	connection.commit()
		
	#End connection
	connection.close()
		
	
	
	
#fetchAll
def fetchAll(dbDir, dbName):
	
	#build complete db Path
	dbFileFormat = '.db'
	dbPath = dbDir + dbName + dbFileFormat
	
	#Create connection to db at dbPath
	connection = sqlite3.connect(dbPath)
		
	#Create cursor
	cursor = connection.cursor()
		
	#SQL Query
	sql = """
	SELECT *
	FROM poses
	"""
		
	#ExecuteQuery
	cursor.execute(sql)
		
	#getResult
	resultList = cursor.fetchall()
		
	#End connection
	connection.close()
		
	#return result
	return resultList
		
	
	
	
#getObjectNames
def getObjectNames(dbDir, dbName):
		
	#build complete db Path
	dbFileFormat = '.db'
	dbPath = dbDir + dbName + dbFileFormat
	
	#Create connection to db at dbPath
	connection = sqlite3.connect(dbPath)
		
	#Create cursor
	cursor = connection.cursor()
		
	#SQL Query
	sql = """
	SELECT poseName
	FROM poses
	"""
		
	#ExecuteQuery
	cursor.execute(sql)
		
	#getResult
	resultListOfTuples = cursor.fetchall()
		
	#End connection
	connection.close()
		
	#Bring result in nice list form
	resultList = []
		
	for resultTuple in resultListOfTuples:
		resultList.append(resultTuple[0])
		
	#return result
	return resultList
		
		
	
	
#printDb
def printDb(dbDir, dbName):
		
	#build complete db Path
	dbFileFormat = '.db'
	dbPath = dbDir + dbName + dbFileFormat
	
	#Create connection to db at dbPath
	connection = sqlite3.connect(dbPath)
		
	#Create cursor
	cursor = connection.cursor()
		
	#SQL Query
	sql = """
	SELECT *
	FROM poses
	"""
		
	#ExecuteQuery
	cursor.execute(sql)
		
	#getResult
	resultList = cursor.fetchall()
		
	#End connection
	connection.close()
		
	#return result
	print(resultList)
		
		
	
	
#removePose
def removePose(dbDir, dbName, poseName):
		
	#build complete db Path
	dbFileFormat = '.db'
	dbPath = dbDir + dbName + dbFileFormat
	
	#Create connection to db at dbPath
	connection = sqlite3.connect(dbPath)
		
	#Create cursor
	cursor = connection.cursor()
		
	#SQL Query
	sql = """
	DELETE FROM poses WHERE poseName = (?)
	"""
		
	#ExecuteQuery
	cursor.execute(sql, [poseName])
		
	#Connection commit
	connection.commit()
		
	#End connection
	connection.close()
		
		
	
	
#removeAll
def removeAll(dbDir, dbName):
		
	#build complete db Path
	dbFileFormat = '.db'
	dbPath = dbDir + dbName + dbFileFormat
	
	#Create connection to db at dbPath
	connection = sqlite3.connect(dbPath)
		
	#Create cursor
	cursor = connection.cursor()
		
	#SQL Query
	sql = """
	DELETE FROM poses
	"""
		
	#ExecuteQuery
	cursor.execute(sql)
		
	#Connection commit
	connection.commit()
		
	#End connection
	connection.close()
		
	
	

	
#getPoseSettings
def getPoseSettings(dbDir, dbName, poseName):
		
	#build complete db Path
	dbFileFormat = '.db'
	dbPath = dbDir + dbName + dbFileFormat
	
	#Create connection to db at dbPath
	connection = sqlite3.connect(dbPath)
		
	#Create cursor
	cursor = connection.cursor()
		
	#SQL Query
	sql = """
	SELECT manipulatorSettings
	FROM poses
	WHERE poseName = (?)
	"""
		
	#ExecuteQuery
	cursor.execute(sql, [poseName])
		
	#getResult (List > Tuple > Str)
	resultStr = cursor.fetchall()[0][0]
		
	#End connection
	connection.close()
		
	return resultStr
	

	
	
	
#getDatabases
def getDatabases(dbDir):
	
	#Get list of all db files in dbDir
	fileList = []
	#iterate through all items (files and dir) in path
	for item in os.listdir(dbDir):
		#check if item is file not dir
		if (os.path.isfile(os.path.join(dbDir, item))):
			#check if file has .db ending
			if (item.split('.')[-1] == 'db'):
				#Get first value of splitList as dbName and append
				dbName = item.split('.')[0]
				fileList.append(dbName)
	
	return fileList



	
#convertDictToDbString
def convertDictToDbString(itemsDict):
	
	#pickle itemsDict
	itemsDictStr = pickle.dumps(itemsDict)
	return itemsDictStr
	
	
#convertDbStringToDict
def convertDbStringToDict(dbString):
		
	return pickle.loads(dbString.encode('ascii'))
		
		
		
		
		
	