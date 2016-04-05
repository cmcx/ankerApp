# umsetzung von rodeanch.xls (by Alain Fraysse, http://alain.fraysse.free.fr)
# -*- coding: utf-8 -*-

# version 0.91  - divide graphics and special case into three separate files: special case (incl. basic functions), graphics
# version 0.9   - trying to clean the code...
#               - trying harder to clean the code
#               - translate everything into german



import math
import pylab

# Introduction

print('Guten Tag. Dieses Programm kann Ihnen helfen, das richtige Ankergeschirr für eine bestimmte Windsituation auszuwählen.')
print('Dazu werden einige Daten abgefragt. Über Gleichungen, die Sie im Quellcode des Programms nachlesen können, werden dann Empfehlungen für drei Szenarien ausgegeben.')
#print('Schließlich gibt das Programm einige Grafiken aus, die eine Übersicht über Lasten und Leinenlängen bei verschiedenen Windstärken liefern.')
print('Disclaimer: Die Empfehlungen des Programms basieren auf den Formeln von Alain Fraysse (http://alain.fraysse.free.fr) und das heißt auf theoretischen Überlegungen. Sie können bestenfalls eine Hilfestellung sein und ersetzen NICHT ein Assessment der konkreten Situation durch den Schiffsführer oder die Schiffsführerin!')
print('')
print('Bitte geben Sie jetzt Ihre Daten ein und bestätigen Sie die Eingabe jeweils mit der Entertaste.')


# Variables
boatLength = float(raw_input('Bootslänge (Meter): '))
chainLength = float(raw_input('Länge der Ankerkette (Meter): '))
chainDiameter = int(raw_input('Kettendurchmesser (mm): '))

anchorWeight = int(raw_input('Ankergewicht (kg): '))

# anchorType 1 = classic, 2 = hhp, expect-schleife einbauen!
anchorType = int(raw_input('Ankertyp (1 = Delta, Bügel, Rocna, Spade; 2 = andere) :'))
#while int(anchorType) != 1 or 2:
#    print('Ihre Eingabe lautet' + str(anchorType) + '. Damit kann ich nicht arbeiten.')
#    anchorType = raw_input('Bitte geben Sie entweder 1 oder 2 ein, je nach Ankertyp (1 = Delta, Bügel, Rocna, Spade; 2 = andere) : ')
    
windSpeed = int(raw_input('Windgeschwindigkeit (kn): '))

waterDepth = float(raw_input('Wassertiefe ohne Freibord (m): '))
freeboard = float(raw_input('Freibord (m): '))
seabedHoldingInput = int(raw_input('Ankergrund (1=exzellent, 2=gut, 3=mäßig, 4=schlecht): '))

seabedHoldingTable = {4:5, 3:12, 2:25, 1:40} # {poor:5, medium:12, good:25, excellent:40}
seabedHoldingNames = {4:"schlecht", 3:"maessig", 2:"gut", 1:"excellent"}
seabedHolding = seabedHoldingTable[seabedHoldingInput]

angulation = int(raw_input('Maximaler Winkel der Kette am Anker (Grad, ganzzahlig, ein guter Wert wäre 5 Grad): ')) # welchen maximalen winkel darf die kette am anker haben?

# helper variables
p1 = 0.02385 * (chainDiameter**2)

# constants
massPower = 1.4 # wird im xls-sheet leider nicht weiter erklärt, ich denke an massenträgheitskoeffizient
K = 0.003
p = 1.66 # K und p sind Konstanten, unterschiedlich für Katamarane und Monohulls, hier sind die Werte für Monohulls festgelegt)

# functions

def printout(x,y):
    print x + " = " + str(y)

def hhp(anchorWeight):
    '''
    computes the reduced weight for anchors with High Holding Power (Bügel, Delta, Rocna, Spade)
    '''
    return int(anchorWeight - (anchorWeight * 30/100))

# ancre = =(tension/kfond)^(1/m_p)
def ancre(tension, seabedHolding, massPower):
    return (tension / seabedHolding)**(1/massPower)

# minimal anchor weight all chain = ancre*reduc^(-1/m_p)
def minimalAnchorweight(tension, seabedHolding, massPower, reduc):
    '''
    liefert das minimale Ankergewicht, nimmt als Argumente tension, seabedHolding, massPower und reduc/reduc2
    '''
    return ancre(tension, seabedHolding, massPower) * (reduc**(-1/massPower))
            
