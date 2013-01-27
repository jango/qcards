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

import csv
import os.path
from utils import convert_str, render_string

OPTIONS = [   
            'front_fields',
            'back_fields',
            'front_mask',
            'back_mask',
            'filename_field'
          ]

class CSVCard:
    def __init__(self, mapping, csv_line):
        """Initialize CSV flash card."""
        self.csv_line = csv_line
        self.file_name = self.csv_line[mapping['filename_field']]

        self.card_props = {
            'card_front' : render_string(mapping['front_mask'], mapping['front_fields'], csv_line),
            'card_back' : render_string(mapping['back_mask'], mapping['back_fields'], csv_line)
        }

    def _render(self):
        """Renders the card."""
        for prop in self.card_props:
            self.card_props[prop] = convert_str(
                self.card_props[prop],
                r'<b>',
                r'</b>',
                r'<i>',
                r'</i>',
                r'<u>',
                r'</u>'
            )

        return [self.card_props["card_front"], self.card_props["card_back"]]

    def dump_cards(self, output_dir, resource_dir, cards):
        """Dumps a collection of cards into a file."""
        file_dic = {}
        for card in cards:
            if file_dic.has_key(card.file_name):
                file_dic[card.file_name] += [card]
            else:
                file_dic[card.file_name] = [card]

        for fl in file_dic:
            with open(os.path.join(output_dir, fl + '.csv'), 'wb') as csvfile:
                writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)   
            
                for card in file_dic[fl]:
                   writer.writerow([v.encode('utf8') for v in card._render()])
