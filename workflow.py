from gwf import *
import pandas as pd
import pickle
import os

s = pickle.load(open('.config.pl', 'rb'))

filefolder = s.folder + '/files/'
if not os.path.exists(filefolder):
    os.makedirs(filefolder)

studies = pd.read_csv(s.studyfolder + '/studies.csv', sep=';')

annotstub = filefolder + 'annot'
annot = annotstub + '.genes.annot'
bimloc = s.snploc + '.bim'

target('annotate', input=[bimloc, s.geneloc], output=annot) << '''
        magma --annotate --snp-loc {} --gene-loc {} --out {}'''.format(bimloc, s.geneloc, annotstub)

for i, study in studies.iterrows():
    genestub = filefolder + study.shortname
    gene_results = genestub + '.genes.raw'
    pval = s.studyfolder + '/' + study.shortname + '.txt'
    outstub = filefolder + study.shortname
    outfile = outstub + '.sets.out'

    target('gene_analysis.{}'.format(study.shortname), input=[bimloc, annot], output=gene_results, memory='20g') << '''
        magma --bfile {} --pval {} N={} --gene-annot {} --out {}'''.format(s.snploc, pval, study.N, annot, genestub)

    target('gene_set.{}'.format(study.shortname), input=[gene_results, s.setfile], output=outfile, memory='20g') << '''
        magma --gene-results {} --set-annot {} --out {}'''.format(gene_results, s.setfile, outstub)

resultfile = s.folder + '/results.csv'

target('collect', input=[filefolder + name + '.sets.out' for name in studies.shortname], output=resultfile) << '''
    python collect.py {} {} {}'''.format(s.studyfolder, filefolder, resultfile)

print '''python collect.py {} {} {}'''.format(s.studyfolder, filefolder, resultfile)
