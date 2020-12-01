import numpy as np
from playsound import playsound
from pydub import AudioSegment
from pydub.playback import play


def playOneSound(sounds, playing):
    playing = True
    sound_path = "./sounds/"
    filename = sound_path + sounds[0]
    sound = AudioSegment.from_file(filename, format='wav')
    play(sound)
    playing = True


def playTwoSounds(sounds, playing):
    playing = True
    sound_path = "./sounds/"
    f1 = sound_path + sounds[0]
    f2 = sound_path + sounds[1]
    sound1 = AudioSegment.from_file(f1, format='wav')
    sound2 = AudioSegment.from_file(f2, format='wav')
    sound = sound1.overlay(sound2)
    play(sound)


def doNothing(sounds, playing):
    return


actions = {
    0: doNothing,
    1: playOneSound,
    2: playTwoSounds
}


def playSound(coords, velocities, regions, references, playing):

    sounds = []
    for i in range(len(coords)):
        coord = coords[i]
        velocity = velocities[i]
        threshold = 0

        row = coord[0]
        col = coord[1]

        region = regions[row][col]
        if region == 0:
            return
        target_vel = np.array(references[region][1])
        sound = references[region][0]
        speed = np.linalg.norm(velocity)
        cosine = np.dot(velocity, target_vel) / (speed * np.linalg.norm(target_vel))


        if cosine > 0.7 and speed > threshold:
            sounds.append(sound)

    if playing == False:
        action = actions[len(sounds)]
        action(sounds, playing)
    playing = False


if __name__ == "__main__":
    playing = False
    regions = np.array([[1, 2], [3, 4]])
    references = {
        1: ('a.wav', [1, 1]),
        2: ('b.wav', [1, -1]),
        3: ('c.wav', [1, 1]),
        4: ('c2.wav', [1, 1])
    }

    velocity = np.array([1, 1])

    coords = []
    velocities = []

    playSound(coords, velocities, regions, references, playing)
    print("Played nothing")

    c1 = [0, 0]
    v1 = [1, 1]

    coords.append(c1)
    velocities.append(v1)

    playSound(coords, velocities, regions, references, playing)
    print("Played one sound")

    c2 = [0, 1]
    v2 = [1, -1]

    coords.append(c2)
    velocities.append(v2)

    playSound(coords, velocities, regions, references, playing)
    print("Played two sounds")

    c3 = [0, 1]
    v3 = [1, 1]

    coords = [c1, c3]
    velocities = [v1, v3]

    playSound(coords, velocities, regions, references, playing)
    print("Played one sound")

    c4 = [0, 0]
    v4 = [-1, 1]

    coords = [c3, c4]
    velocities = [v3, v4]

    playSound(coords, velocities, regions, references, playing)
    print("Played nothing again")

    playing = True
    coords = [c1, c2]
    velocities = [v1, v2]
    playSound(coords, velocities, regions, references, playing)
    print("Played nothing again")
