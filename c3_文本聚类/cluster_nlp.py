from pyhanlp import *
import os
import random
ClusterAnalyzer = JClass('com.hankcs.hanlp.mining.cluster.ClusterAnalyzer')
analyzer = ClusterAnalyzer()

data_path='spider/data'
whole_file=[i for i in os.walk(data_path)]
class_cluster=whole_file[0][1]
for i in range(1,len(class_cluster)+1):
    for file_name in whole_file[i][2]:
        kind=class_cluster[i-1]
        whole_path=os.path.join(whole_file[i][0],file_name)
        analyzer.addDocument(kind+'_'+file_name[:-4],whole_path)

print('-'*30)
print('kmeans,六个簇')

result = analyzer.kmeans(6)

whole_result=list()
for i in range(len(result)):
    temp_class = [j[:2] for j in result[i]]
    list_temp=list()
    for j in class_cluster:
        list_temp.append([j,temp_class.count(j)])
    whole_result.append([i,list_temp])

print(analyzer.evaluate(data_path, "kmeans") * 100)

for i in whole_result:
    print('第'+str(i[0])+'个簇','聚类结果为',i[1])
    max_index1 = i[1].index(max(i[1], key=lambda x: x[1]))
    print('该簇中最多的类为',i[1][max_index1][0],'个数为',i[1][max_index1][1])


print('-'*30)
print('重复二分聚类 repeated bisectio,六个簇')


result = analyzer.repeatedBisection(6)

whole_result=list()
for i in range(len(result)):
    temp_class = [j[:2] for j in result[i]]
    list_temp=list()
    for j in class_cluster:
        list_temp.append([j,temp_class.count(j)])
    whole_result.append([i,list_temp])

print(analyzer.evaluate(data_path, "repeated bisection") * 100)

for i in whole_result:
    print('第'+str(i[0])+'个簇','聚类结果为',i[1])
    max_index1 = i[1].index(max(i[1], key=lambda x: x[1]))
    print('该簇中最多的类为',i[1][max_index1][0],'个数为',i[1][max_index1][1])
