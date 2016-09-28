#!/usr/bin/python
# -*- coding:  utf-8 -*
################################################################################
#
# Copyright (c) 2016 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
This module is used to ....
Authors: shiduo(shiduo@baidu.com)
Date:2016-5-26
"""
import jieba
import numpy
import scipy
import math
import scipy.linalg
import scipy.sparse
class LSI(object):
    """
    classdocs
    @Description: 
    @Param:
    textlist 是文本列表，每个元素是app的same
    @Def: 
    @Date: 2016-5-26
    """


    def __init__(self, textlist):
        """
        Constructor
        """
        self.textlist=textlist
        self.termlist=[]
        self.worddict=[]
        self.M,self.U, self.S, self.Vt=None,None,None,None
    def print_list_list(self,pythonlist):
        i=0
        for item in pythonlist:
            print str(i)+' '+','.join(item)
            i+=1
    def print_list(self,pythonlist):
        i=0
        for item in pythonlist:
            print str(i)+' '+item
            i+=1
    def get_terms(self):
        textlist=self.textlist
        for item in textlist:
            seg_list = jieba.cut_for_search(item)
            itemstr = ",".join(seg_list)
            term = itemstr.lower().split(',')
            self.termlist.append(term)
#         self.print_list_list(self.termlist)
    def TFIDF(self):  
        WordsPerDoc = numpy.sum(self.M, axis=0)#axis=0是按列求和
        DocsPerWord = numpy.sum(self.M, axis=1)  #axis=1是按行求和
        rows, cols = self.M.shape  
        for i in range(rows):  
            for j in range(cols):  
                self.M[i,j] = (self.M[i,j] /WordsPerDoc[j]) * math.log(float(cols) / DocsPerWord[i])  
    def set_matrix(self):
        n=len(self.textlist)
        termlist=self.termlist
        mtmplist=list(set([x for item in self.termlist for x in item]))
        self.worddict=mtmplist
        m=len(mtmplist)
        i=0
        word_id_list=[]
        for x in mtmplist:
            word_id_list.append((i,x))
#         self.print_list(mtmplist)
        tmp=numpy.zeros((m,n))
#         word_titleid_list=[]
        i=0
        for item in termlist:
#             itemlist=[]
            for word in item:
#                 tmptuple=(mtmplist.index(word),i)
#                 itemlist.append(tmptuple) 
                tmp[mtmplist.index(word)][i]=1
            i+=1
#             word_titleid_list.append(itemlist)
#         print word_titleid_list
#         print len(word_titleid_list)
        self.M = tmp
        self.TFIDF()
#         print self.M
    def calc_svd(self):
#         print self.M
        self.U, self.S, self.Vt = scipy.linalg.svd(self.M,full_matrices=False) 
        self.S=numpy.mat(numpy.eye(self.S.shape[0])*self.S)
#         print numpy.dot(numpy.dot(self.U,self.S),self.Vt)
         
    def query_vector(self,query):
        seg_list = jieba.cut_for_search(query)
        rows, cols = self.M.shape 
        tmp=numpy.zeros((rows,1)) 
        for item in seg_list:
            try:
                tmp[self.worddict.index(item)][0]=1
            except:
                continue
        tmp=numpy.dot(tmp.T,numpy.dot(self.U,numpy.linalg.inv(self.S)))
        
        m,n=self.Vt.shape
        relist=[]
        for i in range(n):
            v_v=numpy.mat(self.Vt[:,i])
            v_v=v_v.T
            num = float(tmp * v_v) #若为行向量则 A * B.T  
            denom = numpy.linalg.norm(tmp) * numpy.linalg.norm(v_v)  
            cos = num / denom #余弦值  
            relist.append((cos,i))
        relist.sort()
        sorted(relist,key=lambda x: (x[0], -x[1]))
        relist.reverse()
        simvalue,simindex=relist[0]
        print self.textlist[simindex], simvalue
if __name__ == '__main__':
    textlist=[u'美颜相机',u'美图秀秀',u'美人相机',u'小咖秀',u'in',u'秒拍',u'美咖相机',u'唯品会',u'小咖相机']
    lsi_model=LSI(textlist)
    lsi_model.get_terms()
    lsi_model.set_matrix()
    lsi_model.calc_svd()
    lsi_model.query_vector(u'秒拍HD')
