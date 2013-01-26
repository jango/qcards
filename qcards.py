#!/usr/bin/python
"""
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import os
import re
import csv
import codecs
import logging
import argparse
import ConfigParser
from cards import CSVCard
from cards import LaTeXCard
from cards.utils import get_abs_path, parse_mappings

# Setup logging.
FORMAT = '%(asctime)-15s %(levelname)s %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger('qcards')
logger.setLevel(logging.INFO)

def run(args):
    loc = os.path.join(os.path.dirname(os.path.abspath(__file__)))
    res = os.path.join(os.path.dirname(os.path.abspath(__file__)), "resources")

    config = ConfigParser.ConfigParser()
    
    # Figure out absolute path to the configuration file.
    cfg_path = get_abs_path(args.config, loc)
           
    try:
        config.readfp(open(cfg_path))
    except Exception as e:
        logger.error("Can't read config file at %s" % cfg_path)
        logger.error(e)
        return

    # General parameters check.
    if not config.has_section('general'):
        logger.error("Config must have a 'general' section.")
        return
    else:
        if not config.has_option('general', 'output_dir'):
            logger.error("Section 'general' of the config file must have 'output_dir' parameter.")
            return
        else:
            # Figure out absolute path to the output_dir.
            output_dir = get_abs_path(config.get('general', 'output_dir'), os.path.dirname(cfg_path))

            if not os.path.exists(output_dir):
                logger.error("Output directory '%s' does not exist." % output_dir)
                return 

        if not config.has_option('general', 'input_file'):
            logger.error("Section 'general' of the config file must have 'input_file' parameter.")
            return
        else:
            # Figure out absolute path to the input_file.
            input_file = get_abs_path(config.get('general', 'input_file'), os.path.dirname(cfg_path))

            if not os.path.exists(input_file):
                logger.error("Input file '%s' does not exist." % input_file)
                return 

    # Parse some settings for the input file.
    try:
        QUOTE_CHAR = config.get('general', 'csv_quotechar').strip('"')
    except:
        QUOTE_CHAR = '"'

    try:
        DELIMITER =  config.get('general', 'csv_delimiter').strip('"')
    except:
        DELIMITER = ','

    try:
        HAS_HEADER = config.getboolean('general', 'csv_hasheader')
    except:
        HAS_HEADER = True

    logger.info("Configured with the following parameters:")
    logger.info("Output directory:\n%s" % output_dir)
    logger.info("Input file:\n%s" % input_file)


    # Configure each card type.
    card_types = {}
    card_options = {}

    if config.has_section('latex'):
        card_types[LaTeXCard] = dict(config.items('latex'))

    if config.has_section('csv'):
        card_types[CSVCard] = dict(config.items('csv'))

    if (len(card_types) == 0):
        logger.error("Either 'latex' or 'csv' section must be present in the configuration file.")
        return
        
    logger.info("Rendering cards...")

    try:
        # Parse mappings.
        for card in card_types:
            card_options[card.__name__] = parse_mappings(card_types[card], card)

        # Read CSV.

        card_array = {}
        with open(input_file, 'rb') as csvfile:
            reader = csv.reader(csvfile, delimiter=DELIMITER, quotechar=QUOTE_CHAR)

            # If CSV has a header, skip one line.
            if HAS_HEADER:
                reader.next()

            for row in reader:
                for card_type in card_types:

                    # Instantiate class dynamically.
                    class_ = getattr(card_type, card_type.__name__.split(".")[-1])
                    card = class_(card_options[card_type.__name__], row)

                    if card_array.has_key(card_type):
                        card_array[card_type] += [card]
                    else:
                        card_array[card_type] = [card]
        
        # Dump cards.
        for key in card_array:
            card_array[key][0].dump_cards(output_dir, res, card_array[key])

        logger.info("Done!")
        logger.info("Execute `generate_pdfs.sh` in the LaTeX directory to generate PDFs.")

    except Exception as e:
        logger.error("Failed to render the files:")
        logger.error(str(e))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate TeX and CSV flah cards from csv.')
    parser.add_argument('-c', '--config', type=str, required=True, help='path to the configuration file')
    args = parser.parse_args()
    run(args)
