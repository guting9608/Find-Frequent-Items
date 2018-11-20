import sys
import random
import itertools
import time

def splitData(line_list,splitRatio):
    length=len(line_list)
    splitSize=int(length*splitRatio)
    splitSet=[]
    copiedSet=line_list
    random.seed(noOfItr)
    beginningIndex=random.randint(1,length)
    splitSet=line_list[beginningIndex:beginningIndex+splitSize]
    return splitSet


def getRandomSample(ratio):
    lineList=[]
    file=open('datset.txt',"r+")
    for line in file: #(24, 44, 419, 724)
        items =line[1:-2].split(",")
        basketList=set()
        for item in items:
            item=int(item.strip())
            basketList.add(item)
        lineList.append(basketList)
    lineListLen=len(lineList)
    rand_smpl = splitData(lineList,ratio)  
    return rand_smpl


def getCanFreqItemsAndNegBorder(sample,_pass,sup):
    global canFreqItems
    global negBorder
    flag=False
    Items={}

    for basket in sample:
        if _pass==1:
            for item in basket:
                if item in Items:
                    Items[item]+=1
                else:
                    Items[item]=1
        
        elif _pass==2:
            tempPairs=list(itertools.combinations(basket,_pass))

            for tuples in tempPairs:
                temp2Items=list(itertools.combinations(tuples,_pass-1))
                for item in temp2Items: #item is a tuble (1,) 
                    if sum(item) in canFreqItems: #canFreqItems's key is a number 
                        flag=True
                    else:
                        flag=False
                        break
                if flag==True:
                    tuples=tuple(sorted(tuples))
                    if tuples in Items:
                        Items[tuples]+=1
                    else:
                        Items[tuples]=1
        else:
            tempPairs=list(itertools.combinations(basket,_pass))

            for tuples in tempPairs:
                temp2Items=list(itertools.combinations(tuples,_pass-1))
                for item in temp2Items: #item is a tuble (1,) 
                    if item in canFreqItems: #canFreqItems's key is a number 
                        flag=True
                    else:
                        flag=False
                        break
                if flag==True:
                    tuples=tuple(sorted(tuples))
                    if tuples in Items:
                        Items[tuples]+=1
                    else:
                        Items[tuples]=1

    for item in Items:
        if Items[item]>=sup:
            canFreqItems[item]=Items[item]
        else:
            negBorder[item]=Items[item]

    lenCanFreqItemsCurItr=len(canFreqItems)
    return canFreqItems,negBorder,lenCanFreqItemsCurItr


def getList(my_dict):
    my_list = list(my_dict.keys())
    return my_list


def getFreqItems(inputList,_pass,sup):    
    global FreqItems
    flag=False
    Items={}    
    for subList in inputList:
        if _pass==1:
            for item in subList:
                if item in Items:
                    Items[item]+=1
                else:
                    Items[item]=1
        
        elif _pass==2:
            tempPairs=list(itertools.combinations(subList,_pass))

            for tuples in tempPairs:
                temp2Items=list(itertools.combinations(tuples,_pass-1))
                for item in temp2Items: #item is a tuble (1,) 
                    if sum(item) in canFreqItems: #canFreqItems's key is a number 
                        flag=True
                    else:
                        flag=False
                        break
                if flag==True:
                    tuples=tuple(sorted(tuples))
                    if tuples in Items:
                        Items[tuples]+=1
                    else:
                        Items[tuples]=1
        else:
            tempPairs=list(itertools.combinations(subList,_pass))

            for tuples in tempPairs:
                temp2Items=list(itertools.combinations(tuples,_pass-1))
                for item in temp2Items: #item is a tuble (1,) 
                    if item in FreqItems: #canFreqItems's key is a number 
                        flag=True
                    else:
                        flag=False
                        break
                if flag==True:
                    tuples=tuple(sorted(tuples))
                    if tuples in Items:
                        Items[tuples]+=1
                    else:
                        Items[tuples]=1

    for key in Items:
        if Items[key]>=80:
            FreqItems[key]=Items[key]
            

    lenFreqItemsCurItr=len(FreqItems)
    return FreqItems,lenFreqItemsCurItr



def compare(list1,list2):
    for item in list1:
        if item in list2:
            return True
    return False
 

if __name__ == '__main__':

    samplingRate = 0.1
    supRatio = 4/15
    sup = int(supRatio*samplingRate*300)

    file = open(sys.argv[1])

    negBorder={}
    canFreqItems={}
    FreqItems={}

    repeatToivonen=True
    noOfItr=0
    start=time.time()

    while repeatToivonen==True:
        noOfItr+=1
        repeatToivonen=False

        baskets=getRandomSample(samplingRate)     
        _pass=1    
        lenCanFreqItemsCurItr=1
        lenCanFreqItemsPrevItr=0
        while lenCanFreqItemsCurItr!=lenCanFreqItemsPrevItr:
            lenCanFreqItemsPrevItr=lenCanFreqItemsCurItr    
            canFreqItems,negBorder,lenCanFreqItemsCurItr=getCanFreqItemsAndNegBorder(baskets,_pass,sup)
            _pass+=1

            
        canFreqItemsList=getList(canFreqItems)

        negBorderList=getList(negBorder)


        line=getRandomSample(1)
        lenFreqItemsCurItr=1
        lenFreqItemsPrevItr=0     
        _pass=1
        while lenFreqItemsCurItr!=lenFreqItemsPrevItr:
            lenFreqItemsPrevItr=lenFreqItemsCurItr    
            freqItems,lenFreqItemsCurItr=getFreqItems(line,_pass,sup)
            _pass+=1               
 
        FreqItemList=getList(FreqItems)    


        flag = compare(negBorderList,FreqItemList)

        end = time.time()
        time_needed=end-start
        print(time_needed)


        f = open('Output/OutputForIteration_'+str(noOfItr)+'.txt', 'w') 
        f.write('Sample Created:\n')
        f.write(str(baskets)+"\n")
        f.write("frequent itemsets:\n")
        f.write(str(canFreqItemList)+"\n")
        f.write("negative border:\n")
        f.write(str(negBorderList)+"\n")
        f.close()

        repeatToivonen=flag





