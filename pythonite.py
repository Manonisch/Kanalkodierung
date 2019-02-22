from numpy.polynomial import polynomial as P

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
    print('for n:', n)
    for index in cyclesFullList :
        print(' the cycles are', index,'\n')
    return cyclesFullList
    
# What is a polynominal? -> (x+alpha^m1)*(x+alpha^m2)*(x+alpha^m4)*... -> from List at each cycle = x+alpha^listitem    
#def getMinimalPolynoms(cycles, n, restpolynoms) :

import itertools
    
def getMinimalPolynoms(cycles , n, restpolynoms) :  
    minimalPolynoms = {}
    for index in cycles :
        print('the cycle for minimalpolynom m' + str(min(index)) + '(x), is', index, restpolynoms)
        partpol = []
        # STEP: Ausmultiplizieren -> polynomal with 2 unknowns -> This is the big question
        # STEP: Zusammenfassen: if x^3*n^4+x3*n^3 -> x^3(n^4+n^3) + addieren
        r =  range(0, len(index)+1)
        for x in r :
            comb = list(itertools.combinations(index, len(index)-x))
            i = 0
            while i < len(comb) :
                print('single is', comb[i])
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
                strElem = str(element)
                print('elem is', element, restpolynoms[str(element)])
                combInt = combInt ^ restpolynoms[str(element)]
            print(combInt, 'is combInt') 

            
            partpol.append(combInt)

            
        print('partpol for m'+ str(min(index)) + '(x), is', partpol)
        
        #STEP make the list to a single minimalPolynomInteger for better safekeeping... or would it be better to keep them seperated?
        minimalInt = 0
        j = 0
        for elem in partpol :
            included = 0
            if elem > 0 :
                included = 1
            
            minimalInt = minimalInt + 2**j * included 
            j = j + 1
            print('minimalInt is: ', minimalInt, 'j is: ', j)
        
        mKey = 'm'+ str(min(index)) + '(x)'
        minimalPolynoms[mKey] = partpol
        minimalPolynoms[mKey + 'Int'] = minimalInt
        
    print('dict of polynoms is', minimalPolynoms)
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
restpolym = {'0':1,'1':2,'2':4,'3':3,'4':6,'5':7,'6':5,'7':8,'8':1 }
getMinimalPolynoms([[1,2,3],[2,4,5,7]],8,restpolym)

#getCycles(56)    
#getCycles(25)   
#getCycles(63)

#testcases
a = (1,1)
b = (1,1)
print(P.polymul(a,b)) 