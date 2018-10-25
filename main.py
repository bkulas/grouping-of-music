from music21 import *
import mgr
import constant

bwv295 = corpus.parse('bach/bwv295')

soprano = bwv295.parts[0]
alto = bwv295.parts[1]
tenor = bwv295.parts[2]
basso = bwv295.parts[3]

sopranoAnalysis = mgr.analyseMelody(soprano)
altoAnalysis = mgr.analyseMelody(alto)
tenorAnalysis = mgr.analyseMelody(tenor)
bassoAnalysis = mgr.analyseMelody(basso)

mot = mgr.getSimpleMotives(altoAnalysis,2)
mot3 = mgr.getSimpleMotives(altoAnalysis,3)

simi = mgr.countSimilar(mot, constant.NOTESNAMES)
simi3 = mgr.countSimilar(mot3, constant.NOTESNAMES)

esimi = mgr.countExactSimilar(mot)
esimi3 = mgr.countExactSimilar(mot3)

important = mgr.getImportantMotives(mot,simi,1)
important3 = mgr.getImportantMotives(mot3,simi3,1)

print(important)
print(important3)

mgr.removeRepetition(important3)

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
