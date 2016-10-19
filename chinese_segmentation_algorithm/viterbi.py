# -*- coding:  utf-8 -*
"""
This module is used to ....
Authors: shiduo
 
"""
import re
import pickle
import time
PrevStatus = {
    'B': 'ES',
    'M': 'MB',
    'S': 'SE',
    'E': 'BM'
}
MIN = -3.14e100

re_flag = re.compile(u"[。；，：“”‘’（）、？《》]")

def calc_label_term(word,word_dict,flag):
    word_prob={}
    if 'B' in flag:
        word_prob['B'] =  word_dict['B'].get(word,0.0)
    else:
        word_prob['B'] = 0.0
    if 'M' in flag:
        word_prob['M'] = word_dict['M'].get(word,0.0)
    else:
        word_prob['M'] = 0.0
    if 'E' in flag:
        word_prob['E'] = word_dict['E'].get(word,0.0)
    else:
        word_prob['E'] = 0.0
    if 'S' in flag:
        word_prob['S'] = word_dict['S'].get(word,0.0)
    else:
        word_prob['S'] = 0.0
    return word_prob

def calc_start(word_prob, label_start):
    value_dict = {'B':MIN,'M':MIN,'E':MIN,'S':MIN}
    max_word_type = ''
    max_word_prob = MIN
    for key in "BS":
        tmp_prob = word_prob[key]+label_start[key]
        if tmp_prob > max_word_prob:
            max_word_prob = tmp_prob
            max_word_type = key
        value_dict[key] = tmp_prob
    return max_word_type,max_word_prob,value_dict

def strange_word(word, word_dict):
    if word_dict['B'].get(word):
        return False
    if word_dict['M'].get(word):
        return False
    if word_dict['E'].get(word):
        return False
    if word_dict['S'].get(word):
        return False
    return True

def calc_first_type(word,word_dict,label_start):
    flag = "BMES"
    word_prob = calc_label_term(word,word_dict,flag)
    max_word_type,max_word_prob,value_dict = calc_start(word_prob, label_start)
    
    return max_word_type,value_dict

def calc_second_type(word, label_old_type, word_dict,label_dict,value_dict):
#     print word
#     print value_dict
    second_value_dict = {'B':MIN,'M':MIN,'E':MIN,'S':MIN}
    """
    'B': 'ES',
    'M': 'MB',
    'S': 'SE',
    'E': 'BM'
    """
    flag = "BMES"
    word_prob = calc_label_term(word,word_dict,flag)
    max_label_prob2 = MIN
    max_label_tpye = ''
    for key1 in flag:
        max_label_prob1 = MIN
        for key2 in PrevStatus[key1]:
            tmp_prob = value_dict[key2] + label_dict[key2][key1]  
            if tmp_prob > max_label_prob1:
                max_label_prob1 = tmp_prob  
#             print key2,key1,tmp_prob,max_label_prob1
        second_value_dict[key1] = max_label_prob1 + word_prob[key1]
#         print key1,second_value_dict[key1],word_prob[key1]
        if second_value_dict[key1] > max_label_prob2:
            max_label_prob2 = second_value_dict[key1]
            max_label_tpye = key1
#     print max_label_tpye,label_old_type,PrevStatus[max_label_tpye]
    if label_old_type not in PrevStatus[max_label_tpye]:
        second_value_dict = {'B':MIN,'M':MIN,'E':MIN,'S':MIN}
        max_label_prob1 = MIN
        for key in label_dict[label_old_type]:
            tmp_prob = value_dict[label_old_type] + label_dict[label_old_type][key] + word_prob[key]
            second_value_dict[key] = tmp_prob
            if tmp_prob > max_label_prob1:
                max_label_prob1 = tmp_prob
                max_label_tpye = key
#     print second_value_dict
    return max_label_tpye,second_value_dict

def viterbi(label_start,word_dict, label_dict, test_sentences,code_style):
    sentences_len = len(test_sentences)
    label_name_list = []
    for i in range(sentences_len):
        word = test_sentences[i]
#         print_word_value(word, word_dict)
        if i==0:
            new_label_type, value_dict = calc_first_type(word,word_dict,\
                                                         label_start)
            label_name_list.append(new_label_type)
            label_type = new_label_type
            continue
        new_label_type,second_value_dict = calc_second_type(word,label_type, word_dict, \
                                          label_dict,value_dict)
        label_name_list.append(new_label_type)    
        value_dict = second_value_dict
        label_type = new_label_type
#     print label_name_list
    return label_name_list
def search_DAG(sen,d_dict):  
#         sen = unicode(sen,code_style)
        p = d_dict
        sen = sen.strip()  
        result=[]
        append=result.append
        passid=0
        total = len(sen)
        unknow = ''
        unknowlist = []
        sen_xrange=xrange(total)
        for i in sen_xrange:
            if i<passid:
                continue
            try:
                c=sen[i]
                y=p[c]
            except KeyError:
                append('U')
