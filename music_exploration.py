# Weryfikacja wyznaczania motywów na prostym utworze London bridge is falling down
#%%
import music21 as m21
import sys
sys.path.append("..")
import mgr
import tools.visualization as vis
#%%
lonbrid_file = '/Users/basia/Doktorat - lokalnie/Analiza muzyki/Bazy danych/London_Bridge_is_falling_down.mxl'
lonbrid_file2 = '/Users/basia/Doktorat - lokalnie/Analiza muzyki/Bazy danych/London_Bridge_is_falling_down-kopia.mxl'
two_of_us_file = '/Users/basia/Doktorat - lokalnie/Analiza muzyki/Bazy danych/Just_the_two_of_us.mxl'

twoofus = m21.converter.parse(two_of_us_file)
lonbrid = m21.converter.parse(lonbrid_file)
lonbrid2 = m21.converter.parse(lonbrid_file2)
motives, timeSign, przedtakt = mgr.analyseComposition(lonbrid, 0.9, 0, 10, True)
motives2, timeSign2, przedtakt2 = mgr.analyseComposition(lonbrid2, 0.9, 0, 10, True)
motives3, timeSign3, przedtakt3 = mgr.analyseComposition(twoofus, 0.9, 0, 10, True)
#%%
vis.show_motives_in_piece(motives, lonbrid)
#%% TODO problem z wyświetleniem motywów - moze uda sie zrobic jakies znalezienie motywow w oryginalnym utworze i zmiane koloru bez naruszania struktury utworu.
vis.show_motives_in_piece(motives2, lonbrid2)
#%%
def submelodys(melody, length):
    notes = []
    submelodys = []
    for thisNote in melody.recurse().notesAndRests:
        if type(thisNote) == m21.note.Note or type(thisNote) == m21.note.Rest:
            notes.append(thisNote)
    for i in range(len(notes)-length+1):
        submelodys.append(notes[i:i+length])
    return submelodys

def allSubmelodys(melody, maxlength):
    subs = []
    for i in range(maxlength):
        sub = submelodys(melody, i+1)
        subs.append(sub)
    return subs

#druga wersja moe być na długość lub offset pierwszego dźwieku w takcie - kwestia przedłuzonych nut.
def durations_of_firsts(melody):
    durations = []
    for i in melody.recurse().notesAndRests:
        if i.offset == 0.0:
            durations.append(i.duration)
    return durations