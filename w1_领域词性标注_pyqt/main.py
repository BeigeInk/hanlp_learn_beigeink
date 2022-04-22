import sys,os,time,re
from PyQt5 import QtCore, QtGui, QtWidgets
from ui import *
from nlp_model import nlp_model
from model.run import BILSTM_CRF
import warnings
warnings.filterwarnings("ignore")

list_model=['条件随机场CRF','隐马尔可夫HMM','HanLP自带NER','BILSTM&CRF']

def cut_sent(para):
    para = re.sub('([。！？\?])([^”])',r"\1\n\2",para) # 单字符断句符
    para = re.sub('(\.{6})([^”])',r"\1\n\2",para) # 英文省略号
    para = re.sub('(\…{2})([^”])',r"\1\n\2",para) # 中文省略号
    para = re.sub('(”)','”\n',para)   # 把分句符\n放到双引号后，注意前面的几句都小心保留了双引号
    para = para.rstrip()       # 段尾如果有多余的\n就去掉它
    #很多规则中会考虑分号;，但是这里我把它忽略不计，破折号、英文双引号等同样忽略，需要的再做些简单调整即可。
    return para.split("\n")

class py_ui(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self,*args, obj=None, **kwargs):
        super(py_ui,self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.pushButton_2.clicked.connect(self.upload_file)
        self.list_w_ini()
        self.listWidget.clicked.connect(self.choice_model)
        self.pushButton_3.clicked.connect(self.save_path)
        self.resultpath=os.getcwd()+r'/save'
        self.lineEdit_ini()
        self.pushButton.clicked.connect(self.run_whole)
        self.model_choice_index=0

    #获取保存文件的路径+名字
    def get_whole_path(self):
        self.save_path_whole=self.resultpath
        line_e_text=self.lineEdit.text()
        if '.txt' in line_e_text:
            self.save_path_whole+='\\'+line_e_text
        else:
            self.save_path_whole+='\\'+line_e_text+'.txt'
       # print(self.save_path_whole)

    #展示并且保存
    def show_result(self,result_txt):
        self.textBrowser_2.clear()
        temp_show=cut_sent(result_txt)
        cnt = 0
        for i in temp_show:
            whole_show = i
            if whole_show == '\n' or whole_show == '' :
                continue
            self.textBrowser_2.append(whole_show)
            cnt += 1
            if cnt>=100:
                break
        self.textBrowser_2.moveCursor(self.textBrowser_2.textCursor().Start)
        with open(self.save_path_whole,'w',encoding='utf-8') as f:
            f.write(result_txt)

    #运行按钮行为
    def run_whole(self):
        self.get_whole_path()
        if self.model_choice_index<=2:
            result=nlp_model(self.model_choice_index,self.filename)
        else:
            result=BILSTM_CRF(self.filename)
        self.show_result(result)
        self.lineEdit_ini()

    #输入框初始化
    def lineEdit_ini(self):
        local_time = time.localtime(time.time())
        format_time = time.strftime("%Y%m%d_%H%M%S", local_time)
        #print(format_time)
        self.lineEdit.setText(QtCore.QCoreApplication.translate('MainWindow',format_time))

    #保存文件夹的路径
    def save_path(self):
        Dir_path=QtWidgets.QFileDialog.getExistingDirectory(self,
                                                       '选择文件夹','./')
        if Dir_path!='':
            self.resultpath=Dir_path
            self.label_6.setText((QtCore.QCoreApplication.translate("MainWindow",Dir_path)))

    #list weiget添加item
    def list_w_ini(self):
        for i in range(len(list_model)):
            item=QtWidgets.QListWidgetItem(list_model[i])
            self.listWidget.addItem(item)
    #上传训练文件
    def upload_file(self):
        filename = QtWidgets.QFileDialog.getOpenFileName(self,
                                                         "选择文件", "./data",
                                                         "Text(*.txt)")
        filepath=filename[0]
        if filepath=='':
            return
        _translate = QtCore.QCoreApplication.translate
        show_path=filepath.split('/')[-1]
        print(show_path)
        self.label_3.setText(_translate("MainWindow",show_path))
        self.filename=filepath
        self.show_ori_data()
    #展示原本数据
    def show_ori_data(self):
        self.textBrowser.clear()
        with open(self.filename,'r',encoding='utf-8') as f:
            data_whole=f.read()
        whole_show=cut_sent(data_whole)
        #print(whole_show)
        cnt = 0
        while cnt <= 100 and cnt<len(whole_show):
            if whole_show[cnt] == '\n' or whole_show[cnt] == '':
                cnt+=1
                continue
            self.textBrowser.append(whole_show[cnt])
            cnt += 1
           # print(cnt)
        self.textBrowser.moveCursor(self.textBrowser.textCursor().Start)

    #选择模型
    def choice_model(self):
        self.model_choice_index=self.listWidget.currentRow()

def main():
    myapp = QtWidgets.QApplication(sys.argv)
    mywin = py_ui()
    mywin.show()
    sys.exit(myapp.exec_())


if __name__ == '__main__':
    main()