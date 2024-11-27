"""
Extract identified interactors in Gillingham et al. (2014) and Li et al. (2016) 
to find their human orthologs using DIOPT Ortholog Finder version 9.0
https://www.flyrnai.org/cgi-bin/DRSC_orthologs.pl

The queries to get the interactors' orthologs were made on the 2024-04-12.
"""

import re
import pandas as pd
import numpy as np

# ignore warnings from pyopenxl
import warnings
warnings.simplefilter('ignore')

# Datasets to read
GILLINGHAM = 'data/mmc2.xlsx'
LI = 'data/mmc3.xlsx'

# Files to write
GILLINGHAM_INTERACTORS = 'data/orthologs/gillingham2014_interactors.txt'
GILLINGHAM_BAITS = 'data/orthologs/gillingham2014_baits.txt'
LI_INTERACTORS = 'data/orthologs/li2016_interactors.txt'
LI_BAITS = 'data/orthologs/li2016_baits.txt'

# Gillingham (2014)
gillingham = pd.read_excel(GILLINGHAM, skiprows=range(1, 8), header=1,
                         sheet_name='S1A - Total Spectral Counts')
# interactors = np.unique(gillingham['FBgn'].tolist())
interactors = np.unique(gillingham['Symbol'].tolist())
baits = np.unique([col for col in gillingham.columns if re.match(r'Rab\d+', col)])

with open(GILLINGHAM_INTERACTORS, 'w') as f:
    f.write('\n'.join(interactors))
with open(GILLINGHAM_BAITS, 'w') as f:
    f.write('\n'.join(baits))

# Li (2016)    
li = pd.read_excel(LI, skiprows=1, header=0, sheet_name='Bait-prey information', usecols=['Bait', 'Official Symbol', 'Average Spectal Counts'])
li = li.pivot_table(index=['Official Symbol'], columns=['Bait'], values='Average Spectal Counts')
interactors = np.unique(li.index)
baits = np.unique(li.columns)

with open(LI_INTERACTORS, 'w') as f:
    f.write('\n'.join(interactors))
with open(LI_BAITS, 'w') as f:
    f.write('\n'.join(baits))