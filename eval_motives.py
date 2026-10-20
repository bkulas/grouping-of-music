# Evaluation of motifs discovery algorithm on BPS-MOTIF dataset
#%%
import pretty_midi
import numpy as np
import csv
import music21 as m21
import mgr
from mir_eval.pattern import establishment_FPR, occurrence_FPR, three_layer_FPR
import time
import sys
from eval_motives_func import *
from motives_selection import get_patterns_from_motives, select_best_motives
import sys

#sys.path.append("../../grouping-of-music/")

'''directory of the JKUPDD dataset'''
jkupdd_data_dir = r'../motif_discovery-main/JKUPDD/JKUPDD-noAudio-Aug2013/groundTruth'
jkupdd_corpus = ['bachBWV889Fg', 'beethovenOp2No1Mvt3', 'chopinOp24No4', 'gibbonsSilverSwan1612', 'mozartK282Mvt2']
jkupdd_notes_csv = ['wtc2f20.csv', 'sonata01-3.csv', 'mazurka24-4.csv', 'silverswan.csv', 'sonata04-2.csv']

#%%
bps_motif_path = "/Users/basia/Doktorat - lokalnie/ToolforMusicAnalysis/Beethoven_motif-main/"
motif_midi = "motif_midi/"
csv_label = "csv_label/"
csv_notes = "csv_notes/"
motif_mxl = "motif_mxl/"
theta = 0.9
longest = 20

if(len(sys.argv)< 3):
    print("Za mało danych")
elif(len(sys.argv)==3):
    theta=float(sys.argv[1])
    longest=int(sys.argv[2])

# wybiera zadany procent największych motywów.
def get_biggest(patterns, percent):
    size = int(percent*len(patterns))
    if size == 0: size = 1
    patterns.sort(key=len)
    return patterns[-size:]



#%%
#def main():

all_P_est, all_R_est, all_F_est = [], [], []
all_P_occ, all_R_occ, all_F_occ = [], [], []
all_P_thr, all_R_thr, all_F_thr = [], [], []
all_lenghts_ref = []
all_lenghts = []
runtime = 0
runtime_eval_all = 0
all_nP_est, all_nR_est, all_nF_est = [], [], []
all_nP_occ, all_nR_occ, all_nF_occ = [], [], []
all_nP_thr, all_nR_thr, all_nF_thr = [], [], []

