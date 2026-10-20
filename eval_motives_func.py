import numpy as np
import csv
import pretty_midi



## from motif_discovery-main - BPS-motif
def load_all_motives_csv(filename):
    '''Load all motives from CSV file'''
    dt = [
        ('onset', np.float32),
        ('end', np.float32),
        ('type', '<U4'),
        ('measure', np.int32),
        ('start_beat', np.float32),
        ('duration', np.float32),
        ('track', np.int32),
        ('time_sig', '<U5'),
        ('measure_score', np.int32),
        ('onset_midi', np.float32),
        ('end_midi', np.float32),
    ] # datatype

    # Format data as structured array
    with open(filename, 'r') as f:
        reader = csv.reader(f, delimiter=',')
        next(reader) # skip header
        motives_csv = np.array([tuple(row) for row in reader], dtype=dt)
    print('number of motives =', motives_csv.size)
    return np.sort(motives_csv, order=['onset', 'end'])

def load_all_motives_midi(filename):
    '''Load all motives from MIDI file'''
    dt = [
        ('onset', np.float32),
        ('end', np.float32),
        ('pitch', np.int32),
    ] # datatype

    midi_data = pretty_midi.PrettyMIDI(filename)
    notes_midi = [
        np.array([(note.start, note.end, note.pitch) for note in instrument.notes], dtype=dt)
        for instrument in midi_data.instruments
    ] # [(notes in track i), ...]
    return notes_midi

def load_all_motives(filename_csv, filename_midi):
    '''Combine motif informations of CSV and MIDI files'''
    motives_csv = load_all_motives_csv(filename_csv)
    motives_midi = load_all_motives_midi(filename_midi)
    motives = {}
    max_n_notes = 0
    max_duration = 0
    for motif in motives_csv:
        type = motif['type']
        if type not in motives.keys():
            motives[type] = [] # create a motif type

        track = motif['track'] # track id
        onset_midi, end_midi = motif[['onset_midi', 'end_midi']] # onset and end in midi time
        onset_calibration = motif['onset_midi'] - motif['onset'] # onset calibration if pickup measure
        track_notes = motives_midi[track]
        cond = (track_notes['onset'] >= onset_midi) & (track_notes['onset'] < end_midi)
        motif_notes = track_notes[cond]

        if motif_notes.size > max_n_notes:
            max_n_notes = motif_notes.size
        if motif['end'] - motif['onset'] > max_duration:
            max_duration = motif['end'] - motif['onset']

        motif_notes['onset'] -= onset_calibration
        motif_notes['end'] -= onset_calibration
        motives[type].append(motif_notes)

    assert len([motif for types in motives.values() for motif in types]) == motives_csv.size
    print('number of motif types', len(motives.keys()))
    print('max_n_notes', max_n_notes)
    print('max_duration', max_duration)
    return motives
## end of motives from motif_discovery-main