from subprocess import call
import argparse
from sys import argv
import pickle

parser = argparse.ArgumentParser()
args = {'gwf': 'the path to the gwf workflow',
        'studyfolder': 'the folder containing the studies with the snp p values',
        'snploc': 'plink file stub, such as hapmap or 1000 genomes (see MAGMA documentation)',
        'geneloc': 'gene locations file (see MAGMA documentation)',
        'setfile': 'gene set file (see MAGMA documentation)',
        'folder': 'folder where output files are placed'}

for arg, hlp in args.items():
    parser.add_argument('--' + arg, action='store', dest=arg, help=hlp)

s = parser.parse_args(argv[1:])

pickle.dump(s, open('.config.pl', 'wb'))

call([s.gwf])

