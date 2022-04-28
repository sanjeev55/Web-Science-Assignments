import pandas as pd
import numpy as np
import re
import math as m

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

text0 = readtext('Text_0.txt')
# print(text0)
text1 = readtext('Text_1.txt')
# print(text1)
text2 = readtext('Text_2.txt')
# print(text2)

#---------------Similarity using Jaccard Score------------------------
def get_shingle(size,f):

    for i in range (0,len(f)-size+1):
        yield tuple(f[i:i+size])


def jaccardCoefficient(shingle1, shingle2):

    jc = len(shingle1 & shingle2) / len(shingle1 | shingle2)

    return jc

# For 2 shingles part
shingles0 = { i for i in get_shingle(2,text0.split())}
# print(shingles0)
shingles1 = {i for i in get_shingle(2, text1.split())}
# print(shingles1)
shingles2 = {i for i in get_shingle(2, text2.split())}
# print(shingles2)

Similarity01 = jaccardCoefficient(shingles0, shingles1)
print("Similarity between text0 and text1 using Jaccard Coefficient:%s"%(round(Similarity01,5)))
Similarity02 = jaccardCoefficient(shingles0, shingles2)
print("Similarity between text0 and text2 using Jaccard Coefficient:%s"%(round(Similarity02,5)))
Similarity12 = jaccardCoefficient(shingles1, shingles2)
print("Similarity between text1 and text2 using Jaccard Coefficient:%s"%(round(Similarity12,5)))



#--------------Similarity using Cosine Similarity-------------------
corpus = [text0, text1, text2]

word_bag = sorted(set(text0.split()+text1.split()+text2.split()))
# calculating tf
def term_frequency(word_bag, corpus):
    data = {}
    for val in word_bag:
        corpusCount = 0
        list = []
        while corpusCount < corpus.__len__():
            tfd = corpus[corpusCount].split()
            tfdCount = 0

            for word in tfd:
                if val == word:
                    tfdCount = tfdCount + 1

            corpusCount = corpusCount + 1
            list.append(tfdCount)
            data.update({val: list})
    df = pd.DataFrame(data, index=corpus)
    return df

tf = term_frequency(word_bag, corpus)
print(tf)

# calculating df

def document_frequency(word_bag, corpus):
    data = {}

    for val in word_bag:
        docCount = 0
        corpusCount = 0

        while corpusCount < (corpus.__len__()):
            tfd = corpus[corpusCount].split()

            tfdCount = 0

            for word in tfd:
                if val == word:
                    docCount = docCount + 1
                    break

            corpusCount = corpusCount + 1
            data.update({val: docCount})
    return data

df = document_frequency(word_bag, corpus)
print(df)

# calculating tf-idf

def tfidf(tf,df,corpus):
    docCount = corpus.__len__()
    # print(docCount - 1)
    count = 0
    finalDf = {}


    while count < docCount:
        tfidfList = []
        for word in word_bag:
            dfVal = df[word]
            # print("document frequency of word %s:%s"%(word,dfVal))
            tfVAl = tf.iloc[count][word]

            # print("IDf of %s : %s"%(word, m.log10((docCount-1)/dfVal)))

            tfidfVal = tfVAl * m.log10((docCount)/dfVal)
            # print(tfidfVal)

            tfidfList.append(tfidfVal)
            # print(tfidfList)
            # print("Term Frequency of %s in d%s:%s"%(word,count, tfVAl))
        finalDf.update({'d'+str(count): tfidfList})
        # print(finalDf)


        count = count + 1
    df = pd.DataFrame(finalDf,index=word_bag)
    return df

weighted = tfidf(tf,df,corpus)
print(weighted)

def cosineSimilarity(t1,t2): #manually input the document number
    d = t1.array
    q = t2.array

    magnitudeD = np.linalg.norm(d)
    # print(magnitudeD)

    magnitudeQ = np.linalg.norm(q)
    # print(magnitudeQ)

    cosine = np.dot(d,q)/(magnitudeQ * magnitudeD)

    return cosine

cosineValue01 = cosineSimilarity(weighted['d0'],weighted['d1'])
cosineValue02 = cosineSimilarity(weighted['d0'],weighted['d2'])
cosineValue12 = cosineSimilarity(weighted['d1'],weighted['d2'])
# cosineValue02 = cosineSimilarity(text0,text2)
# cosineValue12 = cosineSimilarity(text1,text2)
print('Cosine Similarity of text0 and text1: %s'%round(cosineValue01,5))
print('Cosine Similarity of text0 and text2: %s'%round(cosineValue02,5))
print('Cosine Similarity of text1 and text2: %s'%round(cosineValue12,5))


#----------Similarity using Euclidean Distance---------------

def euclideanDistance(t1,t2):
    v1 = t1.array
    v2 = t2.array
    distance = np.linalg.norm(v2-v1)
    return distance

euclideanSimilarity01 = euclideanDistance(weighted['d0'],weighted['d1'])
print("Similarity of text0 and text1 using Euclidean Distance: %s"%(round(euclideanSimilarity01,5)))
euclideanSimilarity02 = euclideanDistance(weighted['d0'],weighted['d2'])
print("Similarity of text0 and text2 using Euclidean Distance: %s"%(round(euclideanSimilarity02,5)))
euclideanSimilarity12 = euclideanDistance(weighted['d1'],weighted['d2'])
print("Similarity of text1 and text2 using Euclidean Distance: %s"%(round(euclideanSimilarity12,5)))



#From the code above, we can observe that:
#According to Jaccard Score, Text 1 and Text 2 are most similar with the score of 0.02913
#According to Cosine Similarity, Text 1 and Text 2 are most similar with the score of 0.07387
#According to Euclidean Distance, Text 0 and Text 1 are most similar with the score of 9.40287