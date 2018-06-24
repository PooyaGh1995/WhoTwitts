
from os import system
from os import path

tarafdar_text = open('tarafdar.txt', 'r').read()
montaged_text = open('montaged.txt', 'r').read()
tarafdar_words = getFrequencyDictForText(getNormalizedText(tarafdar_text)
montaged_words = getFrequencyDictForText(getNormalizedText(montaged_text)

def getNormalizedText(txt):
    normalizer=Normalizer()
    return normalizer.normalize(txt)

#3.generate word frequency dictionary using multidict (skip "az" "be" "ra" va.... words)

def getFrequencyDictForText(sentence):
    fullTermsDict = multidict.MultiDict()
    tmpDict = {}
    arr=[]
    rfile=open('results.txt','a')
    rfile.write("------ word frequencies of file -------\n")
    # making dict for counting frequencies
    #for text in sentence.split(" "):
    i=1
    j=0

    for w in word_tokenize(sentence):


        if re.match("\.|و|از|که|را|برای|با|به|تا|،|در|بر|برای|؟|؛|است|#|https|//t|این|رو|تو|من|یک|یکی|هم|یه|نیست|بود|آن|این|:|شما|هر|«|»|!|اون|داره|شد|چه|یا|کردن|اگر|بی|اگه|-|بعد|اما|پس|شده|شد|کنید|نه|چرا|چی|دیدن|کنه|میکنه|کی|زد|\(|\)|ما|\.\.\.|\…|امروز|الان|فقط|خیلی|حالا|چون|مثل|@\w*|کرد|میکنن|کنن|دیگه",w):

            #print(str(i))
            i=i+1
            continue
        val = tmpDict.get(w,0)
        tmpDict[w.lower()] = val+1

        sorted_values=sorted(tmpDict.values(),reverse=True)
        sorted_keys=sorted(tmpDict,key=tmpDict.__getitem__,reverse=True)

    for key in tmpDict:

        print(key)
        try:
            key2=str(get_display(arabic_reshaper.reshape(str(key))))
        except:
            key2=key
        #key=get_display(key)

        fullTermsDict.add(key2,tmpDict[key])
        arr.append(key2)
        #rfile.write("%s: " % str(key))
        #rfile.write("%s\n" % str(tmpDict[key]))

        rfile.write("%s: " % str(sorted_keys[j]))
        rfile.write("%s\n" % str(sorted_values[j]))
        j=j+1
    #return fullTermsDict
    return arr


montaged_tweets = []
for i in range(len(montaged_words)/60):
    montaged_tweets.append(' '.join(montaged_words[60 * i:60* i + 60]))

tarafdar_tweets = []
for i in range(len(tarafdar_words)/60):
    tarafdar_tweets.append(' '.join(tarafdar_words[60 * i:60* i + 60]))

country = ['کشور'.decode('utf-8'),'ایران'.decode('utf-8')]
people = ['ملت'.decode('utf-8'),'جامعه'.decode('utf-8'),'مردم'.decode('utf-8')]
female = ['زن'.decode('utf-8'),'زنان'.decode('utf-8'),'خانوم'.decode('utf-8'), 'دختر'.decode('utf-8'),
         'دختران'.decode('utf-8')]
economic = ['دلار'.decode('utf-8'), 'ریال'.decode('utf-8'), 'ارز'.decode('utf-8'), 'گرانی'.decode('utf-8')]
government = ['دولت'.decode('utf-8'), 'روحانی'.decode('utf-8'), 'وزیر'.decode('utf-8'), 'رییس'.decode('utf-8')
             , 'جمهور'.decode('utf-8')]
leadership = ['رهبر'.decode('utf-8'), 'رهبری'.decode('utf-8'), 'ولایت'.decode('utf-8')]
foregin_policy = ['اسراییل'.decode('utf-8'), 'اسرائیل'.decode('utf-8'), 'فلسطین'.decode('utf-8')
                 , 'سوریه'.decode('utf-8'),  'لبنان'.decode('utf-8'), 'آمریکا'.decode('utf-8'), 'ترامپ'.decode('utf-8')]



os.system("bin/mallet import-file --input /home/pooya/Desktop/mallet_result.txt --output labeled_mallet")
