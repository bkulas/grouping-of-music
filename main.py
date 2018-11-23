from music21 import *
import mgr
#import constant
#import matplotlib.pyplot as plt

bwv295 = corpus.parse('bach/bwv295')

a = mgr.analyseComposition(bwv295)

for i in range(a.__len__()):
    print(a[i])

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

#motiveGraph = mgr.createMotiveGraph(newMotives2)
#weights2 = [motiveGraph.get_edge_data(i[0],i[1])['weight'] for i in motiveGraph.edges()]
#plt.hist(weights2)
#mgr.reduceMotiveGraph(motiveGraph)

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
#e.show()
