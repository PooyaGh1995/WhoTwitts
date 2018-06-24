import os
import numpy as np
import re
from sklearn.datasets import load_files
from sklearn.metrics import accuracy_score, roc_auc_score
from hazm import *
import multidict as multidict

# Read the train Data
path_to_tweets = os.path.expanduser('/home/pooya/Desktop/twitter/')
tweets_train = load_files(os.path.join(path_to_tweets, 'train'), encoding="UTF-8")
text_train, y_train = tweets_train.data, tweets_train.target

#f1=open("Montaged.txt")
#f1=f1.read()
#f2=open("Tarafdar.txt")
#f2=f2.read()
#train=[]
#train.append(f1)
#train.append(f2)
#train_labels=[1,0]
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


def to_vw_format(document, label=None):
    #t=""
    #for w in getFrequencyDictForText(getNormalizedText(document)):
    #    t=t+w+" "
    #t=t+str(label or '') + ' |text ' + ' '.join(w)+'\n'
    #print(t)
    #return t
    return str(label or '') + ' |text ' + ' '.join(re.findall('\w{3,}', document.lower())) + '\n'
    #return str(label or '') + ' |text ' + ' '.join()
    #
    #return str(label or '') + ' |text ' + ' '.join(re.findall('\w{3,}', document.lower())) + '\n'
#to_vw_format(str(text_train[1]), 1 if y_train[0] == 1 else -1)

# Splitting train data to train and validation sets
train_size = int(0.7 * len(text_train))
train, train_labels = text_train[:train_size], y_train[:train_size]
valid, valid_labels = text_train[train_size:], y_train[train_size:]
#valid=[]
#valid_labels=[1]
#with open("test.txt") as f:
#    f=f.read()
#    valid.append(f)
# Convert and save in vowpal wabbit format
with open('whotwitts_train.vw', 'w') as vw_train_data:
    for text, target in zip(train, train_labels):
        vw_train_data.write(to_vw_format(str(text), 1 if target == 1 else -1))
with open('whotwitts_valid.vw', 'w') as vw_train_data:
    for text, target in zip(valid, valid_labels):
        vw_train_data.write(to_vw_format(str(text), 1 if target == 1 else -1))

os.system("vw -d whotwitts_train.vw --loss_function logistic -f whotwitts_model.vw")
os.system("vw -i whotwitts_model.vw -t -d whotwitts_valid.vw -p whotwitts_valid_pred.txt --quiet")
os.system("vw -d whotwitts_train.vw --loss_function logistic --ngram 2 -f whotwitts_model_bigram.vw --quiet")
os.system("vw -d whotwitts_train.vw --loss_function logistic --ngram 2 --invert_hash whotwitts_readable_model_bigram.vw")
os.system("vw -i whotwitts_model_bigram.vw -t -d whotwitts_valid.vw -p whotwitts_valid_pred_bigram.txt --quiet")
os.system("vw -d whotwitts_train.vw --loss_function logistic --ngram 3 -f whotwitts_model_thgram.vw --quiet")
os.system("vw -d whotwitts_train.vw --loss_function logistic --ngram 3 --invert_hash whotwitts_readable_model_thgram.vw")
os.system("vw -i whotwitts_model_thgram.vw -t -d whotwitts_valid.vw -p whotwitts_valid_pred_thgram.txt --quiet")
#!

with open('whotwitts_valid_pred.txt') as pred_file:
    valid_prediction = [float(label) for label in pred_file.readlines()]

with open('whotwitts_valid_pred_bigram.txt') as pred_file:
    valid_prediction_bigram = [float(label) for label in pred_file.readlines()]

with open('whotwitts_valid_pred_thgram.txt') as pred_file:
    valid_prediction_thgram = [float(label) for label in pred_file.readlines()]

#with open('whotwitts_valid.txt') as valid_file:
#    valid = [float(label) for label in valid_file.readlines()]

