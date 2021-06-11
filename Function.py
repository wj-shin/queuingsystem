import math
import random


MARKOV_TYPE_OF_DATA  = 2
MARKOV_MIN_STATE_PROB = 0.000001
NUM_INTERVALS=100

# uniform Random Variable을 반환하는 함수입니다. minVal 과 maxVal 사이의 임의의 값을 반환
def getUniformRandomVariable(minVal,maxVal):
    return random.uniform(minVal, maxVal)

# exponentialRandomVariabl을 반환하는함수
def getExponentialRandomVariable(l):
    return -1 * math.log(1-random.uniform(0,1))/l

# 통계적 확률을 계산하기 위한 시뮬레이션 함수입니다.
def simulateMarKovChain(numSamples, arrvRate,svcRate,samplePDF,maxCustomers):
    print(len(samplePDF))
    counter = 0
    state = 0
    numLosts = 0
    prevTime = 0
    curTime = 0
    delta = 1/3600
    idx=0
    while(counter < numSamples):
        nextArrv = getExponentialRandomVariable(arrvRate)
        nextSvc  = getExponentialRandomVariable(svcRate)
        prevTime = curTime
        curTime = curTime + delta
        arrive          =   True if(nextArrv<=delta) else False
        arrive_depart   =   True if(nextSvc<=(delta-nextArrv)) else False
        depart          =   True if(nextSvc<=delta) else False
        lostDepart      =   True if(nextSvc>=nextArrv) else False
        if(state == 0):
            if(arrive):
                counter=counter+1
                if(arrive_depart):
                    state=state+0
                else:
                    state=state+1
            else:
                counter=counter+0
                state=state+0
            samplePDF[state]= samplePDF[state]+1
        elif(state==maxCustomers):
            if(arrive):
                state=state+0
                counter=counter+1
                if(depart):
                    if(lostDepart):
                        numLosts=numLosts+1
                    else:
                        numLosts=numLosts+0
                else:
                    numLosts=numLosts+1
            else:
                counter=counter+0
                numLosts=numLosts+0
                if(depart):
                    state=state-1
                else:
                    state=state+0
            samplePDF[state]=samplePDF[state]+1
        else:
            if(arrive):
                counter=counter+1
                if(depart):
                    state=state+0
                else:
                    state=state+1
            else:
                counter=counter+0
                if(depart):
                    state=state-1
                else:
                    state=state+0
            samplePDF[state]=samplePDF[state]+1
    clock =curTime/delta
    for i in range(len(samplePDF)):
        samplePDF[i]=samplePDF[i]/clock
    sampleMean=0
    for i in range(len(samplePDF)):
        sampleMean = sampleMean + i *samplePDF[i]
    return samplePDF,numLosts,sampleMean


def process(arrvRate,svcRate):
    numSamples = 100000
    cost1 = []
    cost2 = []
    for maxCustomers in range(1,100):
        samplePDF = [0 for values in range(maxCustomers+1)]
        samplePDF,numLosts,sampleMean = simulateMarKovChain(numSamples,arrvRate,svcRate,samplePDF,maxCustomers)
        numLosts = numLosts/numSamples
        cost1.append(numLosts)
        cost2.append(sampleMean/maxCustomers)
    return cost1, cost2
