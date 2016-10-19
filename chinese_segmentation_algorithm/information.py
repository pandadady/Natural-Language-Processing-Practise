# -*- coding:  utf-8 -*
"""
This module is used to ....
Authors: shiduo
"""
import math
import re
import pickle
re_flag = re.compile(u"[。；，：“”‘’（）、？《》]")
def suggest_freq(word, total):
        """
        Suggest word frequency to force the characters in a word to be
        joined or splitted.

        Parameter:
            - segment : The segments that the word is expected to be cut into,
                        If the word should be treated as a whole, use a str.
            - tune : If True, tune the word frequency.

        Note that HMM may affect the final result. If the result doesn't change,
        set HMM=False.
        """
#         ftotal = float(total)
        freq = 1
#         freq = max(int(freq * total) + 1, d_dict.get(word, 1))
        return freq
def create_DAG(d_dict,term,term_len,d_set):
    if term in d_set:
        return
    d_set.add(term)
    try:
        d_dict[term[0]].append((term,term_len))
    except:
        d_dict[term[0]] = []
        d_dict[term[0]].append((term,term_len))
def resort_DAG(d_dict):  
    for key in d_dict:
        d_dict[key].sort(key=lambda x:x[1])
        d_dict[key].reverse()     
def count_label(terms,label_dict,word_dict,label_start,label_all,d_dict,d_set):
    """
    label_dict = {}
    label_dict['B'] = {}
    label_dict['M'] = {}
    label_dict['E'] = {}
    label_dict['S'] = {}
    label_dict['ALL'] = {}
    P={'B': {'E': -0.510825623765990, 'M': -0.916290731874155},
    'E': {'B': -0.5897149736854513, 'S': -0.8085250474669937},
    'M': {'E': -0.33344856811948514, 'M': -1.2603623820268226},
    'S': {'B': -0.7211965654669841, 'S': -0.6658631448798212}}
    """
    line_len = len(terms) 
    for i in range(line_len):
        E_num = 0
        S_num = 0
        termi_len = len(terms[i])
        if termi_len == 0:
            continue
        create_DAG(d_dict,terms[i],termi_len,d_set)
#         if re_han.match(terms[i]):
        if termi_len == 1:
            label_all['S'] += 1
            S_num = 1 
            if i==0:
                label_start['S']+=1
        elif termi_len == 2:
            label_all['B'] += 1
            label_all['E'] += 1
            label_dict['B']['E'] += 1 #B->E
            E_num = 1
            if i==0:
                label_start['B']+=1
        elif termi_len>= 3:
            label_all['B'] += 1
            label_all['E'] += 1
            label_all['M'] += len(terms[i]) - 2
            label_dict['B']['M'] += 1 #B->M
            label_dict['M']['M'] += len(terms[i]) - 3 #M->M
            label_dict['M']['E'] += 1 #M->E
            
            E_num = 1
            if i==0:
                label_start['B']+=1
        if i+1<line_len:
            termi1_len = len(terms[i+1])
            if termi1_len == 1:
                if S_num == 1:
                    label_dict['S']['S'] +=1 #S->S
                if E_num == 1:
                    label_dict['E']['S'] +=1 #E->S
            if termi1_len > 1:
                if S_num == 1:
                    label_dict['S']['B'] +=1 #S->B
                if E_num == 1:
                    label_dict['E']['B'] +=1 #E->B
        count_term(terms[i], termi_len, word_dict)
def count_term(term, termi_len, word_dict):
    
    if termi_len == 1:
        try:
            word_dict['S'][term] += 1
        except:
            word_dict['S'][term] = 1
        try:
            word_dict['ALL']['S'] +=1
        except:
            word_dict['ALL']['S'] =1
    if termi_len == 2:
        try:
            word_dict['B'][term[0]] += 1
        except:
            word_dict['B'][term[0]] = 1
        try:
            word_dict['ALL']['B'] +=1
        except:
            word_dict['ALL']['B'] =1
        try:
            word_dict['E'][term[1]] += 1
        except:
            word_dict['E'][term[1]] = 1
        try:
            word_dict['ALL']['E'] +=1
        except:
            word_dict['ALL']['E'] =1
    if termi_len >= 3:
        for i in range(termi_len):
            if i == 0:
                try:
                    word_dict['B'][term[0]] += 1
                except:
                    word_dict['B'][term[0]] = 1
                try:
                    word_dict['ALL']['B'] +=1
                except:
                    word_dict['ALL']['B'] =1
            elif i == termi_len-1:
                try:
                    word_dict['E'][term[termi_len-1]] += 1
                except:
                    word_dict['E'][term[termi_len-1]] = 1
                try:
                    word_dict['ALL']['E'] +=1
                except:
                    word_dict['ALL']['E'] =1
            else:
                try:
                    word_dict['M'][term[i]] += 1
                except:
                    word_dict['M'][term[i]] = 1
                try:
                    word_dict['ALL']['M'] +=1
                except:
                    word_dict['ALL']['M'] =1
