# -*- coding:  utf-8 -*
"""
This module is used to ....
Authors: shiduo
Date:2016年8月11日
./score ../gold/msr_training_words.utf8 ../gold/msr_test_gold.utf8 msr_test_result.utf8 > score.utf8
"""
import lib.viterbi as viterbi
import pickle
def test_algorithm():

    with open('./train_dict.pickle', 'r') as f:
        word_dict = pickle.load(f)
        label_dict = pickle.load(f)
        label_start = pickle.load(f)
        d_dict = pickle.load(f)
    code_style = 'utf8'
    testpath = './icwb2-data/testing/msr_test.utf8'
    ff1 = open(testpath, 'r')
    resultpath = './icwb2-data/gold/msr_test_result.utf8'
    ff2 = open(resultpath, 'w')
    
    i = 0
    for line in ff1:
        i += 1
        print i
        line = line.strip()
        recognized = viterbi.mycut(label_start,word_dict, label_dict, d_dict,line, code_style)
        ff2.write(recognized.encode('utf8')+'\n')
    ff1.close()
    ff2.close()
if __name__ == '__main__':
    test_algorithm()
