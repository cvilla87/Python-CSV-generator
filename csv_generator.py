import configparser
import string
import random
import re
import codecs
from faker import Faker


def change_locale():
    _curr_loc = random.choice(locales)
    _curr_cty = _curr_loc[3:]
    return Faker(_curr_loc), _curr_cty


# Load and parse config file
config = configparser.ConfigParser()
config.read('config.ini')

main_cfg = config['MAIN']
sep = main_cfg['sep']
num_lines = main_cfg.getint('lines')
set_header = main_cfg.getboolean('header')
switch_locale = main_cfg.getboolean('switch_locale')
days = main_cfg.getint('days_back')
locales = [re.sub(r'\s', '', loc) for loc in list(main_cfg['locales'].split(','))]
custom_datatypes = [re.sub(r'\s', '', loc) for loc in list(main_cfg['custom_datatypes'].split(','))]

if config.has_section(main_cfg['dataset']):
    type_dataset = main_cfg['dataset']
else:
    type_dataset = 'dummy'

header = sep.join([f[0] for f in config.items(type_dataset)])
columns = sep.join([f[1] for f in config.items(type_dataset)])


# Columns validation
template = []
if type_dataset == "dummy":
    for col in columns.split(sep):
        template.append(col)
else:
    fake = Faker()
    for col in columns.split(sep):
        try:
            _ = getattr(fake, col)()
            template.append(col)
        except AttributeError:
            if col in custom_datatypes:
                template.append(col)
            else:
                template.append("text")  # Faker "text" provider generator


# Generation of the full dataset into memory
cont = 0
dataset = []
if set_header:
    dataset.append(header)

if type_dataset == "dummy":
    # Faker it's not used
    while cont < num_lines:
        line = ""
        for col in template:
            # In this case, "col" is the number of characters to fill.
            line += "".join(random.sample(string.ascii_letters, int(col))) + sep
        dataset.append(line.rstrip("|"))
        cont += 1
else:
    fake, curr_cty = change_locale()

    while cont < num_lines:
        line = ""

        # If switch_locale is True and it has been generated 100 more rows, it will switch to a new locale.
        if switch_locale and cont % 100 == 0:
            fake, curr_cty = change_locale()

        # Each block of 100 rows will contain approximately 5 different people.
        fake.seed_instance(random.randint(0, 4))

        for col in template:
            if col not in custom_datatypes:
                # It can be called directly via Faker API with no arguments needed.
                line += str(getattr(fake, col)()).replace("\n", " ") + sep
            else:
                # Special cases where Faker call requires some argument.
                if col == "amount":
                    line += str(round(random.uniform(0, 3000), 2)) + sep
                elif col == "ts":
                    # The smaller range for the seed, the more probability of repeated values
                    fake.seed_instance(random.randint(0, 5000))
                    line += str(fake.date_time_between(start_date=f"-{days}d", end_date="now", tzinfo=None)) + sep
                elif col == "gps_loc":
                    fake.seed_instance(random.randint(0, 2000))  # It will imply a pretty big variation of the location
                    line += str(fake.local_latlng(country_code=curr_cty, coords_only=True)) + sep
                elif col == "text":
                    line += fake.text(30) + sep
                else:
                    exit(f"ERROR: Column type not expected: {col}")
        dataset.append(line.rstrip("|"))
        cont += 1


# Write to file in one single action
with codecs.open("data.csv", "w", encoding="utf-8") as f:
    f.writelines("\n".join(dataset))
