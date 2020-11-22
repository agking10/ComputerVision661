import numpy as np
from pydub import AudioSegment
from pydub.playback import play


def play_note(coords, velocity, regions, references, instrument):
    threshold = 0
    
    row = coords[0]
    col = coords[1]

    region = regions[row][col]
    note = references[region]
    note_path = './' + instrument + '/' + note
    
    if velocity > threshold:
        sound = AudioSegment.from_wav(note_path)
        play(sound)

instrument = 'xylophone'
regions = np.array([[1,2],[3,4]])
references = {
    1: 'a.wav',
    2: 'b.wav',
    3: 'c.wav',
    4: 'c2.wav'
}

velocity = 10

x = 0
y = 0
for i in range(2):
    for j in range(2):
        play_note((x,y), velocity, regions, references, instrument)
        y += 1
    x += 1
    y = 0


                   
