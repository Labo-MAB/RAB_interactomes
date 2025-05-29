# Comparing Rab interactive studies

 __Authors__: Francis Bourassa ([@francis-B](https://github.com/Francis-B))
 
 __Email__: <Francis.Bourassa@USherbrooke.ca>

## Description

This repository contains the code used to generate the comparison between RAB interactive studies (Figure 2D; Supplementary Figure 2C) and the correlation between replicate (Supplementary figure) in the following paper:

St-Laurent, V. G., Marchand, B., Larcher, R., Nassari, S., Bourassa, F., Moreau, M., Jean, D., Boisvert, F.-M., Brunet, M. A., & Jean, S. (2024). A Proximity MAP of RAB GTPases. Cold Spring Harbor Laboratory. https://doi.org/10.1101/2024.11.05.621850

## Data files

This analysis was perform by comparing results from the following articles:

- Gillingham, A. K., Sinka, R., Torres, I. L., Lilley, K. S., & Munro, S. (2014). Toward a Comprehensive Map of the Effectors of Rab GTPases. In Developmental Cell (Vol. 31, Issue 3, pp. 358–373). Elsevier BV. https://doi.org/10.1016/j.devcel.2014.10.007
- Gillingham, A. K., Bertram, J., Begum, F., & Munro, S. (2019). In vivo identification of GTPase interactors by mitochondrial relocalization and proximity biotinylation. In eLife (Vol. 8). eLife Sciences Publications, Ltd. https://doi.org/10.7554/elife.45916
- Li, Y., Wang, Y., Zou, L., Tang, X., Yang, Y., Ma, L., Jia, Q., Ni, Q., Liu, S., Tang, L., Lin, R., Wong, E., Sun, W., Wang, L., Wei, Q., Ran, H., Zhang, L., Lian, H., Huang, W., … Wan, Y. (2016). Analysis of the Rab GTPase Interactome in Dendritic Cells Reveals Anti-microbial Functions of the Rab32 Complex in Bacterial Containment. In Immunity (Vol. 44, Issue 2, pp. 422–437). Elsevier BV. https://doi.org/10.1016/j.immuni.2016.01.027

Their dataset can be downloaded respectively from [here](https://www.cell.com/cms/10.1016/j.immuni.2016.01.027/attachment/ac9eee8d-37fa-4d8e-aa0f-636470ed5d7c/mmc3.xlsx), [here](https://www.cell.com/cms/10.1016/j.devcel.2014.10.007/attachment/9420b819-9a34-4822-a7a2-4f85947a86b5/mmc2.xlsx), [here](https://elifesciences.org/download/aHR0cHM6Ly9jZG4uZWxpZmVzY2llbmNlcy5vcmcvYXJ0aWNsZXMvNDU5MTYvZWxpZmUtNDU5MTYtc3VwcDEtdjIueGxzeA--/elife-45916-supp1-v2.xlsx?_hash=D3fefhHVjzBuU7dNfqq4KGGBSPWLnXUZHOgodgNLmtE%3D) and [here](https://www.ebi.ac.uk/pride/archive/projects/PXD033693) (we used the proteinGroups.txt file from the MQ_results.zip). Our own dataset can be found in *data/* folder.

For the last dataset, we had to perform the SAINT analysis. To do so, we created the files needed by SAINT with the *create_saint_input.py* script. The output from SAINT was then used in the notebook for the comparison.

The GO annotations and the GO terms used in this analysis can be downloaded from the notebook directly.

Finally, the orthologs tables used to compare fruit fly genes and mouse genes with human genes can be found in the *orthologs/* folder. All tables were generated with [DIOP Ortholog Finder](https://www.flyrnai.org/cgi-bin/DRSC_orthologs.pl).

## Dependancies

The python package used for the analysis can be found in the *conda/* folder and be created with conda with the following command from the repo directory:

```{bash}
conda install -f conda/environment.yml
```
The SAINT binaries was downloaded [here](https://sourceforge.net/projects/saint-apms/files/SAINTexpress_v3.6.1__2015-05-03.zip/download).
