import numpy as np
import os
from utils import whiten, write_wavfile, reqshift
import pickle

def test_whitten_returns_array():
    test_dir = os.path.dirname(__file__)
    data_path = os.path.join(test_dir, 'data', 'gravitational_wave_data.pkl')
    
    with open(data_path, 'rb') as f:
        loaded_data = pickle.load(f)

    strain_H1 = loaded_data['strain_H1']
    psd_H1 = loaded_data['psd_H1']
    dt = loaded_data['dt']
    
    res = whiten(strain_H1, psd_H1, dt)
    assert type(res) == np.ndarray

def test_whitten_returns_same_size():
    test_dir = os.path.dirname(__file__)
    data_path = os.path.join(test_dir, 'data', 'gravitational_wave_data.pkl')
    
    with open(data_path, 'rb') as f:
        loaded_data = pickle.load(f)

    strain_H1 = loaded_data['strain_H1']
    psd_H1 = loaded_data['psd_H1']
    dt = loaded_data['dt']
    
    res = whiten(strain_H1, psd_H1, dt)
    assert res.size == strain_H1.size