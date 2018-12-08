# Remove duplicates from a particular csv file

import pandas

source = pandas.read_csv('./national_M2017_dl_classed.csv')

source.drop_duplicates('occ_title', inplace=True)

source.to_csv('./no_dupes.csv')