print("=============== 1 =================")
print("Accuracy: {}".format(round(accuracy_score(valid_labels, [int(pred_prob > 0) for pred_prob in valid_prediction]), 5)))
print("+++++++ precision and recall for 1-gram +++++++++")
# !head data/sentiment.te.pred
file = open("whotwitts_valid_pred_thgram.txt","r")
data = file.read()
ugly_arr = data.split('\n')
# print cc
predict_onegram_value = []
for i in ugly_arr:
    #if i in ['1','-1']:
    try:
        predict_onegram_value.append(float(i))
    except:
        print("invalid float: "+i)

#print(valid_labels)
# print predict_value
# for i in cc:
#     predict_value.append(int(i))
# 1 is reformist so p for reformist
#-1 is priciplist so n for principlist
print(predict_onegram_value[:10])
tp = 0
tn = 0
print(len(predict_onegram_value),len(valid_labels))
for i in range(len(predict_onegram_value)):
    if valid_labels[i] == 1:
        if predict_onegram_value[i] > 0:
            tp +=1
    else:
        if predict_onegram_value[i] < 0:
            tn +=1
fp = len(predict_onegram_value) - tp
fn = len(predict_onegram_value) - tn

print(tp,tn,fp,fn)

precision = float(tp) / (tp + fp)
recall = float(tp) / (tp + fn)
print("in 1-gram precision is {0} and recall is {1}".format(precision, recall))
print("=============== 2 =================")
print("Accuracy: {}".format(round(accuracy_score(valid_labels, [int(pred_prob > 0) for pred_prob in valid_prediction_bigram]), 5)))
print("+++++++ precision and recall for 2-gram +++++++++")
# !head data/sentiment.te.pred
file = open("whotwitts_valid_pred_thgram.txt","r")
data = file.read()
ugly_arr = data.split('\n')
# print cc
predict_bigram_value = []
for i in ugly_arr:
    #if i in ['1','-1']:
    try:
        predict_bigram_value.append(float(i))
    except:
        print("invalid float: "+i)

#print(valid_labels)
# print predict_value
# for i in cc:
#     predict_value.append(int(i))
# 1 is reformist so p for reformist
#-1 is priciplist so n for principlist
print(predict_bigram_value[:10])
tp = 0
tn = 0
print(len(predict_bigram_value),len(valid_labels))
for i in range(len(predict_bigram_value)):
    if valid_labels[i] == 1:
        if predict_bigram_value[i] > 0:
            tp +=1
    else:
        if predict_bigram_value[i] < 0:
            tn +=1
fp = len(predict_bigram_value) - tp
fn = len(predict_bigram_value) - tn

print(tp,tn,fp,fn)

precision = float(tp) / (tp + fp)
recall = float(tp) / (tp + fn)
print("in 2-gram precision is {0} and recall is {1}".format(precision, recall))
print("=============== 3 =================")
print("Accuracy: {}".format(round(accuracy_score(valid_labels, [int(pred_prob > 0) for pred_prob in valid_prediction_thgram]), 5)))
print("+++++++ precision and recall for 3-gram +++++++++")
# !head data/sentiment.te.pred
file = open("whotwitts_valid_pred_thgram.txt","r")
data = file.read()
ugly_arr = data.split('\n')
# print cc
predict_threegram_value = []
for i in ugly_arr:
    #if i in ['1','-1']:
    try:
        predict_threegram_value.append(float(i))
    except:
        print("invalid float: "+i)

#print(valid_labels)
# print predict_value
# for i in cc:
#     predict_value.append(int(i))
# 1 is reformist so p for reformist
#-1 is priciplist so n for principlist
print(predict_threegram_value[:10])
tp = 0
tn = 0
print(len(predict_threegram_value),len(valid_labels))
for i in range(len(predict_threegram_value)):
    if valid_labels[i] == 1:
        if predict_threegram_value[i] > 0:
            tp +=1
    else:
        if predict_threegram_value[i] < 0:
            tn +=1
fp = len(predict_threegram_value) - tp
fn = len(predict_threegram_value) - tn

print(tp,tn,fp,fn)

precision = float(tp) / (tp + fp)
recall = float(tp) / (tp + fn)
print("in 3-gram precision is {0} and recall is {1}".format(precision, recall))
