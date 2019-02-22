import numpy as np
import binary 
import wordgenerator as wg
import decoder as dec

n = 15
l = 7
k = n-l
r = l/n
hX = 1+16+64+128
mean = 0
gX = 1+16+64+128+256
dB = 10



def main(n, l, k, r, hX, mean, gX, dbStart, dbEnd, dbStep):

    np.random.seed(23)
    #STEP: Initialise all the variables
    #Step: Get the HMatrix
    hMatrix = dec.getMatrix(hX, n)
    firstRow = hMatrix[:,0]
    y = np.count_nonzero(firstRow)  
    # For different iterTimes = 6
    iterTimes = 6
    # ------------ TODO: Make Loop: 1000000 words, dbquantsteps, safe errors
    failures = 0
    tries = 0
    
    #Step: Encode
    preChannel = encode(l, gX, n)
    originalString = wg.hardQuant(preChannel)
    #STEP: Channel 
    received = channel(r, dB, preChannel)
    #STEP: Decode
    decoded = decode(hMatrix, quantWord, originalString, y, n, itertimes)
    #STEP: Compare & Plot
    compare(originalString, decoded, failures, tries)
    return
    
def encode(l, gX, n):    
    word = wg.generateWord(l)
    print('word', bin(word), word, l)
    encoded = wg.encodeBCHWord(word, gX, l)
    print('encoded', encoded, word, gX)
    preChannel = wg.dequantiseHard(encoded, n)
    return preChannel

def channel(r, dB, preChannel):
    noise = wg.getNoiseRatio(r, dB)
    print('noise', noise, r, dB)
    softReceived = wg.addNoise(preChannel, 0, noise)
    print('softReceived', softReceived, noise, preChannel)
    # Step: Quantisierung am Ende
    quantReceived = wg.hardQuant(softReceived)
    print('quantReceivedHard', quantReceived, softReceived)
    quantReceivedSoft = wg.softQuantMLG(softReceived)
    print('quantReceivedSoft', quantReceivedSoft, softReceived)
    return quantReceived

def decode(hMatrix, quantWord, originalString, y, n, itertimes):
    si = dec.calculateSyndrom(hMatrix, quantWord)
    print('si is', si)
    newWord = []
    if sum(si) == 0 :
        print('no correction needed' , originalString, quantWord)
    else :    
        rj = dec.getRjHard(quantWord, y)
        print('rj at first is', rj, y)
        # STEP: Berechne ej
        ej = dec.getEJ(quantWord, hMatrix, si, n)       
        print('ej is', ej)
            
        # STEP Berechen neuen rj, dann Flippe!
        newrj = dec.getRJ(rj, ej, y, quantWord)
        print('newR is', newrj)

        # STEP: Flip Bits -> WIE? 
        newWord = dec.flipBits(newrj)
        print('newword is', newWord)

        # STEP: Berechne si mit yh,j mod 2
        si = dec.calculateSyndromSecond(hMatrix, newWord, si, n)
        print('si at one is', si)

        i = 1

        # and now we can build this in iteration 
        while sum(si) != 0 and i < iterTimes :
            quantWord = newWord
                
            rj = newrj
            
            # STEP: Berechne ej
            ej = dec.getEJ(quantWord, hMatrix, si, n)       
            print('ej in dec is', ej, i)
            # STEP Berechen neuen rj, dann Flippe!
            newrj = dec.getRJ(rj, ej, y, quantWord)
            print('newrj in dec is', newrj, i)
            # STEP: Flip Bits -> WIE? 
            newWord = dec.flipBits(newrj)
            print('newWord is flipped to', newWord, 'from', quantWord, i, 'VS', originalString)                
            si = dec.calculateSyndromSecond(hMatrix, newWord, si, n)    
            print('si in dec is', si, i)
            i = i + 1
            print('and sum(si) is', sum(si))
            
        else:
            print('no correction needed')
            #STEP: is the new Word the Old Word? IF SO it should be counted as correct. If not so, it should be counted as incorrect

    return newWord   
    
def compare(originalString, newWord, failures, tries):
    tries = tries + 1
    if originalString == newWord :
        print('is correct')
    else :
        print('decoding failure')
        failures = failures + 1
    return    
    
def plotter():

    return    