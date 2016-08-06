import pandas as pd
from sys import argv

studyfolder, filefolder, resultfile = argv[1:]

studies = pd.read_csv(studyfolder + '/studies.csv', sep=';', usecols=['shortname', 'longname', 'N', 'sig'])

results = []
for shortname in studies.shortname:
    m = pd.read_csv(filefolder + shortname + '.sets.out', skiprows=3, sep='\s+', usecols=['SET', 'P'])
    m = m.rename(columns={'P': shortname})
    m = m.transpose()
    m.columns = m.iloc[0]
    m = m.reindex(m.index.drop('SET'))
    results.append(m)

results = pd.concat(results)

output = pd.merge(studies, results, how='inner', left_on='shortname', right_index=True)

output[output.columns] = output[output.columns].astype(str)
output.to_csv(resultfile, index=False, sep=';')

