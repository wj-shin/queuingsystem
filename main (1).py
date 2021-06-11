from Function import *
import fire

def main(alpha=0.4,arrvRate=90,svcRate=75):
    cost3=[]
    cost1,cost2 = process(arrvRate,svcRate)
    for i in range(len(cost1)):
        cost3.append((alpha*cost1[i])+((1-alpha)*cost2[i]))
    for i in range(len(cost3)):
        print(cost1[i],",",cost2[i],",",cost3[i])
    propercustomer=cost3.index(max(cost3))
    print(propercustomer)
if __name__=="__main__":
    fire.Fire()
