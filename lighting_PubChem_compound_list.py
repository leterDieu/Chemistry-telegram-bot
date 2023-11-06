import json


with open('backup_fixed_PubChem_compound_list.json', 'r', encoding='utf-8') as r_file:
    compounds_data = json.loads(r_file.read())


light_compounds_list = []
for summary in compounds_data:
    if summary['mf'] not in light_compounds_list:
        light_compounds_list.append(summary['mf'])


with open('light_PubChem_compounds_list.json', 'w', encoding='utf-8') as w_file:
    w_file.write(json.dumps(light_compounds_list))
