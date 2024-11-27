"""
Use ftp to download GO annotations and urllib to download the GO terms.
Downloaded files are saved in the GOA directory.
"""

from ftplib import FTP
from urllib.request import urlretrieve

def download():
    # Download GO annotations
    annotation_files = [
        'FLY/goa_fly.gaf.gz',
        'HUMAN/goa_human.gaf.gz',
        'MOUSE/goa_mouse.gaf.gz',
    ]

    with FTP('ftp.ebi.ac.uk') as ftp:
        ftp.login()
        ftp.cwd('pub/databases/GO/goa/')
        for file_ in annotation_files:
            outfile = 'data/GOA/' + file_.split('/')[1]
            with open(outfile, 'wb') as f:
                ftp.retrbinary(f'RETR {file_}', f.write)
                
    # Download go-basic.obo
    urlretrieve('http://geneontology.org/ontology/go-basic.obo', 'GOA/go-basic.obo')
