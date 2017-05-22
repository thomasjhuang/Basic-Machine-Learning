import pandas as pd
import numpy as np
import sys
import math as m
import timeit
import pylab
import matplotlib.pyplot as plt


def readcsv(filename):
    df = pd.read_csv(filename, encoding='utf-8')
    return df

def kmeans(df, k, clust_opt, plot_opt):
    
    #if clust opt = 5 then you take a 3 percent sample of data
    if(clust_opt == 5):
        df = df.sample(int(0.03 * len(df)))
        
    #deletes all columns that are not the four attributes that we want
    for column in df.iteritems():
        label = column[0]
        if(label != 'latitude' and label != 'longitude' and label != 'reviewCount' and label != 'checkins'):
            del df[label]
            
    #standardize data        
    if(clust_opt == 3):
        df = (df - df.mean()) / (df.max() - df.min())
    
    #log transform over reviewCount and checkins 
    if(clust_opt == 2):
        np.log(df['reviewCount'])
        np.log(df['checkins'])
    
    #'centroids' stores centroid locations, indexed 0 - k many centroids
    centroids = df.sample(k)
        
    centroids = centroids.reset_index()
    del centroids['index']

    #dict of cluster dataframes, key values are string integers
    clusters={}
    for x in range(0, k):
        clusters["{0}".format(x)] = pd.DataFrame()
    
    previous = df
    while(True):
        #fill clusters with data
        min_dist = sys.float_info.max;
        for ind,df_row in df.iterrows():
            data = df_row.as_matrix()
            for index,c_row in centroids.iterrows():
                centroid = c_row.as_matrix()
                if(clust_opt == 4):
                    dist = manhattan(data, centroid)
                else:
                    dist = euclid(data, centroid)
                if(dist < min_dist):
                    min_dist = dist
                    mindex = index
            clusters[str(mindex)] = clusters[str(mindex)].append(df_row) 

        #each cluster must coincide with each centroid
        #error it goes through every element and replaces with a single cluster mean
        i = 0
        for c_ind,c_row in centroids.iterrows():
                for column in clusters[str(i)]:
                    mean = clusters[str(i)][column].mean()
                    centroids.ix[c_ind, column] = mean
                i = i + 1
       
        #check if means have changed
        if(previous.equals(centroids)):
            break
        previous = centroids
    
    #print within cluster
    within_cluster(centroids, clusters, k)
    #personal_score(centroids, clusters, k)

    #print out centroids
    p = 0
    for index, row in centroids.iterrows():
        print("Centroid{0}=".format(p), np.array2string(row.as_matrix(), separator=','))
        p += 1
    
    #plot
    plot(clusters, centroids, clust_opt, k)
    plt.show()
        
def euclid(a, b):
    dist = m.sqrt(m.pow(a[0] - b[0], 2) + m.pow(a[1] - b[1], 2) + m.pow(a[2] - b[2], 2) + m.pow(a[3] - b[3],2))
    return dist

def manhattan(a, b):
    dist = np.fabs(a[0] - b[0]) + np.fabs(a[1] - b[1]) + np.fabs(a[2] - b[2]) + np.fabs(a[3] - b[3])
    return dist

def personal_score(centroids,clusters,k):
    total = 0
    centroids = centroids.astype(float)
    prev = centroids.iloc[0]
    for i in range(0,k):
        for c_ind,c_row in centroids.iterrows():
            centroid = c_row.as_matrix()
            total = total + (euclid(centroid, prev)*len(clusters[str(i)]))
            prev = centroid
    print('WL=',total)
    

def plot(clusters, centroids, plot_opt, k):
    #plotting latitude vs. longitude
    if(plot_opt == 1):
        for i in range(0,k):
            for column in clusters[str(i)].iteritems():
                label = column[0]
                if(label != 'latitude' and label != 'longitude'):
                    del clusters[str(i)][label]
                    
        color = iter(plt.cm.rainbow(np.linspace(0,1,k+1)))
        centroids = centroids.astype(float)
        ax = centroids.plot(kind='scatter',x='latitude',y='longitude',c=next(color),label='Centroids')
        prev = ax
        for i in range(0,k):
            if(clusters[str(i)].empty == False):
                temp = clusters[str(i)].astype(float)
                new_ax = temp.plot(kind='scatter',x='latitude', y='longitude', c=next(color), label='Cluster{0}'.format(i), ax=prev, title='latitude vs. longitude')
                prev = new_ax
        return prev

    #plotting reviewCount vs. checkins
    if(plot_opt == 2):
        for i in range(0,k):
            for column in clusters[str(i)].iteritems():
                label = column[0]
                if(label != 'reviewCount' and label != 'checkins'):
                    del clusters[str(i)][label]
                    
        color = iter(plt.cm.rainbow(np.linspace(0,1,k+1)))
        centroids = centroids.astype(float).reset_index()
        ax = centroids.plot(kind='scatter',x='reviewCount',y='checkins',c=next(color),label='Centroids')
        prev = ax
        for i in range(0,k):
            if(clusters[str(i)].empty == False):
                temp = clusters[str(i)].astype(float).reset_index()
                new_ax = clusters[str(i)].plot(kind='scatter',x='reviewCount', y='checkins', c=next(color), label='Cluster{0}'.format(i), ax=prev, title='reviewCount vs. checkins')
                prev = new_ax
        return prev

def within_cluster(centroids, clusters, k):
    total = 0
    centroids = centroids.astype(float)
    for i in range(0,k):
        for c_ind,c_row in centroids.iterrows():
            centroid = c_row.as_matrix()
            for cu_ind, cu_row in clusters[str(i)].iterrows():
                cluster = cu_row.as_matrix().astype(float)
                total = total + m.pow(euclid(centroid, cluster), 2)
    print('WC-SSE=',total)
    return total
    
def main():
    readin = sys.argv[1]
    k = pd.to_numeric(sys.argv[2])
    clust_opt = pd.to_numeric(sys.argv[3])
    if(sys.argv[4] == 'no'):
        plot_opt = 0
    else:
        plot_opt = sys.argv[4]
    df = readcsv(readin)
    kmeans(df, k, clust_opt, plot_opt)
main()
