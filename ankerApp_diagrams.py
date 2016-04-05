#!/usr/bin/python
# -*- coding: utf-8 -*-

# 0.93 tabellen für notwendige kettenlängen nach tiefen und windgeschwindigkeiten
# 0.92  sechste Tabelle hinzugefügt (ankergewicht für haltekoeffizienten und windgeschwindigkeiten)
# 0.91 - make two programs, one for the special case, one for the diagrams

# rodeanch part 2 - diagrams


import math
import pylab


print('Nachfolgend werden Ihnen eine Reihe von Diagrammen angezeigt, aus denen Sie die nötige Länge Ihres Ankergeschirrs ablesen können.')
print('Bei der Berechnung wird eine von der Windgeschwindigkeit abhängige dynamische Last auf das Ankergeschirr zugrunde gelegt, die den dämpfenden Effekt')
print('von mindestens sechs Metern Ankerleine mit einberechnet!')
print('Selbst wenn ausreichend Kette zur Verfügung steht sollte also eine wenigstens sechs Meter lange Entlastungsleine ins Ankergeschirr integriert werden.')
print('Die Berechnung geht davon aus, dass der Winkel der Kette am Anker bis zu fünf Grad (gegenüber der Horizontalen) betragen kann.')
print('Die gesamte Mathematik wurde aus einer Excel-Tabelle von Alain Fraysse (http://alain.fraysse.free.fr) übernommen.')
print('Disclaimer: Die berechneten Diagramme basieren auf theoretischen Annahmen und können höchstens bei einer Einschätzung helfen, sind aber keine zuverlässigen Vorgaben für spezifische Situationen!')
print('Die berechneten Werte gelten nur für Monohulls. Das originale Excel-Sheet von Alain Fraysse ermöglicht aber auch die Berechnung von Geschirrlängen für Multihulls.')
print('')
print('Die erste Tabelle zeigt die nötige Geschirrlänge für Tiefen von 4-10 Metern. Die Tiefe setzt sich zusammen aus Wassertiefe und Freibord! ')
print('Bei einer Wassertiefe von 7 Metern und einem Freibord von 1 Meter wäre also der Wert für eine Tiefe von 8 Metern ausschlaggebend.')
print('Die zweite Tabelle zeigt die nötige Geschirrlänge für Tiefen von 12-24 Metern. Auch hier gilt Tiefe = Wassertiefe plus Freibord.')
print('Die dritte Tabelle zeigt die theoretische Last auf dem Ankergeschirr, die dynamische Last (Kette plus Leine) und die Last, wenn nur Kette verwendet wird.')
print('Die vierte und fünfte Tabelle zeigen Vergleichswerte für verschiedene Bootslängen und dienen eher einer Einschätzung der Berechnungsgrundlage als')
print('dem praktischen Nutzen an Bord.')
print('Die sechste Tabelle zeigt das minimale Ankergewicht bei einer optimalen Zugrichtung (max. 5 Grad) der Kette am Anker für verschiedene Windgeschwindigkeiten')
print('und verschiedene Haltekoeffizienten des Ankergrunds (exzellent bis schlechter Ankergrund). Die Tabelle gilt nur für Anker mit einer High Holding Power (z.B. Delta, Rocna, Spade, Bügel). Klassische Anker müssen für die gleiche Haltekraft etwa 30 Prozent schwerer gewählt werden.')
print('')
print('Bitte geben Sie jetzt die Schiffsdaten ein.')
print('')



# Variables
boatLength = float(raw_input('Bootslänge (Meter): '))
chainLength = float(raw_input('Länge der Ankerkette (Meter): '))
chainDiameter = int(raw_input('Kettendurchmesser (mm): '))

anchorWeight = int(raw_input('Ankergewicht (kg): '))

# anchorType 1 = classic, 2 = hhp, expect-schleife einbauen!
#anchorType = int(raw_input('Ankertyp (1 = Delta, Bügel, Rocna, Spade; 2 = andere) :'))
#while int(anchorType) != 1 or 2:
#    print('Ihre Eingabe lautet' + str(anchorType) + '. Damit kann ich nicht arbeiten.')
#    anchorType = raw_input('Bitte geben Sie entweder 1 oder 2 ein, je nach Ankertyp (1 = Delta, Bügel, Rocna, Spade; 2 = andere) : ')
    