for i in range(1,33):
    # if i in [7,11,12,19,23,24,26,29]:
    #     continue
    piece = str(i).zfill(2)
    print('piece', piece)

    filename_csv = bps_motif_path + csv_label + piece+"-1.csv"
    filename_midi = bps_motif_path + motif_midi + piece+"-1.mid"

    ref_motives = load_all_motives(filename_csv, filename_midi)

    patterns_ref = [[list(occur[['onset', 'pitch']]) for occur in motif] for motif in ref_motives.values()]

    beethoven =  m21.converter.parse(bps_motif_path+motif_mxl+piece+"-1.mxl")

    start_time = time.time()
    motives, timeSign, przedtakt = mgr.analyseComposition(beethoven, theta, 0, longest, pauses = False)
    runtime_one = time.time() - start_time
    runtime += runtime_one
    print('runtime_one %.4f' % runtime_one)

    #lista motywów w formie (onset, pitch)
    patterns = get_patterns_from_motives(motives, timeSign, przedtakt)
    # patterns = []
    # for i in motives: #### Jeśli nie ma flat to tutaj są klasy długości motywów
    #     for j in i:
    #         pattern = []
    #         for k in j:
    #             if przedtakt == True:
    #                 pattern.append(list(zip([x-timeSign.beatCount for x in k[10]], k[9])))
    #             #korekta obliczenia onsetu gdy metrum /8 lub alla breve
    #             else:
    #                 pattern.append(list(zip(k[10], k[9]))) # x - timeSign if przedtakt == True
    #         patterns.append(pattern)


    new = []
    new1, patterns1 = select_best_motives(patterns, patterns_ref, new)
    # new2, patterns2 = select_best_motives(patterns1, patterns_ref, new1)

    eval_time = time.time()
    F_est, P_est, R_est = establishment_FPR(patterns_ref, patterns)
    F_occ, P_occ, R_occ = occurrence_FPR(patterns_ref, patterns)
    F_thr, P_thr, R_thr = three_layer_FPR(patterns_ref, patterns)

    # nF_est, nP_est, nR_est = establishment_FPR(patterns_ref, new2)
    # nF_occ, nP_occ, nR_occ = occurrence_FPR(patterns_ref, new2)
    # nF_thr, nP_thr, nR_thr = three_layer_FPR(patterns_ref, new2)
    runtime_eval = time.time() - eval_time
    runtime_eval_all += runtime_eval

    print('est P %.4f, R %.4f, F %.4f' % (P_est, R_est, F_est))
    print('occ P %.4f, R %.4f, F %.4f' % (P_occ, R_occ, F_occ))
    print('thr P %.4f, R %.4f, F %.4f' % (P_thr, R_thr, F_thr))
    # print("After selection:")
    # print('new est P %.4f, R %.4f, F %.4f' % (nP_est, nR_est, nF_est))
    # print('new occ P %.4f, R %.4f, F %.4f' % (nP_occ, nR_occ, nF_occ))
    # print('new thr P %.4f, R %.4f, F %.4f' % (nP_thr, nR_thr, nF_thr))
    print('runtime_eval %.4f' % runtime_eval)

    all_lenghts_ref.append(len(patterns_ref))
    all_lenghts.append(len(patterns))

    all_P_est.append(P_est)
    all_R_est.append(R_est)
    all_F_est.append(F_est)
    all_P_occ.append(P_occ)
    all_R_occ.append(R_occ)
    all_F_occ.append(F_occ)
    all_P_thr.append(P_thr)
    all_R_thr.append(R_thr)
    all_F_thr.append(F_thr)

    # all_nP_est.append(nP_est)
    # all_nR_est.append(nR_est)
    # all_nF_est.append(nF_est)
    # all_nP_occ.append(nP_occ)
    # all_nR_occ.append(nR_occ)
    # all_nF_occ.append(nF_occ)
    # all_nP_thr.append(nP_thr)
    # all_nR_thr.append(nR_thr)
    # all_nF_thr.append(nF_thr)

    # ten = get_biggest(patterns,0.1)

    # tenF_est, tenP_est, tenR_est = establishment_FPR(patterns_ref, ten)
    # tenF_occ, tenP_occ, tenR_occ = occurrence_FPR(patterns_ref, ten)
    # tenF_thr, tenP_thr, tenR_thr = three_layer_FPR(patterns_ref, ten)

    # print('est P %.4f, R %.4f, F %.4f' % (tenP_est, tenR_est, tenF_est))
    # print('occ P %.4f, R %.4f, F %.4f' % (tenP_occ, tenR_occ, tenF_occ))
    # print('thr P %.4f, R %.4f, F %.4f' % (tenP_thr, tenR_thr, tenF_thr))

    # all_tenP_est.append(tenP_est)
    # all_tenR_est.append(tenR_est)
    # all_tenR_est.append(tenR_est)
    # all_tenF_est.append(tenF_est)
    # all_tenP_occ.append(tenP_occ)
    # all_tenR_occ.append(tenR_occ)
    # all_tenF_occ.append(tenF_occ)
    # all_tenP_thr.append(tenP_thr)
    # all_tenR_thr.append(tenR_thr)
    # all_tenF_thr.append(tenF_thr)

mean_P_est = np.mean(all_P_est)
mean_R_est = np.mean(all_R_est)
mean_F_est = np.mean(all_F_est)
mean_P_occ = np.mean(all_P_occ)
mean_R_occ = np.mean(all_R_occ)
mean_F_occ = np.mean(all_F_occ)
mean_P_thr = np.mean(all_P_thr)
mean_R_thr = np.mean(all_R_thr)
mean_F_thr = np.mean(all_F_thr)
print('Mean_est P %.4f, R %.4f, F %.4f' % (mean_P_est, mean_R_est, mean_F_est))
print('Mean_occ P %.4f, R %.4f, F %.4f' % (mean_P_occ, mean_R_occ, mean_F_occ))
print('Mean_thr P %.4f, R %.4f, F %.4f' % (mean_P_thr, mean_R_thr, mean_F_thr))
mean_nP_est = np.mean(all_nP_est)
mean_nR_est = np.mean(all_nR_est)
mean_nF_est = np.mean(all_nF_est)
mean_nP_occ = np.mean(all_nP_occ)
mean_nR_occ = np.mean(all_nR_occ)
mean_nF_occ = np.mean(all_nF_occ)
mean_nP_thr = np.mean(all_nP_thr)
mean_nR_thr = np.mean(all_nR_thr)
mean_nF_thr = np.mean(all_nF_thr)
print("After selection:")
print('Mean_est P %.4f, R %.4f, F %.4f' % (mean_nP_est, mean_nR_est, mean_nF_est))
print('Mean_occ P %.4f, R %.4f, F %.4f' % (mean_nP_occ, mean_nR_occ, mean_nF_occ))
print('Mean_thr P %.4f, R %.4f, F %.4f' % (mean_nP_thr, mean_nR_thr, mean_nF_thr))
print('Runtime %.4f Averaged Runtime %.4f' % (runtime / 60, runtime / 1440))
print('Eval Runtime %.4f Averaged Eval Runtime %.4f' % (runtime_eval_all / 60, runtime_eval_all / 1440))

