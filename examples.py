#%%
from music21 import *
import mgr
import grouping
import csv
import matplotlib as plt
import numpy as np

londonfile = "/Users/basia/Doktorat - lokalnie/Analiza muzyki/Bazy danych/London_Bridge_is_falling_down.mid"

london = converter.parse(londonfile)

motives = mgr.analyseComposition(london,0)

#%%
perceptual = "/Users/basia/Doktorat - lokalnie/Analiza muzyki/Bazy danych/music-copyright-expanded/PerceptualData"

rows=[]
with open(perceptual, newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in spamreader:
        print(', '.join(row))
        rows.append(row)
    
full_simi = [float(i[1]) for i in rows[1:]]
melody_simi = [float(i[2])  for i in rows[1:]]
lyrics_simi = [i[3]  for i in rows[1:]]
for i in range(len(lyrics_simi)):
    if lyrics_simi[i] == '':
        lyrics_simi[i] = 0
lyrics_simi = [float(i) for i in lyrics_simi]

lyrics_simi.remove(lyrics_simi[14])
melody_simi.remove(melody_simi[14])
full_simi.remove(full_simi[14])

# %%
diag = [melodicSimilarity0[i][i] for i in range(len(melodicSimilarity0))]
barWidth = 0.4
y_pos = np.arange(len(diag))
y_pos2 = [x+barWidth for x in y_pos]
plt.bar(y_pos, diag, width = barWidth, color = '#FF800E')
plt.bar(y_pos2, melody_simi, width = barWidth, color = '#5F9ED1')


diag_scaled = [i/max(diag) for i in diag]
melody_simi_scaled = [i/max(melody_simi) for i in melody_simi]
barWidth = 0.4
y_pos = np.arange(len(diag))
y_pos2 = [x+barWidth for x in y_pos]
plt.bar(y_pos, diag, width = barWidth, color = '#FF800E')
plt.bar(y_pos2, melody_simi_scaled, width = barWidth, color = '#5F9ED1')