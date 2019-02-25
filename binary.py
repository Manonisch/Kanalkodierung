from __future__ import print_function
import chalk

green = chalk.Chalk('green')
bold_green = green + chalk.utils.FontFormat('bold')


from colorama import init
init()

# enter polynom b and sequence a
def bitwiseMod(a,b):
    remainder = 0
    aPlus = a
    sigBitA = a.bit_length()
    sigBitB = b.bit_length()
    while sigBitA >= sigBitB :
        bPlus = b
        # get significant bit at 2^63 and 2^6        
        if sigBitA > sigBitB :
            # -> shift binary sequence b to b' until significant bits align else continue with b' = b
            shifter = sigBitA - sigBitB
            bPlus = bPlus << shifter              
        aPlus = aPlus ^ bPlus
        sigBitA = aPlus.bit_length()
    remainder = aPlus
    return remainder    
    
# if remainder = 1 -> divide all words from 2^0 to 2^63 -> print remainder 
def restpolynom(n, b) :
    r = 1  
    remainder = 0
    remainderDict = {}
    #print('polynom rest list is for' , bin(b))
    while r <= n and remainder != 1 :
        remainder = bitwiseMod(2**r, b)
        remainderDict[str(r)] = remainder    
        #print ('the polynom rest for the potency alpha' , r, 'is ', green(remainder))
        if r == n :
            if remainder != 1 :
                raise Exception('restpolynom r == n, but remainder != 1')
            #else :
                #print(bold_green('****************** polynom is irreduzible and primitive **********************'), b, bin(b), '\n\n')
        #else :
            #if remainder == 1 :
                #print('polynom is irreduzible', b , bin(b), 'with cycle ', r , '\n\n') 
            
        r = r+1
    remainderDict['0'] = 1
    return remainderDict
                
# where g is k1 und n is n    
def testPolynoms(g, n) :
    integer = 2**g
    polynomlist = []
    i = 1
    r = range(0,2**g - 1, 2)
    
    for numbr in r :       
        polynom = integer + numbr + i 
        remainder = bitwiseMod (2**n, polynom)
        if remainder == 1 :
            polynomlist.append(polynom)
            #print('\n', 'the polynom ', bold_green(polynom), bold_green(bin(polynom)), 'has remainder ', remainder, '\n')
            
    return polynomlist 

#needs k1 as g and n as n 
def mainMod(g, n):
    listi = testPolynoms(g,n)
    #print(' \n -------------------------------- \n in GF(2^', g ,') there are ', len(listi), ' irreduzible polynoms :\n', listi, ' \n --------------------------- \n\n' ) 
    for polynom in listi :
        rDict = restpolynom(n, polynom)
        print(rDict)
#Testcases    
#mainMod(6, 63)

#Testcases    
#mainMod(4, 15)

#Testcases    
#mainMod(4, 5)

#def hereBeCycles(n)


#def soWhatAboutMinimalPolynoms(modPol, listOfRest, cycles) :
    # first


