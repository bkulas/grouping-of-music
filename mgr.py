from music21 import *
import networkx as nx
import numpy as np

#Kompletna analiza utworu: wyznaczenie zbioru motywów na podstawie grafu, którego krawędziami są podobieństwa
#TODO wyznaczyć "centralny motyw"
#TODO zmienić motywy na grupy o konkretnej liczbie realizacji (dodatkowa funkcja)
def analyseComposition(composition, mode=0.6, tryb=0, longest = 25, pauses = True):
    charMotives = []
#    for p in composition.parts:
    analysis = analyseMelody(composition, pauses)
    note_count = len(analysis[0])
    przedtakt = analysis[13]
    timeSign = analysis[10]
    occurances = []
    for i in range(3,min(note_count, longest)):
        if i-3 >= charMotives.__len__():
            charMotives.append([])
        sequences = getSequences(analysis,i)
        #important = getImportantMotives(motives) # important - zostawia tylko to co dokładnie się powtorzyło
        #newMotives = removeRepetition(important) # usuwa dokładne repetycje
        if tryb==0: #test czy warto usuwać repetycje przed grafem podobieństwa
            sequences, removed = removeRepetition(sequences)
            occurances.append(removed)
        Mgraph = createMotiveGraph(sequences)
        reduceMotiveGraph(Mgraph, mode)
        motivesGroups = getMotivesGroupsFromGraph(Mgraph)
        mtv = characteristicMotives(sequences, motivesGroups)
        if tryb==0: addRemoved(mtv,removed,sequences, mode)
        if mtv != [[]]: charMotives[i - 3].extend(mtv)
    removeSubmotives2(charMotives)
    return (charMotives, timeSign, przedtakt)

# def analyseMotivesWithGraph(motives: list):
#     motivesFinal = []
#     for i, m in enumerate(motives):
#         Mgraph = createMotiveGraph(m)
#         reduceMotiveGraph(Mgraph)
#         motiveGroups = getMotivesGroupsFromGraph(Mgraph)
#         groups = characteristicMotives(motives, motiveGroups)
#         if groups != [[]]: motivesFinal[i].extend(groups)
#     return motivesFinal

def countChromatic(first: int, second: int, semitones: list, octaves: list) -> int:
    return abs(semitones[second] - semitones[first] + 12*(octaves[second]-octaves[first]))

def analyseMelody(melody, pauses) -> list:
#    print('analysis')
    categories = [note.Note]
    if pauses == True:
        categories.append(note.Rest)
    print('categories: ', categories)
    measure = []
    offsets = []
    onsets = []
    notesWithOctaves = []
    notesNames = []
    notes = []
    octaves = []
    rythm4 = []
    rythm8 = []
    semitones = []
    midis = []
    first = True
    ts = 0
    for elem in melody.recurse():
        if type(elem) == key.Key:
            melkey = elem              ## TODO przygotować się na zmiany kluczy
        if type(elem) == meter.TimeSignature and ts == 0:
            timeSign = elem             ## TODO przygotować się na zmiany metrum
            ts = 1
    for thisNote in melody.recurse().notesAndRests:
        if first == True and type(thisNote) == note.Note:
            if thisNote.offset != 0:
                przedtakt = True
                print('przedtakt: ', przedtakt)
            else: 
                przedtakt = False
                print('przedtakt: ', przedtakt)
            first = False
        if type(thisNote) in categories:# or type(thisNote) == note.Rest:
            if thisNote.measureNumber is None:
                break
            measure.append(thisNote.measureNumber)
            offsets.append(thisNote.offset)
            notesNames.append(thisNote.name)
            notes.append(thisNote)
            rythm4.append(thisNote.quarterLength)
            rythm8.append(thisNote.quarterLength * 2)
            onset = (thisNote.measureNumber - 1)*(timeSign.beat*timeSign.barDuration.quarterLength) + thisNote.offset
            onsets.append(onset)
        if type(thisNote) == note.Note:
            notesWithOctaves.append(thisNote.nameWithOctave) #
            semitones.append(thisNote.pitch.pitchClass) #
            midis.append(thisNote.pitch.midi) #
            octaves.append(thisNote.octave) #
        # if type(thisNote) == note.Rest:
        #     notesWithOctaves.append('rest') #
        #     semitones.append(-1) #
        #     midis.append(-1) #
        #     octaves.append(-1) #

    (intervals, diatonicIntervals, chromaticIntervals, contour) = getIntervals(notes,semitones,octaves)
    return (notes, notesNames, intervals, diatonicIntervals, chromaticIntervals, contour, rythm4, rythm8, measure, offsets, timeSign, midis, onsets, przedtakt)

