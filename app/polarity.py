#!/usr/bin/python
# -*- coding:utf-8 -*-

import json
import codecs
import string
import unicodedata
import re


class polarity:
	sentimentDict = dict()
	sentWordsFile = 'app/polaridad.txt'
	jsonFile = 'app/test2.json'
	stopWordsFile = 'app/stopWordsES.txt' 
	jsonObject = dict()
	polarityDict = dict()
	stopWords = list()
	symbolsList = ['.', ',', ':', '—', ";", '"',"!", '¡', '¿',
	"?", "#", "%", "/", "&", "(", ")", '€', '¦', "=", '"', "'",
	"{", '±', '“', '”', "}", "[", "]", "$", "_", "-", "|", "‘",
	"’", "@", "🖒", "+", "*", "💔", "💗", "🇲", "🇽", "📉", "😎",
	"💞", "👑", "😘", "💕", "🙈", "😊", "⚜", "️", "🖤", " 💖",
	"🍔", "😭", "😨", "😱", "❤", "😂", "😁", "🙏", "👀", "🐾", "😀",
	"📄", "🇬", "🇩", "🤗", " 😩", "⚠", "🎄", "🔴", "👉", "👇", "🏽",
	"➡", "🔙", "🙄", "👏", "😅", "🛵", "🍕", "🖥", "👍", "🏻", "😍",
	"💚", "💛", "🙌", "📰", "😒", "😰", "😬", "✌", "😠", "😡", "☑",
	"😠", "😡", "🤥", "❣", "😩", "🤤", "☀", "🌻", "💁", "🤣", "♂",
	"•", "📽", "💥", "✍", "🙋", "♀", "📸", "🎅", "🐌", "💨", "🙊", "⚡"]


	def loadSentDictionary(self, fileIn):
		sentimentDict = {} #dictionary that saves the values for the sentiment analysis
		lines = codecs.open(fileIn, "r", "utf-8")
		for line in lines: #ciclo para cargar la palabras
			line = line.strip()
			lineParts = line.split('|')
			sentimentDict[lineParts[0]] = int(lineParts[1])
		return sentimentDict

	def loadJsonFile(self, jsonFile):
		jsonObject = json.loads(open(jsonFile).read())
		return jsonObject

	def loadStopWords(self, fileName):
		stopWords = []
		f = codecs.open(fileName, "r", "utf-8")
		for line in f:
			line =line.strip()
			stopWords.append(line)
		return stopWords

	def replaceUsernames(self, s, replaceBy):
		temp = re.compile(r"@\.[A-Za-z0-9_-]*")
		s = temp.sub(replaceBy, s)
		temp = re.compile(r"@[A-Za-z0-9_-]*")
		s = temp.sub(replaceBy, s)
		return s

	def removeAccents(self, inputStr):
	    nkfdForm = unicodedata.normalize('NFKD', inputStr)
	    return u"".join([c for c in nkfdForm if not unicodedata.combining(c)])

	def replaceLinks(self, s, replaceBy):
		#quita url www.algo.com/djj
		re.purge()
		temp = re.compile(r"\s*www\.\w+\.(com|net|me|org)?(\s|/*[-\w+&@#/%!?=~_:.\[\]()0-9]*)")
		s = temp.sub(replaceBy, s)
		#quita http://
		temp = re.compile(r"((http|ftp|https)://[-/?=&\w.]*)")
		s = temp.sub(replaceBy, s)
		return s

	def replaceHashtags(self, s, replaceBy):
		s = re.sub(r'#[A-Za-z0-9_-]*', replaceBy, s)
		return s

	def replaceSymbols(self, s, symbolsList, replaceBy):
	    for c in symbolsList:
	        s = s.replace(c, replaceBy)
	    return s

	def replaceNumbers(self, s, replaceBy):
		s = re.sub(r'([0-9]+(st|th|rd|nd|,[0-9]+|.[0-9]+)?)', replaceBy, s)
		return s

	def removeSpaces(self, s, replaceBy):
		s = re.sub("\s+" , replaceBy, s)
		return s

	def cleanTexts(self, currentText):
		cleanedText = currentText.lower()
		cleanedText = self.replaceUsernames(cleanedText,' ')
		cleanedText = self.removeAccents(cleanedText)
		cleanedText = self.replaceLinks(cleanedText,' ')
		cleanedText = self.replaceHashtags(cleanedText,' ')
		cleanedText = self.replaceSymbols(cleanedText, self.symbolsList,' ')
		cleanedText = self.replaceNumbers(cleanedText, ' ')
		cleanedText = self.removeSpaces(cleanedText, ' ')
		return cleanedText

	def removeStopWords(self, text):
		finalText = []
		words = text.split()
		for word in words:
			if word not in self.stopWords:
				finalText.append(word)
			wholeText = ' '.join(finalText)
		return wholeText

	def createHashtagVocabulary(self, listIn):#creates a list with the hashtag words
		text = list()
		for each in listIn:
			if each != '':
				words = each.split()
				for word in words:
					if word != '':
						text.append(word)
		return text

	def calculatePolarity(self, hashtagVocabulary):
		polarity = list()
		positive = 0
		negative = 0
		for word in hashtagVocabulary:
			if word in self.sentimentDict:
				value = self.sentimentDict.get(word,0)
				if value > 0:
					positive = positive + value
				if value < 0:
					negative = negative + value
		denominator = abs(positive) + abs(negative)
		if denominator > 0:
			Ppos = abs(positive) / denominator #positive polarity
			Pneg = abs(negative) / denominator #negative polarity
		else:
			Ppos = 0.0
			Pneg = 0.0
		return Ppos, Pneg

	def getPolarity(self, jsonName):
		self.jsonFile = jsonName
		self.sentimentDict = self.loadSentDictionary(self.sentWordsFile)
		self.jsonObject = self.loadJsonFile(self.jsonFile)
		self.stopWords = self.loadStopWords(self.stopWordsFile)

		#iterates the hashtags inside the json file
		for key in self.jsonObject:
			#print('====== {} ======'.format(key))
			tweetList = self.jsonObject[key]['tweet_list']
			textsList = list()
			#gets the tweet list per hashtag
			for tweet in tweetList:
				textsList.append(tweet['text'])
			finalTextsList = list()
			for each in textsList:
				cleanedText = self.cleanTexts(each)
				finalText = self.removeStopWords(cleanedText)
				if finalText != '':
					finalTextsList.append(finalText)
			textsList = []
			hashtagVocabulary = self.createHashtagVocabulary(finalTextsList)
			(polarityP, polarityN) = self.calculatePolarity(hashtagVocabulary)
			#print('positive: {}    negative: {}'.format(polarityP, polarityN))
			self.polarityDict[key] = {"positivePolarity": polarityP, "negativePolarity": polarityN}

		return self.polarityDict
