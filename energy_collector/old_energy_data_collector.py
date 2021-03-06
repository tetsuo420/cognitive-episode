import datetime
import json
import mmap
import os
import pprint as pp
import re

from prettytable import PrettyTable
from zenlog import log


FOLDER_NAMES = ['1-DFTmin_opt', '2-MP2min_sp', '3-M062Xmin_opt', '4-M062Xmax_sp']
DFT_RE = re.compile(r'SCF Done:.*=\s+([^\n]+\d+\.\d+)')
M06_RE = re.compile(r'RM062X.*=\s+([^\n]+\d+\.\d+)')
USER = 'Pol Sanz Berman'

class energy_data_collector():

    def __init__(self):
        energies = self.get_energies_from_files()
        self.print_energies_on_file(energies)

    def get_energies_from_files(self):
        log.d('Getting energies from files.')
        energies_dict = {}

        for folder_name in FOLDER_NAMES:
            temp_file_list = [file for file in os.listdir(folder_name) if file.endswith('.log')]

            for molecule_name in temp_file_list:

                text = None
                temp_dict = {}

                with open(folder_name+'/'+molecule_name, 'r') as f:
                    text = f.read()

                if folder_name in ['1-DFTmin_opt', '2-MP2min_sp']:
                    energy_value = round(float(DFT_RE.findall(text)[-1]), 5)
                    temp_dict[folder_name] = energy_value
                elif folder_name in ['3-M062Xmin_opt', '4-M062Xmax_sp']:
                    energy_value = round(float(M06_RE.findall(text)[-1]), 5)
                    temp_dict[folder_name] = energy_value

                if molecule_name[:-4] not in energies_dict:
                    energies_dict[molecule_name[:-4]] = [temp_dict]
                else:
                    energies_dict[molecule_name[:-4]].append(temp_dict)

        log.i(f'Energies from {len(energies_dict.keys())} files recovered.')

        # pp.pprint(energies_dict)
        return energies_dict

    def print_energies_on_file(self, energy_dict):
        time = datetime.datetime.now()
        file_name = (f'PSanz - {time.strftime("%d-%m-%y")}.txt')
        x = PrettyTable()
        x.field_names = ['Molecule Name','DFTmin_opt', 'MP2min_sp', 'M062Xmin_opt', 'M062Xmax_sp']
        temp_table = list(energy_dict.values())      
        temp_table2 = list(energy_dict.keys())
        for j in temp_table:         
            for i in temp_table2:
                x.add_row([i , next(iter(j[0].values())), next(iter(j[1].values())), next(iter(j[2].values())), next(iter(j[3].values()))])
                temp_table2.remove(i)
                break
        table_title = (f'{USER} - {time.strftime("%d-%m-%y")} - Gaussian Energy Calculation Results')   
        print(x.get_string(title=table_title))
        with open(file_name, 'w+') as f:
            f.write(str(x.get_string(title=table_title)))
        log.info(f'Data correctly saved as \'{file_name}\' in \'{os.getcwd()}\'')
        return str(x)
 

at = energy_data_collector()
