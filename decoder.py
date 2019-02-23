import numpy as np
import wordgenerator as wg
# Decoder functions

def getMatrix(hX, n):
    hXBin = format(hX, 'b')
    l = hX.bit_length()
    i = 0
    
    hMatrix = np.zeros((n,n))
    while i < n :
        j = 0
        while j < l :
            elem = (i+j)%n
            hMatrix[i,elem] = hXBin[j] 
            j = j + 1
        i = i+1 
    return hMatrix
    
def calculateSyndrom(hMatrix, word):
    newWord =  np.asarray(word)
    syndrom = hMatrix @ word
    i = 0
    syndrom =  syndrom.astype(int)
    lenw = len(word)
    while i < lenw :
        syndrom[i] = syndrom[i]%2
        i = i + 1
    return syndrom

def getRjHard(word, y) :
    rj = []
    for bit in word :
        if bit == 0 : 
            rj.append(y)
        else : 
            rj.append(-y)
    return rj    

def getRjSoft(word, x) :
    rj = []
    for bit in word :
        newbit = bit
        if newbit < -1 :
            newbit = -1
        elif newbit > 1 :
            newbit = 1
        rj.append(-round(newbit * (2**(x-1) - 1), 0))
    return rj

def getEJ(word, hMatrix, si, n):
    i = 0
    ej = []
    while i < n :
        sumelem = 0
        indexes, = np.where(hMatrix[:,i] == 1)
        for ind in indexes :
            sumelem = sumelem + (2 * ( word[i] ^ si[ind] ) - 1)
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
            newWord.append(0)
        else :
            newWord.append(1)
    return newWord
    
def calculateSyndromSecond(hMatrix, word, si, n):
    i = 0
    syndrom = []
    while i < n :
        sumelem = 0
        indexes, = np.where(hMatrix[i,:] == 1)
        for ind in indexes :
            sumelem = sumelem + ( word[ind] ^ si[i] )
        sumelem = sumelem % 2
        syndrom.append(sumelem)
        i = i + 1
    return syndrom

    # TODO: NOT NEEDED
def decode(originalString, entryString, iterTimes, hX, encodingStructure, x = 0):
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
    si = calculateSyndrom(hMatrix, quantWord)

    if sum(si) == 0 :
        if originalString == quantWord :
            print('is correct')
        else :
            print('decoding failure')
        return 
    rj = []
    ej = []
        
    if encodingStructure == 'hard' :   
        rj = getRjHard(quantWord, y)    
    else :        
        rj = getRjSoft(quantWord, x)
    ej = getEJ(quantWord, hMatrix, si, n)               
    newrj = getRJ(rj, ej, y, quantWord)
    newWord = flipBits(newrj)
    si = calculateSyndromSecond(hMatrix, newWord, si, n)
    
    i = 1
    while sum(si) != 0 and i < iterTimes :
        quantWord = newWord
            
        rj = newrj
        ej = getEJ(quantWord, hMatrix, si, n)       
        newrj = getRJ(rj, ej, y, quantWord)
        newWord = flipBits(newrj)
        si = calculateSyndromSecond(hMatrix, newWord, si, n)            
        i = i + 1
        
    else:
        if originalString == quantWord :
            print('is correct')
        else :
            print('decoding failure')
        return 
    return    
    