# mean_tenP_est = np.mean(all_tenP_est)
# mean_tenR_est = np.mean(all_tenR_est)
# mean_tenF_est = np.mean(all_tenF_est)
# mean_tenP_occ = np.mean(all_tenP_occ)
# mean_tenR_occ = np.mean(all_tenR_occ)
# mean_tenF_occ = np.mean(all_tenF_occ)
# mean_tenP_thr = np.mean(all_tenP_thr)
# mean_tenR_thr = np.mean(all_tenR_thr)
# mean_tenF_thr = np.mean(all_tenF_thr)
# print('Mean_est P %.4f, R %.4f, F %.4f' % (mean_tenP_est, mean_tenR_est, mean_tenF_est))
# print('Mean_occ P %.4f, R %.4f, F %.4f' % (mean_tenP_occ, mean_tenR_occ, mean_F_occ))
# print('Mean_thr P %.4f, R %.4f, F %.4f' % (mean_tenP_thr, mean_tenR_thr, mean_tenF_thr))
# %%
benchmark = {
    'SIATEC': [0.1804, 0.6444, 0.2803, 0.2102, 0.2771, 0.2235, 0.0408, 0.2994, 0.0713, 28.5082],
    'COSIATEC': [0.2118, 0.4557, 0.2893, 0.2769, 0.1282, 0.1548, 0.0489, 0.1601, 0.0742, 208.4119],
    'SIATECCompress': [0.2136, 0.4326, 0.2835, 0.1430, 0.1121, 0.1103, 0.0579, 0.1703, 0.0856, 636.6930],
    'Hsiao et al.': [0.5709, 0.8339, 0.6733, 0.1491, 0.4174, 0.2002, 0.1222, 0.2644, 0.1646, 119.5330]
}

# benchmark={
#     "Hsiao": [0.3726, 0.8528, 0.5156, 0.2101, 0.5328, 0.2943, 0.0855, 0.3830, 0.1382, 2484.6020]
# }

# %%
import matplotlib.pyplot as plt
benchmark["Proposed"] = [mean_P_est, mean_R_est, mean_F_est, mean_P_occ, mean_R_occ, mean_F_occ, mean_P_thr, mean_R_thr, mean_F_thr, runtime/60]
#benchmark["mine - n"] = [mean_nP_est, mean_nR_est, mean_nF_est, mean_nP_occ, mean_nR_occ, mean_nF_occ, mean_nP_thr, mean_nR_thr, mean_nF_thr, runtime/60]
#benchmark["0.7 15"] = [0.4588, 0.7443, 0.5643, 0.2633, 0.4019, 0.3099, 0.1968, 0.3651, 0.2547, 18.6993]
#benchmark["0.5 15"] = [0.6681,	0.7461,	0.6994,	0.1376,	0.4436,	0.2066,	0.2235,	0.2269,	0.2219, 20.8785]
xpoints = np.array(["P_est", "R_est", "F_est", "P_occ", "R_occ", "F_occ", "P_thr", "R_thr", "F_thr"])
ypoints = np.array([x[:-1] for x in list(benchmark.values())])
plt.plot(xpoints, ypoints[0], xpoints, ypoints[1], xpoints, ypoints[2], xpoints, ypoints[3], xpoints, ypoints[4])#, xpoints, ypoints[5])
plt.legend(benchmark)
plt.show()

#%%
# Bar width and x locations
w, x = 0.18, np.arange(len(xpoints))

fig, ax = plt.subplots()
ax.bar(x - 2*w, ypoints[0], width=w, label='SIATEC')
ax.bar(x - w, ypoints[1], width=w, label='COSIATEC')
ax.bar(x , ypoints[2], width=w, label='SIATECCompress')
ax.bar(x + w, ypoints[3], width=w, label='HSIAO')
ax.bar(x + 2*w, ypoints[4], width=w, label='Proposed')

