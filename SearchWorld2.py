import requests
from lxml import etree
#创建Vocabulary类
class Vocabulary:
    def __init__(self,name):
        self.name=name
        self.GenderAndMeaning=[]
        self.Sentences=[]
while True:
    #定义Vocabulary类
    word_name=input("想要搜索的词是?\n")
    word=Vocabulary(word_name)
    url='https://cn.bing.com/dict/'+word.name
    response=requests.get(url)
    html=response.text
    parse_html = etree.HTMLParser()
    tree=etree.fromstring(html,parse_html)
    #测试用
    #with open(word.name+".html","wt",encoding='utf-8') as fl:
    #    fl.write(html)
    
    #提取单词意思
    Meanings=tree.cssselect("body > div.contentPadding > div > div > div.lf_area > div > ul > li")
    for meaning in Meanings:
        mean=meaning.cssselect('span.def > span')[0]
        gender=meaning.cssselect('span.pos')[0]
        word.GenderAndMeaning.append([gender.text,mean.text])
    Sentences=tree.cssselect('#sentenceSeg > div.se_li')
    
    #提取句子
    for sen in Sentences:
        sentences=sen.cssselect("div.sen_en.b_regtxt > *")
        S=''
        for Letter in sentences:
            S=S+Letter.text
        word.Sentences.append(S)
    
    print("【word】"+word.name)
    line=[i[0]+'\t'+i[1] for i in word.GenderAndMeaning]
    print("\n".join(line))
    sentence=[str(i+1)+"."+word.Sentences[i] for i in range(len(word.Sentences))]
    print("\n".join(sentence))
    
    with open("Word.txt","at",encoding='utf-8') as f:
        f.write("【word】")
        f.write(word.name)
        f.write("\n")
        f.write("\n".join(line))
        f.write("\n")
        f.write("\n".join(sentence))
        f.write("\n")
    flag=input("Rerun?[y/n]\n")
    if flag=='n':
        break