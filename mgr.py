from music21 import *
import networkx as nx

a = converter.parse("tinynotation: 3/4 g4 e e f4 d d c8 e g2 B4 A G")
b = converter.parse("tinynotation: 3/4 c4 C d")

for thisNote in a.recurse().notes:
    thisNote.addLyric(thisNote.nameWithOctave) #pitch
    thisNote.addLyric(thisNote.name)
    thisNote.addLyric(thisNote.quarterLength) #rythm per 4th note
    thisNote.addLyric(thisNote.pitch.pitchClass) #półtony od C trzeba powiązać z oktawą do interwałów
    thisNote.addLyric(thisNote.pitch.octave)

#Kompletna analiza utworu: wyznaczenie motywów na podstawie grafu, którego krawędziami są podobieństwa
#TODO poprawić wynikowe motywy - usunąć zakładki (motywy występujące po kolei przy kolejnych nutach) i zbyt duże odchylenia, wyznaczyć "centralny motyw"
def analyseComposition(composition):
    charMotives = []
#    for p in composition.parts:
    analysis = analyseMelody(composition)
    for i in range(2,8):
        if i-2 >= charMotives.__len__():
            charMotives.append([])
        motives = getSimpleMotives(analysis,i)
        important = getImportantMotives(motives)
        newMotives = removeRepetition(important)
        Mgraph = createMotiveGraph(newMotives)
        reduceMotiveGraph(Mgraph)
        motivesGroups = getMotivesGroupsFromGraph(Mgraph)
        mtv = characteristicMotives(newMotives, motivesGroups)
        if mtv != [[]]: charMotives[i - 2].extend(mtv)
            #charMotives.extend([newMotives])
    #motivesFinal = analyseMotivesWithGraph(charMotives)
    leaveLongestMotives(charMotives)
    return charMotives

def analyseMotivesWithGraph(motives: list):
    motivesFinal = []
    for i, m in enumerate(motives):
        Mgraph = createMotiveGraph(m)
        reduceMotiveGraph(Mgraph)
        motiveGroups = getMotivesGroupsFromGraph(Mgraph)
        groups = characteristicMotives(motives, motiveGroups)
        if groups != [[]]: motivesFinal[i].extend(groups)
    return motivesFinal

def countChromatic(first: int, second: int, semitones: list, octaves: list) -> int:
    return abs(semitones[second] - semitones[first] + 12*(octaves[second]-octaves[first]))

def analyseMelody(melody) -> list:
#    print('analysis')
    notesWithOctaves = []
    notesNames = []
    notes = []
    octaves = []
    rythm4 = []
    rythm8 = []
    semitones = []
    for thisNote in melody.recurse().notes:
        if type(thisNote)  == note.Note:
            notesWithOctaves.append(thisNote.nameWithOctave)
            notesNames.append(thisNote.name)
            notes.append(thisNote)
            octaves.append(thisNote.octave)
            rythm4.append(thisNote.quarterLength)
            rythm8.append(thisNote.quarterLength * 2)
            semitones.append(thisNote.pitch.pitchClass)
    (intervals, diatonicIntervals, chromaticIntervals, contour) = getIntervals(notes,semitones,octaves)
    return (notes, notesNames, intervals, diatonicIntervals, chromaticIntervals, contour, rythm4, rythm8)

def getIntervals(notes: list, semitones: list, octaves: list) -> list:
    intervals = []
    chromaticIntervals = []
    diatonicIntervals = []
    contour = []
    for i in range(notes.__len__()-1):
        intervals.append(interval.Interval(noteStart=notes[i], noteEnd=notes[i+1]).name)
        chromaticIntervals.append(countChromatic(i,i+1,semitones,octaves))
        diatonicIntervals.append(intervals[i][-1])
        if notes[i] > notes[i+1]:
            contour.append('-')
        else:
            contour.append('+')
    return (intervals, diatonicIntervals, chromaticIntervals, contour)

def getSimpleMotives(analysis: list, count: int) -> list:
    motives = []
    for i in range(analysis[0].__len__()-(count-1)):
        s1 = []
        s2 = []
        s3 = []
        s4 = []
        s5 = []
        s6 = []
        s7 = []
        s8 = []
        s9 = 1
        for j in range(count):
            s1.append(analysis[0][i+j])
            s2.append(analysis[1][i+j])
        if i<(analysis[0].__len__()-(count-1)):
            for j in range(count-1):
                s3.append(analysis[2][i + j])
                s4.append(analysis[3][i + j])
                s5.append(analysis[4][i + j])
                s6.append(analysis[5][i + j])
        for j in range(count):
            s7.append(analysis[6][i + j])
            s8.append(analysis[7][i + j])
        motives.append([s1,s2,s3, s4,s5,s6,s7,s8,s9])
    return motives#(motivesNotes, motivesNotesNames, motivesIntervals, motivesDiatonicIntervals,
            #motivesChromativIntervals, motivesContour, motivesRythm4, motivesRythm8, power)

#motive - lista nut
def showMotive(motive: list):
    s1 = stream.Measure()
    s1.append(motive)
    s1.show()

