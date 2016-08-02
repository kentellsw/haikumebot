#!/usr/bin/env python
# -*- coding: utf-8 -*-

from wordnik import *
apiUrl = 'http://api.wordnik.com/v4'
apiKey = '991beecd60e328b63010507cfe805eeebe915efc004f1fea3'
client = swagger.ApiClient(apiKey, apiUrl)

#wordApi = WordApi.WordApi(client)
#example = wordApi.getTopExample('irony')
#print example.text

#wordApi = WordApi.WordApi(client)
#example = wordApi.getDefinitions('cat')
#print example[0].text

#wordApi = WordApi.WordApi(client)
#example = wordApi.getAudio('cat')
#print example[0].fileUrl

wordApi = WordsApi.WordsApi(client)
example = wordApi.getRandomWord(minLength=1,maxLength=3)
print example.id
print example.word
print example.originalWord
print example.suggestions
print example.canonicalForm
print example.vulgar

#wordApi = WordsApi.WordsApi(client)
#example = wordApi.getRandomWords(limit=2)
#print '#1: '+example[0].word+', #2: '+example[1].word
#print example[1].word
