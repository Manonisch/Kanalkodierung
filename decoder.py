import numpy as np
import wordgenerator as wg
# Decoder

# HARD Iterative Decoding
# STEP: Stelle H(x) auf
# STEP: Quantise to 1/0
# STEP: Berechne si mit yh,j mod 2
# STEP: Berechne ej
# STEP: Berechne rj, Get Bit , entscheide if bit = 0 , rj = y, else rj = -y
# STEP: dazu Schrittlaufvariable tau je iterationsschritt, dazu können verschieden viele Iterationsschritte festgelegt werden
# STEP: Flip Bits
# Starting iterations, leave everything but change how rj is assembled
# STEP: Do until, iterationsteps are reached or si = 0

# Variables needed: the b, the number of iterations, the controllmatrix, the encodingStruct in "hard" or "soft"

#Test
def getMatrix(hX, n):
    # hX is a number 
    hXBin = format(hX, 'b')
    l = hX.bit_length()
    i = 0
    
    hMatrix = np.zeros((n,n))
    # lines
    while i < n :
        j = 0
        # elements 
        while j < l :
            elem = (i+j)%n
            hMatrix[i,elem] = hXBin[j] 
            j = j + 1
        i = i+1 
    return hMatrix
    
#Test ?
def calculateSyndrom(hMatrix, word):
    newWord =  np.asarray(word)
    syndrom = hMatrix @ word
    i = 0
    syndrom =  syndrom.astype(int)
    #print('syndrom before', syndrom, i)
    lenw = len(word)
    while i < lenw :
        syndrom[i] = syndrom[i]%2
        i = i + 1
    #print(syndrom)    
    # for line in hMatrix i 
    # sum = 0
    # for each bit j in HMatrix 
    #   sum = sum + (hMatrixLine(j) * word(j))
    # syndrom.append(sum%2)      
    return syndrom

def getRjHard(word, y) :
    rj = []
    for bit in word :
        if bit == 0 : 
            rj.append(y)
        else : 
            rj.append(-y)
    return rj    
#TODO
def getRjSoft(word, x) :
    rj = []
    for bit in word :
        newbit = bit
        if newbit < -1 :
            newbit = -1
        elif newbit > 1 :
            newbit = 1
        print(newbit, bit, 2**(x-1) - 1)    
        rj.append(-round(newbit * (2**(x-1) - 1), 0))
    print('aoftrj is', rj)
    return rj

def getEJ(word, hMatrix, si, n):
    i = 0
    ej = []
    while i < n :
        # For Columns
        sumelem = 0
        indexes, = np.where(hMatrix[:,i] == 1)
        # print('indexes is', indexes, 'at i', i)
        for ind in indexes :
            sumelem = sumelem + (2 * ( word[i] ^ si[ind] ) - 1)
            # print('corresponding sums are', sumelem, 'where elem is', (2 * ( word[i] ^ si[ind] ) - 1), 'for yhj', word[i], 'and si', si[ind])
        ej.append(sumelem)
        i = i + 1
    return ej

def getRJ(rj, ej, y, word) :
    newRj = []
    i = 0
    for bit in word :
        newRj.append(min(max((rj[i] - ej[i]), -y), y))
        i = i + 1
    return newRj

def flipBits(rj) :
    newWord = []
    for elem in rj :
        if elem >= 0 :
            #print('got rj', elem, 'and flip to', 0)
            newWord.append(0)
        else :
            #print('got rj', elem, 'and flip to', 1)
            newWord.append(1)
    return newWord
    
#Test -> here be some failures TODO
def calculateSyndromSecond(hMatrix, word, si, n):
    i = 0
    syndrom = []
    while i < n :
        # For Rows
        sumelem = 0
        indexes, = np.where(hMatrix[i,:] == 1)
        #print('indexes is', indexes, 'at i', i)
        for ind in indexes :
            #print('indexes are', ind, 'in row' i)
            sumelem = sumelem + ( word[ind] ^ si[i] )
            #print('corresponding sums are', sumelem, 'where elem is', (word[ind] ^ si[i]), 'for yhj', word[ind], 'and si', si[i])
        sumelem = sumelem % 2
        syndrom.append(sumelem)
        i = i + 1
    return syndrom

def decode(originalString, entryString, iterTimes, hX, encodingStructure, x = 0):

    # STEP: Stelle H(x) auf
    hMatrix = getMatrix(hX)
    n = len(entryString)
    firstRow = hMatrix[:,0]
    y = np.count_nonzero(firstRow)        
    quantword = entryString
    
    if encodingStructure == 'hard' :
        # Only for hard 
        quantWord = wg.hardQuant(entryString)
    else :
        # Only for Soft (liegt zwischen)
        quantWord = wg.softQuantMLG(entryString)
    
    # STEP: Berechne si mit yh,j mod 2
    si = calculateSyndrom(hMatrix, quantWord)

    if sum(si) == 0 :
        print('no correction needed')
        #STEP: is the new Word the Old Word? IF SO it should be counted as correct. If not so, it should be counted as incorrect
        if originalString == quantWord :
            print('is correct')
        else :
            print('decoding failure')
        return 
    rj = []
    ej = []
        
    if encodingStructure == 'hard' :   
        # STEP: Berechne rj0, Get Bit , entscheide if bit = 0 , rj = y, else rj = -y
        rj = getRjHard(quantWord, y)    
    else :        
        # STEP: Berechne rj0, Get Bit , entscheide if bit = 0 , rj = y, else rj = -y
        rj = getRjSoft(quantWord, x)
        
    # STEP: Berechne ej
    ej = getEJ(quantWord, hMatrix, si, n)       
        
    # STEP Berechen neuen rj, dann Flippe!
    newrj = getRJ(rj, ej, y, quantWord)
    
    # STEP: Flip Bits -> WIE? 
    newWord = flipBits(newrj)
    
    # STEP: Berechne si mit yh,j mod 2
    si = calculateSyndromSecond(hMatrix, newWord, si, n)
    
    i = 1
    
    # and now we can build this in iteration 
    while sum(si) != 0 and i < iterTimes :
        quantWord = newWord
            
        rj = newrj
        
        # STEP: Berechne ej
        ej = getEJ(quantWord, hMatrix, si, n)       
        
        # STEP Berechen neuen rj, dann Flippe!
        newrj = getRJ(rj, ej, y, quantWord)

        # STEP: Flip Bits -> WIE? 
        newWord = flipBits(newrj)
                    
        si = calculateSyndromSecond(hMatrix, newWord, si, n)    
        
        i = i + 1
        
    else:
        print('no correction needed')
        #STEP: is the new Word the Old Word? IF SO it should be counted as correct. If not so, it should be counted as incorrect
        if originalString == quantWord :
            print('is correct')
        else :
            print('decoding failure')
        return 
    
    return    
    