# testangul =(ch1_^2-fond^2)*P1_/(2*fond*tension)
def testangul(tension, chainLength, depth, p1):
    return ((chainLength**2) - (depth**2)) * (p1 / (2 * depth * tension))

# sinalpha = WENN(testangul<1;(1-testangul)*fond/ch1_;0)
def sinalpha(depth, chainLength, tension, p1):
    if testangul(tension, chainLength, depth, p1) < 1:
        sinalpha = (1 - testangul(tension, chainLength, depth, p1)) * depth / chainLength
    else:
        sinalpha = 0
    return sinalpha

# reduc = 1-(alpha/alpha0)^2
def reduction1(depth, chainLength, tensionAllChain, p1):
    return 1 - ((math.asin(sinalpha(depth, chainLength, tensionAllChain, p1)) / math.radians(20))**2) 

# reduc2 = 1-(alpha2/alpha0)^2
def reduction2(angulation):
    return 1 - ((math.radians(angulation)/math.radians(20))**2)

# function for computing the dynamic tension (only used in the graphing)

def tensionDyn(windSpeed, boatLength=11.6):
    tensionStatic = 0.003 * (boatLength**1.66) * (windSpeed**2)
    return tensionStatic * 2.2 #(mixed rode)
    
def tensionStat(windSpeed, boatLength=11.6):
    return 0.003 * (boatLength**1.66) * (windSpeed**2)

# Calculations
chainWeight = p1 * chainLength
depth = waterDepth + freeboard


# fardage = K*long^p*vent^2; fardage = tension

tensionStatic = K * (boatLength**p) * (windSpeed**2)
tensionDynamic = tensionStatic * 2.2 #(mixed rode)
tensionAllChain = tensionStatic * 5 #(all chain rode)



alpha = math.asin(sinalpha(depth, chainLength, tensionAllChain, p1))
alpha0 = math.radians(20)
alpha2 = math.radians(angulation)

reduc2 = reduction2(angulation)
reduc1 = reduction1(depth, chainLength, tensionAllChain, p1)


print("################")
print("Ergebnisse")
print("################")
print("")
print("Kettengewicht: " + str(int(chainWeight)) + " kg")
print("Gesamttiefe: " + str(depth) + " m")
print("Statische Last, theoretisch " + str(tensionStatic) + " daN")
print("Dynamische Last mit Kette: " + str(tensionAllChain) + " daN")
print("Dynamische Last mit Kette plus Leine :" + str(tensionDynamic) + " daN")

print("")
print("##########")
print("Szenarien")
print("##########")
# Results
# 1st case: Whole available chain alone
#--------------------------------------------

if reduc1 >= 0 and chainLength > depth:
    # minimal anchor weight all chain = ancre*reduc^(-1/m_p)
    minimalAnchorWeight1 = minimalAnchorweight(tensionAllChain, seabedHolding, massPower, reduc1)
    angulationAllChain = math.degrees(alpha)
    scopeAllChain = chainLength / depth
                 
    print("Fall 1: Nur die verfügbare Kette")
    print("--------------------------------")
    print("Last auf der Kette: " + str(tensionAllChain))
    print("Winkel der Kette am Anker: " + str(angulationAllChain))
    print("Minimales Ankergewicht: " + str(minimalAnchorWeight1))
    print("Verhältnis Tiefe:Kettenlänge: " + str(scopeAllChain))
else:
    print("Die Berechnung der Daten fuer Fall 1 geht nur, wenn die Kettenlänge mindestens der angegebenen Tiefe entspricht und")
    print("der Winkel am Anker nicht groeßer ist als 20 Grad.")
    if reduc1 <= 0:
        print("Der voraussichtliche Winkel der Kette am Anker ist unter den angegebenen Bedingungen größer als 20 Grad.")
    if chainLength < depth:
        print("Die Kette ist kuerzer als das Wasser tief ist - der Anker kommt leider nicht am Grund an!")
        

# 2nd case: all chain rode with given angulation

# helper variables
def allChainRode(tension, depth, angulation, seabedHolding, massPower, reduction, p=1.66):
                        
    hb = tensionAllChain / (p * depth)
    v2 = hb * math.tan(math.radians(angulation))

        # angulation
        # minimal anchor weight = ancre*reduc2^(-1/m_p)
    minimalAnchorWeight2 = minimalAnchorweight(tensionAllChain, seabedHolding, massPower, reduction)
        # minimal chain length = fond*(WURZEL(1+2*b/COS(alpha2)+v2_^2)-v2_)
    minimalChainLength = depth * (math.sqrt(1 + (2 * hb / math.cos(alpha2)) + (v2**2)) -v2)
        # scope
    scope2 = minimalChainLength / depth
    return minimalAnchorWeight2, minimalChainLength, scope2