def getIntervals(notes: list, semitones: list, octaves: list) -> list:
    intervals = []
    chromaticIntervals = []
    diatonicIntervals = []
    contour = []
    for i in range(notes.__len__()-1):
        if type(notes[i]) == note.Rest or type(notes[i+1]) == note.Rest:
            intervals.append('rest')
            diatonicIntervals.append('rest')
            chromaticIntervals.append('rest')
            contour.append('rest')
        else:
            intervals.append(interval.Interval(noteStart=notes[i], noteEnd=notes[i+1]).name)
            chromaticIntervals.append(countChromatic(i,i+1,semitones,octaves))
            diatonicIntervals.append(intervals[i][-1])
            if notes[i] > notes[i+1]:
                contour.append('-')
            else:
                contour.append('+')
    return (intervals, diatonicIntervals, chromaticIntervals, contour)

def getSequences(analysis: list, count: int) -> list:
    motives = []
    for i in range(len(analysis[0])-(count-1)):
        for j in range(count):
            if type(analysis[0][i+j]) == note.Rest:
                break
        s1 = []
        s2 = []
        midis = []
        measures = []
        offsets = []
        onsets = []
        s3 = []
        s4 = []
        s5 = []
        s6 = []
        s7 = []
        s8 = []
        s9 = 1 # moc realizacji
        for j in range(count):
            s1.append(analysis[0][i+j])
            s2.append(analysis[1][i+j])
            measures.append(analysis[8][i+j])
            offsets.append(analysis[9][i+j])
            midis.append(analysis[11][i+j])
            onsets.append(analysis[12][i+j])
        if i<(analysis[0].__len__()-(count-1)):
            for j in range(count-1):
                s3.append(analysis[2][i + j])
                s4.append(analysis[3][i + j])
                s5.append(analysis[4][i + j])
                s6.append(analysis[5][i + j])
        for j in range(count):
            s7.append(analysis[6][i + j])
            s8.append(analysis[7][i + j])
        motives.append([s1,s2,s3,s4,s5,s6,s7,s8,s9, midis, onsets, measures, offsets, i])
        # DONE dodać jeszcze indeks sekwencji zamiast przy tworzeniu grafu createMotiveGraph()
        # uporządkować potrzebne informacje realizacji, zrobić ratio,  dotęp poprzez nazwę ['chromatic'] ['notes']
        # po takich zmianach potrzebne chyba testy jednostkowe
    toRemove = []
    for i in range(len(motives)):
        for j in motives[i][0]:
            if type(j) == note.Rest and i not in toRemove:
                #print(j)
                toRemove.append(i)
    for i in toRemove[-1::-1]:
        #print(motives[i][1])
        motives.remove(motives[i])
    return motives#(motivesNotes, motivesNotesNames, motivesIntervals, motivesDiatonicIntervals,
            #motivesChromativIntervals, motivesContour, motivesRythm4, motivesRythm8, power
            #midis, onsets, measures, offsets, index)

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
#usuwa wszystko co sie nigdy nie powtórzyło dokładnie - spore naduzycie
def getImportantMotives(motives: list) -> list:
    importantMotives = motives
    similars = countExactSimilar(motives)
    c = 0
    for m in range(motives.__len__()):
        if similars[m] == 1:
            del importantMotives[m-c]
            c = c+1
    return importantMotives

