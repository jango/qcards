import csv
import os.path
from utils import convert_str

class CSVCard:
    def __init__(self, file_name, card_front, card_back):
        """Initialize CSV flash card."""
        self.file_name = file_name
        self.card_props = {
            'card_front': card_front,
            'card_back': card_back
        }

    def _render(self):
        """Renders the card."""
        for prop in self.card_props:
            self.card_props[prop] = convert_str(
                self.card_props[prop],
                r'<span style="font-weight:600;">',
                r'</span>',
                r'<span style="text-decoration: italic;">',
                r'</span>',
                r'<span style="text-decoration: underline;">',
                r'</span>'
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
        


if __name__ == "__main__":
    # Test card rendering.
    card_a = CSVCard("file_a", r'header', r'footer')
    card_b = CSVCard("file_b", r'header', r'footer')
    card_a.dump_cards(r'/tmp', r'/tmp', [card_a, card_b])


