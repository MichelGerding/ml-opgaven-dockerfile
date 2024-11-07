""" 
Convert preprocessed py_midicsv midi csv file back to csv format readable by
py_midicsv. 
"""

import argparse
import random
import json
from pathlib import Path


def decode_seq(seq):
    res = []
    seq = seq.strip()
    for char in seq:
        res.append(enc_to_note[char])
    return res


def new_track(trk_no):
    track_start = (
        f"{trk_no}, 0, Start_track\n"
        f"{trk_no}, 0, Program_c, {trk_no - 2}, 0\n" # Set channel instrument (piano)
    )
    return track_start


parser = argparse.ArgumentParser()
parser.add_argument('-i', '--infile')
parser.add_argument('-o', '--outfile')
parser.add_argument('--tempo', default=250000)
args = parser.parse_args()

infile = args.infile
outfile = args.outfile
tempo = args.tempo

# Load note encoding dictionary.
with open('encoding.json', 'r') as f:
    note_to_enc = json.load(f)
note_to_enc = {int(k): v for k, v in note_to_enc.items()}
enc_to_note = {v: k for k, v in note_to_enc.items()}

res = (
f"0, 0, Header, 1, 6, 240\n" # standard header where nTracks=2, division=240
f"1, 0, Start_track\n"
f"1, 0, Time_signature, 4, 2, 24, 8\n" # time signature is 4/4 by default
f"1, 0, Tempo, {tempo}\n"
f"1, 0, End_track\n"
)

# Split the voice into multiple tracks, because MIDI seems to be unable to play
# three voices simultaneaously in one track.
still_playing = dict()  # note: (track, channel) 
tracks = []
n_words = 0  
seq = ''
ticks_per_timestep = 30
notes_encoded = Path(infile).read_text()
for char in notes_encoded:
    # First read the entire word.
    if seq == '' and char == ' ': # empty timestep
        seq += char
        continue
    elif char != ' ':
        seq += char
        continue

    # Process the word.
    notes = [] if seq == ' ' else decode_seq(seq)
    to_remove = []
    ticks = n_words * ticks_per_timestep
    for n in still_playing.keys():
        if n not in notes: # stop playing note
            trk, chn = still_playing[n]
            tracks[trk-2] += f"{trk}, {ticks}, Note_off_c, {chn}, {n}, 60\n"
            to_remove.append(n)
    still_playing = {k: v for k, v in still_playing.items() if k not in to_remove}
    trk = 2
    for n in notes:
        if n not in still_playing: # new note
            if len(tracks) <= trk - 2:
                tracks.append(new_track(trk))
            chn = trk - 2  # channels start from 0
            tracks[trk-2] += f"{trk}, {ticks}, Note_on_c, {chn}, {n}, 60\n"
            still_playing.update({n: (trk, chn)})
            trk += 1
    n_words += 1
    seq = ''

ticks = ticks + ticks_per_timestep
for n in still_playing.keys(): 
    trk, chn = still_playing[n]
    tracks[trk-2] += f"{trk}, {ticks}, Note_off_c, {chn}, {n}, 60\n"
for i, trk in enumerate(tracks):
    tracks[i] += f"{2 + i}, {ticks}, End_track\n"

res += ''.join(tracks)
res += f"0, 0, End_of_file"

with open(outfile, 'w') as f:
    f.write(res)
