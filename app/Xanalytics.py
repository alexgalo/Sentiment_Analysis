from app.polarity import polarity
from app.crawler import *
from app import create_app
from rq import get_current_job
from os import listdir

import time

#print('iniciando tasks')
app = create_app()
#print('app context')
app.app_context().push()
#print('push')


#crawler = TwitterCrawler()

#polarityDict = dict()
#polarizer = polarity()
#polarityDict = object.getPolarity()


def getKeys(polarityDict):
    keysDict = list()
    keysDict = polarityDict.keys()

    return keysDict

#print(getKeys(polarityDict))

def getPositiveValues(polarityDict):
    positiveValues = list()

    for hashtag in polarityDict:
        positiveValues.append(polarityDict[hashtag]['positivePolarity'])

    return positiveValues

#print(getPositiveValues(polarityDict))

def getNegativeValues(polarityDict):
    negativeValues = list ()

    for hashtag in polarityDict:
        negativeValues.append(polarityDict[hashtag]['negativePolarity'])

    return negativeValues

#print(getNegativeValues(polarityDict))

def test(seconds):
    print('starting task')
    for i in range(seconds):
        print(i)
        time.sleep(1)
    print('task complete')

def getLastJSON():
	jsonPath = 'json_db'
	filesList = listdir(jsonPath)
	filesList = sorted(filesList)
	lastJSONFile = filesList[-1]
	return lastJSONFile

def pipelineAnalyticsLoad():
	#obtener el ultimo json
	app.logger.info('Obteniendo el ultimo json')
	#lastJSONFile = getLastJSON()

	#crear obj polarity
	app.logger.info('Calculando la polaridad')
	polarityDict = dict()                       #instancia de dict
	polarizer = polarity()                     #instancia de la clase polarity
	jsonPath = 'json_db/'
	jsonFileName = getLastJSON()
	jsonPath = jsonPath + jsonFileName
	polarityDict = polarizer.getPolarity(jsonPath)      #metodo getPolarity regresa dict: label|+|- 

	app.logger.info('Obteniendo la polaridad')
	keysL = list()
	keysL = getKeys(polarityDict)                       #regresa una lista con las llaves
	#obtener polaridad +
	positiveL = list()
	positiveL = getPositiveValues(polarityDict)             #regresa una lista con los valores positivos
	#obtener polaridad -
	negativeL = list()
	negativeL = getNegativeValues(polarityDict)             #regresa una lista con los valores negativos

	return (keysL, positiveL, negativeL)

# *
def pipelineAnalytics():
    keysL = list()
    positiveL = list()
    negativeL = list()

    # Obtener el ultimo json
    app.logger.info('Iniciando analytics')
    
    now = time.strftime("%X")
    nowHour = now.split(':')[0]
    nowMinute = now.split(':')[1]
    print('La hora actual es: ',nowHour, nowMinute)

    #app.logger.info('Obteniendo JSON file')
    lastJSONFile = getLastJSON()
    hourParts = lastJSONFile.split('-')
    hourParts = hourParts[3].split('.')[0]
    hour = hourParts.split(':')[0]
    minute = hourParts.split(':')[1]

    dataCrawler = ''
    if((int(hour) == int(nowHour)) or ((int(hour)-1) == int(nowHour))):
        #si el json es de hace mas de 10 min
        if((int(nowMinute)-int(minute)) > 10):
            #crear obj crawler
            app.logger.info('Ejecutando el crawler')
            crawler = TwitterCrawler()                  #instancia de la clase TwitterCrawler
            #obtener json generado con crawler
            dataCrawler = crawler.pipeline()            #metodo pipeline genera un json con los tweets
    
    #crear obj polarity
    app.logger.info('Calculando la polaridad')
    polarityDict = dict()                       #instancia de dict
    polarizer = polarity()                     #instancia de la clase polarity
    
    if(dataCrawler == ''):
        jsonFileName = lastJSONFile
    else:
        jsonFileName = dataCrawler

    jsonPath = 'json_db/'
    jsonPath = jsonPath + jsonFileName
    polarityDict = polarizer.getPolarity(jsonPath)      #metodo getPolarity regresa dict: label|+|- 
    
    
    app.logger.info('Obteniendo la polaridad')
    keysL = getKeys(polarityDict)                       #regresa una lista con las llaves
    #obtener polaridad +
    positiveL = getPositiveValues(polarityDict)             #regresa una lista con los valores positivos
    #obtener polaridad -
    negativeL = getNegativeValues(polarityDict)             #regresa una lista con los valores negativos
    print(':s')

    return (keysL, positiveL, negativeL)
