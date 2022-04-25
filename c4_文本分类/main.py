from pyhanlp import *
from pyhanlp.static import STATIC_ROOT, download
import os

def install_jar(name, url):
    dst = os.path.join(STATIC_ROOT, name)
    if os.path.isfile(dst):
        return dst
    download(url, dst)
    return dst

install_jar('text-classification-svm-1.0.2.jar', 'http://file.hankcs.com/bin/text-classification-svm-1.0.2.jar')
install_jar('liblinear-1.95.jar', 'http://file.hankcs.com/bin/liblinear-1.95.jar')

AbstractDataSet = JClass('com.hankcs.hanlp.classification.corpus.AbstractDataSet')
Document = JClass('com.hankcs.hanlp.classification.corpus.Document')
FileDataSet = JClass('com.hankcs.hanlp.classification.corpus.FileDataSet')
MemoryDataSet = JClass('com.hankcs.hanlp.classification.corpus.MemoryDataSet')
Evaluator = JClass('com.hankcs.hanlp.classification.statistics.evaluations.Evaluator')
IClassifier = JClass('com.hankcs.hanlp.classification.classifiers.IClassifier')
NaiveBayesClassifier = JClass('com.hankcs.hanlp.classification.classifiers.NaiveBayesClassifier')
LinearSVMClassifier = JClass('com.hankcs.hanlp.classification.classifiers.LinearSVMClassifier')
IDataSet = JClass('com.hankcs.hanlp.classification.corpus.IDataSet')
FMeasure = JClass('com.hankcs.hanlp.classification.statistics.evaluations.FMeasure')
BigramTokenizer = JClass('com.hankcs.hanlp.classification.tokenizers.BigramTokenizer')
HanLPTokenizer = JClass('com.hankcs.hanlp.classification.tokenizers.HanLPTokenizer')
ITokenizer = JClass('com.hankcs.hanlp.classification.tokenizers.ITokenizer')
IOUtil = SafeJClass('com.hankcs.hanlp.corpus.io.IOUtil')




def train_or_load_classifier_SVM():
    model_path = data_path + '.svm.ser'
    if os.path.isfile(model_path):
        return LinearSVMClassifier(IOUtil.readObjectFrom(model_path))
    classifier = LinearSVMClassifier()
    classifier.train(data_path)
    model = classifier.getModel()
    IOUtil.saveObjectTo(model, model_path)
    return LinearSVMClassifier(model)

def train_or_load_classifier_Bay():
    model_path = data_path + '.Bay.ser'
    if os.path.isfile(model_path):
        return NaiveBayesClassifier(IOUtil.readObjectFrom(model_path))
    classifier = NaiveBayesClassifier()
    classifier.train(data_path)
    model = classifier.getModel()
    IOUtil.saveObjectTo(model, model_path)
    return NaiveBayesClassifier(model)

def predict(classifier, text):
    print("《%16s》\t属于分类\t【%s】" % (text, classifier.classify(text)))
    # 如需获取离散型随机变量的分布，请使用predict接口
    print("《%16s》\t属于分类\t【%s】" % (text, classifier.predict(text)))

def evaluate(classifier, tokenizer):
    training_corpus = FileDataSet().setTokenizer(tokenizer).load(data_path, "UTF-8", 0.9)
    classifier.train(training_corpus)
    testing_corpus = MemoryDataSet(classifier.getModel()).load(data_path, "UTF-8", -0.1)
    result = Evaluator.evaluate(classifier, testing_corpus)
    print(classifier.getClass().getSimpleName() + "+" + tokenizer.getClass().getSimpleName())
    print(result)

data_path='spider/data'
classifier = train_or_load_classifier_Bay()
#classifier = train_or_load_classifier_SVM()
test_file=[i for i in os.walk('spider/test')]
class_test=test_file[0][1]
result_classi=dict()
for i in range(1,7):
    class_now=class_test[i-1]
    path_now=test_file[i][0]
    class_result=list()
    for j in test_file[i][2]:
        with open(os.path.join(path_now,j),'r',encoding='utf8') as f:
            text=f.read()
            class_result.append(classifier.classify(text))
    #print(class_result)
    temp_dict=dict()
    for j in class_test:
        temp_dict[j]=class_result.count(j)
    result_classi[class_now]=temp_dict

true_pre=0
whole_pre=0
for i in class_test:
    print(i,result_classi[i])
    true_pre+=result_classi[i][i]
    whole_pre+=sum(result_classi[i][j] for j in class_test)
    print('准确率',result_classi[i][i]/sum(result_classi[i][j] for j in class_test)*100)
print("总共准确率为",true_pre/whole_pre*100)

evaluate(NaiveBayesClassifier(), HanLPTokenizer())
evaluate(NaiveBayesClassifier(), BigramTokenizer())
evaluate(LinearSVMClassifier(), HanLPTokenizer())
evaluate(LinearSVMClassifier(), BigramTokenizer())