minimalAnchorWeight2, minimalChainLength, scope2 = allChainRode(tensionAllChain, depth, angulation, seabedHolding, massPower, reduc2)
print('')
print('Fall 2: Nur Kette bei einem gegebenen Winkel von ' + str(angulation) + ' Grad')
print('------------------------------------------------------------')
print('Zug auf der Kette: ' + str(tensionAllChain) + ' daN')
print('Minimales Ankergewicht mit klassischem Anker: ' + str(minimalAnchorWeight2) + ' kg')
print('Minimales Ankergewicht mit HHP-Anker: ' + str(hhp(minimalAnchorWeight2)) + ' kg')
print('Minimale Kettenlänge: ' + str(int(minimalChainLength)) + ' m')
print('Verhältnis Kettenlänge/Tiefe: ' + str(scope2))

# 3rd case: Available chain + nylon with given angulation

def nylonLength(tensionDynamic, chainLength, angulation, depth):
    d3 = tensionDynamic / 1.66 * math.cos(math.radians(angulation))

    # hch = d3_*(WURZEL(1 + 2*ch1_*SIN(alpha2)/d3_ + (ch1_/d3_)^2) -1)
    hch = d3*(math.sqrt(1 + (2 * chainLength * math.sin(math.radians(angulation)) / d3) + ((chainLength/d3)**2))-1)

        # nylonLength = WENN(f3_>0;f3_/SIN(beta);0) | f3 = depth-hch
    # tanbeta = ch1_*P1_/tension+TAN(alpha2)
    tanbeta = (chainLength * 1.66 / tensionDynamic) + math.tan(math.radians(angulation))

    # beta =ARCTAN(tanbeta)
    beta = math.atan(tanbeta)

    if depth-hch > 0:
              nylonLength = (depth-hch) / math.sin(beta)
    else:
              nylonLength = 0
    return nylonLength
                    
        # anchorWeight same as in 2nd case
minimalAnchorweight3 = minimalAnchorweight(tensionDynamic, seabedHolding, massPower, reduc2)

#print('d3 = ' + str(d3))
#print('hch = ' + str(hch))
#print('depth-hch = ' + str(depth-hch))
#print('tanbeta = ' + str(tanbeta))

rodeLength = chainLength + nylonLength(tensionDynamic, chainLength, angulation, depth)
scope = rodeLength / depth
print('')
print('Fall 3: gesamte Kette plus Leine mit einem gegebenen Winkel von ' + str(angulation) + ' Grad')
print('--------------------------------------------------------------------------')
print("Minimales Ankergewicht mit klassischem Anker (kg): " + str(int(minimalAnchorweight3)))
print("Minimales Ankergewicht mit HHP-Anker (kg): " + str(hhp(minimalAnchorweight3)))
print("Empfohlene Laenge der Ankerleine, falls die Kette alleine nicht ausreicht: " + str(nylonLength(tensionDynamic, chainLength, angulation,depth)) + " m")
print("Gesamtlänge: " + str(rodeLength) + " m")
print("Verhältnis Gesamtlänge zu Tiefe: " + str(scope))

# Case 4: kette plus leine for a given anchor weight


