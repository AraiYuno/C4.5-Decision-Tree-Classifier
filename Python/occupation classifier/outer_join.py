# Join two csv files on a particular column.

import pandas

main_source = pandas.read_csv('./data/occupation_types.csv')
income_source = pandas.read_csv('./data/occupation_incomes_classed.csv')

result = pandas.merge(main_source, income_source, 'outer', 'occ_title',
                      None, None, False, False, False)

result.to_csv('./result.csv')