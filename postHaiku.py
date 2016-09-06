import pymongo
import iPoet2
import random
host="localhost"
client = pymongo.MongoClient(host, 27017)
db = client.social
userCollection = db.fb_users
postsCollection = db.fb_posts
groupsCollection = db.fb_groups

stroka1=[]
stroka2=[]
stroka3=[]

def searchPhrases(filter):
    global client
    global db
    global postsCollection
    cursor = postsCollection.find({})
    localCount = 0
    i=0
    result=[]
    for post in cursor:
        i=i+1
        try:
            postText=post["text"]
            list=iPoet2.stringTokenizer(postText, ".!?'\"")
            for sentense in list:
                #print (">>",sentense)
                phrase=iPoet2.filterPhrase(sentense, filter)
                if phrase!=[]: result.append(phrase)
        except Exception as e:
            a=True
            #print ("exception:"+str(e))

    return result

def duplicate(original):
    lines=[]
    for sentence in original:

        scheme=iPoet2.sentenceScheme(sentence)
        line=searchPhrases(scheme)
        print (sentence, scheme,line)
        lines.append(line)
    return lines


# phrases_5_1=searchPhrases("u-u-u u-u")
# phrases_5_2=searchPhrases("u-u u-u-u")
# phrases_5_3=searchPhrases("u-u-u-u-u")
# phrases_5=phrases_5_1+phrases_5_2+phrases_5_3
#
# print("u-u-u u-u",phrases_5_1)
# print("u-u u-u-u",phrases_5_2)
# print("u-u-u-u-u",phrases_5_3)
#
# phrases_7_1=searchPhrases("u-u-u-u u-u-u")
# phrases_7_2=searchPhrases("u-u-u-u-u-u-u")
# phrases_7_3=searchPhrases("u-u u-u-u-u-u")
# phrases_7_4=searchPhrases("u-u-u-u-u u-u")
# phrases_7_5=searchPhrases("u u-u-u-u-u-u")
# phrases_7=phrases_7_5+phrases_7_1+phrases_7_2+phrases_7_3+phrases_7_4
# print(phrases_7_1)
# print(phrases_7_2)
# print(phrases_7_3)
#
# # ph5_1=phrases_5_1[ random.randint(0, len(phrases_5_1))]
# # ph7=phrases_7_1[ random.randint(0, len(phrases_7_1))]
# # ph5_2=phrases_5_2[ random.randint(0, len(phrases_5_2))]
# for i in range(100):
#     ph5A=phrases_5[ random.randint(0, len(phrases_5))]
#     ph7=phrases_7[ random.randint(0, len(phrases_7))]
#     ph5B=phrases_5[ random.randint(0, len(phrases_5))]
#     print (ph5A)
#     print (ph7)
#     print (ph5B)
#     print("-------------------")

# lermontov=["Моя душа, я помню, с детских лет",
#     "Чудесного искала. Я любил",
#     "Все обольщенья света, но не свет,",
#     "В котором я минутами лишь жил;",
#     "И те мгновенья были мук полны,",
#     "И населял таинственные сны",
#     "Я этими мгновеньями. Но сон",
#     "Как мир не мог быть ими омрачен.",]
#
# lines=duplicate(lermontov)
# print(lines)


def loadPhrases(text,filter):
    lines=iPoet2.stringTokenizer(text, ",!..?\r\n\"'")
    result=[]
    for sentence in lines:
        print(">>>",sentence)
        phrase=iPoet2.filterPhrase(sentence, filter)
        if phrase!=[]:   result.append(phrase)
    return result


seasonText=iPoet2.readFromFile("leto.txt")
phrases=loadPhrases(seasonText,"u-u-u u-u")
phrases=phrases+loadPhrases(seasonText,"u-u u-u-u")
phrases=phrases+loadPhrases(seasonText,"u-u-u-u-u")

# print("u-u-u u-u",phrases_5_1)
# print("u-u u-u-u",phrases_5_2)
# print("u-u-u-u-u",phrases_5_3)

print (phrases)

