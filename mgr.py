from music21 import *

a = converter.parse("tinynotation: 3/4 g4 e e f4 d d c8 e g2 B4 A G")
b = converter.parse("tinynotation: 3/4 c4 C d")

for thisNote in a.recurse().notes:
    thisNote.addLyric(thisNote.nameWithOctave) #pitch
    thisNote.addLyric(thisNote.name)
    thisNote.addLyric(thisNote.quarterLength) #rythm per 4th note
    thisNote.addLyric(thisNote.pitch.pitchClass) #półtony od C trzeba powiązać z oktawą do interwałów
    thisNote.addLyric(thisNote.pitch.octave)

def countChromatic(first: int, second: int, semitones: list, octaves: list) -> int:
    return semitones[second] - semitones[first] + 12*(octaves[second]-octaves[first])

def analyseMelody(melody):
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
    motivesNotes = []
    motivesNotesNames = []
    motivesIntervals = []
    motivesDiatonicIntervals = []
    motivesChromativIntervals = []
    motivesContour = []
    motivesRythm4 = []
    motivesRythm8 = []
    for i in range(analysis[0].__len__()-(count-1)):
        s1 = []
        s2 = []
        s3 = []
        s4 = []
        s5 = []
        s6 = []
        s7 = []
        s8 = []
        for j in range(count):
            s1.append(analysis[0][i+j])
            s2.append(analysis[1][i+j])
            s7.append(analysis[6][i+j])
            s8.append(analysis[7][i+j])
        if i<(analysis[0].__len__()-count):
            for j in range(count-1):
                s3.append(analysis[2][i + j])
                s4.append(analysis[3][i + j])
                s5.append(analysis[4][i + j])
                s6.append(analysis[5][i + j])
        motivesNotes.append(s1)
        motivesNotesNames.append(s2)
        motivesIntervals.append(s3)
        motivesDiatonicIntervals.append(s4)
        motivesChromativIntervals.append(s5)
        motivesContour.append(s6)
        motivesRythm4.append(s7)
        motivesRythm8.append(s8)
    return (motivesNotes, motivesNotesNames, motivesIntervals, motivesDiatonicIntervals,
            motivesChromativIntervals, motivesContour, motivesRythm4, motivesRythm8)

def showMotive(motive: list):
    s1 = stream.Measure()
    s1.append(motive)
    s1.show()

#zliczamy podobne motywy na liście motywów analysis wg wartości value
def countSimilar(analysis: list, value: int ) -> list:
    similars = []
    for i in range(analysis[value].__len__()):
        c = 0
        for j in range(analysis[value].__len__()):
            flag = 0
            for k in range(analysis[value][0].__len__()):
                if analysis[value][i][k] != analysis[value][j][k]:
                    flag = 1
            if flag == 0:
                c=c+1
        similars.append(c)
    return similars

def countExactSimilar(analysis: list ) -> list:
    exactSimilars = []
    for i in range(analysis[0].__len__()):
        c = 0
        for j in range(analysis[0].__len__()):
            flag = 0
            if analysis[3][i] != analysis[3][j] or analysis[4][i] != analysis[4][j]\
                    or analysis[5][i] != analysis[5][j] or analysis[6][i] != analysis[6][j]:
                flag = 1
            if flag == 0:
                c=c+1
        exactSimilars.append(c)
    return exactSimilars

def getImportantMotives(motives: list, similars: list, value: int) -> list:
    importantMotives = motives
    c = 0
    for m in range(motives[0].__len__()):
        if similars[m] == 1:
            del importantMotives[0][m-c]
            del importantMotives[1][m-c]
            del importantMotives[2][m-c]
            del importantMotives[3][m-c]
            del importantMotives[4][m-c]
            del importantMotives[5][m-c]
            del importantMotives[6][m-c]
            del importantMotives[7][m-c]
            c = c+1
    #removeRepetition(importantMotives)
    return importantMotives

def removeRepetition(motives: list):
    removed = []
    newMotives = []
    for elem in motives[1]:
        flag = 0
        for elem2 in newMotives:
            if elem == elem2:
                removed.append(elem2)
                flag = 1
                break
        if flag == 0:
            newMotives.append(elem)

