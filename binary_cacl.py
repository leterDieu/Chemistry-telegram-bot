import periodictable as pt
from typing import Tuple
import json
from typing import List
import math
import copy
from operator import itemgetter


with open('light_PubChem_compounds_list.json', 'r', encoding='utf-8') as r_file:
    compounds_list = json.loads(r_file.read())

with open('elements_list.json', 'r', encoding='utf-8') as r_file:
    elements_data = json.loads(r_file.read())


def get_element(element_symbol: str) -> Tuple[bool, str]:
    try:
        response = ''
        for key, value in elements_data[element_symbol].items():
            response += (True, f'{key}: {value}\n')
    except KeyError:
        response = (False, 'Incorrect element symbol')

    return response


def does_compound_exist(formula: str) -> Tuple[bool, str]:
    hill_formula = str(pt.formula(formula).hill)
    if hill_formula in compounds_list:
        return True, hill_formula
    return False, "Formula doesn't exist in the database."


def generate_mw_table(element_symbol: str, mass_percentage: float, limit1=60, limit2=60) -> List[dict]:
    element = elements_data[element_symbol]
    element_mass = element['mass']
    seek_mass = (element_mass / mass_percentage * 100 - element_mass)

    possible_masses_table = []
    for i in range(1, limit2 + 1):
        for j in range(1, limit1 + 1):
            if math.gcd(i, j) != 1 or i > limit1 or j > limit2:
                continue
            possible_masses_table.append(
                {'seeked_elem_index': j, 'given_elem_index': i, 'seeked_elem_mass': seek_mass * i / j,
                 'given_elem': element_symbol})

    return possible_masses_table


def get_best_matching_binary_compound(element_symbols: str, mass_percentage: float, limit1=60, limit2=60) -> List[dict]:
    if mass_percentage < 1:
        mass_percentage = 1
    elif mass_percentage > 99:
        mass_percentage = 99

    options = generate_mw_table(element_symbols, mass_percentage, limit1, limit2)
    table_with_differences = []
    for option in options:
        for elem, props in elements_data.items():
            temp = copy.deepcopy(option)
            if elem == temp['given_elem']:
                continue
            temp['difference'] = abs(props['mass'] - option['seeked_elem_mass'])
            temp['seeked_elem'] = elem
            table_with_differences.append(temp)

    table_with_checked_formulas = []
    for stats in sorted(table_with_differences, key=itemgetter('difference')):
        raw_formula = (stats['seeked_elem'] + str(stats['seeked_elem_index']) +
                       stats['given_elem'] + str(stats['given_elem_index']))

        mass_odds = round(stats['difference'], 6)

        if mass_odds > 2:
            break

        check_response = does_compound_exist(raw_formula)
        if check_response[0]:
            table_with_checked_formulas.append({'mol': str(check_response[1]), 'odds': check_response[1],
                                                'raw': f'{str(check_response[1])}, {mass_odds}g/mol mass odds.'})

    return table_with_checked_formulas


def wrap_table(element_symbols: str, m_perc: float, limit1=60, limit2=60) -> str:
    raw_table = get_best_matching_binary_compound(element_symbols, m_perc, limit1, limit2)
    if not len(raw_table):
        return "Couldn't find anything"
    return '\n'.join([option['raw'] for option in raw_table])