#windSpeed = int(raw_input('Windgeschwindigkeit (kn): '))

#waterDepth = float(raw_input('Wassertiefe ohne Freibord (m): '))
#freeboard = float(raw_input('Freibord (m): '))
#seabedHoldingInput = int(raw_input('Ankergrund (1=exzellent, 2=gut, 3=mäßig, 4=schlecht): '))

seabedHoldingTable = {4:5, 3:12, 2:25, 1:40} # {poor:5, medium:12, good:25, excellent:40}
seabedHoldingNames = {4:"schlecht", 3:"maessig", 2:"gut", 1:"excellent"}
#seabedHolding = seabedHoldingTable[seabedHoldingInput]

#angulation = int(raw_input('Maximaler Winkel der Kette am Anker (Grad, ganzzahlig, ein guter Wert wäre 5 Grad): ')) # welchen maximalen winkel darf die kette am anker haben?

# helper variables
p1 = 0.02385 * (chainDiameter**2)

# constants
massPower = 1.4 # wird im xls-sheet von Alain Fraysse leider nicht weiter erklärt, ich denke an massenträgheitskoeffizient
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

def tensionDyn(windSpeed, boatLength):
    tensionStatic = 0.003 * (boatLength**1.66) * (windSpeed**2)
    return tensionStatic * 2.2 #(mixed rode)
    
def tensionStat(windSpeed, boatLength):
    return 0.003 * (boatLength**1.66) * (windSpeed**2)

def tensionAllChain(windspeed, boatlength):
    return tensionStat(windspeed, boatlength) * 5
                       
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


# Calculations
chainWeight = p1 * chainLength
#depth = waterDepth + freeboard


# fardage = K*long^p*vent^2; fardage = tension

#tensionStatic = K * (boatLength**p) * (windSpeed**2)
#tensionDynamic = tensionStatic * 2.2 #(mixed rode)
#tensionAllChain = tensionStatic * 5 #(all chain rode)

def alpha(depth, chainLength, tensionAllChain, p1):
    return math.asin(sinalpha(depth, chainLength, tensionAllChain, p1))

def alpha2(angulation):
    return math.radians(angulation)

alpha0 = math.radians(20)

#reduc2 = reduction2(angulation)
#reduc1 = reduction1(depth, chainLength, tensionAllChain, p1)





# case x1: rode lengths for wind speeds

# build two lists and plot them against each other in a regular graph

def nylonLengthList(depth, chainLength, boatLength, angulation=5):
    '''
    return a list of nylon lengths for a given depth and a range of windspeeds
    '''
    # open the empty list
    nylonLengths = []
    for j in range(1, 70):    # fill the list
        #j += 1
        nylonLengths.append(nylonLength(tensionDyn(j, boatLength),chainLength , angulation, depth))
       # print tensionDyn(j)
    return nylonLengths

# generate a list of windspeeds from 1 to 70
windSpeeds = []
for i in range(1,70):
    windSpeeds.append(i)

# generate a list of lists with nylonlengths for depths from 3 to 10 meters in steps of 1 meter
nylonLengthLists = []
for i in range(4,11,1):
    nylonLengthLists.append(nylonLengthList(i, chainLength, boatLength)) # depth has to be water depth plus freeboard here, so the graph starts with a water depth of 3.5 m

# plot every element of the metalist against the windspeed
label = 4
for i in nylonLengthLists:
    pylab.plot(windSpeeds,i, label=str(label) + ' m')
    label += 1
    
pylab.title('Leinenlaengen nach Tiefen')
pylab.ylabel('Leinenlaenge (m)')
pylab.xlabel('Windgeschwindigkeit (kn)')
pylab.legend(loc='upper left', title='Tiefen')
pylab.xticks()

pylab.grid()
pylab.show()


# generate a list of lists with nylonlengths for depths from 10 to 24 meters in steps of 2 meters

nylonLengthLists = []
for i in range(12,25,2):
    nylonLengthLists.append(nylonLengthList(i, chainLength, boatLength)) # depth has to be water depth plus freeboard here, so the graph starts with a water depth of 3.5 m

# plot every element of the metalist against the windspeed
label = 12
for i in nylonLengthLists:
    pylab.plot(windSpeeds,i, label=str(label) + ' m')
    label += 2
    
