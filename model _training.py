import glob
from music21 import stream, note, chord
import music21 as m21
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers
import random
from tensorflow import keras

# Function to parse MIDI files and extract notes
def get_notes(midi_files):
    notes = []
    for file in midi_files:
        midi = m21.converter.parse(file)
        notes_to_parse = None

        # Handle parts of the music piece
        parts = m21.instrument.partitionByInstrument(midi)
        if parts:  # If multiple instruments
            notes_to_parse = parts.parts[0].recurse()  # Choose first part
        else:  # Single instrument
            notes_to_parse = midi.flat.notes

        for element in notes_to_parse:
            if isinstance(element, m21.note.Note):
                notes.append(str(element.pitch))  # Get pitch name
            elif isinstance(element, m21.chord.Chord):
                notes.append('.'.join(str(n) for n in element.normalOrder))  # Convert chord to normal order

    return notes

# List of MIDI files
lst1 = [files]

# Extract notes from all MIDI files
all_notes = []
no_midi = 0
for i in lst1:
    midi_files = glob.glob(i)
    notes = get_notes(midi_files)
    all_notes.extend(notes)
    no_midi += 1

print("Number of MIDI files found:", no_midi)

# Save extracted notes to a file
with open(r"C:\Users\Nano\Downloads\newdataset", 'a') as f:
    for note in all_notes:
        f.write("%s\n" % note)

# Load notes from the file
with open(r"C:\Users\Nano\Downloads\newdataset", 'r') as f:
    notes = [line.strip() for line in f.readlines()]

# Adjust sequence length to 50 for better sequence generation
sequence_length = 50

# Get unique notes and create a mapping to integers
unique_notes = sorted(list(set(notes)))
note_to_int = {note: number for number, note in enumerate(unique_notes)}

# Generate input sequences (X) and output notes (y)
input_sequences = []
output_notes = []

for i in range(len(notes) - sequence_length):
    seq_in = notes[i:i + sequence_length]
    seq_out = notes[i + sequence_length]
    input_sequences.append([note_to_int[note] for note in seq_in])
    output_notes.append(note_to_int[seq_out])

# Reshape X and normalize it
X = np.reshape(input_sequences, (len(input_sequences), sequence_length, 1))
X = X / float(len(unique_notes))  # Normalize the values

# One-hot encode the output notes
y = np.zeros((len(output_notes), len(unique_notes)))
for i, note in enumerate(output_notes):
    y[i][note] = 1

# Check shapes of X and y to verify correctness
print("Shape of X:", X.shape)
print("Shape of y:", y.shape)

# Define the LSTM model
model = tf.keras.Sequential()
model.add(layers.LSTM(256, input_shape=(X.shape[1], X.shape[2]), return_sequences=True))
model.add(layers.Dropout(0.3))
model.add(layers.LSTM(256, return_sequences=False))
model.add(layers.Dropout(0.3))
model.add(layers.Dense(256, activation='relu'))
model.add(layers.Dense(len(unique_notes), activation='softmax'))

# Compile the model
model.compile(loss='categorical_crossentropy', optimizer='adam')

# Model summary
model.summary()

# Train the modela
model.fit(X, y, epochs=100, batch_size=64)

model.save('music_composer_model_01.keras')
