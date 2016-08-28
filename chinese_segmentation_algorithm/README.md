#Chinese Segmentation Algorithm

##Summary
    Chinese sentence is hard to split into words because there is not any blanks. 
    
    There are some chinese segmentation algorithm models. This article is going to introduct HMM model which 
    
    is used in chinese segmentation.
##HMM
    HMM is short for hidden markov model. It is usually used to solve 3 problems, one of these is calculation of 
    
    hidden state chain. Chinese segmentation algorithm is based on calculation of hidden state chain.
    
    The sentence is composed with chinese characters. Some of these characters are words which have 2 and more 
    
    than 2 characters. Others are single words. Chinese segmentation algorithm is going to recognising words 
    
    correctly. In the HMM , there are 2 chains, visible chain and hidden state chain. The sentence is considered as
    
    visible chain. Here is introduced part-of-speech tagging. The word which has 2 characters is tagged B and E,
    
    the first is tagged B , the second is tagged E. The word which has more 2 characters is tagged B,M and E,
    
    the middle characters are tagged M. The word which has 1 character is tagged S. The tagging of sentence is 
    
    considered as hidden state chain. In the calculation of hidden state chain, visible chain is known, and 
    
    tagging of sentence is the main target. Here is introduced state matrix and emission matrix. State matrix have
    
    2 parts, one is probability of one state transfermation into other state, another is probability of state of 
    
    first characters . Emission matrix is probability of state of characters. 
    
    Viterbi algorithm is used to find the path of max probability.
    
##DAG

    DAG is short for directed acyclic graph. It is used in chinese segmentation algorithm as supplement of HMM.
    
    There is 2 reasons. The first reason is that only rely on probability calculation is not able to have 
    
    precise word segmentation result. The second reason is that DAG and max matching are able to have precise 
    
    word segmentation result , Especially the words that had been trained before.
    
##Experiment

    The dataset is here,http://sighan.cs.uchicago.edu/bakeoff2005/. It is a public dataset available for 
    
    research use It has complete training, testing, and gold-standard data sets, as well as the scoring script.
    
    Here is the score of my program.
    
    <table>
<tr>
<td>
=== SUMMARY:
</td>
</tr>
<tr>
<td>
=== TOTAL INSERTIONS:	5389
</td>
</tr>
<tr>
<td>
=== TOTAL DELETIONS:	385
</td>
</tr>
<tr>
<td>
=== TOTAL SUBSTITUTIONS:	4471
</td>
</tr>
<tr>
<td>
=== TOTAL NCHANGE:	10245
</td>
</tr>
<tr>
<td>
=== TOTAL TRUE WORD COUNT:	106873
</td>
</tr>
<tr>
<td>
=== TOTAL TEST WORD COUNT:	111877
</td>
</tr>
<tr>
<td>
=== TOTAL TRUE WORDS RECALL:	0.955
</td>
</tr>
<tr>
<td>
=== TOTAL TEST WORDS PRECISION:	0.912
</td>
</tr>
<tr>
<td>
=== F MEASURE:	0.933
</td>
</tr>
<tr>
<td>
=== OOV Rate:	0.026
</td>
</tr>
<tr>
<td>
=== OOV Recall Rate:	0.000
</td>
</tr>
<tr>
<td>
=== IV Recall Rate:	0.981
</td>
</tr>
</table>

    msr_test_result.utf8	5389	385	4471	10245	106873	111877	0.955	0.912	0.933	0.026	0.000	0.981
    
    
    
    
     
    
