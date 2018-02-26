#! /usr/bin/env python
# encoding: utf-8

from __future__ import unicode_literals

import numpy as np
import soundfile as sf

class Audio(object):
    def __init__(self, data, sample_rate):
        if data is not None:
            self.data = data
            if len(self.data.shape) == 1:
                self.data = self.data[:, np.newaxis]
            self.sample_rate = sample_rate
        else:
            self.data, self.sample_rate = None, None

    @classmethod
    def from_file(cls, filename):
        data, sample_rate = sf.read(filename)
        return cls(data, sample_rate)

    def trim_silences(self, threshold_db):
        self.data = np.expand_dims(trim(np.squeeze(self.data), top_db=threshold_db)[0], axis=1)

    def play(self, blocking=True):
        import sounddevice as sd
        sd.play(self.data, self.sample_rate, blocking=blocking)

    def write(self, filename):
        sf.write(filename, self.data, self.sample_rate)


def power_to_db(S, amin=1e-10):
    magnitude = np.abs(S)
    ref_value = np.max(magnitude)

    log_spec = 10.0 * np.log10(np.maximum(amin, magnitude))
    log_spec -= 10.0 * np.log10(np.maximum(amin, ref_value))

    return log_spec


class DummyArray(object):
    def __init__(self, interface, base=None):
        self.__array_interface__ = interface
        self.base = base


def _maybe_view_as_subclass(original_array, new_array):
    if type(original_array) is not type(new_array):
        new_array = new_array.view(type=type(original_array))
        if new_array.__array_finalize__:
            new_array.__array_finalize__(original_array)
    return new_array


def as_strided(x, shape=None, strides=None, subok=False, writeable=True):
    x = np.array(x, copy=False, subok=subok)
    interface = dict(x.__array_interface__)
    if shape is not None:
        interface['shape'] = tuple(shape)
    if strides is not None:
        interface['strides'] = tuple(strides)

    array = np.asarray(DummyArray(interface, base=x))
    array.dtype = x.dtype

    view = _maybe_view_as_subclass(x, array)

    if view.flags.writeable and not writeable:
        view.flags.writeable = False

    return view


def frame(y, frame_length=2048, hop_length=512):
    n_frames = 1 + int((len(y) - frame_length) / hop_length)
    y_frames = as_strided(y, shape=(frame_length, n_frames),
                          strides=(y.itemsize, hop_length * y.itemsize))
    return y_frames


def rmse(y, frame_length=2048, hop_length=512):
    y = np.pad(y, int(frame_length // 2), mode='reflect')
    x = frame(y, frame_length=frame_length, hop_length=hop_length)
    return np.sqrt(np.mean(np.abs(x) ** 2, axis=0, keepdims=True))


def _signal_to_frame_nonsilent(y, frame_length=2048, hop_length=512, top_db=60):
    mse = rmse(y=y,
               frame_length=frame_length,
               hop_length=hop_length) ** 2
    return power_to_db(mse.squeeze()) > - top_db


def frames_to_samples(frames, hop_length=512, n_fft=None):
    return (np.atleast_1d(frames) * hop_length).astype(int)


def trim(y, top_db=25, frame_length=2048, hop_length=512):
    non_silent = _signal_to_frame_nonsilent(y,
                                            frame_length=frame_length,
                                            hop_length=hop_length,
                                            top_db=top_db)
    nonzero = np.flatnonzero(non_silent)

    start = int(frames_to_samples(nonzero[0], hop_length))
    end = min(y.shape[-1],
              int(frames_to_samples(nonzero[-1] + 1, hop_length)))

    full_index = [slice(None)] * y.ndim
    full_index[-1] = slice(start, end)

    return y[full_index], np.asarray([start, end])