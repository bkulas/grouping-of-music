#%%
import music21 as m21
import harmony as hrm
import rhythm as rth
import mgr
import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import roc_curve, auc
import csv
#%%
DATABASE = 1
lmd_plag = "/Users/basia/Doktorat - lokalnie/Analiza muzyki/Bazy danych/LMD_plagiarism/"
#%%
## Baza dancyh BMM 
if DATABASE == 1 :
    ori_path = "/Users/basia/Doktorat - lokalnie/Analiza muzyki/Bazy danych/BMMDet_MPDSet-master/data/midi/dataset_real_ori/"
    plag_path = "/Users/basia/Doktorat - lokalnie/Analiza muzyki/Bazy danych/BMMDet_MPDSet-master/data/midi/dataset_real_plag/"

    original = []
    for i in sorted(os.listdir(ori_path)):
        print(i)
        original.append([i, m21.converter.parse(ori_path+i)])

    plagiat = []
    for i in sorted(os.listdir(plag_path)):
        print(i)
        if i != '.DS_Store':
            plagiat.append([i, m21.converter.parse(plag_path+i)])
    original.remove(original[27])
    plagiat.remove(plagiat[27])
    original.remove(original[26])
    plagiat.remove(plagiat[26])


#%%
## Baza danych Yuan
if DATABASE == 2 :
    db2_path = "/Users/basia/Doktorat - lokalnie/Analiza muzyki/Bazy danych/music-copyright-expanded/CopyrightCases/simpleMIDI/"

    original = []
    plagiat = []
    for i in sorted(os.listdir(db2_path)):
        print(i)
        if i[-4:] != '.mid':
            continue
        if i[2] == 'a':
            original.append([i, m21.converter.parse(db2_path+i)])
        else: plagiat.append([i, m21.converter.parse(db2_path+i)])
    original.remove(original[26])
    plagiat.remove(plagiat[26])
    original.remove(original[19])
    plagiat.remove(plagiat[19])
    original.remove(original[14])
    plagiat.remove(plagiat[14])

    yuanpath = "/Users/basia/Doktorat - lokalnie/Analiza muzyki/Bazy danych/music-copyright-expanded/Yuan_raw_data.csv"
    rows =[]
    with open(yuanpath, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=';', quotechar='|')
        for row in reader:
            rows.append(row)
    yuanlabels = [[int(i[0]),int(i[9])] for i in rows[1:]]
    yuanlabels.remove(yuanlabels[26])
    yuanlabels.remove(yuanlabels[19])
    yuanlabels.remove(yuanlabels[14])
#%%
motives_ori = [[original[i][0], mgr.analyseComposition(original[i][1], 0.8)] for i in range(len(original))]
motives_pl = [[plagiat[i][0], mgr.analyseComposition(plagiat[i][1], 0.8)] for i in range(len(plagiat))]
melodicSimilarity0 = []
melodicSimilarity0 = [[mgr.countJaccardIndex(a[1][0],b[1][0],0) for a in motives_ori] for b in motives_pl]
#%%
motives_ori = [[original[i][0], mgr.analyseComposition(original[i][1],2)] for i in range(len(original))]
motives_pl = [[plagiat[i][0], mgr.analyseComposition(plagiat[i][1],2)] for i in range(len(plagiat))]
melodicSimilarity2 = []
melodicSimilarity2 = [[mgr.countJaccardIndex(a[1][0],b[1][0],0) for a in motives_ori] for b in motives_pl]
#%%
similarity_ori = [[mgr.countJaccardIndex(a[1][0],b[1][0],0) for a in motives_ori] for b in motives_ori]
similarity_pl = [[mgr.countJaccardIndex(a[1][0],b[1][0],0) for a in motives_pl] for b in motives_pl]

#%%
original_chords = []
for i in original:
    original_chords.append([i[0],hrm.getChordsFromMelody(i[1])])
#%%
plagiat_chords = []
for i in plagiat:
    plagiat_chords.append([i[0], hrm.getChordsFromMelody(i[1])])

