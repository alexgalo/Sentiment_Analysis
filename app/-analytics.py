from app.polarity import polarity
from app.crawler import *
from app import create_app
from rq import get_current_job

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

def pipelineAnalytics():
    #obtener el ultimo json
        #si el json es de hace mas de 10 min
    
    #crear obj crawler
    app.logger.info('Ejecutando el crawler')
    crawler = TwitterCrawler()                  #instancia de la clase TwitterCrawler
    dataCrawler = crawler.pipeline()            #metodo pipeline genera un json con los tweets
            
    #crear obj polarity
    app.logger.info('Calculando la polaridad')
    polarityDict = dict()                       #instancia de dict
    polarizer = polarity()                      #instancia de la clase polarity
    polarityDict = polarizer.getPolarity()      #metodo getPolarity regresa dict: label|+|- 
    
    #listas de valores para graficar
    app.logger.info('Obteniendo la polaridad')
    keysL = getKeys(polarityDict)                       #regresa una lista con las llaves
    positiveL = list()
    positiveL = getPositiveValues(polarityDict)             #regresa una lista con los valores positivos
    negativeL = getNegativeValues(polarityDict)             #regresa una lista con los valores negativos
    print('PIPE :)')

    return (keysL, positiveL, negativeL)
