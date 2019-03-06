from __future__ import print_function
from colorama import init

import numpy as np
import binary 
import wordgenerator as wg
import decoder as dec
import chalk

green = chalk.Chalk('green')
red = chalk.Chalk('red')
bold_green = green + chalk.utils.FontFormat('bold')
bold_red = red + chalk.utils.FontFormat('bold')

init()



#n = 63
#l = 31
n = 15
l = 7
k = n-l
r = l/n
# hX = 2**0+2**1+2**3+2**7+2**15+2**31
hX = 2**0+2**4+2**6+2**7
mean = 0
# gX = 2**0 + 2**1 + 2**2 + 2**4 + 2**8 + 2**16 + 2**32
gX = 2**0+2**4+2**6+2**7+2**8
print(hX,  bin(hX), gX, bin(gX),)
# = x8 +x7 +x6 +x4 + 1 == 1 + 16 + 64 + 128 + 256
dB = 6
np.random.seed(25)

hMatrix = dec.getMatrix(hX, n)
print('hMatrix', hMatrix, hX, n)
firstRow = hMatrix[:,0]
y = np.count_nonzero(firstRow)  
x = 4
word = wg.generateWord(l)
# ..................................................................
#word = 76
print('word', bin(word), word, l)
#encoded = wg.encodeBCHWord(word, hMatrix, l, n)
encoded = wg.encodeLDPCWord(word, gX, hMatrix, l, n)
print('encoded', encoded, word, gX)
preChannel = wg.dequantiseHard(encoded, n)
originalString = wg.hardQuant(preChannel)
#originalString = [1,0,0,0,1,0,1,1,1,0,0,0,0,0,0]
print('preChannel & originalString', preChannel, encoded, originalString)
noise = wg.getNoiseRatio(r, dB)
print('noise', noise, r, dB)
softReceived = wg.addNoise(preChannel, 0, noise)
print('softReceived', softReceived, noise, preChannel)
# Step: Quantisierung am Ende
quantReceived = wg.hardQuant(softReceived)
print('quantReceivedHard', quantReceived, softReceived)
quantReceivedSoft = wg.softQuantMLG(softReceived)
print('quantReceivedSoft', quantReceivedSoft, softReceived)


print('is y', y, firstRow, hMatrix)
#teststring = [1,1,1,0,1,0,1,1,1,0,0,0,0,0,0]
# quantWord = quantReceived
quantWord = quantReceivedSoft
#quantWord = teststring
print('quantisierung hard', quantWord, quantReceived, originalString)
si = dec.calculateSyndrom(hMatrix, quantReceived)
print('si is', si)
if sum(si) == 0 :
    print('no correction needed' , originalString, quantWord)
else :    
    # rj = dec.getRjHard(quantWord, y)
    rj = dec.getRjSoft(quantWord, x)
    print('rj at first is', rj, y)
    # STEP: Berechne ej
    ej = dec.getEJ(quantReceived, hMatrix, si, n)       
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

    iterTimes = 12
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
        print('\n','newWord is flipped to', '\n', newWord, '\n', 'from', '\n', quantWord, i, '\n', 'VS', '\n', originalString)                
        si = dec.calculateSyndromSecond(hMatrix, newWord, si, n)    
        print('si in dec is', si, i)
        i = i + 1
        print('and sum(si) is', sum(si))
        
    else:
        print('no correction needed')
        #STEP: is the new Word the Old Word? IF SO it should be counted as correct. If not so, it should be counted as incorrect
        if originalString == newWord :
            print('\n', 'the word ', bold_green(newWord), 'is ', originalString, 'and that is', bold_green('correct'), '\n')
        else :
            print('\n', 'the word ', bold_red(newWord), 'is not', originalString, bold_red('and that is decoding failure'), '\n')