# %%
harmonicSimilarity = [[hrm.countHarmonicSimilarity(i[1],j[1]) for i in original_chords] for j in plagiat_chords]


# %%
# TODO: podobieństwo rytmiczne 
rythmicSimilarity = [[rth.countRythmicSimilarity(i[1],j[1]) for i in original] for j in plagiat]
#%%
sim1 = np.add(harmonicSimilarity,np.multiply(10,melodicSimilarity0))
simX = np.multiply(harmonicSimilarity,np.add(0.1,melodicSimilarity0))
#sim2 = np.add(harmonicSimilarity,np.multiply(5,melodicSimilarity2))

# %%
maksy = []
indeksy = []
roznice = []
diag = [simX[i][i] for i in range(len(simX))]
for i in simX:
    maksy.append(max(i))
    indeksy.append(np.where(i == max(i))[0][0])

#for i in range(len(maksy)):
#    roznice.append(sim2[i][i]-maksy[i])
# %%
import matplotlib.pyplot as plt
import numpy as np
#%%
barWidth = 0.4
y_pos = np.arange(len(diag))
y_pos2 = [x+barWidth for x in y_pos]
plt.bar(y_pos, diag, width = barWidth, color = '#FF800E')
plt.bar(y_pos2, maksy, width = barWidth, color = '#5F9ED1')
plt.legend(['Similarity for plagiarism cases', 'Maximum value of similarities for songs in the corpus'])
#TODO punkty dla podobieństwa percepcyjnego z pliku perceptual_simi.csv
#plt
 
# Show graphic
plt.show()

# %%
sns.color_palette("colorblind")
sns.heatmap(melodicSimilarity0, annot=True, annot_kws={"size": 5})
plt.show()
# sns.heatmap(melodicSimilarity2, annot=True, annot_kws={"size": 5})
# plt.show()
sns.heatmap(harmonicSimilarity, annot=True, annot_kws={"size": 5})
plt.show()

#%% test dla bazy Yuan
from sklearn.metrics import roc_curve, auc
#y = np.diag(np.full(39,1)) 
y = [i[1] for i in yuanlabels] 
fpr, tpr, thresholds = roc_curve(y, np.diag(harmonicSimilarity))
roc_auc = auc(fpr, tpr)
plt.style.use('tableau-colorblind10') 
#plt.title('Receiver Operating Characteristic')
plt.plot(fpr, tpr, label = 'AUC = %0.2f' % roc_auc)
plt.legend(loc = 'lower right')
#plt.plot([0, 1], [0, 1],'r--')
plt.xlim([0, 1])
plt.ylim([0, 1])
plt.ylabel('True Positive Rate')
plt.xlabel('False Positive Rate')
plt.show()
#%%
mel = np.diag(melodicSimilarity0)
mel_plag = [mel[i] for i in range(len(mel)) if y[i]==1]
mel_notplag = [mel[i] for i in range(len(mel)) if y[i]==0]
#%%
barWidth = 0.4
y_pos = [i for i in range(len(y)) if y[i]==1]
y_pos2 = [i for i in range(len(y)) if y[i]==0]
plt.bar(y_pos, [mel[i] for i in y_pos], width = barWidth, color = '#FF800E')
plt.bar(y_pos2, [mel[i] for i in y_pos2], width = barWidth, color = '#5F9ED1')
plt.legend(['Infringement', 'No infringement'])
plt.ylabel('Similarity')
plt.xlabel('Number of the case')
np.mean(mel_plag) #0.23891449172261497
np.mean(mel_notplag) #0.09580498866213152

#%%
SIZE = len(original)

