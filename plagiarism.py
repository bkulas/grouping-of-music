#%%
import music21
import mgr
import os
#%%
data_path = "/Users/basia/Analiza muzyki/Bazy danych/Plagiat/1/midi"
original=[]
for i in [1,3,4]:
    original.append(music21.converter.parse("/Users/basia/Analiza muzyki/Bazy danych/Plagiat/"+str(i)+"/midi/case"+str(i)+"_original.mid"))
# %%
plagiat=[]
for i in [1,3,4]:
    plagiat.append(music21.converter.parse("/Users/basia/Analiza muzyki/Bazy danych/Plagiat/"+str(i)+"/midi/case"+str(i)+"_plagiat.mid"))

#%%
motives_ori = [mgr.analyseComposition(original[i],0) for i in range(len(original))]
# %%
motives_pl = [mgr.analyseComposition(plagiat[i],0) for i in range(len(plagiat))]
# %%
similarity = []
similarity = [[mgr.countJaccardIndex(a,b,0) for a in motives_ori] for b in motives_pl]
similarity_ori = [[mgr.countJaccardIndex(a,b,0) for a in motives_ori] for b in motives_ori]
similarity_pl = [[mgr.countJaccardIndex(a,b,0) for a in motives_pl] for b in motives_pl]
# %%
ori_path = "/Users/basia/Analiza muzyki/BMMDet_MPDSet-master/data/midi/dataset_real_ori/case10_Anftrag Deutsches Reich-Stahlgewitter"
plag_path = "/Users/basia/Analiza muzyki/BMMDet_MPDSet-master/data/midi/dataset_real_plag/"

# %%
for i in sorted(os.listdir(ori_path)):
    original.append(music21.converter.parse(ori_path+i))
# %%
for i in sorted(os.listdir(plag_path)):
    plagiat.append(music21.converter.parse(plag_path+i))

# %%
