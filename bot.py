#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#Got a lot of this code from masnun.com/2015/12/05/creating-a-twitter-retweet-bot-in-python.html
#modifications made by Kent Sullivan

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler, API
from tweepy import Stream
import json
import logging
import warnings
from pprint import pprint
from wordnik import *
from secrets import *
import re

warnings.filterwarnings("ignore")
apiUrl = 'http://api.wordnik.com/v4'
apiKey = WordnikapiKey
client = swagger.ApiClient(apiKey, apiUrl)

auth_handler = OAuthHandler(C_KEY, C_SECRET)
auth_handler.set_access_token(A_TOKEN, A_TOKEN_SECRET)

twitter_client = API(auth_handler)
 
logging.getLogger("main").setLevel(logging.INFO)
 
class PyStreamListener(StreamListener):
    def on_data(self, data):
        tweet = json.loads(data)
        poem="" #poem to tweet
        line1 = ""
        line2 = ""
        line3 = ""
        try:
            #calling the LineGen function 3 times
            line1 = self.linegen("line1",5)
            line2 = self.linegen("line2",7)
            line3 = self.linegen("line3",5)
            print('Poem: \n%s\n%s\n%s' %(line1,line2,line3))
            poem='\n{}\n{}\n{}'.format(line1,line2,line3)

#           Post back to Twitter
            screen_name = "@" + tweet['user']['screen_name']
            twitter_client.update_status('{}:{}'.format(screen_name,poem),tweet['id'])
 
        except Exception as ex:
            logging.error(ex)

        return True

    def on_error(self, status):
        print status
        
    def getrand(self, low=3, high=15):
        #grabs a word from the API and send it to sylco function for counting. www.eayd.in/?p=232
        wordApi = WordsApi.WordsApi(client)
        random = wordApi.getRandomWord(minLength=low,maxLength=high)
        v = self.sylco(random.word)
        return (random.word, v)
 
    def sylco(self,word):
     
        word = word.lower()
     
        # exception_add are words that need extra syllables
        # exception_del are words that need less syllables
     
        exception_add = ['serious','crucial']
        exception_del = ['fortunately','unfortunately']
     
        co_one = ['cool','coach','coat','coal','count','coin','coarse','coup','coif','cook','coign','coiffe','coof','court']
        co_two = ['coapt','coed','coinci']
     
        pre_one = ['preach']
     
        syls = 0 #added syllable number
        disc = 0 #discarded syllable number
     
        #1) if letters < 3 : return 1
        if len(word) <= 3 :
            syls = 1
            return syls
     
        #2) if doesn't end with "ted" or "tes" or "ses" or "ied" or "ies", discard "es" and "ed" at the end.
        # if it has only 1 vowel or 1 set of consecutive vowels, discard. (like "speed", "fled" etc.)
     
        if word[-2:] == "es" or word[-2:] == "ed" :
            doubleAndtripple_1 = len(re.findall(r'[eaoui][eaoui]',word))
            if doubleAndtripple_1 > 1 or len(re.findall(r'[eaoui][^eaoui]',word)) > 1 :
                if word[-3:] == "ted" or word[-3:] == "tes" or word[-3:] == "ses" or word[-3:] == "ied" or word[-3:] == "ies" :
                    pass
                else :
                    disc+=1
     
        #3) discard trailing "e", except where ending is "le"  
     
        le_except = ['whole','mobile','pole','male','female','hale','pale','tale','sale','aisle','whale','while']
     
        if word[-1:] == "e" :
            if word[-2:] == "le" and word not in le_except :
                pass
     
            else :
                disc+=1
     
        #4) check if consecutive vowels exists, triplets or pairs, count them as one.
     
        doubleAndtripple = len(re.findall(r'[eaoui][eaoui]',word))
        tripple = len(re.findall(r'[eaoui][eaoui][eaoui]',word))
        disc+=doubleAndtripple + tripple
     
        #5) count remaining vowels in word.
        numVowels = len(re.findall(r'[eaoui]',word))
     
        #6) add one if starts with "mc"
        if word[:2] == "mc" :
            syls+=1
     
        #7) add one if ends with "y" but is not surrouned by vowel
        if word[-1:] == "y" and word[-2] not in "aeoui" :
            syls +=1
     
        #8) add one if "y" is surrounded by non-vowels and is not in the last word.
     
        for i,j in enumerate(word) :
            if j == "y" :
                if (i != 0) and (i != len(word)-1) :
                    if word[i-1] not in "aeoui" and word[i+1] not in "aeoui" :
                        syls+=1
     
        #9) if starts with "tri-" or "bi-" and is followed by a vowel, add one.
     
        if word[:3] == "tri" and word[3] in "aeoui" :
            syls+=1
     
        if word[:2] == "bi" and word[2] in "aeoui" :
            syls+=1
     
        #10) if ends with "-ian", should be counted as two syllables, except for "-tian" and "-cian"
     
        if word[-3:] == "ian" : 
        #and (word[-4:] != "cian" or word[-4:] != "tian") :
            if word[-4:] == "cian" or word[-4:] == "tian" :
                pass
            else :
                syls+=1
     
        #11) if starts with "co-" and is followed by a vowel, check if exists in the double syllable dictionary, if not, check if in single dictionary and act accordingly.
     
        if word[:2] == "co" and word[2] in 'eaoui' :
     
            if word[:4] in co_two or word[:5] in co_two or word[:6] in co_two :
                syls+=1
            elif word[:4] in co_one or word[:5] in co_one or word[:6] in co_one :
                pass
            else :
                syls+=1
     
        #12) if starts with "pre-" and is followed by a vowel, check if exists in the double syllable dictionary, if not, check if in single dictionary and act accordingly.
     
        if word[:3] == "pre" and word[3] in 'eaoui' :
            if word[:6] in pre_one :
                pass
            else :
                syls+=1
     
        #13) check for "-n't" and cross match with dictionary to add syllable.
     
        negative = ["doesn't", "isn't", "shouldn't", "couldn't","wouldn't"]
     
        if word[-3:] == "n't" :
            if word in negative :
                syls+=1
            else :
                pass  
     
        #14) Handling the exceptional words.
     
        if word in exception_del :
            disc+=1
     
        if word in exception_add :
            syls+=1    
     
        # calculate the output
        return numVowels - disc + syls




    def linegen(self,linenum,tot):
        v=0 #vowel count
        l=0 #line sylable total
        #while line is less that 6 variables.
        linenum = linenum
        line = ""
        while (l<tot):
            #This chunk to get random word
            word, v = self.getrand()
            if v+l<=tot:
                line = line +' '+ word
                l=l+v
                print('%s has %s vowels' %(word,v))
                print('%s: %s ||Count:%s' %(linenum,line,l))
            else:
                print('Oops we need a smaller word than %s which has %s vowels' %(word,v))
                word, v = self.getrand(4,4)
                line = line +' '+ word
                l=l+v
                print('%s has %s vowels' %(word,v))
                print('%s: %s ||Count:%s' %(linenum,line,l))
        return line


if __name__ == '__main__':
    listener = PyStreamListener()
    stream = Stream(auth_handler, listener)
    stream.filter(track=['TrinaTrunner','haikume'])
