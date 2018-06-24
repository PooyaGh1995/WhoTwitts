import os
import re
import string
import math
from hazm import *
import multidict as multidict

target_names = ['t', 'm']

class NB(object):

    def getNormalizedText(self,txt):
        normalizer=Normalizer()
        return normalizer.normalize(txt)

    def getFrequencyDictForText(self,sentence):
        fullTermsDict = multidict.MultiDict()
        tmpDict={}
        word_counts={}
        rfile=open('results.txt','a')
        rfile.write("------ word frequencies of file -------\n")
        i=1
        j=0

        for w in word_tokenize(sentence):
            if re.match("\.|و|از|که|را|برای|با|به|تا|،|در|بر|برای|؟|؛|است|#|https|//t|این|رو|تو|من|یک|یکی|هم|یه|نیست|بود|آن|این|:|شما|هر|«|»|!|اون|داره|شد|چه|یا|کردن|اگر|بی|اگه|-|بعد|اما|پس|شده|شد|کنید|نه|چرا|چی|دیدن|کنه|میکنه|کی|زد|\(|\)|ما|\.\.\.|\…|امروز|الان|فقط|خیلی|حالا|چون|مثل|@\w*|کرد|میکنن|کنن|دیگه",w):
                i=i+1
                continue
            val = tmpDict.get(w,0)
            tmpDict[w.lower()] = val+1
            sorted_values=sorted(tmpDict.values(),reverse=True)
            sorted_keys=sorted(tmpDict,key=tmpDict.__getitem__,reverse=True)

        for key in tmpDict:
            #print(key)
            try:
                key2=str(get_display(arabic_reshaper.reshape(str(key))))
            except:
                key2=key
            ### new approach
            word_counts[key2]=tmpDict[key]
            ### new approach
            fullTermsDict.add(key2,tmpDict[key])
            rfile.write("%s: " % str(sorted_keys[j]))
            rfile.write("%s\n" % str(sorted_values[j]))
            j=j+1
        #return fullTermsDict
        return word_counts

    def fit(self, X, Y):

        self.log_class_priors = {}
        self.word_counts = {}
        self.vocab = set()

        n = len(X)
        self.log_class_priors['m'] = math.log(sum(1 for label in Y if label == 1) / n)
        self.log_class_priors['t'] = math.log(sum(1 for label in Y if label == 0) / n)
        self.word_counts['m'] = {}
        self.word_counts['t'] = {}

        for x, y in zip(X, Y):
            c = 'm' if y == 1 else 't'
            #counts = self.get_word_counts(self.tokenize(x))
            counts=self.getFrequencyDictForText(self.getNormalizedText(x))
            for word, count in counts.items():
                if word not in self.vocab:
                    self.vocab.add(word)
                if word not in self.word_counts[c]:
                    self.word_counts[c][word] = 0.0

                self.word_counts[c][word] += count

    def predict(self, X):
        result = []
        for x in X:
            counts=self.getFrequencyDictForText(self.getNormalizedText(x))
            m_score = 0
            t_score = 0
            for word, _ in counts.items():
                if word not in self.vocab: continue


                log_w_given_m = math.log( (self.word_counts['m'].get(word, 0.0000001) ) / (sum(self.word_counts['m'].values()) ) )
                log_w_given_t = math.log( (self.word_counts['t'].get(word, 0.0000001) ) / (sum(self.word_counts['t'].values()) ) )

                m_score += log_w_given_m
                t_score += log_w_given_t

            m_score += self.log_class_priors['m']
            t_score += self.log_class_priors['t']


            if m_score > t_score:
                result.append(1)
            else:
                result.append(0)
        return result

if __name__=='__main__':
    X=[]
    y=[]
    T=[]
    with open("Montaged.txt") as f:
        X.append(f.read())
    with open("Tarafdar.txt") as f:
        X.append(f.read())
    with open("test.txt") as f:
        T.append(f.read())
    y=[1,0]
    nb=NB()
    nb.fit(X,y)
    r=nb.predict(T)
    print(r)
    if(r[0]==0):
        print("tweet in /test.txt file seems to belong to --Tarafdar-- class!")
    else:
        print("tweet in /test.txt file seems to belong to --Montaghed-- class!")