#                 print i
                unknow = unknow+str(i)+'/'
                continue
            for item in y:
                x, x_len = item
                
                if i+x_len <= total and x == sen[i:i+x_len]:
                    if unknow !='':
                        unknowlist.append(unknow[:len(unknow)-1])
                        unknow = ''
                    if x_len ==1 :
                        append('S')
                    elif x_len ==2 :
                        append('B')
                        append('E')
                    elif x_len >=3:
                        append('B')
                        for n in xrange(x_len-2):
                            append('M')
                        append('E')
                    passid=i+x_len
                    break
#             if passid == total:
#                 return ','.join(result)
        if unknow !='':
            unknowlist.append(unknow[:len(unknow)-1])
            unknow = ''
#         print result
        return result,unknowlist
def mycut(label_start,word_dict, label_dict, d_dict,test_sentences, code_style):
    test_sentences = unicode(test_sentences,code_style)
    label_name_list = ['S' for x in test_sentences]
#     print label_name_list
#     label_name_list =  viterbi(label_start, word_dict, label_dict, test_sentences, code_style)
    
    subulines = re_flag.split(test_sentences)
    total = 0
    for uline in subulines:
        unline_len = len(uline)
        if unline_len == 0 :
            total+=1
            continue
        s = total
        e = total + unline_len
        tmp,unknowlist = search_DAG(uline,d_dict)
#         print s,e,tmp
#         if True:
        if 'U' not in tmp and len(unknowlist)==0:
#             print label_name_list
            label_name_list[s:e] =  tmp
            total += unline_len+1
#             print label_name_list
            continue
#         print unknowlist
        for unknow in unknowlist:
            fidlist = unknow.split('/')
#             print fidlist
            strr = ''
            for fid in fidlist:
                strr += uline[int(fid)]
            s_u = int(fidlist[0])
            
            e_u = int(fidlist[len(fidlist)-1])
            strr_tmp = viterbi(label_start, word_dict, label_dict, strr, code_style)
#             print tmp
#             print s_u,e_u
#             print strr_tmp
            tmp[s_u:e_u+1] = strr_tmp
#             print tmp
        label_name_list[s:e] =  tmp
        total += unline_len+1
#     print label_name_list
    splited_sentences = sentence_split(test_sentences,label_name_list ,code_style)
    return splited_sentences
def print_word_value(word, word_dict):
    print word,
    print 'B',word_dict['B'].get(word,1),
    print 'M',word_dict['M'].get(word,1),
    print 'E',word_dict['E'].get(word,1),
    print 'S',word_dict['S'].get(word,1)
def sentence_split(test_sentences,result_list, code_style):
    result_len = len(result_list)
    splited_sentences = ""
    for i in range(result_len):
#         print i,test_sentences[i]
        if (result_list[i] == 'E' or result_list[i] == 'S' ) and test_sentences[i]!=u'。':
            splited_sentences += test_sentences[i]+'  '
        else:
            splited_sentences += test_sentences[i]
    return splited_sentences
if __name__ == '__main__':
    
    start = time.time()
    with open('../train_dict.pickle', 'r') as f:
        word_dict = pickle.load(f)
        label_dict = pickle.load(f)
        label_start = pickle.load(f)
        d_dict = pickle.load(f)
    code_style = 'utf8'
#     print d_dict[u'魑']
#     print d_dict[u'海']
#     for item in d_dict[u'大']:
#         print item[0],item[1]
#     test_sentences = u'魑魑魑魑希腊的魑魑魑魑经济结构较特殊魑魑魑魑。'.encode('utf8')
#     test_sentences = u'希腊的经济结构较特殊。'.encode('utf8')
    test_sentences =  u'海运业雄踞全球之首，按吨位计占世界总数的１７％。'.encode('utf8')
#     test_sentences = u'他来到中国，成为第一个访华的大船主。'.encode('utf8')
    recognized = mycut(label_start,word_dict, label_dict, d_dict,test_sentences, code_style)
    print recognized
    end = time.time()
    print 'time:',end-start
#     print u"挫折  多  了  ，  不能  正确  对待  ，  久而久之  ，  便  容易  心灰意懒  ，  一蹶不振  。".encode('utf8')
    
#     label_start = prob_start.P
#     label_dict = prob_trans.P
#     word_dict = prob_emit.P
#     test_sentences = u'挫折多了，不能正确对待，久而久之，便容易心灰意懒，一蹶不振。'.encode('utf8')
#     recognized = mycut(label_start,word_dict, label_dict, test_sentences, code_style)
#     print recognized