def rodeLength4(windSpeed, depth, anchorWeight, chainLength, tensionDynamic, tensionAllChain, seabedHolding, massPower, p1):
    '''
    Case 4: kette plus leine for a given anchor weight
    compute maximum angulation and minimal rode length for given windspeed and anchorweight
    could be helpful when swinging room is reduced or the water is very deep
    rode = (chainLength, chainDiameter
        '''
    # assert an angulation of 0 and compute the minimal anchorweight and chain rode
    # 
    # compare the actual anchorweight with the minimal anchorweight
    # if actualAnchorWeight > minimalAnchorWeight: raise angulation +1, compare again, until mAW > aA, then take the last angulation where aA > mAW

    angulation = 0
    reduc2 = reduction2(angulation)
    maw = minimalAnchorweight(tensionDynamic, seabedHolding, massPower, reduc2)
    #print ('maw = ' + str(maw))
    #print ('ankergewicht = ' + str(anchorWeight))
    #print ('anchorweight > maw: ' + str(anchorWeight > maw))
    
    if anchorWeight > maw:
        while anchorWeight > maw and angulation < 19:
            angulation += 1
            reduc1 = reduction1(depth, chainLength, tensionAllChain, p1)
            reduc2 = reduction2(angulation)
            #print ('reduc2 = ' + str(reduc2) + ' for angulation of ' + str(angulation) + ' degrees')
            maw = minimalAnchorweight(tensionDynamic, seabedHolding, massPower, reduc2)
            #print ('maw = ' + str(maw))
        if nylonLength(tensionDynamic, chainLength, angulation, depth) > 0 or allChainRode(tensionAllChain, depth, angulation, seabedHolding, massPower, reduc2)[1] > 40:
            return "kette plus leine", angulation-1, nylonLength(tensionDynamic, chainLength, angulation-1, depth), minimalAnchorweight(tensionDynamic, seabedHolding, massPower, reduction2(angulation-1))
        else:            
            rode = allChainRode(tensionAllChain, depth, angulation, seabedHolding, massPower, reduc2)
            return "nur kette", angulation-1, rode[1], rode[0] # rode[1] = minimalAnchorWeight, minimalChainLength, scope
    else:
        return False
    
rode4 = rodeLength4(windSpeed, depth, anchorWeight, chainLength, tensionDynamic, tensionAllChain, seabedHolding, massPower, p1)


print("")
print("Fall 4: Minimale Geschirrlänge (Kette oder Kette plus Ankerleine) mit gegebenem Ankergewicht")
print("---------------------------------------------------------------------------------------------")

if rode4 == False:
    #print("Under the given conditions, your actual anchor ("+str(anchorWeight)+" kg) is lighter than the minimal anchor weight calculated. Please find a better spot.")
    print("Unter den gegebenen Bedingungen ist Ihr Anker (" + str(anchorWeight) + " kg) leichter als das berechnete minimale Ankergewicht. Bitte suchen Sie sich einen besseren Ankerplatz oder nehmen Sie einen besseren Anker.")

else:
    print("Ihr Anker wiegt " + str(anchorWeight) + "kg.")
    print("Die Kette wird am Anker einen Winkel von " + str(rode4[1]) + " Grad haben.")
    print("Das Geschirr sollte aus " + rode4[0] + " bestehen.")
    if rode4[0] == "kette plus leine":
        print("Sie brauchen " + str(rode4[2]) + " Meter Ankerleine zusätzlich zur Kette.")
    else:
        print("Legen Sie " + str(rode4[2]) + " Meter Kette plus 6 Meter Ankerleine (die Berechnung beinhaltet den dämpfenden Effekt der Leine).")


    # if actualAnchorWeight < minimalAnchorWeight: reduce angulation -1, compare again until aA > mAW, then return results

    print('Gutes Ankern!')

# Data for different seabed holdings (1-4)
print("")
print("Überblick: Ankergeschirr für unterschiedliche Haltekoeffizienten des Ankergrunds mit Minimallängen")
print("--------------------------------------------------------------------------------")

for i in range(1,5):
    seabedHolding = seabedHoldingTable[i]
    rode4 = rodeLength4(windSpeed, depth, anchorWeight, chainLength, tensionDynamic, tensionAllChain, seabedHolding, massPower, p1)
    
    if rode4 == False:
        #print("With " + str(seabedHoldingNames[i]) + " seabed holding, your actual anchor ("+str(anchorWeight)+" kg) is lighter than the minimal anchor weight calculated. Please find a better spot.")
        print("Für " + str(seabedHoldingNames[i]) + "en Ankergrund ist Ihr Anker ("+str(anchorWeight)+" kg) leichter als das berechnete minimale Ankergewicht. Bitte versuchen Sie es mit einem schwereren Anker oder auf besserem Ankergrund.")
    else:
        #print("With " + str(seabedHoldingNames[i]) + " seabed holding, the rode needs to consist of " + rode4[0])
        print("Für " + str(seabedHoldingNames[i]) + "en Ankergrund brauchen Sie als Ankergeschirr " + rode4[0])
        if rode4[0] == "kette plus leine":
            #print("You need to attach " + str(rode4[2]) + " metres of nylon to your chain.")
            print("Sie brauchen " + str(rode4[2]) + " Meter Ankerleine zusätzlich zu Ihrer Kette.")
        else:
            print("Legen Sie " + str(rode4[2]) + " Meter Kette aus plus mindestens sechs Meter Ankerleine für den Dämpfungseffekt.")

