from music21 import *
import mgr
import grouping
import random
pathsMonteverdi = corpus.getComposer('monteverdi')
pathsBach = corpus.getComposer('bach')
pathsMozart = corpus.getComposer('mozart')
pathsHaydn = corpus.getComposer('haydn')
pathsTrecento = corpus.getComposer('trecento')

monteverdi = grouping.getMxlFiles(pathsMonteverdi)
bach = grouping.getMxlFiles(pathsBach)
mozart = grouping.getMxlFiles(pathsMozart)
haydn = grouping.getMxlFiles(pathsHaydn)
trecento = grouping.getMxlFiles(pathsTrecento)

monteverdiAll = [corpus.parse(i) for i in monteverdi]
bachAll = [corpus.parse(i) for i in bach]
mozartAll = [corpus.parse(i) for i in mozart]
haydnAll = [corpus.parse(i) for i in haydn]
trecentoAll = [corpus.parse(i) for i in trecento]

monteverdi = grouping.getMelodyNoChords(monteverdiAll)
bach = grouping.getMelodyNoChords(bachAll)
mozart = grouping.getMelodyNoChords(mozartAll)
haydn = grouping.getMelodyNoChords(haydnAll)
trecento = grouping.getMelodyNoChords(trecentoAll)

indxsBa = random.sample(range(len(bach)),34)
#indxsMoz = random.sample(range(len(mozart)),3)
indxsMon = random.sample(range(len(monteverdi)),33)
#indxsHa = random.sample(range(len(haydn)),2)
indxsTr = random.sample(range(len(trecento)),33)

compositions = [bach[i] for i in indxsBa]  + [monteverdi[i] for i in indxsMon] + [trecento[i] for i in indxsTr]# + [haydn[i] for i in indxsHa] + [mozart[i] for i in indxsMoz]

#compositions = random.sample(bach,3) + random.sample(mozart,3) + random.sample(monteverdi,3) + random.sample(haydn,2) + random.sample(trecento,3)
#compositions = bach[0:3] + mozart[0:3] + monteverdi[0:3] + haydn[0:2] + trecento[0:3]
#labels = ['bach']*3 + ['mozart']*3 + ['monte']*3 + ['haydn']*2 + ['trec']*3
labels = ['bach'+str(i) for i in indxsBa] + ['monte'+str(i) for i in indxsMon]+ ['trec'+str(i) for i in indxsTr]

motives = [mgr.analyseComposition(i,0) for i in compositions]
motives1 = [mgr.analyseComposition(i,1) for i in compositions]
motives2 = [mgr.analyseComposition(i,2) for i in compositions]

#próg 1.9
jaccard90 = [[mgr.countJaccardIndex(a,b,0) for a in motives] for b in motives]#wagi 111
jaccard91 = [[mgr.countJaccardIndex(a,b,1) for a in motives] for b in motives]#wagi 123
jaccard92 = [[mgr.countJaccardIndex(a,b,2) for a in motives] for b in motives]#wagi 149
#próg 1.7
jaccard70 = [[mgr.countJaccardIndex(a,b,0) for a in motives1] for b in motives1]#wagi 111
jaccard71 = [[mgr.countJaccardIndex(a,b,1) for a in motives1] for b in motives1]#wagi 123
jaccard72 = [[mgr.countJaccardIndex(a,b,2) for a in motives1] for b in motives1]#wagi 149
#próg 1.5
jaccard50 = [[mgr.countJaccardIndex(a,b,0) for a in motives2] for b in motives2] #wagi 111
jaccard51 = [[mgr.countJaccardIndex(a,b,1) for a in motives2] for b in motives2] #wagi 123
jaccard52 = [[mgr.countJaccardIndex(a,b,2) for a in motives2] for b in motives2] #wagi 149

f = open("testB2.txt", "w")
for i in labels:
    f.write(i)
for i in indxsBa:
    f.write(pathsBach[i])
for i in indxsMon:
    f.write(pathsMonteverdi[i])
for i in indxsTr:
    f.write(pathsTrecento[i])
f.close()

dArray = grouping.prepareDistanceArray(jaccard90)
grouping.dendrogram(dArray,1,labels,0.95, "testB2_9threshold9weights1single")
grouping.dendrogram(dArray,2,labels,0.95, "testB2_9threshold9weights1complete")
grouping.dendrogram(dArray,3,labels,0.95, "testB2_9threshold9weights1average")

