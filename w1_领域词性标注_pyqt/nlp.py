from pyhanlp import *
import zipfile,os,sys,re
from pyhanlp.static import download, remove_file, HANLP_DATA_PATH
#pyuic5 -o ui.py untitled.ui
## 指定 PKU 语料库
PKU98=r'E:\Anaconda\envs\py36\lib\site-packages\pyhanlp\static\data\test\pku98'
PKU199801 = os.path.join(PKU98, '199801.txt')
PKU199801_TRAIN = os.path.join(PKU98, '199801-train.txt')
PKU199801_TEST = os.path.join(PKU98, '199801-test.txt')
POS_MODEL = os.path.join(PKU98, 'pos.bin')
NER_MODEL = os.path.join(PKU98, 'ner.bin')

## 以下开始 CRF 命名实体识别

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

CRF=CRFNERecognizer()
print('CRF')
crf_any=train_and_test(CRF)

HMM=HMMNERecognizer()
HMM.train(PKU199801_TRAIN)
print('HMM')
hmm_any=train_and_test(HMM)

NER_temp=NERTrainer()

NER_temp=NERTrainer()
NER=PerceptronNERecognizer(NER_temp.train(PKU199801_TRAIN,NER_MODEL).getModel())
print('NER')
ner_any=train_and_test(NER)