#usuwa dokładne powtórzenia w motywach: takie same interwały, takie same wartości rytmiczne
def removeRepetition(motives: list):
    removed = []
    for a in motives:
        for b in motives:
            if a != b:
                if a[3:7] == b[3:7]:
                    removed.append(b)
                    a[8] += 1
                    motives.remove(b)
    return motives, removed

#graf reprezentujący motywy i ich wzajemne podobieńśtwo
#wieszchołki - motywy, krawędzie - liczba wspólnych elementów
def createMotiveGraph(motives: list):
    g=nx.Graph()
    # for i in range(len(motives)):
    #     motives[i].append(i) # dodanie indeksu wierzchołka - zamienić na indeks sekwencji dodany wcześniej
    #     g.add_node(i)
    for i in motives:
        g.add_node(i[13]) #dodanie wierzchołka po jego indeksie
    for i in range(len(motives)):
        for j in range(len(motives)-i-1):
            similarity = countSimilarity(motives[i],motives[i+j+1])
            g.add_edge(motives[i][-1],motives[i+j+1][-1],weight = similarity)
    return g

# kolejne nuty traktowane jako baza do liczenia podobieństwa
def countSimilarity(m1: list, m2: list) -> float:
    similarity = 0
    for i in range(len(m1[5])):
        if m1[3][i] == m2[3][i] and m1[5][i] == m2[5][i]:
            similarity = similarity+(1/(len(m1[5])))
        elif m1[4][i] == m2[4][i] and m1[5][i] == m2[5][i]:
            similarity = similarity+(1/(len(m1[4])))
        elif m1[5][i] == m2[5][i]:
            similarity = similarity+((1/(len(m1[4])))/3)
        elif m1[3][i] == m2[3][i]:
            similarity = similarity+((1/(len(m1[3])))/2)
        elif m1[4][i] == m2[4][i]:
            similarity = similarity+((1/(len(m1[4])))/2)
    for i in range(len(m1[6])-1):
        if m1[6][i+1] != 0 and m2[6][i+1] != 0:
            if m1[6][i]/m1[6][i+1] == m2[6][i]/m2[6][i+1]:
                similarity = similarity+(1/((len(m1[6]))-1))
    return similarity

#przygotowanie pod wagi dla kazdej cechy do treningu
def countCompatibility(s1: list, s2: list):
    zgodnosc = []
    for j in range(3,7):
        zgodnosc.append([])
        for i in range(len(s1[j])):
            #print(j, i)
            #print(s1[j][i] == s2[j][i])
            zgodnosc[j].append(s1[j][i] == s2[j][i])
    return zgodnosc

# wektory cech traktowane jako baza
def countSimilarityNew(m1: list, m2: list):
    zgodnosc = countCompatibility(m1,m2)
    cs = []
    w = [1/2, 1/2, 1]
    for i in zgodnosc:
        c_value = sum([int(j) for j in i])/len(i)
        cs.append(c_value)
    similarity = max(cs[0],cs[1])*w[0] + cs[2]*w[1] + cs[3]*w[2]
    return similarity

#PRÓG ODCIĘCIA dla podobieństwa realizacji motywów
def reduceMotiveGraph(g: nx.Graph, mode: int):
    if mode == 0:
        threshold = 1.9
    elif mode == 1:
        threshold = 1.7
    elif mode == 2:
        threshold = 1.5
    elif mode < 1 and mode > 0:
        threshold = mode*2 # theta (mode) z zakresu (0,1) reprezentuje procent podobieństwa
    edges_to_remove = []
    for (u, v, d) in g.edges(data=True):
        if d['weight'] < threshold:
            edges_to_remove.append([u,v])
            #g.remove_edge(u,v)
    for i in edges_to_remove:
        g.remove_edge(i[0],i[1])
# TODO mozna dodać warunek, ze jesli stopien wierzchołka jest mały to ta miara podobieństwa musi być duza. Potem znowu zostają wierzchołki o stopniu 0, wiec lepiej je usuwać później. Albo zeby realizacja była podobna do conajmniej 1/3 realizacji w zbiorze. Sprawdzic to na wiarygodnym przykładzie.
    # nodes_to_remove = []
    # for i in g.nodes:
    #     if g.degree(i) == 0:
    #         nodes_to_remove.append(i)
    # for i in nodes_to_remove:
    #     g.remove_node(i)

    return g