#zliczamy podobne motywy na liście motywów analysis wg wartości value
def countSimilar(analysis: list, value: int ) -> list:
    similars = []
    for i in range(analysis.__len__()):
        c = 0
        for j in range(analysis.__len__()):
            flag = 0
            if analysis[i][value] != analysis[j][value]:
                flag = 1
            if flag == 0:
                c=c+1
        similars.append(c)
    return similars

def countExactSimilar(analysis: list ) -> list:
    exactSimilars = []
    for i in range(analysis.__len__()):
        c = 0
        for j in range(analysis.__len__()):
            flag = 0
            if analysis[i][3] != analysis[j][3] or analysis[i][4] != analysis[j][4]\
                    or analysis[i][5] != analysis[j][5] or analysis[i][6] != analysis[j][6]:
                flag = 1
            if flag == 0:
                c=c+1
        exactSimilars.append(c)
    return exactSimilars

#zachowujemy tylko te motywy na liście motives, które są podobne wg czterech kryteriów
def getImportantMotives(motives: list) -> list:
    importantMotives = motives
    similars = countExactSimilar(motives)
    c = 0
    for m in range(motives.__len__()):
        if similars[m] == 1:
            del importantMotives[m-c]
            c = c+1
    #removeRepetition(importantMotives)
    return importantMotives

#usuwa dokładne powtórzenia w motywach: takie same interwały, takie same wartości rytmiczne
def removeRepetition(motives: list):
#    print('RemoveRepetition for', motives)
    removed = []
    newM = []
    for elem in motives:
        flag = 0
        for elem2 in newM:
#            if elem[1] == elem2[1] and elem[4] == elem2[4] and elem[6] == elem2[6]:
            if elem[4] == elem2[4] and elem[6] == elem2[6] and elem[5]==elem2[5] and elem[3]==elem2[3]:
                removed.append(elem)
                newM[newM.index(elem2)][8] = newM[newM.index(elem2)][8]+1
                flag = 1
                break
        if flag == 0:
            newM.append(elem)
#    print(newM)
    return newM

#graf reprezentujący motywy i ich wzajemne podobieńśtwo
#wieszchołki - motywy, krawędzie - liczba wspólnych elementów
def createMotiveGraph(motives: list):
    g=nx.Graph()
    for i in range(motives.__len__()):
#        print(motives[i])
        motives[i].append(i)
#        print(i, motives[i])
        g.add_node(i)
    for i in range(motives.__len__()):
        for j in range(motives.__len__()-i-1):
            similarity = countSimilarity(motives[i],motives[i+j+1])
            g.add_edge(motives[i][9],motives[i+j+1][9],weight = similarity)
#    print(g.nodes())
#    print(nx.get_edge_attributes(g,'weight'))
    return g
    #g.add_nodes_from(motives)

def countSimilarity(m1: list, m2: list) -> int:
    similarity = 0
    for i in range(m1[5].__len__()):
        if m1[3][i] == m2[3][i] and m1[5][i] == m2[5][i]:
            similarity = similarity+(1/(m1[5].__len__()))
        elif m1[4][i] == m2[4][i] and m1[5][i] == m2[5][i]:
            similarity = similarity+(1/(m1[4].__len__()))
        elif m1[5][i] == m2[5][i]:
            similarity = similarity+((1/(m1[4].__len__()))/3)
        elif m1[3][i] == m2[3][i]:
            similarity = similarity+((1/(m1[3].__len__()))/2)
        elif m1[4][i] == m2[4][i]:
            similarity = similarity+((1/(m1[4].__len__()))/2)
    for i in range(m1[6].__len__()-1):
        if m1[6][i+1] != 0 and m2[6][i+1] != 0:
            if m1[6][i]/m1[6][i+1] == m2[6][i]/m2[6][i+1]:
                similarity = similarity+(1/((m1[6].__len__())-1))
    return similarity

def reduceMotiveGraph(g: nx.Graph):
    #print("początkowo krawędzi: ", g.number_of_edges())
    for (u, v, d) in g.edges(data=True):
        if d['weight'] < 1.8:
            g.remove_edge(u,v)
    #print("na koniec krawędzi: ", g.number_of_edges())
    #print(g.edges())
    return g

def getMotivesGroupsFromGraph(g: nx.Graph):
    motives = []
    for i in range(g.edges().__len__()):
        flag = 0
        for n in range(motives.__len__()):
            if g.edges()[i][0] in motives[n]:
                flag = 1
                if g.edges()[i][1] in motives[n]:
                    break
                else: motives[n].append(g.edges()[i][1])
            elif g.edges()[i][1] in motives[n]:
                flag = 1
                if g.edges()[i][0] in motives[n]:
                    break
                else: motives[n].append(g.edges()[i][0])
        if flag == 0: motives.append([g.edges()[i][0],g.edges()[i][1]])
    #print(motives)
    return motives

