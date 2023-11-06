import periodictable as pt
import json

data = {}
for e in list(pt.elements)[1:]:
    data[e.symbol] = {'name': e.name, 'ions': e.ions, 'mass': e.mass, 'number': e.number,
                              'charge': e.charge, 'isotopes': e.isotopes}

with open('elements_list.json', 'w', encoding='utf-8') as w_file:
    w_file.write(json.dumps(data, indent=4))
