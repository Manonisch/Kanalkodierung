from numpy.polynomial import Polynomial as polly
from binary import restpolynom  as restp
import numpy as np

def getCycles(n):
    cyclesFullList = []
    cyclesList = []
    cyclealpha = 1
    
    while cyclealpha < n :    
    
        if cyclealpha not in cyclesList :
            list = []
            alpha = cyclealpha 
            while alpha not in cyclesList :
                cyclesList.append(alpha)
                list.append(alpha)
                alpha = alpha * 2
                if alpha >= n :
                    alpha = alpha % n
            else :
                cyclesFullList.append(list)
        else :
            cyclealpha = cyclealpha + 1
    # print('for n:', n)
    for index in cyclesFullList :
        print(' the cycles are', index,'\n')
    return cyclesFullList
    
# What is a polynominal? -> (x+alpha^m1)*(x+alpha^m2)*(x+alpha^m4)*... -> from List at each cycle = x+alpha^listitem    
#def getMinimalPolynoms(cycles, n, restpolynoms) :

import itertools
    
def getMinimalPolynoms(cycles , n, restpolynoms) :  
    minimalPolynoms = {}
    for index in cycles :
        # print('the cycle for minimalpolynom m' + str(min(index)) + '(x), is', index, restpolynoms)
        partpol = []
        # STEP: Ausmultiplizieren -> polynomal with 2 unknowns -> This is the big question
        # STEP: Zusammenfassen: if x^3*n^4+x3*n^3 -> x^3(n^4+n^3) + addieren
        # IDEA:  (x + n^1)(x+n^2) = x2 + xn1 + xn2 + n1n2 = x2 + x(n2+n1)+ n3
        for x in range(0, len(index)+1) :
            comb = list(itertools.combinations(index, len(index)-x))
            # print('is', len(index)+1, index, x, comb)            
            i = 0
            while i < len(comb) :
                # print('single is', comb[i])
                val = 0
                for nr in comb[i] :
                    val = val + nr
                # STEP: Mod nehmen if n^m, m>= grenze => m = m mod grenze
                if val >= n :               
                    val = val % n                    
                comb[i] = val
                i = i + 1
            
            combInt = 0
                      
            for element in comb :
                # print('power to the strElem', element, restpolynoms, comb)
                # print('elem is', element, restpolynoms[str(element)])
                combInt = combInt ^ restpolynoms[str(element)]
            # print(combInt, 'is combInt') 

            
            partpol.append(combInt)

            
        # print('partpol for m'+ str(min(index)) + '(x), is', partpol)
        
        #STEP make the list to a single minimalPolynomInteger for better safekeeping... or would it be better to keep them seperated?
        minimalInt = 0
        j = 0
        for elem in partpol :
            included = 0
            if elem > 0 :
                included = 1
            
            minimalInt = minimalInt + 2**j * included 
            j = j + 1
           # print('minimalInt is: ', minimalInt, 'j is: ', j)
        
        mKey = 'm'+ str(min(index)) + '(x)'
        minimalPolynoms[mKey] = partpol
        minimalPolynoms[mKey + 'Int'] = minimalInt
        
    #print('dict of polynoms is', minimalPolynoms, 'and thats it')
    return minimalPolynoms
    
# STEP: Gleiche streichen n^3+n^3 = 2*n^3 -> mod 2
        
# STEP: From List of restpolynoms -> n^m = binaryinteger of alpharestpolynom, in one x -> binary addition of all alpharest polynoms
        #xList = []
        #binInt = 0
        #for item in xList :
        #    binInt = binInt ^ item
            
# STEP: for each x^f -> compute sum(2^f * binInt) -> is minimalpolynom integer for the cycle, 

# STEP: save to the cycle as last entry  

# -> each polynomrest should be delivered in a lookup table so that they can be directly substituted
# structure should be like: 'polynom power':'restpolynom as integer'

#testcases
#restpolym = {'0':1,'1':2,'2':4,'3':3,'4':6,'5':7,'6':5,'7':8,'8':1 }
#getMinimalPolynoms([[1,2,3],[2,4,5,7]],8,restpolym)

cyclesAre = [[1,2,4,8,16,32], [3,6,12,24,48,33], [5,10,20,40,17,34], [7,14,28,56,49,35], [9,18,36], [11,22,44,25,50,37], [13,26,52,41,19,38], [15,30,60,57,51,39], [21,42],[23,46,29,58,53,43], [27, 54, 45], [31,62,61,59,55,47]]

listPoly = [115, 109, 103, 97, 91, 67, ]
gEntry = [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,1,0,1,1,1]
for item in listPoly :
    print('MMMMMMMMMMMMMMMMMY ITEM', item)
    restDict = restp(63,item)
    print(restDict)
    minimalPolynomList = getMinimalPolynoms(cyclesAre,63,restDict)

    m5 = np.ravel(np.array(minimalPolynomList['m5(x)']))
    m11 = np.ravel(np.array(minimalPolynomList['m11(x)']))
    m15 = np.ravel(np.array(minimalPolynomList['m15(x)']))
    m21 = np.ravel(np.array(minimalPolynomList['m21(x)']))
    m23 = np.ravel(np.array(minimalPolynomList['m23(x)']))
    m31 = np.ravel(np.array(minimalPolynomList['m31(x)']))
    a = polly([1,2,3, 1, 1])
    ar = np.array(a)
    # print('m5 is', m5,'m11 is', m11,'m15 is', m15,'m21 is', m21,'m23 is', m23,'m31 is', m31, 'and then', minimalPolynomList['m5(x)'], a, a*a, ar)
    gX = m5
    lister = [m11,m15,m21,m23, m31]
    for elem in lister :
        gX = np.convolve(gX, elem)
        #print(gX)
    #print('gX is', gX)

    gXReal = []
    for elem in gX :
        # print(elem)
        e = elem % 2
        gXReal.append(e)
        
    print('gX is', gX, gXReal)   
    if gEntry == gXReal :
        print('we have a winner', gEntry, gXReal)
    
#getCycles(56)    
#getCycles(25)   
#getCycles(63)

#testcases
a = (1,1)
b = (1,1)
#print(poly.polymul(a,b)) 