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

import os.path
from utils import convert_str, render_string

OPTIONS = [   
             'front_fields',
             'front_mask',
             'back_fields',
             'back_mask',
             'header_fields',
             'header_mask',
             'footer_fields',
             'footer_mask',
             'filename_field'
           ]

class LaTeXCard:
    # LaTeX card template.
    def __init__(self, mapping, csv_line):
        """Initialize LaTeX flash card."""
        self.csv_line = csv_line
        self.file_name = self.csv_line[mapping['filename_field']]
        self.card_props = {
                "card_footer" : render_string(mapping['footer_mask'], mapping['footer_fields'], csv_line),
                "card_header" : render_string(mapping['header_mask'], mapping['header_fields'], csv_line),
                "card_front"  : render_string(mapping['front_mask'], mapping['front_fields'], csv_line),
                "card_back"   : render_string(mapping['back_mask'], mapping['back_fields'], csv_line)
        }

        self.CARD_TEMPLATE = u"""\\cardfrontfoot{%s}\\begin{flashcard}[%s]{%s}\Large{%s}\\end{flashcard}"""


    def _render(self):
        """Renders the card."""
        for prop in self.card_props:
            self.card_props[prop] = convert_str(
                self.card_props[prop],
                r'{\bf ',
                r'}',
                r'\emph{',
                r'}',
                r'\underline{',
                r'}'
            )

        return (self.CARD_TEMPLATE % (
                self.card_props["card_footer"],
                self.card_props["card_header"],
                self.card_props["card_front"],
                self.card_props["card_back"]
               )).encode('utf-8')

    def dump_cards(self, output_dir, resource_dir, cards):
        """Dumps a collection of cards into a file."""
        file_dic = {}
        for card in cards:
            if file_dic.has_key(card.file_name):
                file_dic[card.file_name] += [card]
            else:
                file_dic[card.file_name] = [card]

        # Read the template.
        template = "".join(open(os.path.join(resource_dir, "latex_template.tex"), "rb").readlines())

        # Generate file with commands to create PDFs.
        tex_to_pdf = open(os.path.join(output_dir, 'generate_pdfs.sh'), 'w')
        tex_to_pdf.write("#!/usr/bin/sh\n")

        for fl in file_dic:
            with open(os.path.join(output_dir, fl + '.tex'), 'wb') as texfile:
                rendered_cards = ""

                for card in file_dic[fl]:
                    rendered_cards += card._render() + "\n"

                texfile.write(template.replace("%__CARDS__%", rendered_cards))

                tex_file = os.path.join(output_dir, fl + '.tex')

                cmd = "latex -interaction=nonstopmode --output-format=pdf --output-directory=\"" + output_dir + "\" \"" + tex_file + "\""
                tex_to_pdf.write(cmd + "\n")

        tex_to_pdf.write("rm *.aux\n")
        tex_to_pdf.write("rm *.log\n")

        tex_to_pdf.close()
