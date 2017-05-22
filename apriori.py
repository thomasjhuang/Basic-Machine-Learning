
import pandas as pd
import operator
import numpy as np
from itertools import starmap
import sys
import math as m
from collections import defaultdict
from itertools import chain, combinations
import matplotlib.pyplot as plt

def readcsv(filename):
    df = pd.read_csv(filename, encoding='utf-8')
    return df

def joinSet(itemSet, length):
        return set([i.union(j) for i in itemSet for j in itemSet if len(i.union(j)) == length])

def apriori(readin, minsup, minconf):
    itemset, transactions = getTS(readin)
    #print(itemset)
    freqSet = defaultdict(int)
    largeSet = dict()
    printRules = dict()
    printItems = dict()
    ls_keys = list(largeSet.keys())
    assocRules = dict()
    Cset = find_minsup(itemset, transactions, minsup, freqSet)
    curr_Lset = Cset
    k = 2
    
    while(curr_Lset != set([])):  
        count = 0
        largeSet[k-1] = curr_Lset
        curr_Lset = joinSet(curr_Lset, k)
        curr_Cset = find_minsup(curr_Lset,transactions,minsup,freqSet)
        curr_Lset = curr_Cset
        printItems[k] =  len(curr_Cset)
        
        def getSupport(item):
            return float(freqSet[item])/len(transactions)
       
        for key,value in list(largeSet.items())[1:]:
            for item in value:
                _subsets = map(frozenset, [x for x in subsets(item)])
                for element in _subsets:
                    remain = item.difference(element)
                    if len(remain) > 0:
                        confidence = getSupport(item)/getSupport(element)
                        if confidence >= minconf:
                            count = count + 1
        print('ASSOCIATION-RULES', k, count)
        
        k = k + 1
    count = 0
    for k, v in printItems.items():
        print('FREQUENT-ITEMS', k, v)
        count += v
   
    
def find_minsup(itemSet, transactionList, minSupport, freqSet):
        _itemSet = set()
        localSet = defaultdict(int)

        for item in itemSet:
                for transaction in transactionList:
                        if item.issubset(transaction):
                                freqSet[item] += 1
                                localSet[item] += 1

        for item, count in localSet.items():
                support = float(count)/len(transactionList)

                if support >= minSupport:
                        _itemSet.add(item)

        return _itemSet

def dff(fname):
        file_iter = open(fname, newline='')
        for line in file_iter:
                line = line.strip().rstrip(',') 
                record = set(line.split(','))
                yield record
                
def subsets(arr):
    return chain(*[combinations(arr, i + 1) for i, a in enumerate(arr)])
            
def getTS(data_iterator):
    transactionList = list()
    itemSet = set()
    for record in data_iterator:
        transaction = frozenset(record)
        transactionList.append(transaction)
        for item in transaction:
            itemSet.add(frozenset([item]))              
    return itemSet, transactionList

def main():
    readin = sys.argv[1]
    minsup = pd.to_numeric(sys.argv[2])
    minconf = pd.to_numeric(sys.argv[3])
    df = readcsv(readin)
    readin = list(dff('yelp4.csv'))
    apriori(readin, minsup, minconf)
    
main()
    