dArray1 = grouping.prepareDistanceArray(jaccard70)
grouping.dendrogram(dArray1,1,labels,0.95, "testB2_9threshold7weights1single")
grouping.dendrogram(dArray1,2,labels,0.95, "testB2_9threshold7weights1complete")
grouping.dendrogram(dArray1,3,labels,0.95, "testB2_9threshold7weights1average")

dArray2 = grouping.prepareDistanceArray(jaccard50)
grouping.dendrogram(dArray2,1,labels,0.95, "testB2_9threshold5weights1single")
grouping.dendrogram(dArray2,2,labels,0.95, "testB2_9threshold5weights1complete")
grouping.dendrogram(dArray2,3,labels,0.95, "testB2_9threshold5weights1average")

dArray = grouping.prepareDistanceArray(jaccard91)
grouping.dendrogram(dArray,1,labels,0.95, "testB2_9threshold9weights123single")
grouping.dendrogram(dArray,2,labels,0.95, "testB2_9threshold9weights123complete")
grouping.dendrogram(dArray,3,labels,0.95, "testB2_9threshold9weights123average")

dArray1 = grouping.prepareDistanceArray(jaccard71)
grouping.dendrogram(dArray1,1,labels,0.95, "testB2_9threshold7weights123single")
grouping.dendrogram(dArray1,2,labels,0.95, "testB2_9threshold7weights123complete")
grouping.dendrogram(dArray1,3,labels,0.95, "testB2_9threshold7weights123average")

dArray2 = grouping.prepareDistanceArray(jaccard51)
grouping.dendrogram(dArray2,1,labels,0.95, "testB2_9threshold5weights123single")
grouping.dendrogram(dArray2,2,labels,0.95, "testB2_9threshold5weights123complete")
grouping.dendrogram(dArray2,3,labels,0.95, "testB2_9threshold5weights123average")

dArray = grouping.prepareDistanceArray(jaccard92)
grouping.dendrogram(dArray,1,labels,0.95, "testB2_9threshold9weights149single")
grouping.dendrogram(dArray,2,labels,0.95, "testB2_9threshold9weights149complete")
grouping.dendrogram(dArray,3,labels,0.95, "testB2_9threshold9weights149average")

dArray1 = grouping.prepareDistanceArray(jaccard72)
grouping.dendrogram(dArray1,1,labels,0.95, "testB2_9treshold7weights149single")
grouping.dendrogram(dArray1,2,labels,0.95, "testB2_9treshold7weights149complete")
grouping.dendrogram(dArray1,3,labels,0.95, "testB2_9treshold7weights149average")

dArray2 = grouping.prepareDistanceArray(jaccard52)
grouping.dendrogram(dArray2,1,labels,0.95, "testB2_9treshold5weights149single")
grouping.dendrogram(dArray2,2,labels,0.95, "testB2_9treshold5weights149complete")
grouping.dendrogram(dArray2,3,labels,0.95, "testB2_9treshold5weights149average")

