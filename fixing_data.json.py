def backing_up(fom: str, to: str):
    with open(fom, 'r', encoding='utf-8') as r_file:
        text = r_file.read()
    with open(to, 'w', encoding='utf-8') as w_file:
        w_file.write(text)


def fixing_missing_commas():
    with open('backup_PubChem_compound_list.json', 'r', encoding='utf-8') as r_file:
        text = r_file.read()

    text = '},\n'.join(text.split('}\n'))

    with open('fixed_PubChem_compound_list.json', 'w', encoding='utf-8') as w_file:
        w_file.write(text)


backing_up('fixed_PubChem_compound_list.json', 'backup_fixed_PubChem_compound_list.json')
