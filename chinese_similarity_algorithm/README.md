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
    
    matrix. The colum of matrix is number of term. The row of matrix is number of doc.
    
##TF-IDF Matrix
    
    The term-doc matrix 
    
    

    
