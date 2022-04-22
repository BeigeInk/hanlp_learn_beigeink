from pyhanlp import *
import zipfile,os,sys,re

#pyuic5 -o ui.py untitled.ui
## 指定 PKU 语料库
PKU98=r'E:\Anaconda\envs\py36\lib\site-packages\pyhanlp\static\data\test\pku98'
PKU199801 = os.path.join(PKU98, '199801.txt')
PKU199801_TRAIN = os.path.join(PKU98, '199801-train.txt')
PKU199801_TEST = os.path.join(PKU98, '199801-test.txt')
POS_MODEL = os.path.join(PKU98, 'pos.bin')
NER_MODEL = os.path.join(PKU98, 'ner.bin')

## 以下开始 CRF 命名实体识别
temp_train=os.getcwd()+r'\train\new_del.txt'

CRFNERecognizer = JClass('com.hankcs.hanlp.model.crf.CRFNERecognizer')
HMMNERecognizer = JClass('com.hankcs.hanlp.model.hmm.HMMNERecognizer')
NERTrainer = JClass('com.hankcs.hanlp.model.perceptron.NERTrainer')
PerceptronNERecognizer = JClass('com.hankcs.hanlp.model.perceptron.PerceptronNERecognizer')


AbstractLexicalAnalyzer = JClass('com.hankcs.hanlp.tokenizer.lexical.AbstractLexicalAnalyzer')
Utility = JClass('com.hankcs.hanlp.model.perceptron.utility.Utility')
PerceptronSegmenter = JClass('com.hankcs.hanlp.model.perceptron.PerceptronSegmenter')
PerceptronPOSTagger = JClass('com.hankcs.hanlp.model.perceptron.PerceptronPOSTagger')

def train_and_test(model):
    anylizer=AbstractLexicalAnalyzer(PerceptronSegmenter(),PerceptronPOSTagger(),model)
    with open('whole.txt','r',encoding='utf-8') as f:
        whole_any=f.read()
        result=anylizer.analyze(whole_any)
        print('\n'.join(str(result).split('\n')[:20]))
        scores = Utility.evaluateNER(model, PKU199801_TEST)
        Utility.printNERScore(scores)
    return anylizer

def re_train(sent,anylyzer):
    while not anylyzer.analyze(sent.text()).equals(sentence):
        anylyzer.learn(sent)

def zip_result(model,filpath):
    anylizer=AbstractLexicalAnalyzer(PerceptronSegmenter(),PerceptronPOSTagger(),model)
    with open(filpath,'r',encoding='utf-8') as f:
        whole_any=f.read()
        result=anylizer.analyze(whole_any)
    return str(result)

def CRF_whole():
    CRF = CRFNERecognizer()
    return CRF

def HMM_whole():
    HMM = HMMNERecognizer()
    HMM.train(temp_train)
    return HMM

def NER_whole():
    NER_temp = NERTrainer()
    NER = PerceptronNERecognizer(NER_temp.train(temp_train, NER_MODEL).getModel())
    return NER

def nlp_model(modelname, input_path):
    print(modelname)
    if modelname==0:
        model=CRF_whole()
    elif modelname==1:
        model=HMM_whole()
    else:
        model=NER_whole()
    return zip_result(model,input_path)