ax.set_xticks(x)
ax.set_xticklabels(xpoints)
#ax.set_title('Grouped Bar Chart')
ax.legend()

plt.show()

# %%
# newM = [j for i in motives for j in i] #flat motives file
# withoutSub = mgr.removeSubmotives(newM)

# %% zapis motywów
names = ['a','b','c','d','e','f','g','h','i','j','k','l']
with open('../../Wyniki/testy_motywow.csv', 'a', newline='') as csvfile:
    #fieldnames = ["onset,"	'midi_number',	'morphetic_number',	'duration',	'staff_number',	'measure','type']
    fieldnames = ["timestamp","theta", "longest", "P_est", "R_est", "F_est", "P_occ", "R_occ", "F_occ", "P_thr", "R_thr", "F_thr", "runtime", "patterns_ref", "patterns_count"]
    writer = csv.writer(csvfile)

    #writer.writerow(fieldnames)
    timestamp = time.time()
    writer.writerow([timestamp, theta, longest, mean_P_est, mean_R_est, mean_F_est, mean_P_occ, mean_R_occ, mean_F_occ, mean_P_thr, mean_R_thr, mean_F_thr, runtime/60, np.mean(all_lenghts_ref), np.mean(all_lenghts)])

#%% wykres ile mamy motywów
# Bar width and x locations
xpoints = np.array(range(24))
ypoints = np.array([all_lenghts_ref, all_lenghts])
w, x = 0.4, np.arange(len(xpoints))

fig, ax = plt.subplots()
ax.bar(x - 0.5*w, ypoints[0], width=w, label='ref')
ax.bar(x + 0.5*w, ypoints[1], width=w, label='estim')

ax.set_xticks(x)
ax.set_xticklabels(xpoints)
#ax.set_title('Grouped Bar Chart')
ax.legend()

plt.show()


# %% Zapis wyników dla mniejszego zbioru danych
with open('../../Wyniki/testy_motywow_mine.csv', 'w', newline='') as csvfile:
    #fieldnames = ["onset,"	'midi_number',	'morphetic_number',	'duration',	'staff_number',	'measure','type']
    fieldnames = ["timestamp", "dataset","theta", "longest", "P_est", "R_est", "F_est", "P_occ", "R_occ", "F_occ", "P_thr", "R_thr", "F_thr", "runtime", "patterns_ref", "patterns_count"]
    writer = csv.writer(csvfile)

    writer.writerow(fieldnames)
    timestamp = time.time()
    writer.writerow([timestamp, "beethoven2", theta, longest, mean_P_est, mean_R_est, mean_F_est, mean_P_occ, mean_R_occ, mean_F_occ, mean_P_thr, mean_R_thr, mean_F_thr, runtime/60, np.mean(all_lenghts_ref), np.mean(all_lenghts)])


## Testowanie wyników wykrywania motywów
S = []
for i in range(len(patterns)):
    F, P, R = establishment_FPR(patterns_ref, [patterns[i]])
    S.append([i,F,P,R,len(patterns[i]), len(patterns[i][0])])

S.sort(key = lambda row: row[4])

## Wykres wartości miary jakoś dla poszczególnych motywów posortowanych po wielkości.
xpoints = np.array(range(len(patterns)))
ypoints = np.array([[x[1] for x in S], [x[2] for x in S], [x[3] for x in S]])
w, x = 0.3, np.arange(len(xpoints))

fig, ax = plt.subplots()
ax.bar(x - 0.5*w, ypoints[0], width=w, label='F')
ax.bar(x , ypoints[1], width=w, label='P')
ax.bar(x + 0.5*w, ypoints[2], width=w, label='R')

ax.set_xticks(x)
ax.set_xticklabels(xpoints)
#ax.set_title('Grouped Bar Chart')
ax.legend()

plt.show()

## wyznaczenie wartości miar dla częśći wyników
ten = int(0.1*len(patterns))
forty = int(0.4*len(patterns))
half = int(0.5*len(patterns))

#indeksy
ten_idx = [x[0] for x in S[-ten:]]
forty_idx = [x[0] for x in S[-forty:]]
half_idx = [x[0] for x in S[-half:]]

ten = get_biggest(patterns,0.1)

