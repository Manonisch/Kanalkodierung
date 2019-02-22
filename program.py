 
sequence = [5, 7, 10, 11, 14, 15, 17, 20, 21, 22, 25, 28, 34, 35, 37, 39, 40, 42, 44, 49, 50, 51, 56, 57, 60]
numberNS = 8

def isOrdered(seq, orderedSeq):
    storagesA = []
    storagesB = []
    storagesC = []
    storagesD = []
    storagesE = []
    storagesF = []

    seqA = orderedSeq['A']
    seqB = orderedSeq['B']
    seqC = orderedSeq['C']
    seqD = orderedSeq['D']
    seqE = orderedSeq['E']
    seqF = orderedSeq['F']
    
    for index in range(len(seq)):

        if seqA.count(seq[index]):
            storagesA.append(seq[index])
        elif seqB.count(seq[index]):
            storagesB.append(seq[index])
        elif seqC.count(seq[index]):
            storagesC.append(seq[index])
        elif seqD.count(seq[index]):
            storagesD.append(seq[index])
        elif seqE.count(seq[index]):
            storagesE.append(seq[index])
        elif seqF.count(seq[index]):
            storagesF.append(seq[index])
                
    value = False    
    if len(storagesA) > 0 and len(storagesB) > 0 and len(storagesC) > 0 and len(storagesD) > 0 and len(storagesE) > 0 and len(storagesF) > 0 :   
        value = True
    
    print('storages are','A', storagesA ,'B', storagesB,'C', storagesC,'D', storagesD,'E', storagesE,'F', storagesF)
    return value

def calcSequences(seq, nrNS):
    steps = 1
    print('starting calc', seq)
    while steps < (max(seq)/nrNS):
        storedSequence = [];    
        for index in range(len(seq)):
            multiplier = 0
            storedSequence = [seq[index]]
            
            while seq.count(seq[index]+steps*multiplier) >= 1 and multiplier < nrNS : 
                multiplier = multiplier + 1;
              
                if seq.count(seq[index]+steps*multiplier) :
                    storedSequence.append(seq[index]+steps*multiplier)
                    
                if multiplier == nrNS :
                   orderedSequence = {'A': [5, 10, 20, 40, 17,34], 'B': [11,22,44,25,50,37], 'C' : [15,30,60,57,51,39], 'D' : [21,42], 'E' : [23,46,29,58,53,43], 'F' : [31,62,61,59,55,47]} 
                   
                   print('found full sequence ', storedSequence, 'of', nrNS , 'with stepwidth', steps,isOrdered(storedSequence, orderedSequence))             
        steps = steps + 1
    return 
    
    
calcSequences(sequence, numberNS)    

sequenceTwo = [5,10,11,15,17,20,21,22,23,25,29,30,31,34,37,39,40,42,43,44,46,47,50,51,53,55,57,58,59,60,61,62]

calcSequences(sequenceTwo, 6)

#calcSequences(sequence, numberNS)


#orderedSequence = {'A': [5, 10, 20, 40, 17,34], 'B': [11,22,44,25,50,37], 'C' : [15,30,60,57,51,39], 'D' : [21,42], 'E' : [23,46,29,58,53,43], 'F' : [31,62,61,59,55,47]}
