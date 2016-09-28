#Chinese Similarity Algorithm

    This article will introduct LSI chinese similarity algorithm. LSI belongs to latent feature model.
    
    It is used in search and recommand system, such as google. It is good at solving the misunderstanding 
    
    problem which happened in the situation of one word with several meanings or one meanings with several words
    
    It has bypassed the problem of natural language understanding. It uses statistical analysis method to 
    
    find the correlation between different words, to make the search results close to the ideal value.
    
##Introduction
    
     The purpose is to find the most similarity doc with query during many docs. The doc is composed with chinese 
     
     setences. The query is chinese word.

##Term-doc Matrix

    In order to get the terms of docs, we use chinese segmentation algorithm to split all the docs, and get a 
    
    terms dict  which is like {term:No.} ,Then assumed that we set the document number from 1 to 10, and we get a 
    
    matrix. The colum of matrix is number of term. The row of matrix is number of doc. The element of matrix is 
    
    the number of term shown in the doc.
    
##TF-IDF Matrix
    
    The term-doc matrix is counting matrix. The TF-IDF matrix is feature matrix. Why we need TF-IDF?
    
    Beacause it can evaluate the importance of a word for a doc of N docs.
    
<img src="http://chart.googleapis.com/chart?cht=tx&chl=TF-IDF_%7Bij%7D%20%3D%20%5Cfrac%7BN_%7Bij%7D%7D%7BN_%7B*j%7D%7D*log(%5Cfrac%7BD%7D%7BD_%7Bi%7D%7D)" style="border:none;" />
    
    Nij is the number of term i shown in the doc j .
    
    N*j is the number of all the terms of doc j
    
    D is the number of doc
    
    Di is the number docs which have term i
    
##SVD

    The process of derivation is too long. Let us see the formula.
    
<img src="http://chart.googleapis.com/chart?cht=tx&chl=M%20%3D%20U%20%5Ccdot%20%5CSigma%20%5Ccdot%20V%5E%7BT%7D" style="border:none;" />

    M is TF-IDF matrix.
    
    U represents correlation between terms and hidden features
    
    VT represents correlation between hidden features and docs
    
    The sigma is hidden features.
    
##Query

    The query word needs to use Term-doc Matrix to change word into colum vector.
    
    Then we calc the correlation between hidden features and query
    
<img src="http://chart.googleapis.com/chart?cht=tx&chl=V_%7Bq%7D%20%3D%20q%5E%7BT%7D%5Ccdot%20U%20%5Ccdot%20%20%5CSigma%5E%7B-1%7D%20" style="border:none;" />

    Then calculate cosine similarity between Vq and Vt. The reslut is a vector of similarity between query and docs.
    
    
    
    

    
