# -*- coding: UTF-8 -*-
"""
>>> a = Preprocessor()
>>> print(a.read_file('../input/itcont.txt'))
Total read 5 lines.
"""
import sys

class Preprocessor:
    """
    Process input medical record.

    Input file format should be:
    id,prescriber_last_name,prescriber_first_name,drug_name,drug_cost
    1000000001,Smith,James,AMBIEN,100
    1000000002,Garcia,Maria,AMBIEN,200
    1000000003,Johnson,James,CHLORPROMAZINE,1000
    1000000004,Rodriguez,Maria,CHLORPROMAZINE,2000
    1000000005,Smith,David,BENZTROPINE MESYLATE,1500

    Output file format should be:
    drug_name,num_prescriber,total_cost
    CHLORPROMAZINE,2,3000
    BENZTROPINE MESYLATE,1,1500
    AMBIEN,2,300
    """
    def __init__(self):
        self.__drug_dict = {}
        self.__prescriber_dict = {}
        self.__counter = 0

    def read_file(self, input_file_name: str):
        """
        Function to read medical record.
        :param input_file_name: The path of input file
        :return: Number of processed line.
        """
        print(input_file_name)
        with open(input_file_name, 'rb') as input_file:
            line = input_file.readline() # skip first row
            line = input_file.readline()

            while line:
                self.__counter += 1

                record = self.__data_cleanser(line)

                prescriber_name = ' '.join(record[1:3])

                try:
                    self.__prescriber_dict[record[3]].add(prescriber_name)
                    self.__drug_dict[record[3]] += record[-1]
                except KeyError:
                    self.__prescriber_dict[record[3]] = {prescriber_name}
                    self.__drug_dict[record[3]] = record[-1]

                line = input_file.readline()

        print('Total read ' + str(self.__counter) + ' lines.')
        return self.__counter

    def __data_cleanser(self, record: bytes):
        """
        Function to preprocess the origin medical record.
        :param record:
        :return:
        """
        record = record.decode('utf8')
        if record.find('"') >= 0:

            start = record.find('"')
            # Strip all commas inside all the quotations
            while start >= 0:
                end = record[start+1:].find('"')
                if end >= 0:
                    end = end+start+1
                    record = record[:start]+record[start:end+1].replace(',', '')+record[end+1:]
                start = record[end+1:].find('"')

        record = record.split(',')

        if len(record) != 5:
            print('A row must have 5 columns but found this row')
            print(','.join(record))
            sys.exit(0)

        record[0] = int(record[0])
        record[4] = int(record[-1].replace('\n', ''))

        return record

    def write_file(self, output_file_name):
        """
        Function to write result
        :param output_file_name: the path of output file
        :return: None
        """
        # Write the output file
        with open(output_file_name, 'wb') as file:
            # Write header of the file
            file.write(b'drug_name,num_prescriber,total_cost\n')

            # Sort the keys by the values of drug_cost and if there is a tie, drug name.
            for drug, value in sorted(self.__drug_dict.items(), key=lambda x: (x[1], x[0]), reverse=True):
                # Write to the output file in descending order
                line = list()
                line.append(drug)
                line.append(str(len(self.__prescriber_dict[drug])))
                line.append(str(self.__drug_dict[drug]))

                next_line = ','.join(line)
                next_line += '\n'
                file.write(bytes(next_line, 'utf8'))

        # # Open and print top 10 lines of the output file
        # print('\nTop 5 lines of the output file\n')
        # with open(output_file_name, 'rb') as file:
        #
        #     line = file.readline()
        #     n_lines = 0
        #     while len(line) > 0 and n_lines < 6:
        #         n_lines += 1
        #         print(line)
        #         line = file.readline()


if __name__ == "__main__":
    input_fname, output_fname = sys.argv[1:]

    test = Preprocessor()
    test.read_file(input_fname)
    test.write_file(output_fname)