y = np.diag(np.full(SIZE,1)) 
#%%
y = [i[1] for i in yuanlabels] 
fpr1, tpr1, thresholds = roc_curve(y, np.diag(harmonicSimilarity))
roc_auc1 = auc(fpr1, tpr1)
fpr2, tpr2, thresholds = roc_curve(y, np.diag(melodicSimilarity0))
roc_auc2 = auc(fpr2, tpr2)
fpr3, tpr3, thresholds = roc_curve(y, np.diag(sim1))
roc_auc3 = auc(fpr3, tpr3)
plt.style.use('tableau-colorblind10') 
#plt.title('Receiver Operating Characteristic')
plt.plot(fpr1, tpr1, label = 'AUC harmonic = %0.2f' % roc_auc1)
plt.plot(fpr2, tpr2, label = 'AUC melodic = %0.2f' % roc_auc2)
plt.plot(fpr3, tpr3, label = 'AUC = %0.2f' % roc_auc3)
plt.legend(loc = 'lower right')
#plt.plot([0, 1], [0, 1],'r--')
plt.xlim([0, 1])
plt.ylim([0, 1])
plt.ylabel('True Positive Rate')
plt.xlabel('False Positive Rate')
plt.show()
#--------------------------------------------------------------------
# # %%


# data = np.random.rand(10, 10) 
# plt.imshow(data, cmap='hot', interpolation='nearest') 
# plt.colorbar() 
# plt.title('Mapa ciepła (heatmap)') 
# plt.show() 
# # Mapa ciepła dla ekspresji genów 
# geny = 50 
# warunki = 10 
# ekspresja_genow = np.random.rand(geny, warunki) 
# plt.imshow(ekspresja_genow, cmap='coolwarm', aspect='auto') 
# plt.colorbar() 
# plt.xlabel('Warunki eksperymentalne') 
# plt.ylabel('Geny') 
# plt.title('Poziomy ekspresji genów w warunkach eksperymentalnych') 
# plt.show() 
# # %%

# plt.imshow(similarity, cmap='coolwarm', annot=True) 
# plt.colorbar() 
# plt.title('Podobieństwo') 
# plt.show() 
# # %%
# sns.heatmap(similarity, annot=True, annot_kws={"size": 5})
# plt.show()

# # %%
# path = "/Users/basia/Analiza muzyki/Bazy danych/music-copyright-expanded/CopyrightCases/MIDI"
# # %%
# podobienstwo_plagiatu = []
# podobienstwo_nieplagiatu = []
# for i in range(len(similarity)):
#     podobienstwo_plagiatu.append(similarity[i][i])
#     if i!=22:
#         podobienstwo_nieplagiatu.append(similarity[i][i+1])
# #%%
# y_pos = np.arange(len(podobienstwo_plagiatu))
 
# #Figsize
# plt.figure(figsize=(10,5))
 
# # Create bars
# plt.bar(y_pos, podobienstwo_plagiatu, color = '#969696')
  
# # Create names on the x-axis
# plt.xticks(y_pos, )
 
# plt.xlabel('Cases', fontsize=12, color='#323232')
# plt.ylabel('Melodic similarity', fontsize=12, color='#323232')
# plt.ylim(top=1)
# plt.title('Melodic similarity of plagiarism cases', fontsize=16, color='#323232')
 
# # Show graphic
# plt.show()

# # %%
# podobienstwo_nieplagiatu = []
# for i in range(len(similarity)-1):
#     podobienstwo_nieplagiatu.append(similarity[i][i+1])
#     #for j in range(len(similarity[i])):
#     #    if i != j:
#     #        podobienstwo_nieplagiatu.append(similarity[i][j])
# y_pos = np.arange(len(podobienstwo_nieplagiatu))
 
# #Figsize
# plt.figure(figsize=(10,5))
 
# # Create bars
# plt.bar(y_pos, podobienstwo_nieplagiatu, color = '#969696')
  
# # Create names on the x-axis
# plt.xticks(y_pos, )
 
# plt.xlabel('Cases', fontsize=12, color='#323232')
# plt.ylabel('Melodic similarity', fontsize=12, color='#323232')
# plt.ylim(top=1)
# plt.title('Melodic similarity of non-plagiarism cases', fontsize=16, color='#323232')
 
# # Show graphic
# plt.show()
# # %%

# %%
