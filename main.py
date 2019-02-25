import numpy as np
import binary 
import wordgenerator as wg
import decoder as dec
import matplotlib.pyplot as plt
import random

#n = 15
#l = 7
n = 63
l = 31

k = n-l
r = l/n
#hX = 2**0+2**4+2**6+2**7
#gX = 2**0+2**4+2**6+2**7+2**8
hX = 2**0+2**1+2**2+2**4+2**8+2**16+2**32
gX = 2**0+2**1+2**3+2**7+2**15+2**31

x = 9

def encode(l, gX, n, hMatrix):    
    word = wg.generateWord(l)
    #print('word', bin(word), word, l)
    encoded = wg.encodeLDPCWord(word, gX, hMatrix, l, n)
    #print('encoded', encoded, word, gX)
    preChannel = wg.dequantiseHard(encoded, n)
    return preChannel

def channel(r, dB, preChannel):
    noise = wg.getNoiseRatio(r, dB)
    #print('noise', noise, r, dB)
    softReceived = wg.addNoise(preChannel, 0, noise)
    #print('softReceived', softReceived, noise, preChannel)
    # Step: Quantisierung am Ende
    quantReceived = wg.hardQuant(softReceived)
    #print('quantReceivedHard', quantReceived, softReceived)
    quantReceivedSoft = wg.softQuantMLG(softReceived)
    #print('quantReceivedSoft', quantReceivedSoft, softReceived)
    return quantReceived, quantReceivedSoft

def decode(hMatrix, quantWord, softReceived, originalString, y, n, iterTimes, type, x):
    si = dec.calculateSyndrom(hMatrix, quantWord)
    newWord = []
    xTwo = 2**(x-1) - 1
    
    if sum(si) == 0 :
        return quantWord
    
    rj = 0
    if type == 'hard' :
        rj = dec.getRjHard(quantWord, y)
    else :
        rj = dec.getRjSoft(softReceived, x)
    
    ej = dec.getEJ(quantWord, hMatrix, si, n)
    newrj = dec.getRJ(rj, ej, y, quantWord)
    newWord = dec.flipBits(newrj)
        
    for i in range(1, iterTimes):
        si = dec.calculateSyndromSecond(hMatrix, newWord, si, n)
        if sum(si) == 0 :
                break
                
        quantWord = newWord
        rj = newrj
        ej = dec.getEJ(quantWord, hMatrix, si, n)   
        if type == 'hard' :     
            newrj = dec.getRJ(rj, ej, y, quantWord)
        else :
            newrj = dec.getRJ(rj, ej, y, quantWord)
 
        newWord = dec.flipBits(newrj)
       
    return newWord   
    
def compare(originalString, newWord, failures, tries):
    tries = tries + 1
    if originalString != newWord :
        failures = failures + 1
    return failures, tries  
    
#    
def plotter(samplesa, samplesb, db_steps):
    print(samplesa, samplesb, db_steps)
    plt.semilogy(db_steps, samplesa, label='hard-reliability')
    plt.semilogy(db_steps, samplesb, label='soft-reliability')
    plt.xlabel('Eb/N0 (dB)')
    plt.ylabel('BER')
    # Place a legend to the right of this smaller subplot.
    plt.legend()
    #print(newWord)
    plt.title("hard/soft reliability-based iterativer MLG")
    plt.savefig('foo.png')
    #plt.show()
    return    

def main(n, l, k, r, hX, gX, dbStart, dbEnd, dbStep, x):

    #np.random.seed(23)
    #STEP: Initialise all the variables
    #Step: Get the HMatrix
    hMatrix = dec.getMatrix(hX, n)
    firstRow = hMatrix[:,0]
    y = np.count_nonzero(firstRow)  
    # For different iterTimes = 6
    iterTimes = 12
    #samplesize = 1000000
    samplesize = 1000
    
    j = dbStart
    type = ['hard', 'soft']
    allplots = []
    for types in type :
        print(types)
        plotterpoints = []
        j = dbStart
        while j <= dbEnd :
            np.random.seed(23)
            random.seed(23)
            failures = 0
            tries = 0
            dB = j    
            for i in range (0, samplesize ) : 
                #STEP: Encode
                preChannel = encode(l, gX, n, hMatrix)
                originalString = wg.hardQuant(preChannel)
                #STEP: Channel 
                received, softReceived = channel(r, dB, preChannel)
                #STEP: Decode
                decoded = decode(hMatrix, received, softReceived, originalString, y, n, iterTimes, types, x)
                #STEP: Compare
                failures, tries = compare(originalString, decoded, failures, tries)
            j = j + dbStep
            plotterpoints.append((failures/tries))
        allplots.append(plotterpoints)
        print('is', type, plotterpoints)
    # STEP: Plot it
    print('starting to plot')
    plotter(np.array(allplots[0]), np.array(allplots[1]), np.arange(dbStart, dbEnd+dbStep, dbStep))
    return
        
 
main(n, l, k, r, hX, gX, 1, 8, 0.1, x)   
    