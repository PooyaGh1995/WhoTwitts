#1.import libs

from __future__ import unicode_literals
from hazm import *

from bidi.algorithm import get_display
import arabic_reshaper

import multidict as multidict
import numpy as np
import time
import re
from PIL import Image
from os import path
from wordcloud import WordCloud
import matplotlib.pyplot as plt
#import matplotlib.pyplot as plt2

#2.normalize text using hazm

def log(log_text):
    global lindex
    log_file.write("%s. %s \n" %(str(lindex),log_text))
    lindex=lindex+1

def getNormalizedText(txt):
    normalizer=Normalizer()
    log("Normalizing text using Hazm normalize method...")
    return normalizer.normalize(txt)

#3.generate word frequency dictionary using multidict (skip "az" "be" "ra" va.... words)

def getFrequencyDictForText(sentence):
    log("Tokenizing normalized text and making frequency dictionary...")
    fullTermsDict = multidict.MultiDict()
    tmpDict = {}
    rfile=open('results.txt','w')
    # making dict for counting frequencies
    #for text in sentence.split(" "):
    i=1
    j=0

    for w in word_tokenize(sentence):


        if re.match("\.|و|از|که|را|برای|با|به|تا|،|در|بر|برای|؟|؛|است|روحانی|#|https|//t",w):

            #print(str(i))
            i=i+1
            continue
        val = tmpDict.get(w,0)
        tmpDict[w.lower()] = val+1

        sorted_values=sorted(tmpDict.values(),reverse=True)
        sorted_keys=sorted(tmpDict,key=tmpDict.__getitem__,reverse=True)

    for key in tmpDict:

        #print(key)
        key2=str(get_display(arabic_reshaper.reshape(str(key))))
        #key=get_display(key)

        fullTermsDict.add(key2,tmpDict[key])

        #rfile.write("%s: " % str(key))
        #rfile.write("%s\n" % str(tmpDict[key]))

        rfile.write("%s: " % str(sorted_keys[j]))
        rfile.write("%s\n" % str(sorted_values[j]))
        j=j+1
    log("%s words ignored." %str(i))
    return fullTermsDict

#4.generate image using wordCloud image_generate_using_frequency method

def makeImage(t,tt):
    log("Making image of word clouds for selected texts...")
    log_file.close()
    _mask = np.array(Image.open("twitter.jpg"))


    wc = WordCloud(background_color="white", max_words=200, mask=_mask, max_font_size=40)
    #wc = WordCloud(background_color="white", max_words=1000, max_font_size=40)
    # generate word cloud
    wc2 = WordCloud(background_color="white", max_words=200, mask=_mask, max_font_size=40)

    wc.generate_from_frequencies(t)
    wc2.generate_from_frequencies(t)

    fig=plt.figure()
    fig.add_subplot(2,1,1)
    # show

    #plt.imshow(wc, interpolation="bilinear")
    #plt.axis("off")
    #plt.show()
    plt.axis("off")
    plt.imshow(wc)
    fig.add_subplot(2,1,2)
    plt.axis("off")
    plt.imshow(wc2)
    plt.show()
    #plt2.imshow(wc2, interpolation="bilinear")
    #plt2.axis("off")
    #plt2.show()

log_file=open('whoTwitts.log','w')
lindex=1

d = path.dirname(__file__)

text = open(path.join(d, 'Rouhani_Twitts.txt'),encoding="utf-8")
text = text.read()
log("Openning first text file for reading...")

text2=open(path.join(d, 'Twitts_About_Rouhani.txt'),encoding="utf-8")
text2=text2.read()
log("Openning Second text file for reading...")
#print(text)
makeImage(getFrequencyDictForText(getNormalizedText(text)),getFrequencyDictForText(getNormalizedText(text2)))


#makeImage(getFrequencyDictForText(getNormalizedText(text2)))

###



###

#5.log in the log.txt file


#6.upload in github