def getMotivesGroupsFromGraph(g: nx.Graph):
    motives = []
    edgesList = list(g.edges)
    for i in range(len(edgesList)):
        flag = 0
        for n in range(motives.__len__()):
            if edgesList[i][0] in motives[n]:
                flag = 1
                if edgesList[i][1] in motives[n]:
                    break
                else: motives[n].append(edgesList[i][1])
            elif edgesList[i][1] in motives[n]:
                flag = 1
                if edgesList[i][0] in motives[n]:
                    break
                else: motives[n].append(edgesList[i][0])
        #print(edgesList(i))
        if flag == 0: motives.append([edgesList[i][0],edgesList[i][1]])
    #print(motives)
    return motives

def characteristicMotives(motives: list, indexes: list):
    characteristic = [[]]
    for c, i in enumerate(indexes):
        for m in motives:
            for j in range(i.__len__()):
                if m[-1] == i[j]:
                    #print(m)
                    #print(c)
                    if c >= characteristic.__len__():
                        characteristic.append([m])
                    else: characteristic[c].append(m)
    return characteristic

#Wyliczanie indeksu dla utworów jako średnia wartości dla grup realizacji 
# motywów różnej wielkości
# wybieramy najlepiej pokrywające się pary grup motywów
def countJaccardIndex(a: list, b: list, mode=0):
    jacIndex = []
    jaccardIndexes = []
    all = []
    if len(a) > len(b):
        itNumber = len(b)
    else: itNumber = len(a)
    for i in range (itNumber): # i - motywy o konkretnej liczbie nut
        if len(a[i])>len(b[i]):
            indexValues = countIndexValues(a[i],b[i])
        else: indexValues = countIndexValues(b[i],a[i])
        if indexValues != []:
            jacIndex = getBestIndexValues(indexValues)
            #print(jacIndex)
            all.extend(jacIndex)
        for i in jacIndex:
           if i == 0.0:
               jacIndex.remove(i)
        nz = [item for item in jacIndex if item != 0]
        if mode == 0 and len(nz)!= 0:
             jaccardIndexes.append(sum(nz)/len(nz))  ##WAGI
            #  jaccardIndexes.append(sum(jacIndex)/len(jacIndex))  ##WAGI DLA MOTYWÓW O DŁUGOŚCI i+2
        # elif mode == 1 and len(jacIndex)!= 0:
        #     jaccardIndexes.append((sum(jacIndex) * (i + 1)) / (len(jacIndex) * (i + 1)))
        # elif mode == 2 and len(jacIndex)!= 0:
        #     jaccardIndexes.append((sum(jacIndex) * (i + 1)*(i + 1)) / (len(jacIndex) * (i + 1)*(i + 1)))
        else: jaccardIndexes.append(0)
    # print("all: ", all)
    # print("Len all: ", len(all))
    # nonzero = [item for item in all if item != 0]
    # print("Non zero all/sum/avg: ", len(nonzero), sum(nonzero), sum(nonzero)/len(nonzero) if nonzero else 0)
    # print("indexes: ",  jaccardIndexes)
    # print("Sum: ", sum(jaccardIndexes))
    # print("Len: ", len(jaccardIndexes))
    jaccardIndex = sum(jaccardIndexes)/len(jaccardIndexes)
    return jaccardIndex

def countSongsSimilarity(a: list, b: list):
    similarity = 0
    indexValues = []
    for i in range(1): # i-ty motyw - grupa realizacji
            if len(a[i])>len(b[i]):
                        print("a[i]: ", a[i][0])
                        print("Len a[i]: ", len(a[i][0]))
                        print("b[i]: ", b[i][0])
                        print("Len b[i]: ", len(b[i][0]))
                        indexValues = countIndexValues(a[i],b[i])
            else: indexValues = countIndexValues(b[i],a[i])
            if indexValues != []:
                jacIndex = getBestIndexValues(indexValues)
            print("jacIndex: ", jacIndex)
    return similarity