"""bwv295 = corpus.parse('bach/bwv295')
motives = mgr.analyseCom position(bwv295)
flatten = [y for x in motives for y in x]
flat = [y for x in flatten for y in x]
print(len(flat))
new = mgr.leaveLongestMotives(motives)
flatten = [y for x in new for y in x]
flat = [y for x in flatten for y in x]
print(len(flat))

bwv66 = corpus.parse('bwv66.6')

corelli = corpus.parse('corelli/opus3no1/1grave.xml')
cpebach = corpus.parse('cpebach/h186.mxl') ###Akordy
demo0 = corpus.parse('demos/chorale_with_parallels.mxl') #dziwne
demo9 = corpus.parse('demos/two-parts.xml')
luca = corpus.parse('luca/gloria.xml')

compositions = [bwv295, bwv66, corelli, demo0, demo9, luca]
print(jaccard)

mgr.showMotives(motives[0])
bwv295.show()

#import constant

#bwv24511 = corpus.parse('bach/bwv245.11.mxl')
#bwv24514 = corpus.parse('bach/bwv245.14.mxl')
#bwv24515 = corpus.parse('bach/bwv245.15.mxl')
#bwv24517 = corpus.parse('bach/bwv245.17.mxl')
#bwv24522 = corpus.parse('bach/bwv245.22.mxl')
#bwv24526 = corpus.parse('bach/bwv245.26.mxl')
#bwv24528 = corpus.parse('bach/bwv245.28.mxl')
#bwv2453 = corpus.parse('bach/bwv245.3.mxl')
#bwv24537 = corpus.parse('bach/bwv245.37.mxl')
#bwv24540 = corpus.parse('bach/bwv245.40.mxl')
#bwv2455 = corpus.parse('bach/bwv245.5.mxl')

#bee132 = corpus.parse('beethoven/opus132.mxl')
#bee133 = corpus.parse('beethoven/opus133.mxl')
#bee591 = corpus.parse('beethoven/opus59no1/movement1.mxl')

Utwory = ['bach/bwv245.11.mxl', 'bach/bwv245.14.mxl','bach/bwv245.15.mxl','bach/bwv245.17.mxl','bach/bwv245.22.mxl']

for u in Utwory:
    motywy = mgr.analyseComposition(u)
    

#c = mgr.analyseComposition(bwv24511)
#d = mgr.analyseComposition(bwv24514)
#e = mgr.analyseComposition(bwv24515)
#f = mgr.analyseComposition(bwv24517)
#g = mgr.analyseComposition(bwv24522)
#h = mgr.analyseComposition(bwv24526)
#i = mgr.analyseComposition(bwv24528)
#j = mgr.analyseComposition(bwv2453)
#k = mgr.analyseComposition(bwv24537)
#l = mgr.analyseComposition(bwv24540)
#m = mgr.analyseComposition(bwv2455)

#b132 = mgr.analyseComposition(bee132)
#b133 = mgr.analyseComposition(bee133)
#b591 = mgr.analyseComposition(bee591)

print("aa")
mgr.countJaccardIndex(a,a)
print("ab")
mgr.countJaccardIndex(a,b)
#print("ba")
#mgr.countJaccardIndex(b,a)
#print("ac")
#mgr.countJaccardIndex(a,c)
#print("ad")
#mgr.countJaccardIndex(a,d)
#print("ae")
#mgr.countJaccardIndex(a,e)
#print("af")
#mgr.countJaccardIndex(a,f)
#print("ag")
#mgr.countJaccardIndex(a,g)
#print("ah")
#mgr.countJaccardIndex(a,h)
#print("bee")
#mgr.countJaccardIndex(b132,b133)
#print("bee")
#mgr.countJaccardIndex(b133,b132)
#print("abee")
#mgr.countJaccardIndex(a,b132)


#soprano = bwv295.parts[0]
#alto = bwv295.parts[1]
#tenor = bwv295.parts[2]
#basso = bwv295.parts[3]

#sopranoAnalysis = mgr.analyseMelody(soprano)
#altoAnalysis = mgr.analyseMelody(alto)
#tenorAnalysis = mgr.analyseMelody(tenor)
#bassoAnalysis = mgr.analyseMelody(basso)

#mot2 = mgr.getSimpleMotives(altoAnalysis,2)
#mot3 = mgr.getSimpleMotives(altoAnalysis,3)
#mot4 = mgr.getSimpleMotives(altoAnalysis,4)
#mot5 = mgr.getSimpleMotives(altoAnalysis,5)

#important2 = mgr.getImportantMotives(mot2)
#important3 = mgr.getImportantMotives(mot3)
#important4 = mgr.getImportantMotives(mot4)
#important5 = mgr.getImportantMotives(mot5)


#print(important2)
#print(important3)

#(removed2,newMotives2) = mgr.removeRepetition(important2)
#(removed3,newMotives3) = mgr.removeRepetition(important3)
#(removed4,newMotives4) = mgr.removeRepetition(important4)
#(removed5,newMotives5) = mgr.removeRepetition(important5)

#mgr.createMotiveGraph(newMotives2)
#motiveGraph2 = mgr.createMotiveGraph(newMotives2)
#mgr.reduceMotiveGraph(motiveGraph2)
#ind2 = mgr.getMotivesGroupsFromGraph(motiveGraph2)
#char2 = mgr.characteristicMotives(newMotives2,ind2)

#mgr.createMotiveGraph(newMotives3)
#motiveGraph3 = mgr.createMotiveGraph(newMotives3)
#mgr.reduceMotiveGraph(motiveGraph3)
#ind3 = mgr.getMotivesGroupsFromGraph(motiveGraph3)
#char3 = mgr.characteristicMotives(newMotives3,ind3)

#mgr.createMotiveGraph(newMotives4)
#motiveGraph4 = mgr.createMotiveGraph(newMotives4)
#mgr.reduceMotiveGraph(motiveGraph4)
#ind4 = mgr.getMotivesGroupsFromGraph(motiveGraph4)
#char4 = mgr.characteristicMotives(newMotives4,ind4)

#mgr.createMotiveGraph(newMotives5)
#motiveGraph5 = mgr.createMotiveGraph(newMotives5)
#mgr.reduceMotiveGraph(motiveGraph5)
#ind5 = mgr.getMotivesGroupsFromGraph(motiveGraph5)
#char5 = mgr.characteristicMotives(newMotives5,ind5)

#print(ind2)
#for i in range(char2.__len__()):
#    print(char2[i])

motiveGraph = mgr.createMotiveGraph(newMotives)
weights2 = [motiveGraph.get_edge_data(i[0],i[1])['weight'] for i in motiveGraph.edges()]
plt.hist(weights2)
mgr.reduceMotiveGraph(motiveGraph)

#newMotives2[21][0].show()
#newMotives2[28][0].show()



#s1 = stream.Measure()
#s1.TimeSignature = meter.TimeSignature('3/4')
#s1.append([notes[0], notes[1], notes[2]])
#s2 = stream.Measure()
#s2.TimeSignature = meter.TimeSignature('3/4')
#s2.append([notes[3],notes[4]])
#p1 = stream.Part()
#p1.append([s1.TimeSignature, s1])
#p1.append([s2.TimeSignature, s2])
#p1.show()
#s3 = stream.Measure()
#s3.TimeSignature = meter.TimeSignature('4/4')
#s3.append([s3.TimeSignature, notes[0],notes[1],notes[3]])
#p1.append(s3)
#p1.show()



#soprano.recurse().getElementsByClass(meter.TimeSignature)[0]

#bChords = bwv295.chordify() #zbiera głosy w jeden akord
#for c in bChords.recurse().getElementsByClass('Chord'):
#    c.closedPosition(forceOctave=4, inPlace=True) #przetwarza akord do pozycji zamkniętej

#for c in bChords.recurse().getElementsByClass('Chord'):
#    rn = roman.romanNumeralFromChord(c, key.Key('A'))
#    c.addLyric(str(rn.figure)) #funkcja w tonacji klucza key.Key()
#    c.annotateIntervals() #podpisuje kolejne interwały w akordzie

#################dodanie pięciolini z akordami`
#bwv295.insert(0, bChords)
#bwv295.show()
#interval.notesToChromatic(bwv295.recurse().notes[2], bwv295.recurse().notes[bwv295.recurse().notes.index(n1)+1])

#s = corpus.parse('AlhambraReel')
#s.show()
#analysis.patel.nPVI(s.flat)

#dir(note)
#f = note.Note("F5")

#a = converter.parse("tinynotation: 4/4 g4 e8 e f4 d8 d c4 e g2")
#a.show()
#b = converter.parse("tinynotation: 2/4 g4 e8 e f4 d8 d c4 e g2")
#b.show()
#c = converter.parse("tinynotation: 4/4 r2 g4 e8 e f4 d8 d c4 e g1")
#c.show()
#d = converter.parse("tinynotation: 4/4 g2 e4 e f2 d4 d c2 e g1")
#d.show()
#e = converter.parse("tinynotation: 4/4 c'4 a8 a b-4 g8 g f4 a c'2")
#e.show()

#for thisNote in a.recurse().notes:
#  thisNote.addLyric(thisNote.nameWithOctave)
#  thisNote.addLyric(thisNote.duration.quarterLength)
#  thisNote.addLyric(thisNote.pitch.pitchClass)
#a.show()

#for thisNote in b.recurse().notes:
#  thisNote.addLyric(thisNote.nameWithOctave)
#  thisNote.addLyric(thisNote.duration.quarterLength)
#  thisNote.addLyric(thisNote.pitch.pitchClass)
#b.show()

#for thisNote in c.recurse().notes:
#  thisNote.addLyric(thisNote.nameWithOctave)
#  thisNote.addLyric(thisNote.duration.quarterLength)
#  thisNote.addLyric(thisNote.pitch.pitchClass)
#c.show()

#for thisNote in d.recurse().notes:
#  thisNote.addLyric(thisNote.nameWithOctave)
#  thisNote.addLyric(thisNote.duration.quarterLength)
#  thisNote.addLyric(thisNote.pitch.pitchClass)
#d.show()

#for thisNote in e.recurse().notes:
#  thisNote.addLyric(thisNote.nameWithOctave)
#  thisNote.addLyric(thisNote.duration.quarterLength)
#  thisNote.addLyric(thisNote.pitch.pitchClass)
#e.show()"""

