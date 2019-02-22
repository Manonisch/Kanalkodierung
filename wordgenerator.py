from random import randint
import binary 
import numpy 
import numpy.random as nprnd
import matplotlib.pyplot as plt
 
def generateWord(l) :
    word = 0
    i = 0
    while i < l :
        word =  word + (2**i)*randint(0,1)
        i = i + 1
    return word    

def encodeBCHWord(word, gX, l, n) : 
    encodedWord = word 
    shiftWord = word << (gX.bit_length()-1)
    print('before', bin(shiftWord), gX.bit_length()-1)
    restWord = binary.bitwiseMod(shiftWord, gX)    
    print('after', bin(restWord))
    encodedWord = shiftWord + restWord
    print('after', bin(encodedWord))
    print('the word: ', word, bin(word), 'was encoded with g(x)', gX, bin(gX), 'zu' , encodedWord, bin(encodedWord))
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
        j = n - len(wordArray)
        i = 0
        while i < j :
            #print('inserting empty spaces', courses, n, len(prepareArray))
            wordArray.insert(0, 0)
            i = i + 1
    j = 0
   
    while j < k :
        # For Rows
        indexes, = numpy.where(hMatrix[j,:] == 1)
        sumelem = 0
        for ind in indexes :
            #print('sum, sum', sumelem, wordArray[ind])
            sumelem = sumelem + wordArray[ind]
            # print('corresponding sums are', sumelem, 'where elem is', (2 * ( word[i] ^ si[ind] ) - 1), 'for yhj', word[i], 'and si', si[ind])
        wordArray[l+j] = sumelem % 2
        j = j + 1
    encodedWord = wordArray
    #print('is encoded Word', encodedWord)
    return encodedWord    

def addNoise(word, mean, noiseRange) :
    newWord = []
    #print('it starts with', word)
    for bit in word :
        #print(bit)
        noiseArray = numpy.random.normal(mean, noiseRange)
        newBit = int(bit) + noiseArray
        newWord.append(newBit)
    #plt.plot(noiseArray,'-')
    #print(newWord)
    #plt.show()
    return newWord

def quant (element) :
    if element >= 0 :
        #print('to one', element)
        element = 1
    else :
        #print('to zero', element)
        element = 0     # FOR LATER
    #print(element)
    return element    
    
# STEP: Quantisation -> Flip Bit    
def hardQuant(word) :    
    quantWord = word
    #print(quantWord)
    quantWord = [quant(elem) for elem in quantWord]
    
    print('receiving', quantWord)        
    return quantWord

def quantSoftMLG(element) :
    if element > 1 :
        #print('to one', element)
        element = 1
    elif element < -1 :
        #print('to -1', element)
        element = -1     # FOR LATER
    #print(element)
    return element    
    
def softQuantMLG(word) :   
    quantWord = word
    quantWord = [quantSoftMLG(elem) for elem in quantWord]
    print('receiving', quantWord)        
    return quantWord    

def stepQuant(word, steps) :
    quantWord = word
    # make array of length steps, filled with 0, 0+ 1/steps, ... until 1
    quantSteps = numpy.linspace(0.0,1.0, steps+1)
    #print(quantSteps)
    # for each element, map the element to the closest steprange
    #for element in quadWord 
            
    return quantWord

def softQuant (word) :
    quantWord = word
    return quantWord    

def dequantiseHard(word, n) :
    #prepared = format(word, 'b')
    prepared = word
    print('original Word', prepared)
    prepareArray = []
    for bit in prepared : 
        newWord = int(bit)
        if newWord == 0 :
            #print('flipping')
            newWord = -1
        prepareArray.append(newWord)
    #ADJUSTIN WORD LENGTH!
    #if len(prepareArray) < n :
    #    courses = n - len(prepareArray)
        #print('inserting empty spaces', courses, n, len(prepareArray))
    #    i = 0
    #    while i < courses :
            #print(i, courses, prepareArray)
    #        prepareArray.insert(0, -1)    
    #        i = i+1
    print('prepare', prepareArray)
    return prepareArray

def getCodeRate(l, gx) :
    n = l + gx.bit_length - 1 
    codeRate = l/n
    return codeRate
    
def getNoiseRatio(r, db) :
    noise = 1/ 2*r*10**(db/10)
    return noise
    
def wordAtChannel(l,gX, dB, rate, n) :
    numpy.random.seed('turtle')

    word = generateWord(l)
    encoded = encodeBCHWord(word, gX, l)
    # Step: Übertragungskanal
    preChannel = dequantiseHard(encoded, n)
    noise = getNoiseRatio(r, dB)
    softReceived = addNoise(preChannel, 0, noise)
    # Step: Quantisierung am Ende
    quantReceived = hardQuant(softReceived)
    
# testcases
i = 18
word = 12
l = 13
a = 12345