def countIndexValues(a: list, b: list):
    indexValues = []
    for j in range(len(a)): # j-ty motyw - grupa realizacji
        for l in range(len(b)):
            index_new = countGroupJaccard(a[j], b[l])
            if len(indexValues) <= j:
                indexValues.append([index_new])
            else: indexValues[j].append(index_new)
    return indexValues

#Wyliczam indeks Jaccarda dla dwóch grup: moc iloczynu zbiorów/moc sumy zbiorów
#Indeks Jaccarda dla dwóch grup z serializacją elementów
def countGroupJaccard(group1: list, group2: list) -> float:
### stare podejscie - liczenie indeksu Jaccarda dla calych motywow, drobne zmiany w realizacjach wykluczaly podobienstwo
    value = 0.0
    sGroup1 = serializeGroup(group1)
    sGroup2 = serializeGroup(group2)
    sum = set(sGroup1) | set(sGroup2)  # usuwa identyczne powtorzenia w grupach DO PRZEMYSLENIA czy to na pewno pomocne
    product = set(sGroup1) & set(sGroup2) # na pewno TO DO zmiana z analizy tylko identycznych motywow, bo to bez sensu, trzeba tu wrzucic jakies podobienstwo
    value = len(product)/len(sum)

### nowe podejscie wykorzystanie podobienstwa z wyznaczania motywów
    # sim = []
    # for i in group1:
    #     for j in group2:
    #         sim.append(countSimilarity(i,j))
    # value = sum(sim)/len(sim)

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

#TODO jak znaleźć indeksy największych wartości? zeby znalec potem odpowiadający im motyw i jego liczność???????????
def getBestIndexValues(indexes: list):
    copy = np.copy(indexes)
    best = []
    rows = len(indexes)
    columns = len(indexes[0])
    d = 0
    for it in range(rows) if rows<columns else range(columns):
        flat = [item for sublist in indexes for item in sublist]
        best.append(max(flat))
        r = int(flat.index(max(flat))/(columns-it))
        c = flat.index(max(flat))%(columns-it)
        # print("r, c  = ", r+d, c+d)
        del indexes[r]
        for i in indexes:
            d+=1
            del i[c]
    # for i in best:
    #     for j in copy:
    #         if i in j:
    #             print("Best: ", i, " in copy: ", j)
    return best#, power

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

#BAD do wyrzucenia.
def leaveLongestMotives(motives: list):
    lista = motives
    flag = 1
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
                                    if motives[i][j-cl][k-c][8] <= m[8]:
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

def checkSubset(realization1, realization2):
    if len(realization1[0]) > len(realization2[0]):
        longer = realization1
        shorter = realization2
    else:
        longer = realization2
        shorter = realization1
    if shorter[10][0] in longer[10]:
        first = longer[10].index(shorter[10][0])
    else:
        return False
    for i in range(len(shorter[10])):
        if first+i >= len(longer[10]):
            return False
        if longer[10][first+i] != shorter[10][i]:
            return False
    return True

def checkMotivesSubset(motive1, motive2):
    n1 = len(motive1)
    n2 = len(motive2)
    subsets = np.zeros((n1, n2))
    for i in range(n1):
        for j in range(n2):
            subsets[i,j] = checkSubset(motive1[i],motive2[j])
    return subsets

def removeSubmotives(motivesList):
    #na wejsciu lista motywów bez podziału na klasy długości - bez sensu (?)
    # TODO sprawdzać moc motywu (chociaz w przypadku gdy mamy zapisane wszystkie wystapienia nie bedzie tego problemu)
    indxs = []
    for i in range(len(motivesList)):
        for j in range(i+1, len(motivesList)):
            s = checkMotivesSubset(motivesList[i], motivesList[j])
            w = np.max(s, axis=1)
            if np.mean(w) == 1: # i POWER(motivesList[j] >= motivesList[i])
                #print("Usunięto ", motivesList[i])
                indxs.append([i,j])
                #print("Poniewaz jest: ", motivesList[j])
    to_remove = list(reversed(np.unique([i[0] for i in indxs])))
    for i in to_remove:
        del motivesList[i]
    return motivesList