def characteristicMotives(motives: list, indexes: list):
    characteristic = [[]]
    for c, i in enumerate(indexes):
        for m in motives:
            for j in range(i.__len__()):
                if m[9] == i[j]:
                    #print(m)
                    #print(c)
                    if c >= characteristic.__len__():
                        characteristic.append([m])
                    else: characteristic[c].append(m)
    return characteristic

#Wyliczanie indeksu dla utworów jako średnia warotści dla grup realizacji motywów różnej wielkości - wybieramy najlepiej pokrywające się pary grup motywów
def countJaccardIndex(a: list, b: list):
    jacIndex = []
    jaccardIndexes = []
    if len(a) > len(b):
        itNumber = len(a)
    else: itNumber = len(b)
    for i in range (itNumber): # i - motywy o konkretnej liczbie nut
#        if a[i] != [] and b[i] != []:
        if len(a[i])>len(b[i]):
            indexValues = countIndexValues(a[i],b[i])
        else: indexValues = countIndexValues(b[i],a[i])
        if indexValues != []:
            jacIndex = getBestIndexValues(indexValues)
#            print("jacIndex", jacIndex)
        jaccardIndexes.append(sum(jacIndex)/len(jacIndex))
    jaccardIndex = sum(jaccardIndexes)/len(jaccardIndexes)
    return jaccardIndex

def countIndexValues(a: list, b: list):
    indexValues = []
    for j in range(len(a)): # j-ta grupa motywów
        for l in range(len(b)):
            index_new = countGroupJaccard(a[j], b[l])
            if len(indexValues) <= j:
                indexValues.append([index_new])
            else: indexValues[j].append(index_new)
    return indexValues

#Wyliczam indeks Jaccarda dla dwóch grup: moc iloczynu zbiorów/moc sumy zbiorów
#Indeks Jaccarda dla dwóch grup z serializacją elementów
def countGroupJaccard(group1: list, group2: list) -> float:
    value = 0.0
    sGroup1 = serializeGroup(group1)
    sGroup2 = serializeGroup(group2)
    sum = set(sGroup1) | set(sGroup2)
    product = set(sGroup1) & set(sGroup2)
    value = len(product)/len(sum)
    return value

#Serializacja znaczących parametrów realizacji motywów do typu string
def serializeGroup(group: list):
    serialized = []
    for i in group:
        string = str(i[3]) + str(i[4]) + str(i[5]) + str(i[6])
        serialized.append(string)
    return serialized

def serializeMotive(motive: list):
    string = str(motive[3]) + str(motive[4]) + str(motive[5]) + str(motive[6])
    return string

def getBestIndexValues(indexes: list):
    best = []
    rows = len(indexes)
    columns = len(indexes[0])
    for it in range(rows) if rows<columns else range(columns):
        flat = [item for sublist in indexes for item in sublist]
        best.append(max(flat))
        r = int(flat.index(max(flat))/(columns-it))
        c = flat.index(max(flat))%(columns-it)
        del indexes[r]
        for i in indexes:
            del i[c]
    return best

#TODO poprawić aby wyświetlany plik z motywami nie był 'uszkodzony'
def showMotives(motives:list):
    sc = stream.Score()
    for i in motives:
        if i != []:
            for j in i:
                if j != []:
                    p1 = stream.Part()
                    for k in j:
                        s1=stream.Measure()
                        s1.append(k[0])
                        p1.append(s1)
                    sc.insert(0,p1)
    sc.show()
    return

def leaveLongestMotives(motives: list):
    lista = motives
    flag =1
    for i in range(len(motives)-1): #motywy długości i+2
        cl=0
        for j in range(len(motives[i])): #j-ta grupa
            c=0
            for k in range(len(motives[i][j-cl])): #k-ta realizacja
                if flag == 1:
                    for l in motives[i+1]:
                        if flag ==1:
                            for m in l:
                               #print(i, j, k, motives[i][j][k-c])
                                if (str(motives[i][j-cl][k-c][4]))[1:-1] in (str(m[4]))[1:-1] and (str(motives[i][j-cl][k-c][5]))[1:-1] in (str(m[5]))[1:-1] and (str(motives[i][j-cl][k-c][6]))[1:-1] in (str(m[6]))[1:-1]:
                                    del lista[i][j-cl][k-c]
                                    if lista[i][j-cl] == []:
                                        del lista[i][j-cl]
                                        cl+=1
                                    c+=1
                                    flag = 0
                                    break
                        else:
                            flag = 1
                            break
                else:
                    flag = 1
    return motives

def removeEmptyGroups(motives: list):
    for i in motives:
        for j in i:
            if j == []:
                print(j)
                del j
    return motives

"""sc1 = stream.Score()
s1 = stream.Measure()
s1.TimeSignature = meter.TimeSignature('3/4')
s1.append(motives[1][0][0][1][0])
p1 = stream.Part()
p1.append([s1.TimeSignature, s1])
s3 = stream.Measure()
s3.TimeSignature = meter.TimeSignature('3/4')
s3.append(motives[1][0][0][2][0])
p2 = stream.Part()
p2.append([s3.TimeSignature,s3])
sc1.insert(0,p1)
sc1.insert(0,p2)
sc1.show()"""