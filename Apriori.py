''' 
Apriori Algorithm
Author: Gekun F.

Implementation of Apriori From 
(Data Mining. Concepts and Techn - Jiawei Han, Micheline Kamber, J/Page 253)

description:
    Implementaion of Apriori algorithm by making use of pyhton set, numpy array
    and pandas DataFrame. This implementation way is faster than existing 
    implementations(open source))
'''

import numpy as np
import pandas as pd
from datetime import datetime
import argparse

'''
Find all frequent 1-itemset in D (suppose every row is a transaction)
Input:  D: pandas DataFrame
        min_sup: python float (constraint: [0,1])
Output: frequent_one_itemset: list of sets 
'''
def find_frequent_1_itemset(D, min_sup):
    NumOfRowInD = D.shape[0]  
    min_sup_count = min_sup * NumOfRowInD
    CurrentKeys = set({}) # A varaible keep all keys in current dictionary
    D_list = D.values.flatten() # Transform D into a list for faster access
    one_itemset = {} # A dictionary keeps count of all 1 itemset
    for item in D_list:
        if item in CurrentKeys:
            one_itemset[item] += 1
        else:
            one_itemset[item] = 1
            CurrentKeys.add(item)    
    # find frequent item based on counts
    frequent_one_itemset = []
    for key in CurrentKeys:
        if one_itemset[key] > min_sup_count:
            frequent_one_itemset.append(set([key]))
    return frequent_one_itemset

'''
Find if all (len(c)-1)-subsets of c are contained in L
Input:  c: python set
        L: python list of sets
Output: python boolean 
'''
def has_infrequent_subset(c, L):
    # Create a list copy to iterate through it
    cTemp = list(c)
    for item in cTemp:
        # Test if any subset of c is a element in L
        cNew = set(c)
        cNew.remove(item)
        if cNew not in L:
            return True  # One (length-1)-subset of c is not in L, return True
    return False # All (length-1)-subsets of c are in L, Return False

'''
Generate next-L by L
Input:  L: python list of sets
Output: newL: python list of sets
'''
def apriori_gen(L):
    newL = []
    # a loop goes through L twice to create combinations.
    # e.g. [1,2,3] --> (1,2), (1,3), (2,3) 
    for i1 in range(len(L)):
        for i2 in range(i1+1, len(L)):
            UnionSet = L[i1].union(L[i2])
            UnionLen = len(UnionSet)
            if ( UnionLen == len(L[i1])+1) and (UnionSet not in 
               newL) and (not has_infrequent_subset(UnionSet,L)):
                    newL.append(UnionSet)
    return newL

'''
Find if all frequent itemsets in "itemsets" in "D" (suppose every row in D is a 
transaction, Given "min_sup")
Input:  D: pandas DataFrame
        itemsets: python list of sets
        min_sup: python float (constraint: [0,1])
Output: frequentItemsets: python list of sets
'''
def FrequentItemsets(D, itemsets, min_sup):
    NumOfRowInD = D.shape[0]
    NumOfColInD = D.shape[1]
    min_sup_count = NumOfRowInD * min_sup
    
    D_list = D.values.flatten()
    counts = np.zeros(len(itemsets))
    
    for i in range(NumOfRowInD):
        OneRow = set(D_list[i*NumOfColInD:(i+1)*NumOfColInD])
        for j in range(len(itemsets)): 
            if len(itemsets[j].difference(OneRow)) == 0:
                counts[j] += 1
             
    frequentItemsets =  []
    for i in range(len(counts)):
        if counts[i] >= min_sup_count:
            frequentItemsets.append(itemsets[i])

    return frequentItemsets

'''
Apriori algorithm From 
(Data Mining. Concepts and Techn - Jiawei Han, Micheline Kamber, J/Page 253)
Input:  D: pandas DataFrame
        min_sup: python float (constraint: [0,1])
Output: UnionSet: python list of list of sets
'''
def Apriori(D, min_sup):
    # Start with 1 frequent itemset
    FrequentOneItemSet = find_frequent_1_itemset(D,min_sup)
    UnionSet = [FrequentOneItemSet] 
    
    L = FrequentOneItemSet[:]
    while L:
        Lnew = apriori_gen(L)
        LnewFrequent = FrequentItemsets(D, Lnew, min_sup)
        if (len(LnewFrequent) == 0):
            return UnionSet
        else:
            UnionSet.append(LnewFrequent)
            L = LnewFrequent[:]
    # return "[]" in case of failure(in later modification) 
    return []

'''
Setting args
Input:  none
Output: parse_args() 
'''
def parse_options():
    parser = argparse.ArgumentParser(description='Apriori Algorithm')
    parser.add_argument('--min_sup', 
                        type=float, 
                        default=0.9, 
                        help='Minimum support, defalut 0.9')
    parser.add_argument('--FilePath', 
                        type=str, 
                        default='adult.data.csv', 
                        help='data file location')
    parser.add_argument('--noDetail', 
                        action='store_false', 
                        default=True, 
                        help='If provided, no detail will be showed.')
    return parser.parse_args()

'''
Final Output
Input:  data: pd Dataframe 
        args: argparse.ArgumentParser
Output: none
(will generate an "OUTPUT.txt" and print to terminal)
'''
def print_and_report(data, args):
    f= open("OUTPUT.txt","w+")
    FinalCount = 0
    AprResult = Apriori(data,args.min_sup)
    for i in range(len(AprResult)):
        FinalCount += len(AprResult[i])
        if args.noDetail:
            print(i+1, "-itemset: ", AprResult[i], "\n")
            f.write(str(i+1)+ "-itemset: "+ str(AprResult[i])+ "\n")
        
    print("Number of frequent Itemsets: ", FinalCount)
    f.write("Number of frequent Itemsets: "+ str(FinalCount))
    f.close()

#%%----------------------------------MAIN--------------------------------------
if __name__ == '__main__':
    # Starting timer
    start = datetime.now()
    # Getting inputs
    args = parse_options()
    # Getting data
    data  = pd.read_csv(args.FilePath)
    # Outputing 
    print_and_report(data, args)
    # Printing time
    print("Running time: ", datetime.now()-start)