# -*- coding: utf-8 -*-

#Just For Test
def loadDataSet():
    #return [ [ 1, 3, 4 ], [ 2, 3, 5 ], [ 1, 2, 3, 5 ], [ 2, 5 ] ]
    #return [['t1', 'a1', 'a3', 'a4', 'a5', 'a6'],['t2', 'a2'],['t1', 'a3', 'a4', 'a5', 'a6'],['t3', 'a1', 'a3', 'a5', 'a6']]
    return [['temperature_1', 'lumbar_pain'], ['fever', 'symptom_1', 'symptom_2', 'symptom_3', 'symptom_5'], ['symptom_3', 'symptom_4', 'symptom_1', 'symptom_2'], ['fever', 'symptom_1']]


def createC1(dataSet):#产生单个item的集合
    '''
    构建初始候选项集的列表，即所有候选项集只包含一个元素，
    C1是大小为1的所有候选项集的集合
    '''
    C1=[]
    for transaction in dataSet:
        for item in transaction: 
            if not [item] in C1:
                C1.append([item])
    
    C1.sort()
    
    return map(frozenset,C1)#给C1.list每个元素执行函数
    
    
def scanD(D,ck,minSupport):#dataset,a list of candidate set,最小支持率
    '''
    计算Ck中的项集在数据集合D(记录或者transactions)中的支持度,
    返回满足最小支持度的项集的集合，和所有项集支持度信息的字典。
    '''
    ssCnt={}
    for tid in D:
        # 对于每一条transaction
        for can in ck:
            # 对于每一个候选项集can，检查是否是transaction的一部分
            # 即该候选can是否得到transaction的支持
            if can.issubset(tid):
                if not ssCnt.has_key(can):
                    ssCnt[can]=1
                else: ssCnt[can]+=1
    
    numItem=float(len(D))
    retList=[]
    supportData={}
    for key in ssCnt:
        # 每个项集的支持度
        support=ssCnt[key]/numItem
        # 将满足最小支持度的项集，加入retList
        if support>=minSupport:
            retList.insert(0,key)
            # 汇总支持度数据
            supportData[key]=support
            
    return retList,supportData#返回频繁k项集，相应支持度
        

def aprioriGen(Lk,k):#create ck(k项集)
    '''
    由初始候选项集的集合Lk生成新的生成候选项集，
    k表示生成的新项集中所含有的元素个数
    '''
    retList=[]
    lenLk=len(Lk)
    for i in range(lenLk):
        for j in range(i+1,lenLk):
            L1=list(Lk[i])[:k-2];L2=list(Lk[j])[:k-2]
            L1.sort();L2.sort()#排序
            if L1==L2:#比较i,j前k-1个项若相同，和合并它俩
                retList.append(Lk[i] | Lk[j])#加入新的k项集 | stanf for union
    return retList
    
    
def apriori(dataSet,minSupport=0.5):
    # 构建初始候选项集C1
    C1=createC1(dataSet)
    # 将dataSet集合化，以满足scanD的格式要求
    D=map(set,dataSet)
    # 构建初始的频繁项集，即所有项集只有一个元素
    L1,supportData=scanD(D,C1,minSupport)#利用k项集生成频繁k项集（即满足最小支持率的k项集）
    L=[L1]#L保存所有频繁项集
    
    # 最初的L1中的每个项集含有一个元素，新生成的
    # 项集应该含有2个元素，所以 k=2
    k=2
    while(len(L[k-2])>0):#直到频繁k-1项集为空
        Ck=aprioriGen(L[k-2],k)#利用频繁k-1项集 生成k项集
        Lk,supK= scanD(D,Ck,minSupport)
        # 将新的项集的支持度数据加入原来的总支持度字典中
        supportData.update(supK)#保存新的频繁项集与其支持度
        # 将符合最小支持度要求的项集加入L
        L.append(Lk)#保存频繁k项集
        # 新生成的项集中的元素个数应不断增加
        k+=1
    # 返回所有满足条件的频繁项集的列表，和所有候选项集的支持度信息
    return L,supportData#返回所有频繁项集，与其相应的支持率
        
    
def calcConf(freqSet,H,supportData,brl,minConf=0.7):
    '''
    计算规则的可信度，返回满足最小可信度的规则。
    
    freqSet(frozenset):频繁项集
    H(frozenset):频繁项集中所有的元素
    supportData(dic):频繁项集中所有元素的支持度
    brl(tuple):满足可信度条件的关联规则
    minConf(float):最小可信度
    '''
    prunedH=[]
    for conseq in H:#后件中的每个元素
        #print('freqSet', freqSet, 'conseq', conseq, 'freqSet-conseq', freqSet-conseq, 'conseq-freqSet',conseq-freqSet)
        conf = supportData[freqSet]/supportData[freqSet-conseq]
        lift = supportData[freqSet]/(supportData[freqSet-conseq] * supportData[conseq])
        if conf>=minConf:
            print freqSet-conseq,'-->',conseq, 'support:', supportData[freqSet], 'conf:',conf,'lift:',lift
            brl.append((freqSet-conseq,conseq,supportData[freqSet],conf,lift))#添加入规则集中
            prunedH.append(conseq)#添加入被修剪过的H中
        
    return prunedH

def rulesFromConseq(freqSet,H,supportData,brl,minConf=0.7):
    '''
    对频繁项集中元素超过2的项集进行合并。
    
    freqSet(frozenset):频繁项集
    H(frozenset):频繁项集中的所有元素，即可以出现在规则右部的元素
    supportData(dict):所有项集的支持度信息
    brl(tuple):生成的规则
    
    '''
    m=len(H[0])#H是一系列后件长度相同的规则，所以取H0的长度即可
    # 查看频繁项集是否大到移除大小为 m　的子集
    if (len(freqSet)>m+1):
        Hmp1=aprioriGen(H,m+1)
        Hmp1=calcConf(freqSet,Hmp1,supportData,brl,minConf)
        # 如果不止一条规则满足要求，进一步递归合并
        if (len(Hmp1)>1):
            rulesFromConseq(freqSet,Hmp1,supportData,brl,minConf)
            
def generateRules(L,supportData,minConf=0.7):
    '''
    根据频繁项集和最小可信度生成规则。
    
    L(list):存储频繁项集
    supportData(dict):存储着所有项集（不仅仅是频繁项集）的支持度
    minConf(float):最小可信度
    '''
    bigRuleList=[]#存储规则
    for i in range(1,len(L)):
        for freqSet in L[i]:
            # 对于每一个频繁项集的集合freqSet
            H1=[frozenset([item]) for item in freqSet]
            # 如果频繁项集中的元素个数大于2，需要进一步合并
            if(i>1):
                rulesFromConseq(freqSet,H1,supportData,bigRuleList,minConf)
            else:
                calcConf(freqSet,H1,supportData,bigRuleList,minConf)
    return bigRuleList
