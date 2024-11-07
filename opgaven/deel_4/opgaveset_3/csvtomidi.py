import py_midicsv as pm
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('-i', '--infile')
parser.add_argument('-o', '--outfile')
args = parser.parse_args()

infile = args.infile
outfile = args.outfile

with open(infile) as f:
    csv_string = f.read().split("\n")

# Parse the CSV output of the previous command back into a MIDI file
midi_object = pm.csv_to_midi(csv_string)

# Save the parsed MIDI file to disk
with open(outfile, "wb") as output_file:
    midi_writer = pm.FileWriter(output_file)
    midi_writer.write(midi_object)
