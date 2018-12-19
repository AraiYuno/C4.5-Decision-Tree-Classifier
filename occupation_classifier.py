import csv

_OCCUPATION_DATA_FILEPATH = './data/occupation_incomes.csv'
_OUTPUT_FILEPATH = './data/occupation_incomes_classed.csv'
_HOURLY_25PCT_INDEX = 9
_HOURLY_MEDIAN_INDEX = 10
_HOURLY_75PCT_INDEX = 11
_ANNUAL_25PCT_INDEX = 14
_ANNUAL_MEDIAN_INDEX = 15
_ANNUAL_75PCT_INDEX = 16
_HOURLY_ONLY_INDEX = 20

class Occupation_Classifier:

    def __init__( self, input_path, output_path ):
        self.classes = ["High Income", "Middle Income", "Low Income"]
        self.input_path = input_path
        self.output_path = output_path
        self.low_cutoff_annual = 0
        self.high_cutoff_annual = 0
        self.low_cutoff_hourly = 0
        self.high_cutoff_hourly = 0

    # returns the value of an entry at the given index as a float
    def get_float( self, entry, index ):
        return float(entry[index].replace(',', ''))

    # Choose the class cut-offs based off of the given entry
    def choose_cutoffs( self, entry ):
        self.low_cutoff_annual = self.get_float(entry, _ANNUAL_25PCT_INDEX)
        self.high_cutoff_annual = self.get_float(entry, _ANNUAL_75PCT_INDEX)
        self.low_cutoff_hourly = self.get_float(entry, _HOURLY_25PCT_INDEX)
        self.high_cutoff_hourly = self.get_float(entry, _HOURLY_75PCT_INDEX)

    def classify_incomes( self ):
        with open(self.input_path, 'r') as input:
            with open(self.output_path, 'w') as output:
                reader = csv.reader(input)
                writer = csv.writer(output, lineterminator='\n')
                processed_data = []

                # add new 'class' column header
                header_entry = next(reader)
                header_entry.append('class')
                processed_data.append(header_entry)

                # assume the first entry contains data for all occupations (true for this file)
                total_entry = next(reader)
                total_entry.append('*')
                self.choose_cutoffs(total_entry)
                processed_data.append(total_entry)

                # classify all occupations based on wages
                for entry in reader:
                    # use hourly wages if annual wages aren't available
                    if (entry[_HOURLY_ONLY_INDEX].lower() == 'true'):
                        median_wage = self.get_float(entry, _HOURLY_MEDIAN_INDEX)
                        low_cutoff = self.low_cutoff_hourly
                        high_cutoff = self.high_cutoff_hourly
                    else:
                        median_wage = self.get_float(entry, _ANNUAL_MEDIAN_INDEX)
                        low_cutoff = self.low_cutoff_annual
                        high_cutoff = self.high_cutoff_annual

                    if median_wage < low_cutoff:
                        entry.append(self.classes[2]) # Low Income
                    elif median_wage > high_cutoff:
                        entry.append(self.classes[0]) # High Income
                    else:
                        entry.append(self.classes[1]) # Middle Income

                    processed_data.append(entry)

                writer.writerows(processed_data)

classifier = Occupation_Classifier(_OCCUPATION_DATA_FILEPATH, _OUTPUT_FILEPATH)
classifier.classify_incomes()
