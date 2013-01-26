import os.path
from utils import convert_str

class LaTeXCard:
    # LaTeX card template.
    def __init__(self, file_name, card_header, card_footer, card_front, card_back):
        """Initialize LaTeX flash card."""
        self.file_name = file_name
        self.card_props = {
            'card_header': card_header,
            'card_footer': card_footer,
            'card_front': card_front,
            'card_back': card_back
        }

        self.CARD_TEMPLATE = u"""\\cardfrontfoot{%s}\\begin{flashcard}[%s]{%s}\Large{%s}\\end{flashcard}"""


    def _render(self):
        """Renders the card."""
        for prop in self.card_props:
            self.card_props[prop] = convert_str(
                self.card_props[prop],
                r'\emph{',
                r'}',
                r'{\bf ',
                r'\1}',
                r'\underline{',
                r'}'
            )

        return self.CARD_TEMPLATE % (
                self.card_props["card_footer"],
                self.card_props["card_header"],
                self.card_props["card_front"],
                self.card_props["card_back"]
               )

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

        print "Use `generate_pdfs.sh` in the LaTeX directory to generate PDFs."
        
        # Generate file with commands to create PDFs.
        tex_to_pdf = open(os.path.join(output_dir, 'generate_pdfs.sh'), 'w')
        tex_to_pdf.write("#!/usr/bin/sh\n")

        print tex_to_pdf
        for fl in file_dic:
            with open(os.path.join(output_dir, fl + '.tex'), 'wb') as texfile:
                rendered_cards = ""

                for card in file_dic[fl]:
                    rendered_cards += card._render() + "\n"

                texfile.write(template.replace("%__CARDS__%", rendered_cards))

                out_dir = os.path.join(output_dir, fl + '.tex')
                pdf_dir = os.path.join(output_dir, fl + '.pdf')
                cmd = "latex -interaction=nonstopmode --output-format=pdf --output-directory=\"" + pdf_dir + "\" \"" + output_dir + "\""
                tex_to_pdf.write(cmd + "\n")

        tex_to_pdf.close()


if __name__ == "__main__":
    # Test card rendering.
    res_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "resources")

    card_a = LaTeXCard("file_a", r'header', r'footer', r'front', r'back')
    card_b = LaTeXCard("file_b", r'header', r'footer', r'front', r'back')
    card_a.dump_cards(r'/tmp', res_dir, [card_a, card_b])

