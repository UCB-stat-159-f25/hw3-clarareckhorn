# function to whiten data
def whiten(strain, interp_psd, dt):
    Nt = len(strain)
    freqs = np.fft.rfftfreq(Nt, dt)
    freqs1 = np.linspace(0, 2048, Nt // 2 + 1)

    # whitening: transform to freq domain, divide by asd, then transform back, 
    # taking care to get normalization right.
    hf = np.fft.rfft(strain)
    norm = 1./np.sqrt(1./(dt*2))
    white_hf = hf / np.sqrt(interp_psd(freqs)) * norm
    white_ht = np.fft.irfft(white_hf, n=Nt)
    return white_ht

# make wav (sound) files from the whitened data, +-2s around the event.
from scipy.io import wavfile

# function to keep the data within integer limits, and write to wavfile:
def write_wavfile(filename,fs,data):
    d = np.int16(data/np.max(np.abs(data)) * 32767 * 0.9)
    wavfile.write(filename,int(fs), d)

# function that shifts frequency of a band-passed signal
def reqshift(data,fshift=100,sample_rate=4096):
    """Frequency shift the signal by constant
    """
    x = np.fft.rfft(data)
    T = len(data)/float(sample_rate)
    df = 1.0/T
    nbins = int(fshift/df)
    # print T,df,nbins,x.real.shape
    y = np.roll(x.real,nbins) + 1j*np.roll(x.imag,nbins)
    y[0:nbins]=0.
    z = np.fft.irfft(y)
    return z

# ligotools/utils.py  (append these functions)

import os
import numpy as np
import matplotlib.pyplot as plt

def plot_matched_filter_time_series(
    time, SNR, timemax,
    strain_whitenbp, template_match,
    det, eventname, plottype="png",
    pcolor="r", outdir="figures",
    zoom_xlim=(-0.15,0.05), ylim_whiten=(-10,10)
):
    """
    create and save the SNR plot, zoomed SNR, whitened data + template, and residual plots.
    Parameters are the arrays and scalars computed in the notebook.
    """
    os.makedirs(outdir, exist_ok=True)

    # SNR full + zoomed SNR (first file)
    plt.figure(figsize=(10,8))
    plt.subplot(2,1,1)
    plt.plot(time - timemax, SNR, pcolor, label=f'{det} SNR(t)')
    plt.grid(True)
    plt.ylabel('SNR')
    plt.xlabel(f'Time since {timemax:.4f}')
    plt.legend(loc='upper left')
    plt.title(f'{det} matched filter SNR around event')

    plt.subplot(2,1,2)
    plt.plot(time - timemax, SNR, pcolor, label=f'{det} SNR(t)')
    plt.grid(True)
    plt.ylabel('SNR')
    plt.xlim(zoom_xlim)
    plt.grid(True)
    plt.xlabel(f'Time since {timemax:.4f}')
    plt.legend(loc='upper left')

    fname = os.path.join(outdir, f"{eventname}_{det}_SNR.{plottype}")
    plt.savefig(fname)
    plt.close()

    # whitened data + template and residual (second file)
    plt.figure(figsize=(10,8))
    plt.subplot(2,1,1)
    plt.plot(time - timemax, strain_whitenbp, pcolor, label=f'{det} whitened h(t)')
    plt.plot(time - timemax, template_match, 'k', label='Template(t)')
    plt.ylim(ylim_whiten)
    plt.xlim(zoom_xlim)
    plt.grid(True)
    plt.xlabel(f'Time since {timemax:.4f}')
    plt.ylabel('whitened strain (units of noise stdev)')
    plt.legend(loc='upper left')
    plt.title(f'{det} whitened data around event')

    plt.subplot(2,1,2)
    plt.plot(time - timemax, strain_whitenbp - template_match, pcolor, label=f'{det} resid')
    plt.ylim(ylim_whiten)
    plt.xlim(zoom_xlim)
    plt.grid(True)
    plt.xlabel(f'Time since {timemax:.4f}')
    plt.ylabel('whitened strain (units of noise stdev)')
    plt.legend(loc='upper left')
    plt.title(f'{det} Residual whitened data after subtracting template around event')

    fname2 = os.path.join(outdir, f"{eventname}_{det}_matchtime.{plottype}")
    plt.savefig(fname2)
    plt.close()

# plotting code in a separate utility function
def plot_psd_and_template(
    datafreq, template_fft, d_eff,
    freqs, data_psd,
    fs, det, eventname,
    plottype="png", outdir="figures",
    xlim=(20, None), ylim=(1e-24, 1e-20)
):
    """
    plot PSD (ASD) and template in frequency domain and save figure
    """
    os.makedirs(outdir, exist_ok=True)

    plt.figure(figsize=(10,6))
    template_f = np.absolute(template_fft) * np.sqrt(np.abs(datafreq)) / d_eff
    plt.loglog(datafreq, template_f, 'k', label='template(f)*sqrt(f)')
    plt.loglog(freqs, np.sqrt(data_psd), label=f'{det} ASD')
    plt.xlim(xlim[0], xlim[1] if xlim[1] is not None else fs/2)
    plt.ylim(ylim)
    plt.grid(True)
    plt.xlabel('frequency (Hz)')
    plt.ylabel('strain noise ASD (strain/rtHz), template h(f)*rt(f)')
    plt.legend(loc='upper left')
    plt.title(f'{det} ASD and template around event')
    fname = os.path.join(outdir, f"{eventname}_{det}_matchfreq.{plottype}")
    plt.savefig(fname)
    plt.close()
