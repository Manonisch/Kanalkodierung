from random import randint
import binary 
import numpy 
import numpy.random as nprnd
import matplotlib.pyplot as plt
import math
 
def generateWord(l) :
    return randint(1, (2**l) - 1)   

def encodeBCHWord(word, gX, l, n) : 
    encodedWord = word 
    shiftWord = word << (gX.bit_length()-1)
    restWord = binary.bitwiseMod(shiftWord, gX)    
    encodedWord = shiftWord + restWord
    return encodedWord
    
def encodeLDPCWord(word, gX, hMatrix, l, n) :
    encodedWord = word    
    k = gX.bit_length()-1
    shiftWord = word << k
    wordArray = []
    wordly =  format(shiftWord, 'b')
    for bit in wordly :
        wordArray.append(int(bit))

    if len(wordArray) < n :
        for i in range(0, (n - len(wordArray))) :
            wordArray.insert(0, 0)

    for j in range(0, k) :    
        # For Rows
        indexes, = numpy.where(hMatrix[j,:] == 1)
        sumelem = 0
        for ind in indexes :
            sumelem = sumelem + wordArray[ind]
        wordArray[l+j] = sumelem % 2

    encodedWord = wordArray
    return encodedWord    

def addNoise(word, mean, noiseRange) :
    newWord = []
    for bit in word :
        noiseArray = numpy.random.normal(mean, noiseRange)
        newBit = int(bit) + noiseArray
        newWord.append(newBit)
    return newWord

def quant (element) :
    if element > 0 :
        element = 0
    elif  element < 0 :
        element = 1
    elif element == 0 :
        element = 1
    return element    
    
# STEP: Quantisation -> Flip Bit    
def hardQuant(word) :    
    quantWord = word
    quantWord = [quant(elem) for elem in quantWord]
    return quantWord

def quantSoftMLG(element) :
    if element > 1 :
        element = 1
    elif element < -1 :
        element = -1     # FOR LATER
    return element    
    
def softQuantMLG(word) :   
    quantWord = word
    quantWord = [quantSoftMLG(elem) for elem in quantWord]
    return quantWord    

def softQuant (word) :
    quantWord = word
    return quantWord    

def dequantiseHard(word, n) :
    prepared = word
    prepareArray = []
    for bit in prepared : 
        newWord = int(bit)
        if newWord == 0 :
            newWord = 1.0
        elif newWord == 1 :
            newWord = -1.0
        prepareArray.append(newWord)
    return prepareArray

def getCodeRate(l, gx) :
    n = l + gx.bit_length - 1 
    codeRate = l/n
    return codeRate
    
def getNoiseRatio(r, db) :
    noise = 1/ (2*r*(10**(db/10)))
    noise = math.sqrt(noise) 
    return noise
    
# TODO NOT NEEDED    
def wordAtChannel(l,gX, dB, rate, n) :
    word = generateWord(l)
    encoded = encodeBCHWord(word, gX, l)
    # Step: Übertragungskanal
    preChannel = dequantiseHard(encoded, n)
    noise = getNoiseRatio(r, dB)
    softReceived = addNoise(preChannel, 0, noise)
    # Step: Quantisierung am Ende
    quantReceived = hardQuant(softReceived)
    
# testcases
