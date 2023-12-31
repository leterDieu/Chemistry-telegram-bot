# Chemistry-telegram-bot
Telegram bot which tailored to solve some chemical problems: reaction equalization, binary formula calculations, etc. as well as to have some helpful tools while working with elements, compounds and reactions.

## Set up files
### Downloading and fixing data from PubChem
Since using PubChem API (with help of pubchempy) is pretty slow, we can download all the data, read it and use it instantly. 
To do so use [this page](https://pubchem.ncbi.nlm.nih.gov/#input_type=list&query=ezzeRYRh4d3W9-PuYZaqxdgrRUszrmEhGwR6bQAVaGwADFQ&collection=compound&alias=PubChem%3A%20PubChem%20Compound%20TOC%3A%20Record%20Description). I preferred working with json, but you also can choose csv or xml. If you want to learn more about browsing data from PubChem visit [this page](https://pubchem.ncbi.nlm.nih.gov/classification/).

My json downloaded with some missing commas between summaries, so I made a program that fixes it (fixing_data.py).

### Creating light compounds list
If we use raw PubChem compounds data it's going to take a lot of time searching for formulas. Since we need to know only an existence of the formula (for now) we can create a list of unique formulas from raw PubChem data. It's easier to use and takes less time 
### Creating simple json with elements' properties
creating_element_list.py creates json file which contains name, ions, mass, number in a periodic table, charge, isotopes of each element in periodic table which you can access by element symbol.
