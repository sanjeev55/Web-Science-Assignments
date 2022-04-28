import pandas as pd
import numpy as np
import random
import re



def readtext(doc):

    characters = ".!@“”‘’()'{}[]\’≈|,;:β-?=α&"
    numbers = r'[0-9]'

    file = open(doc, encoding="utf8")

    #removing line spaces and changing every letter to lower case
    line = file.read().replace("\n","").lower()

    #removing punctuation
    for characters in characters:
        line = line.replace(characters, '')
    #removing numbers
    finalLine = re.sub(numbers,'', line)
    return finalLine

file = readtext('Text_sample.txt')

listWords = sorted(list(map(lambda c2: c2, file)))

corpus = [file]
#Character frequncy
def term_frequency(listWords, corpus):
    data = {}
    for val in listWords:
        corpusCount = 0
        list = []
        while corpusCount < corpus.__len__():
            tfd = listWords
            tfdCount = 0

            for word in tfd:
                if val == word:
                    tfdCount = tfdCount + 1

            corpusCount = corpusCount + 1
            list.append(tfdCount)
            data.update({val: list})
    df = pd.DataFrame(data)

    return df

tf = term_frequency(listWords, corpus)
generativeModel = tf.append(tf.div(tf.sum(axis=1), axis=0))

#Cumulative probabilities
sumList = []
cSum = 0
for val in generativeModel.iloc[1]:
    cSum = cSum + val
    sumList.append(cSum)

generativeModel.loc[len(generativeModel)]  = sumList
generativeModel.index = ['c(x)','p(x)','s(x)']
print(generativeModel)

generatedText = ''
count =0
while count <= 200:
    r = random.random()

#Finding x so that S(x) in the lowest value bigger than r
