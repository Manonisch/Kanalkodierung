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
gX = 2**0+2**1+2**2+2**4+2**8+2**16+2**32
hX = 2**0+2**1+2**3+2**7+2**15+2**31

x = 4

def encode(l, gX, n, hMatrix):    
    word = wg.generateWord(l)
    #print('word', bin(word), word, l)
    encoded = wg.encodeLDPCWord(word, gX, hMatrix, l, n)
    #print('encoded', encoded, word, gX)
    preChannel = wg.dequantiseHard(encoded, n)
    return preChannel

def channel(r, dB, preChannel, noise):
    # print('noise', noise, r, dB)
    softReceived = wg.addNoise(preChannel, 0, noise)
    # Step: Quantisierung am Ende
    quantReceived = wg.hardQuant(softReceived)
    # print('quantReceivedHard', quantReceived, softReceived)
    quantReceivedSoft = wg.softQuantMLG(softReceived)
    # print('quantReceivedSoft', quantReceivedSoft, softReceived)
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
    elif type == 'soft' :
        rj = dec.getRjSoft(softReceived, x)
    else :
        print('WHAT TYPE IS THIS?', type)
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
    
def compare(originalString, newWord, failures, tries,i):
    tries = tries + 1
    if originalString != newWord :
        #if i > 9000 :
            #print('fail', originalString, newWord)
        failures = failures + 1
        # print("this is wrooooong", originalString, 'is not ', newWord)
    return failures, tries  
    
def plotter(samplesa, samplesb, samplesc, db_steps):
    print(samplesa, samplesb, db_steps)
    plt.semilogy(db_steps, samplesa, label='hard-reliability')
    plt.semilogy(db_steps, samplesb, label='soft-reliability')
    plt.semilogy(db_steps, samplesc, label='noDecoding')
    plt.xlabel('Eb/N0 (dB)')
    plt.ylabel('BER')
    # Place a legend to the right of this smaller subplot.
    plt.legend()
    plt.title("hard/soft reliability-based iterativer MLG")
    plt.savefig('foo3.png')
    return    

def plotterIterHard(samples, db_steps):
    print(samples, db_steps)

    for i in range(0, len(samples)):
        txt = ' ' + str(i+2) + ' iterations'
        plt.semilogy(db_steps, samples[i], label=txt)

    plt.xlabel('Eb/N0 (dB)')
    plt.ylabel('BER')
    plt.legend()
    plt.title("hard/soft reliability-based iterativer MLG - testing iteration times for hard")
    plt.savefig('iter.png')
    return    

def plotterXsoft(samples, db_steps):
    print(samples, db_steps)

    for i in range(0, len(samples)):
        txt = ' ' + str(i+2) + ' -Bit Quantisierung'
        plt.semilogy(db_steps, samples[i], label=txt)

    plt.xlabel('Eb/N0 (dB)')
    plt.ylabel('BER')
    plt.legend()
    plt.savefig('x.png')
    return        
    
def main(n, l, k, hX, gX, dbStart, dbEnd, dbStep, x):

    #STEP: Initialise all the variables
    #Step: Get the HMatrix
    hMatrix = dec.getMatrix(hX, n)
    
    firstRow = hMatrix[:,0]
    y = np.count_nonzero(firstRow) 
    #print(y, 'y is')

    # For different iterTimes = 6
    iterTimes = 6
    #samplesize = 1000000
    samplesize = 1000
    
    r = l/n    
    j = dbStart
    #type = ['hard', 'soft', 'no']
    type = ['soft']
    allplots = []
    #for iterTimes in range(2, 11) :
    for x in range(2, 10) :
    #for types in type :
        types = type[0]
        print(types, iterTimes, x)
        plotterpoints = []
        j = dbStart
        while j <= dbEnd :
        
            np.random.seed(23)
            random.seed(23)
            failures = 0
            tries = 0
            dB = j
            noise = wg.getNoiseRatio(r, dB)    
            wordtype = []
            
            for i in range (0, samplesize ) : 
                if types == 'no' :
                    #STEP: Encode
                    preChannel = encode(l, gX, n, hMatrix)
                    originalString = wg.hardQuant(preChannel)
                    #STEP: Channel 
                    received, softReceived = channel(r, dB, preChannel, noise)
                    #STEP: No Decoding
                    decoded = received
                    #STEP: Compare
                    failures, tries = compare(originalString, decoded, failures, tries, i)
                    
                else :
                    #STEP: Encode
                    preChannel = encode(l, gX, n, hMatrix)
                    originalString = wg.hardQuant(preChannel)
                    #STEP: Channel 
                    received, softReceived = channel(r, dB, preChannel, noise)
                    #STEP: Decode
                    decoded = decode(hMatrix, received, softReceived, originalString, y, n, iterTimes, types, x)
                    #STEP: Compare
                    failures, tries = compare(originalString, decoded, failures, tries, i)
            
            j = j + dbStep
            plotterpoints.append((failures/tries))
        
        allplots.append(plotterpoints)
        print('is', type, plotterpoints)
    # STEP: Plot it
    print('starting to plot')
    #plotter(np.array(allplots[0]), np.array(allplots[1]), np.arange(dbStart, dbEnd+dbStep, dbStep))
    #plotter(np.array(allplots[0]), np.array(allplots[1]), np.array(allplots[2]), np.arange(dbStart, dbEnd+(dbStep), dbStep))
    #plotterIterHard(allplots, np.arange(dbStart, dbEnd+(dbStep), dbStep))
    plotterXsoft(allplots, np.arange(dbStart, dbEnd+(dbStep), dbStep))
    return
        
main(n, l, k, hX, gX, 1, 8, 0.1, x)   
    