pylab.title('Leinenlaengen nach Tiefen')
pylab.ylabel('Leinenlaenge (m)')
pylab.xlabel('Windgeschwindigkeit (kn)')
pylab.legend(loc='upper left', title='Tiefen')
pylab.xticks()

pylab.grid()
pylab.show()

#######################################################################################
# calculate the necessary chain length for a given depth and windspeed (like above)
def allChainRode(windspeed, boatlength, depth, angulation):
    '''
    returns the minimal rodelength all chain for a given depth and windspeed
    '''
    hb = tensionAllChain(windspeed, boatlength) / (p * depth)
    v2 = hb * math.tan(math.radians(angulation))

        # minimal chain length = fond*(WURZEL(1+2*b/COS(alpha2)+v2_^2)-v2_)
    minimalChainLength = depth * (math.sqrt(1 + (2 * hb / math.cos(alpha2(angulation))) + (v2**2)) -v2)
        # scope
    return minimalChainLength

# use the existing range of windspeeds
# generate a list of chainlengths according to windspeeds for each particular depth

def chainlengthList(boatlength, depth, angulation=5):
    '''
    build a list with chainlengths according to windspeed (1-70 kn) for a given depth
    '''
    # open the empty list
    chainlengths = []
    for i in range(1,70):
        chainlengths.append(allChainRode(i,boatlength,depth,angulation))
    return chainlengths

chainlengthLists = [] # build a list of lists with lengths/windspeed for different depths with an angulation of 5 degrees
for i in range(4,11,1):
    chainlengthLists.append(chainlengthList(boatLength, i))

label = 4
for i in chainlengthLists:
    pylab.plot(windSpeeds,i, label=str(label) + ' m')
    label += 1
    
pylab.title('Kettenlaengen nach Tiefen')
pylab.ylabel('Kettenlaenge (m)')
pylab.xlabel('Windgeschwindigkeit (kn)')
pylab.legend(loc='upper left', title='Tiefen')
pylab.xticks()

pylab.grid()
pylab.show()

# generate a list of lists with chainlengths for depths from 10 to 24 meters in steps of 2 meters

chainlengthLists = []
for i in range(12,25,2):
    chainlengthLists.append(chainlengthList(boatLength, i)) # depth has to be water depth plus freeboard here, so the graph starts with a water depth of 3.5 m

# plot every element of the metalist against the windspeed
label = 12
for i in chainlengthLists:
    pylab.plot(windSpeeds,i, label=str(label) + ' m')
    label += 2
    
pylab.title('Kettenlaengen nach Tiefen')
pylab.ylabel('Kettenlaenge (m)')
pylab.xlabel('Windgeschwindigkeit (kn)')
pylab.legend(loc='upper left', title='Tiefen')
pylab.xticks()

pylab.grid()
pylab.show()







########################################################################################

#######################################################################################

# calculate the necessary length for a complete mixed rode (minimum 6 meters of nylon) for a given depth and windspeed (like above)
def mixedRode(windspeed, boatlength, depth, angulation):
    '''
    returns the minimal rodelength all chain for a given depth and windspeed
    '''
    hb = tensionDyn(windspeed, boatlength) / (p * depth)
    v2 = hb * math.tan(math.radians(angulation))

        # minimal chain length = fond*(WURZEL(1+2*b/COS(alpha2)+v2_^2)-v2_)
    minimalChainLength = depth * (math.sqrt(1 + (2 * hb / math.cos(alpha2(angulation))) + (v2**2)) -v2)
        # scope
    return minimalChainLength

# use the existing range of windspeeds
# generate a list of chainlengths according to windspeeds for each particular depth

def mixedRodeList(boatlength, depth, angulation=5):
    '''
    build a list with chainlengths according to windspeed (1-70 kn) for a given depth
    '''
    # open the empty list
    rodelengths = []
    for i in range(1,70):
        rodelengths.append(mixedRode(i,boatlength,depth,angulation))
    return rodelengths

rodelengthLists = [] # build a list of lists with lengths/windspeed for different depths with an angulation of 5 degrees
for i in range(4,11,1):
    rodelengthLists.append(mixedRodeList(boatLength, i))

label = 4
for i in rodelengthLists:
    pylab.plot(windSpeeds,i, label=str(label) + ' m')
    label += 1
    
pylab.title('Geschirrlaengen nach Tiefen')
pylab.ylabel('Geschirrlaenge (m)')
pylab.xlabel('Windgeschwindigkeit (kn)')
pylab.legend(loc='upper left', title='Tiefen')
pylab.xticks()

