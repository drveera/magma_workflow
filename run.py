from subprocess import call
import argparse
from sys import argv
import pickle

parser = argparse.ArgumentParser()
args = ['gwf', 'studyfolder', 'snploc', 'geneloc', 'setfile', 'folder']
for arg in args:
    parser.add_argument('--' + arg, action='store', dest=arg)

s = parser.parse_args(argv[1:])

pickle.dump(s, open('.config.pl', 'wb'))

call([s.gwf])

