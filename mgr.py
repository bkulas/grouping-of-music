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

def analyseComposition(composition):
    charMotives = []
    for p in composition.parts:
        analysis = analyseMelody(p)
        for i in range(2,8):
            print(i)
            if i-2 >= charMotives.__len__():
                print('add',i)
                charMotives.append([])
            motives = getSimpleMotives(analysis,i)
            important = getImportantMotives(motives)
            print('Important ', important)
            newMotives = removeRepetition(important)
            Mgraph = createMotiveGraph(newMotives)
            reduceMotiveGraph(Mgraph)
            motivesGroups = getMotivesGroupsFromGraph(Mgraph)
            mtv = characteristicMotives(newMotives, motivesGroups)
            if mtv != [[]]: charMotives[i - 2].extend(mtv)
    return charMotives


def countChromatic(first: int, second: int, semitones: list, octaves: list) -> int:
    return semitones[second] - semitones[first] + 12*(octaves[second]-octaves[first])

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
        if i<(analysis[0].__len__()-count):
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

#usuwa dokładne powtórzenia w motywach: takie same nuty, takie same interwały, takie same wartości rytmiczne
def removeRepetition(motives: list):
    print('RemoveRepetition for', motives)
    removed = []
    newM = []
    for elem in motives:
        flag = 0
        for elem2 in newM:
            if elem[1] == elem2[1] and elem[4] == elem2[4] and elem[6] == elem2[6]:
#            if elem[4] == elem2[4] and elem[6] == elem2[6]:
                removed.append(elem)
                newM[newM.index(elem2)][8] = newM[newM.index(elem2)][8]+1
                flag = 1
                break
        if flag == 0:
            newM.append(elem)
    print(newM)
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
#    for i in range(m1[1].__len__()):
#        if m1[1][i] == m2[1][i]:
#            similarity = similarity+(1/(m1[1].__len__()))
    for i in range(m1[3].__len__()):
        if m1[3][i] == m2[3][i] and m1[5][i] == m2[5][i]:
            similarity = similarity+(1/(m1[5].__len__()))
#    for i in range(m1[4].__len__()):
        elif m1[4][i] == m2[4][i]:
            similarity = similarity+(1/(m1[4].__len__()))
#    for i in range(m1[5].__len__()):
        elif m1[3][i] == m2[3][i]:
            similarity = similarity+((1/(m1[3].__len__()))/2)
    for i in range(m1[6].__len__()-1):
        if m1[6][i]/m1[6][i+1] == m2[6][i]/m2[6][i+1]:
            similarity = similarity+(1/((m1[6].__len__())-1))
    return similarity

def reduceMotiveGraph(g: nx.Graph):
    #print("początkowo krawędzi: ", g.number_of_edges())
    for (u, v, d) in g.edges(data=True):
        if d['weight'] < 1.5:
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

#def countJaccardIndex(a: list, b: list):
#    jaccardIndex = []
#    for i in range(a.__len__()): #poziom długości motywu
#        for j in range(a[i].__len__()): #poziom częsci utworu
#            for k in range(b[i].__len__()):
#                for l in range(a[i][j].__len__()): #poziom grup motywów
#                    indexes = []
#                    for m in range(b[i][k].__len__()):
#                        index = 0
#                        sum = (a[i][j][l].__len__()) + (b[i][k][m].__len__())
#                        for n in range(a[i][j][l].__len__()):
#                            flag = 0
#                            for o in range(b[i][k][m].__len__()):
#                                if a[i][j][l][n][3] == b[i][k][m][o][3] and a[i][j][l][n][4] == b[i][k][m][o][4] \
#                                    and a[i][j][l][n][5] == b[i][k][m][o][5] and a[i][j][l][n][6] == b[i][k][m][o][6]:
#                                    index = index + 1
#                                    sum = sum - 1
#                        if sum != 0: ind = index/sum
#                        else: ind = 0
#                        print(index, sum)
#                        indexes.append(ind)
#                jaccardIndex.append(max(indexes))
#    print(jaccardIndex)
    #srednia = sum(j for j in jaccardIndex)
#    print(srednia)
#    print(sum)
#    indexJaccarda = index/sum
#    print(indexJaccarda)
#    return jaccardIndex

def countJaccardIndex(a: list, b: list):
    jaccardIndex = []
    for i in range (a.__len__()): # i - motywy o konkretnej liczbie nut
        if a[i] != []:
            indexes = []
            for j in range(a[i].__len__()): # j-ta grupa motywów
                index_old = 0
                index_new = 0
#                for k in range(a[i][j].__len__()): #k-ty motyw
                for l in range(b[i].__len__()):
                    index_new = countGroupJaccard2(a[i][j], b[i][l])
                    if index_new > index_old : index_old = index_new
                indexes.append(index_old)
            average = sum(indexes)/len(indexes)
            jaccardIndex.append(average)
            print(indexes)
    print(jaccardIndex)
    return jaccardIndex

#Wyliczam indeks Jaccarda dla dwóch grup: moc iloczynu zbiorów/moc sumy zbiorów
#Indeks Jaccarda dla dwóch grup z serializacją elementów
def countGroupJaccard2(group1: list, group2: list) -> float:
    value = 0.0
    sGroup1 = serializedGroup(group1)
    sGroup2 = serializedGroup(group2)
    sum = set(sGroup1) | set(sGroup2)
    product = set(sGroup1) & set(sGroup2)
    value = len(product)/len(sum)
    return value

#Serializacja znaczących parametrów realizacji motywów do typu string
def serializedGroup(group: list) -> set:
    serialized = []
    for i in group:
        string = str(i[3])+str(i[4])+str(i[5])+str(i[6])
        serialized.append(string)
    return serialized