def unique_pairs(l: list):
    res = []
    for item in l:
        if item not in res:
            res.append(item)
    return res

#wydaje sie być ok
def removeSubmotives2(motivesList):
    #na wejsciu lista motywów z podziałem na klasy długości - usuwamy gdy stopień wyzej znajdziemy ppowtórzenie
    # usuwamy jeśli wszystkie się pokrywają i jednocześnie suma wartości na 8 pozycji (power) jest mniejsza lub równa sumie dla dłuszego
    indxs = []
    for i in range(len(motivesList)-1):
        for n in range(len(motivesList[i])):
            for j in range(len(motivesList[i+1])):
                s = checkMotivesSubset(motivesList[i][n], motivesList[i+1][j])
                w = np.max(s, axis=1)
                power1 = np.sum([p[8] for p in motivesList[i][n]])
                power2 = np.sum([p[8] for p in motivesList[i+1][j]])
                #print(power1, power2)
                if (np.mean(w) == 1 and power1 <= power2): # i POWER(motivesList[j] >= motivesList[i])
                    #print("Usunięto ", motivesList[i][n])
                    indxs.append([i,n,j])
                    #print("Poniewaz jest: ", motivesList[i+1][j])
    to_remove = list(reversed(unique_pairs([[i[0],i[1]] for i in indxs])))
    #print(to_remove)
    for [i,n] in to_remove:
        #print(i,n)
        del motivesList[i][n]
    return motivesList

def power(motive: list):
    firsts = [i[13][0] for i in motive]
    c0 = 0
    power = 1/(np.unique(firsts))
    # for i in firsts:
    #     if i == 0.0: c0+=1
    return power*len(motive)

# def removeEmptyGroups(motives: list):
#     for i in motives:
#         for j in i:
#             if j == []:
#                 print(j)
#                 i.remove(j)
#     return motives

def removeEmptyGroups(motives: list):
    removed =0
    for i in range(len(motives)):
        if not any(motives[i-removed]): 
            #print("empty")
            removed+=1
            motives.remove([])
    return motives

# motives - list of motives selected from melody, 
# cat - number of categories of motives length
def getNumberOfMotives(motives: list, cat: int):
    num = {}
    for i in range(cat):
        num[i] = len(motives[i])
    return num

def summarizeMelody(compositions, motives: list):
    summ = []
    summ.append(['onset','midi_number','morphetic_number','duration','staff_number','measure','type'])
    #motives_csv.append(['start','end','type','measure','start_beat','duration','track','TS','measure_score','start_midi','end_midi'])
    return 0

# dodanie do wyznaczonych motywów usuniętych wcześniej realizacji
def addRemoved(mtv, removed, sequences, threshold):
    #dodanie realizacji do istniejących motywów
    # TODO zabezpieczenie przed dodaniem istniejącej realizacji - obecnie raczej nie mozliwe
    # i[14] numer id sekwencji
    for i in mtv:
        for j in i:
            for r in removed:
                if j[1] == r[1]:
                    i.append(r)
                    id = removed.index(r)
                    del removed[id]
    #znalezienie realizacji identycznej
    motives = []
    for i in sequences:
        for r in removed:
            if i[1] == r[1]:
                motive = [i,r]
                motives.append(motive)
                id = removed.index(r)
                del removed[id]
                #print("dodano realizację: ", motive[1])
    if len(motives) >= 1:
        for i in motives:
            for j in motives:
                sim = countSimilarity(i[0],j[0])
                if i!=j and sim >= threshold*2:
                    i.extend(j)
                    id = motives.index(j)
                    del motives[id]
    for m in motives:
        mtv.append(m)
    for i in mtv:
        if i == []:
            mtv.remove(i)
    return mtv

#TODO def calculateMotivePower(motive: list)
#TODO def selectMainRealizations(motive: list, threshold: float)
#TODO def selectNumberofRealizations(motives: list, number: int)
#Pamiętaj usunąć te zmiany, które robiłaś do testowania co tam było w ogóle napisane...