import numpy as np
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
import seaborn
seaborn.set_context('talk')

def plot_dataset(dataset, N_per_sample=1, nbins=30):
    orig_dataset = dataset.copy()
    dataset = dataset.reshape((len(dataset) // N_per_sample, N_per_sample))
    dataset = np.mean(dataset, axis=1)
    xlim = (6, 14)
    fig, ax = plt.subplots(2, 1, figsize=(8, 6), sharex=True)
    fig.subplots_adjust(hspace=0)
    plt.sca(ax[0])
    plt.plot(dataset, np.arange(len(dataset)), lw=1)
    plt.title('Dataset')
    plt.ylabel('Trial')

    plt.sca(ax[1])
    bins = np.linspace(*xlim, num=nbins)
    plt.hist(dataset, bins=bins, edgecolor='k')
    plt.hist(orig_dataset, bins=bins, edgecolor='k', alpha=0.3, zorder=0)
    plt.axvline(np.mean(dataset), c='r', label='mean')
    plt.axvline(np.mean(dataset) - np.std(dataset), c='r', ls='--', label='stdev')
    plt.axvline(np.mean(dataset) + np.std(dataset), c='r', ls='--')
    plt.xlim(xlim)
    plt.legend(loc='upper right', fontsize='small')
    if N_per_sample > 1:
        plt.text(xlim[0] * 1.1, plt.ylim()[1] * 0.8, 
                 r'$1/\sqrt{N_s}=' + f'{1/np.sqrt(N_per_sample):.2f}$',
                 fontsize='small')
    plt.xlabel('Mean')
    plt.ylabel('Occurence')

    return dataset