def calc_word_prob(word_dict):
    for key1 in word_dict:
        if key1 == 'ALL':
            continue
        for word in word_dict[key1]:
            word_dict[key1][word] =  math.log(word_dict[key1].get(word,1)*1.0/word_dict['ALL'].get(key1,1))
            
def load_file(filepath,code_style,label_dict,word_dict,label_start,label_all,d_dict,d_set):
    ff1 =  open(filepath,'r')
    i = 0 
    for line in ff1:
        i += 1
        line = line.strip()
        try:
            uline = unicode(line,code_style) 
        except:
            print i,line
            break
        subulines = re_flag.split(uline)
        for subuline in subulines:
            terms = subuline.split('  ')
    #         print '/'.join(terms)
            count_label(terms,label_dict,word_dict,label_start,label_all,d_dict,d_set)
    #         create_DAG(d_dict,terms)
    ff1.close()
    
def load_word(wordpath, code_style,label_dict,word_dict,label_start,label_all,d_dict,d_set):
    ff2 =  open(wordpath,'r')
    i = 0
    for line in ff2:
        i += 1
        line = line.strip()
#         print line
        try:
            uterms = unicode(line,code_style) 
        except:
            print i,line
            break
        
        count_label([uterms],label_dict,word_dict,label_start,label_all,d_dict,d_set)
#         create_DAG(d_dict,terms)
    ff2.close()
    
def load_data(filepath1, filepath2, code_style):
    label_start = {'B':0,'M':0.1,'E':0.1,'S':0}
    label_all = {'B':0,'M':0,'E':0,'S':0}
    label_dict = {}
    label_dict['B'] = {'M':0,'E':0}
    label_dict['M'] = {'M':0,'E':0}
    label_dict['E'] = {'B':0,'S':0}
    label_dict['S'] = {'B':0,'S':0}
    word_dict = {}
    word_dict['B'] = {}
    word_dict['M'] = {}
    word_dict['E'] = {}
    word_dict['S'] = {}
    word_dict['ALL'] = {}
    d_dict = {}
    d_set = set([]) 
    load_file(filepath1,code_style,label_dict,word_dict,label_start,label_all,d_dict,d_set)
    load_file(filepath2,code_style,label_dict,word_dict,label_start,label_all,d_dict,d_set)
#     load_word(wordpath, code_style,label_dict,word_dict,label_start,label_all,d_dict,d_set)
    calc_word_prob(word_dict)
    resort_DAG(d_dict)
    total = 0
    for key in label_all:
        total += label_all[key]
        
    for key1 in label_dict:
        for key2 in label_dict[key1]:
            label_dict[key1][key2] = math.log(label_dict[key1][key2]*1.0/total)
    total_start = 0   
    for key in label_start:
        total_start += label_start[key]
    for key in label_start:
        label_start[key] = math.log(label_start[key]*1.0/total_start)
#         
#     print label_start 
#     print label_all
#     print label_dict['B']
#     print label_dict['M']
#     print label_dict['E']
#     print label_dict['S']
#     print word_dict['ALL']['B'] 
#     print word_dict['ALL']['M'] 
#     print word_dict['ALL']['E'] 
#     print word_dict['ALL']['S']

    
#     print label_matrix 
    return word_dict,label_dict,label_start,d_dict
if __name__ == '__main__':

    filepath1 = '../icwb2-data/training/msr_training.utf8'
    filepath2 = '../icwb2-data/gold/msr_training_words.utf8'
    code_style = 'utf8'
    word_dict,label_dict,label_start,d_dict = load_data(filepath1, filepath2, code_style)
    with open('../train_dict.pickle', 'w') as f:
        pickle.dump(word_dict, f)
        pickle.dump(label_dict, f)
        pickle.dump(label_start, f)
        pickle.dump(d_dict, f)
