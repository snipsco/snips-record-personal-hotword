#! /usr/bin/env python
# encoding: utf-8

from __future__ import unicode_literals

import argparse
from codecs import open
import json
import datetime   
import os
import time
import pyaudio
import wave
from utils import Audio

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 1024
RECORD_SECONDS = 2.2
SNR_TRIM = 18
FOLDER_BASE = ""
MAX_RECORD_DURATION = 1.6
MAX_DIFFERENCE_DURATION = 0.3
DATE_FORMAT = '%Y_%m_%dT%H_%M_%S'


def record_one(directory, i):
    dest_path = os.path.join(directory, "{0}.wav".format(i))
    
    audio = pyaudio.PyAudio()

    raw_input(
        """\n\nPress enter to record one sample, say your hotword when "recording..." shows up""")
    time.sleep(0.5)

    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)
    print "recording..."
    frames = []

    for j in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    print "finished recording\n"

    stream.stop_stream()
    stream.close()
    audio.terminate()

    waveFile = wave.open(dest_path, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(2)
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()


def check_audios(durations):
    if any([d > MAX_RECORD_DURATION for d in durations]):
        print "WARNING: at least one your record seems to have a too long " \
              "duration, you are going to have"


def record_and_trim(hotword_key, nb_records=3):
    raw_input("Your will have to record your personal hotword." \
              " Please be sure to be in a quiet environment." \
              " Press enter once you are ready.\n".format(
        nb_records))

    directory = os.path.join(FOLDER_BASE, "personal_{0}".format(str(datetime.datetime.now().strftime(DATE_FORMAT))))
    os.makedirs(directory)

    is_validated = False
    while not is_validated:
        audios = []
        for i in range(nb_records):
            record_one(directory, i)
            dest_path = os.path.join(directory, "{0}.wav".format(i))
            audio = Audio.from_file(dest_path)
            audio.trim_silences(SNR_TRIM)
            while audio.duration() > MAX_RECORD_DURATION:
                print "WARNING: there seems to be too much noise in your" \
                      " environment please retry to record this sample by " \
                      "following the instructions."
                record_one(directory, i)
                audio = Audio.from_file(dest_path)
                audio.trim_silences(SNR_TRIM)
            audios.append(audio)

        if any([abs(
                        audio_1.duration() - audio_2.duration()) > MAX_DIFFERENCE_DURATION
                for i, audio_1 in enumerate(audios) for j, audio_2 in
                enumerate(audios) if i < j]):
            print "WARNING: there seems to be too much difference between " \
                  "your records please retry to record all of them by following " \
                  "the instructions."
        else:
            is_validated = True

    for i, audio in enumerate(audios):
        dest_path = os.path.join(directory, "{0}.wav".format(i))
        audio.write(dest_path)

    config = {
        "hotword_key": hotword_key,
        "kind": "personal",
        "dtw_ref": 0.22,
        "from_mfcc": 1,
        "to_mfcc": 13,
        "band_radius": 10,
        "shift": 10,
        "window_size": 10,
        "sample_rate": RATE,
        "frame_length_ms": 25.0,
        "frame_shift_ms": 10.0,
        "num_mfcc": 13,
        "num_mel_bins": 13,
        "mel_low_freq": 20,
        "cepstral_lifter": 22.0,
        "dither": 0.0,
        "window_type": "povey",
        "use_energy": False,
        "energy_floor": 0.0,
        "raw_energy": True,
        "preemphasis_coefficient": 0.97,
        "model_version": 1
    }

    with open(os.path.join(directory, "config.json"), "wb") as f:
        json.dump(config, f, indent=4)

    print "Your model has been saved in {0}".format(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), directory))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('hotword_key', type=str,
                        help="the name of your personal hotword (no special characters)")
    args = parser.parse_args()
    record_and_trim(args.hotword_key)
