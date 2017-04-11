import pandas as pd
import numpy as np
import sys

def readcsv(filename):
    df = pd.read_csv(filename, encoding='utf-8')
    return df

def classifier(df, att_name,att_type,c_id):
    
    #Form Frequency Tables for Each Class Type
    posdf = df[df['goodForGroups'] == 1]
    negdf = df[df['goodForGroups'] == 0]
    posfq = pd.DataFrame()
    negfq = pd.DataFrame()
    for column in posdf:
        vc = posdf[column].value_counts()
        temp = {column : vc}
        tempdf = pd.DataFrame(temp)
        posfq = posfq.append(tempdf)

    for column in negdf:
        vc = negdf[column].value_counts()
        temp = {column : vc}
        tempdf = pd.DataFrame(temp)
        negfq = negfq.append(tempdf)
    
    posfq = posfq.fillna('BLANK')
    negfq = negfq.fillna('BLANK')
    
    #Defining Variables For Probability Calculation
    neg_sum = 0
    pos_sum = 0
    p_type = 0
    p_class = 0
    _class = 0
    yes = 11621
    no = 5251
    class_sum = yes + no
    #Find the number of unique types within an attribute, necessary for LaPlace smoothing
    uniques = 0
    for item in posfq[att_name].iteritems():
        if(item[1] != 'BLANK'):
            uniques = uniques + 1
    
    #Beginning of Probability Calculuation
   
    
    #Switching each frequency tables to dictionaries
    posfq = posfq[posfq[att_name] != 'BLANK']
    posfq = posfq.to_dict()
    negfq = negfq[negfq[att_name] != 'BLANK']
    negfq = negfq.to_dict()
    
    for val in posfq[att_name].values():
        pos_sum = pos_sum + val
        
    for val in negfq[att_name].values():
        neg_sum = neg_sum + val
        
    if(att_type == 'BLANK'):
        if(c_id):
            return (1/yes + pos_sum + neg_sum)
        else:
            return 1/(no + pos_sum + neg_sum)
    
    
    if(att_name == 'stars' or att_name == 'priceRange'):
        att_type = pd.to_numeric(att_type)
        
    if(att_name == 'open' or att_name == 'delivery' or att_name == 'outdoorSeating' or att_name == 'caters' or att_name == 'goodForKids' or att_name == 'waiterService'):
        if(att_type == 'True'):
            att_type = True
        else:
            att_type = False
            
    pos_val = 0
    neg_val = 0
    if(not(att_type in negfq[att_name])):
        neg_val = 0
    elif(not(att_type in posfq[att_name])):
        pos_val = 0
    else:
        pos_val = posfq[att_name][att_type]
        neg_val = negfq[att_name][att_type]
    
    if(pos_val == 'BLANK'):
        pos_val = 0
    if(neg_val == 'BLANK'):
        neg_val = 0
    
    #c_id = true means goodForGroups = 1, c_id = false means goodForGroups = 0
    
    if(c_id):
        p_class = pos_sum / class_sum
        p_type = (1 + pos_val) / (yes + uniques)
    else:
        p_class = neg_sum / class_sum
        p_type = (1 + neg_val) / (no + uniques)
        
    p_att = (pos_val + neg_val) / class_sum
    
    #if(p_att == 0):
      #  if(c_id):
      #      return (1/yes + pos_sum + neg_sum)
      #  else:
      #      return 1/(no + pos_sum + neg_sum)
    
    #p_posterior = (p_type * p_class) / p_att
    
    return p_type

def predict(train, test, row):
    yes = 11621
    no = 5251
    class_sum = yes + no
    test = test.fillna('BLANK')
    pos_product = yes / class_sum
    neg_product = no / class_sum
    for i in range(1,14) :
            pos_product = pos_product * classifier(train, list(test)[i], str(test.iloc[row, i]), True)
            neg_product = neg_product * classifier(train, list(test)[i], str(test.iloc[row, i]), False)
    
    pos_product = pos_product / (pos_product + neg_product)
    neg_product = neg_product / (neg_product + pos_product)
    
    result = [pos_product, neg_product]
    
    if(pos_product > neg_product):
        if(test.iloc[0,0] == 1):
            return 1
    else:
        if(test.iloc[0,0] == 0):
            return 0
        
    return 0

def loss(df, n):
    split_choice = [0.1,1,10,50]
    split = random.choice(split_choice)
    msk = np.random.rand(len(df)) < (split*0.01)
    train = df[msk]
    test = df[~msk]
    z_loss = 0
    df_10 = test.sample(10)
    for i in range(1,10):
        z_loss = z_loss + predict(train,df_10, i)
    z_loss = z_loss * (1/n)
    print('ZERO-ONE LOSS={0}'.format(z_loss))
    return z_loss

def main():
    test = readcsv('yelp2.csv')
    values = 0
    for i in range(10):
        values = values + loss(test, 10)
    values = values / 10
    
    print('MEAN ZERO-ONE LOSS={0}'.format(values))
main()
