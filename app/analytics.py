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
    app.logger.info('Iniciando Analytics')
    
    
    app.logger.info('Iniciando Crawler en Analytics')
    crawler= TwitterCrawler()
    dataCrawler= crawler.pipeline()

    app.logger.info('Iniciando Polarity en Analytics')
    polarityDict= dict()
    polarizer= polarity()
    
    app.logger.info('Recuperando recursos')
    jsonFileName= getLastJSON()
    print(jsonFileName)
    jsonPath = 'json_db/'
    jsonPath = jsonPath + jsonFileName

    app.logger.info('Obteniendo la polaridad')
    polarityDict = polarizer.getPolarity(jsonPath)      #metodo getPolarity regresa dict: label|+|- 
    keysL = getKeys(polarityDict)                       #regresa una lista con las llaves
    #obtener polaridad +
    positiveL = getPositiveValues(polarityDict)             #regresa una lista con los valores positivos
    #obtener polaridad -
    negativeL = getNegativeValues(polarityDict)             #regresa una lista con los valores negativos
    print(':s')

    return (keysL, positiveL, negativeL)
