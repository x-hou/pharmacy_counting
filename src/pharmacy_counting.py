# -*- coding: UTF-8 -*-
"""
>>> test = Preprocessor()
>>> test.read_file('../insight_testsuite/tests/test_1/input/itcont.txt')
Total read in 5 records.
"""
import sys
import re

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
        :return: None
        """
        with open(input_file_name, 'rb') as input_file:
            line = input_file.readline() # skip first row
            line = input_file.readline()

            while line:
                self.__counter += 1

                record = Preprocessor.data_cleanser(line)
                prescriber_name = record[1] + ' ' + record[2]

                if record[3] not in self.__prescriber_dict:
                    self.__prescriber_dict[record[3]] = {prescriber_name}
                    self.__drug_dict[record[3]] = record[-1]
                else:
                    self.__prescriber_dict[record[3]].add(prescriber_name)
                    self.__drug_dict[record[3]] += record[-1]

                # try:
                #     self.__prescriber_dict[record[3]].add(prescriber_name)
                #     self.__drug_dict[record[3]] += record[-1]
                # except KeyError:
                #     self.__prescriber_dict[record[3]] = {prescriber_name}
                #     self.__drug_dict[record[3]] = record[-1]

                line = input_file.readline()

        print('Total read in ' + str(self.__counter) + ' records.')

    @staticmethod
    def data_cleanser(record: bytes):
        """
        Function to preprocess the origin medical record. Comma inside the record is annoying.
        For example:

        457467862,"ADAIR,",ROBERT,AVODART,4729.76

        Reference: https://stackoverflow.com/questions/38336518/remove-all-commas-between-quotes
        :param record: Record in bytes format
        :return: Cleaned record in a list
        >>> Preprocessor.data_cleanser(b'457467862,"ADAIR,",ROBERT,AVODART,4729.76')
        [457467862, '"ADAIR"', 'ROBERT', 'AVODART', 4729.76]
        >>> Preprocessor.data_cleanser(b'457467862,"ADAIR,",ROBERT,AVODART,4729.76t')
        Type error for record:
        [457467862, '"ADAIR"', 'ROBERT', 'AVODART', '4729.76t']

        """
        record = record.decode('utf8')

        if record.find('"') >= 0:
            # remove commas inside " "
            record = re.sub(r'(?!(([^"]*"){2})*[^"]*$),', '', record)

        record = record.split(',')

        try:
            record[0] = int(record[0])
            record[4] = float(record[-1].replace('\n', '')) # get rid of '\n' in the end
        except:
            print("Type error for record:")

        return record

    def write_file(self, output_file_name):
        """
        Function to write result
        :param output_file_name: the path of output file
        :return: None
        """
        # write the output file
        with open(output_file_name, 'wb') as file:
            # write header of the file
            file.write(b'drug_name,num_prescriber,total_cost\n')

            # sort in descending order based on the total drug cost and if there is a tie, drug name in ascending order
            for drug, value in sorted(self.__drug_dict.items(), key=lambda x: (x[1], x[0]), reverse=True):
                line = list()
                line.append(drug)
                line.append(str(len(self.__prescriber_dict[drug])))
                line.append(str(int(self.__drug_dict[drug])))

                line = ','.join(line)
                line += '\n'
                file.write(bytes(line, 'utf8'))



if __name__ == "__main__":
    input_file, output_file = sys.argv[1:]

    test = Preprocessor()
    test.read_file(input_file)
    test.write_file(output_file)





