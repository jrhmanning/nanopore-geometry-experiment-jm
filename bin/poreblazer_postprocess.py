#!/usr/bin/env python

# © Copyright IBM Corp. 2020 All Rights Reserved
# SPDX-License-Identifier: Apache2.0

import argparse
import json
import os
from pathlib import Path
import tarfile


# Required parameters
parser = argparse.ArgumentParser(description='Amalgamating geometric descriptors.')
parser.add_argument('directory',
                    type=str,
                    action='store',
                    metavar='DIRECTORY',
                    help='Directory for storing input/output files.')
parser.add_argument('-f','--FrameworkName',
                    type=str,
                    action='store',
                    required=True,
                    metavar='FRAMEWORK_NAME',
                    help='Name of the framework used (and associated .cif file).')
args = parser.parse_args()

# Build the geometric dictionary
geometric_dict = {'geometricProperties': []}

inputdir = Path(args.directory)
filename = f'{args.FrameworkName}_summary.dat'

with tarfile.open('summary.tgz', 'r:gz') as tar:
    tar.extract(f'{inputdir}/{filename}')

data = []
with open(inputdir / filename, 'r') as f:
    for line in f:
        data.append(line.strip().split())


output = [
    {'name': 'Volume', 'value': float(data[1][1]), 'unit': 'Angstrom^3'},
    {'name': 'Mass', 'value': float(data[2][2]), 'unit': 'g/mol'},
    {'name': 'Density', 'value': float(data[3][1]), 'unit': 'g/cm^3'},
    {'name': 'PLD', 'value': float(data[4][1]), 'unit': 'Angstrom'},
    {'name': 'LCD', 'value': float(data[5][1]), 'unit': 'Angstrom'},
    {'name': 'Dimensionality', 'value': float(data[6][1]), 'unit': '-'},

    {'name': 'T_S_AC', 'value': float(data[8][1]), 'unit': 'Angstrom^2'},
    {'name': 'T_S_AC_cm3', 'value': float(data[9][1]), 'unit': 'm^2/cm^3'},
    {'name': 'T_S_AC_g', 'value': float(data[10][1]), 'unit': 'm^2/g'},
    {'name': 'T_V_He', 'value': float(data[12][1]), 'unit': 'Angstrom^3'},
    {'name': 'T_V_He_g', 'value': float(data[13][1]), 'unit': 'cm^3/g'},
    {'name': 'T_V_G_A3', 'value': float(data[14][1]), 'unit': 'Angstrom^3'},
    {'name': 'T_V_G', 'value': float(data[15][2]), 'unit': 'cm^3/g'},
    {'name': 'T_V_PO_A3', 'value': float(data[16][2]), 'unit': 'Angstrom^3'},
    {'name': 'T_V_PO', 'value': float(data[17][2]), 'unit': 'cm^3/g'},
    {'name': 'T_FV_PO', 'value': float(data[18][1]), 'unit': '-'},

    {'name': 'NA_S_AC', 'value': float(data[20][1]), 'unit': 'Angstrom^2'},
    {'name': 'NA_S_AC_cm3', 'value': float(data[21][1]), 'unit': 'm^2/cm^3'},
    {'name': 'NA_S_AC_g', 'value': float(data[22][1]), 'unit': 'm^2/g'},
    {'name': 'NA_V_He', 'value': float(data[24][1]), 'unit': 'Angstrom^3'},
    {'name': 'NA_V_He_g', 'value': float(data[25][1]), 'unit': 'cm^3/g'},
    {'name': 'NA_V_G_A3', 'value': float(data[26][1]), 'unit': 'Angstrom^3'},
    {'name': 'NA_V_G', 'value': float(data[27][2]), 'unit': 'cm^3/g'},
    {'name': 'NA_V_PO_A3', 'value': float(data[28][2]), 'unit': 'Angstrom^3'},
    {'name': 'NA_V_PO', 'value': float(data[29][2]), 'unit': 'cm^3/g'},
    {'name': 'NA_FV_PO', 'value': float(data[30][1]), 'unit': '-'},

]

geometric_dict['geometricProperties'] += output

# Dump the geometric dictionary to a json file
# with open(os.path.join(arg.directory, 'geometricProperties.json'), mode='w') as f:
with open(inputdir / 'geometricProperties.json', mode='w') as f:
    json.dump(geometric_dict, f, indent=2)