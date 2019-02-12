from music21 import *
import matplotlib.pyplot as plt
from scipy.cluster import hierarchy

def prepareDistanceArray(jaccardMatrix: list):
    d = []
    width = len(jaccardMatrix[0])
    for i in range(len(jaccardMatrix)):
        d.extend(jaccardMatrix[i][i+1:width])
    distance = [1-i for i in d]
    return distance

def dendrogram(array: list, option=1):
    if option == 1:
        order = 'single'
    elif option == 2:
        order = 'complete'
    elif option == 3:
        order = 'average'
    elif option == 4:
        order = 'weighted'
    elif option == 5:
        order = 'centroid'
    elif option == 6:
        order = 'median'
    elif option == 7:
        order = 'ward'
    Z = hierarchy.linkage(array, order)
    plt.figure()
    dn = hierarchy.dendrogram(Z)
    plt.show()
    return

def filterMxl(path: list):
    if path[-3:] == "mxl":
        return True
    else:
        return False

def getMxlFiles(paths: list):
    mxl = []
    filtered = filter(filterMxl,paths)
    for element in filtered:
        mxl.append(element)
    return mxl

def checkIfContainChords(notes: list):
    for note in notes:
        if type(note) is chord.Chord:
            return True
    return False

def filterNoChords(notes: list):
    if checkIfContainChords(notes):
        return False
    else:
        return True

def getNoChords(notes: list):
    noChords = []
    filtered = filter(filterNoChords, notes)
    for element in filtered:
        noChords.append(element)
    return noChords

def getMelodyNoChords(melodys: list):
    melodyNoChords = []
    filtered = filter(filterMelodyNoChords,melodys)
    for element in filtered:
        melodyNoChords.append(element)
    return melodyNoChords

def filterMelodyNoChords(melody: list):
    notes = melody.recurse().notes
    if checkIfContainChords(notes):
        return False
    else:
        return True