#wykres wyników dla 10% największych
benchmark["mine"] = [mean_P_est, mean_R_est, mean_F_est, mean_P_occ, mean_R_occ, mean_F_occ, mean_P_thr, mean_R_thr, mean_F_thr, runtime/60]
benchmark["ten"] = [mean_tenP_est, mean_tenR_est, mean_tenF_est, mean_tenP_occ, mean_tenR_occ, mean_tenF_occ, mean_tenP_thr, mean_tenR_thr, mean_tenF_thr, runtime/60]
#benchmark["0.7 15"] = [0.4588, 0.7443, 0.5643, 0.2633, 0.4019, 0.3099, 0.1968, 0.3651, 0.2547, 18.6993]
#benchmark["0.5 15"] = [0.6681,	0.7461,	0.6994,	0.1376,	0.4436,	0.2066,	0.2235,	0.2269,	0.2219, 20.8785]
xpoints = np.array(["P_est", "R_est", "F_est", "P_occ", "R_occ", "F_occ", "P_thr", "R_thr", "F_thr"])
ypoints = np.array([x[:-1] for x in list(benchmark.values())])
plt.plot(xpoints, ypoints[0], xpoints, ypoints[1], xpoints, ypoints[2])
plt.legend(benchmark)
plt.show()

#apis do pliku największych
with open('../../Wyniki/testy_motywow_procent_największych.csv', 'a', newline='') as csvfile:
    #fieldnames = ["onset,"	'midi_number',	'morphetic_number',	'duration',	'staff_number',	'measure','type']
    fieldnames = ["timestamp","dataset", "percent of motives", "theta", "longest", "P_est", "R_est", "F_est", "P_occ", "R_occ", "F_occ", "P_thr", "R_thr", "F_thr"]
    writer = csv.writer(csvfile)

    writer.writerow(fieldnames)
    timestamp = time.time()
    writer.writerow([timestamp,"beethoven2", "ten", theta, longest, mean_tenP_est, mean_tenR_est, mean_tenF_est, mean_tenP_occ, mean_tenR_occ, mean_tenF_occ, mean_tenP_thr, mean_tenR_thr, mean_tenF_thr])

#%%
## zbiór danych JKUPDD - spory problem z wczytaniem danych. Przedtakt poprawiony - dla pierwszego i czwartego utworu wyniki porównywalne.
import os
from os.path import join as jpath
from os.path import isdir

def load_jkupdd_notes_csv(csv_dir):
    dt = [
        ('onset', np.float32),
        ('pitch', np.int32),
        ('duration', np.float32),
        ('staff', np.int32),
    ] # datatype

    # Format data as structured array
    with open(csv_dir, 'r') as f:
        reader = csv.reader(f, delimiter=',')
        notes = np.array([tuple([float(x) for i, x in enumerate(row) if i != 2]) for row in reader], dtype=dt)

    # Get unique notes irrespective of 'staffNum'
    _, unique_indices = np.unique(notes[['onset', 'pitch']], return_index=True)
    notes = notes[unique_indices]
    print('deleted notes:', [i for i in range(notes.size) if i not in unique_indices])

    notes = notes[notes['duration'] > 0]
    return np.sort(notes, order=['onset', 'pitch'])

def load_jkupdd_midi(midi_dir):
    melody =  m21.converter.parse(midi_dir)
    return melody

def load_jkupdd_patterns_csv(csv_dir):
    annotators_dir = [jpath(csv_dir, f) for f in os.listdir(csv_dir) if isdir(jpath(csv_dir, f))]
    # print(annotators_dir)
    patterns_dir = [
        jpath(annotator, f) for annotator in annotators_dir for f in os.listdir(annotator) if isdir(jpath(annotator, f))
    ]
    # print(patterns_dir)

    patterns = []
    for pattern_dir in patterns_dir:
        occurrences_csv = [
            jpath(pattern_dir, 'occurrences/csv', f)
            for f in os.listdir(jpath(pattern_dir, 'occurrences/csv')) if f.endswith('.csv')
        ]
        # print(occurrences_csv)

        pattern = []
        for occurrence_csv in occurrences_csv:
            with open(occurrence_csv, 'r') as f:
                reader = csv.reader(f, delimiter=',')
                pattern.append([tuple([float(x) for x in row]) for row in reader])
        # print(pattern)
        patterns.append(list(pattern))

    print('number of patterns', len(patterns))
    [print('pattern %s with %d occurrences' % (chr(i+65), len(pattern)))for i, pattern in enumerate(patterns)]
    return patterns


