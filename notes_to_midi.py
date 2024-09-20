def notes_to_midi(generated_notes, output_file='generated_music_01.mid'):
    output_stream = stream.Stream()

    for item in generated_notes:
        if '.' in item:  # Check if it's a chord
            notes_in_chord = item.split('.')
            chord_notes = [note.Note(int(n)) for n in notes_in_chord]
            new_chord = chord.Chord(chord_notes)
            output_stream.append(new_chord)
        else:
            new_note = note.Note(item)
            output_stream.append(new_note)

    # Save the stream to a MIDI file
    output_stream.write('midi', fp=output_file)
    print(f"MIDI file saved as {output_file}")

# Generate a sequence of notes
num_notes_to_generate = 50
generated_music = generate_music(model, num_notes_to_generate)

# Convert the generated notes back to MIDI format
notes_to_midi(generated_music)


def visualize_midi(output_file='generated_music_01.mid'):
    score = stream.Score()
    midi_stream = stream.parse(output_file)
    score.append(midi_stream)
    score.show('text')  # Display as text, can also use 'musicxml' for better visual representation

# Visualize the saved MIDI file
visualize_midi()