pylab.grid()
pylab.show()

# generate a list of lists with chainlengths for depths from 10 to 24 meters in steps of 2 meters

rodelengthLists = []
for i in range(12,25,2):
    rodelengthLists.append(mixedRodeList(boatLength, i)) # depth has to be water depth plus freeboard here, so the graph starts with a water depth of 3.5 m

# plot every element of the metalist against the windspeed
label = 12
for i in rodelengthLists:
    pylab.plot(windSpeeds,i, label=str(label) + ' m')
    label += 2
    
pylab.title('Geschirrlaengen nach Tiefen')
pylab.ylabel('Geschirrlaenge (m)')
pylab.xlabel('Windgeschwindigkeit (kn)')
pylab.legend(loc='upper left', title='Tiefen')
pylab.xticks()

pylab.grid()
pylab.show()

########################################################################################

# plot the static and dynamic tension according to windspeed for a given boatlength

# generate a list of windspeeds
# --> use the existing one
# generate a list of tensions
staticTensions = []
for i in range(1,70):
    staticTensions.append(tensionStat(i,boatLength))

    
dynamicTensions = []
chainTensions = []
for i in staticTensions:
    dynamicTensions.append(2.2 * i)
    chainTensions.append(5 * i)


pylab.plot(windSpeeds,staticTensions, label='statisch')
pylab.plot(windSpeeds,dynamicTensions, label='dynamisch')
pylab.plot(windSpeeds,chainTensions, label='nur Kette')

pylab.title('Lasten abhaengig von der Windgeschwindigkeit')
pylab.ylabel('Last (daN)')
pylab.xlabel('Windgeschwindigkeit (kn)')
pylab.legend(loc='upper left', title="Lasten")
pylab.grid()
pylab.show()


# minimal anchor weights for different seabed holding in 10 meters depth and windspeeds from 10 to 70 knots
# x-axis = minimal anchor weight, y-axis = windspeed

windspeeds = [10,20,30,40,50,60,70]

def mawWindspeeds(seabedHolding, boatLength):
    '''
    returns a list with minimal anchorweights (shhp) for different windspeeds, an angulation of 5 degrees, mixed rode and a given seabedHolding
    '''
    windspeeds = [10,20,30,40,50,60,70]
    reduc = reduction2(5)
    mawList = []
    for windspeed in windspeeds:
        tension = tensionDyn(windspeed, boatLength)
        maw = minimalAnchorweight(tension, seabedHolding, 1.4, reduc)
        mawList.append(hhp(maw))

    return mawList

mawMetaList2 = []
for i in [1,2,3,4]:
    mawMetaList2.append(mawWindspeeds(seabedHoldingTable[i], boatLength))

#print mawMetaList2

windspeeds = [10,20,30,40,50,60,70]
label = 1 # start with best seabed holding

for i in mawMetaList2:   # compute the plots
    pylab.plot(windspeeds, i, label = str(seabedHoldingNames[label]))
    label += 1

pylab.title('Minimales Ankergewicht fuer Windgeschwindigkeit und Qualitaet des Ankergrunds')
pylab.ylabel('Minimales Ankergewicht')
pylab.xlabel('Windgeschwindigkeit (kn)')
pylab.legend(loc='upper left', title='Ankergrund')
pylab.xticks()

pylab.grid()
pylab.show()
    

#################################################################################################
    
# für jeden windspeed eine liste mit minimal anchor weights machen (für jedes seabed eine zahl)
# compute a list with the minimal anchor weight for each seabed for a given windspeed

# minimalAnchorweight(tension, seabedHolding, massPower, reduc)
def mawSeabeds(windspeed, boatLength):
    '''
    returns a list with minimal anchorweights (shhp) for different seabeds, an angulation of 5 degrees, mixed rode and a given windspeed
    '''
    seabedHolding = [40,25,12,5]
    tension = tensionDyn(windspeed, boatLength)
    
    reduc = reduction2(5)
    mawList = []
    for i in seabedHolding:
        maw = minimalAnchorweight(tension, i, 1.4, reduc)
        mawList.append(hhp(maw))
    return mawList

mawMetaList = []

for i in windspeeds:
    mawMetaList.append(mawSeabeds(i, boatLength))

#print mawMetaList