def jkupdd_eval():

    all_P_est, all_R_est, all_F_est = [], [], []
    all_P_occ, all_R_occ, all_F_occ = [], [], []
    all_P_thr, all_R_thr, all_F_thr = [], [], []
    runtime = 0
    total_n_notes = 0
    for i in range(5):
        print('file %s' % jkupdd_notes_csv[i])
        #note_csv_dir = jpath(jkupdd_data_dir, jkupdd_corpus[i], 'polyphonic/csv', jkupdd_notes_csv[i])
        pattern_csv_dir = jpath(jkupdd_data_dir, jkupdd_corpus[i], 'polyphonic/repeatedPatterns')
        #notes = load_jkupdd_notes_csv(note_csv_dir)
        melody = load_jkupdd_midi(jpath(jkupdd_data_dir, jkupdd_corpus[i], 'polyphonic/mxl', jkupdd_notes_csv[i][:-3]+'mxl'))
        #dataset = Dataset(note_csv_dir)
        #dataset._vectors = [Vector(list(x)[:2]) for x in dataset]
        patterns_ref = load_jkupdd_patterns_csv(pattern_csv_dir)
        melody_midi_dir = jpath(jkupdd_data_dir, jkupdd_corpus[i], 'polyphonic\midi', jkupdd_notes_csv[i][:-3]+'mid')

        #print(notes)
        #total_n_notes += len(notes)

        start_time = time.time()
        motives, timeSign, przedtakt = mgr.analyseComposition(melody, theta, 0, longest)
        patterns_est = get_patterns_from_motives(motives, timeSign, przedtakt)
        # patterns_est = find_motives(notes) # proposed algorithm
        # tecs = new_algorithms.siatechf(dataset, min_cr=2)
        # tecs = orig_algorithms.cosiatech(dataset)
        #tecs = orig_algorithms.siatech_compress(dataset)
        # Convert tecs to mir_eval format
        #patterns_est = [get_all_occurrences(tec) for tec in tecs if len(tec.get_translators())]
        elp = time.time() - start_time
        runtime += elp
        print('elapsed time %.4f sec' % elp)
        # print('len(patterns_est)', len(patterns_est))
        # print(patterns_est)
        # exit()

        # Evaluation
        # elp = time.time()
        F_est, P_est, R_est = establishment_FPR(patterns_ref, patterns_est)
        F_occ, P_occ, R_occ = occurrence_FPR(patterns_ref, patterns_est)
        F_thr, P_thr, R_thr = three_layer_FPR(patterns_ref, patterns_est)
        print('est P %.4f, R %.4f, F %.4f' % (P_est, R_est, F_est))
        print('occ P %.4f, R %.4f, F %.4f' % (P_occ, R_occ, F_occ))
        print('thr P %.4f, R %.4f, F %.4f' % (P_thr, R_thr, F_thr))
        # print('elapsed time, eval %.2f sec' % (time.time() - elp))

        all_P_est.append(P_est)
        all_R_est.append(R_est)
        all_F_est.append(F_est)
        all_P_occ.append(P_occ)
        all_R_occ.append(R_occ)
        all_F_occ.append(F_occ)
        all_P_thr.append(P_thr)
        all_R_thr.append(R_thr)
        all_F_thr.append(F_thr)
        # exit()

        continue


    print('avg notes %d' %(total_n_notes/5))
    mean_P_est = np.mean(all_P_est)
    mean_R_est = np.mean(all_R_est)
    mean_F_est = np.mean(all_F_est)
    mean_P_occ = np.mean(all_P_occ)
    mean_R_occ = np.mean(all_R_occ)
    mean_F_occ = np.mean(all_F_occ)
    mean_P_thr = np.mean(all_P_thr)
    mean_R_thr = np.mean(all_R_thr)
    mean_F_thr = np.mean(all_F_thr)
    print('Mean_est P %.4f, R %.4f, F %.4f' % (mean_P_est, mean_R_est, mean_F_est))
    print('Mean_occ P %.4f, R %.4f, F %.4f' % (mean_P_occ, mean_R_occ, mean_F_occ))
    print('Mean_thr P %.4f, R %.4f, F %.4f' % (mean_P_thr, mean_R_thr, mean_F_thr))
    print('Runtime %.4f min Averaged runtime %.4f min' % (runtime / 60, runtime / 300))

# %%
