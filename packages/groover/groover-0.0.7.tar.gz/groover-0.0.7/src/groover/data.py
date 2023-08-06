from .heat_map import get_heat_map
from .melody_extraction import extract_accompaniment
from .timepoints import get_notes_by_period
import numpy as np


def add_instrument_back_pointer(midi_obj):
    for instrument in midi_obj.instruments:
        for note in instrument.notes:
            note.instrument = instrument


def get_heat_maps(midi_obj, n_bins=24, beat_resolution=480, rid_melody=False, is_drum=False, pitches=range(0, 128)):
    add_instrument_back_pointer(midi_obj)
    notes = []
    for instrument in midi_obj.instruments:
        notes += instrument.notes
    if rid_melody:
        notes = extract_accompaniment(notes)
    notes_by_beats = get_notes_by_period(notes, resolution=beat_resolution)

    return np.stack([
        get_heat_map(
            notes=note_set,
            n_bins=n_bins,
            beat_resolution=beat_resolution,
            is_drum=is_drum,
            pitches=pitches
        )
        for note_set in notes_by_beats])


def get_dataset(midi_objs, n_bins=24, beat_resolution=480, rid_melody=False, is_drum=False, pitches=range(0, 128)):
    dataset = np.zeros((0, 24))
    for midi_obj in midi_objs:
        heat_maps = get_heat_maps(
            midi_obj=midi_obj,
            n_bins=n_bins,
            beat_resolution=beat_resolution,
            rid_melody=rid_melody,
            is_drum=is_drum,
            pitches=pitches)
        dataset = np.concatenate((dataset, heat_maps))

    return dataset
