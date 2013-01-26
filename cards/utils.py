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

import  os

def render_string(mask, fields, row):
    # Check that we have enough values)
    if len(row) < max(fields) + 1:
        raise ValueError("Mask `%s` specifies field `%s`, but row `%s` only has `%s` elements" % (mask, str(max(fields)), str(row), str(len(row)) ))

    vals = []
    for field in fields:
        vals.append(row[field])

    # Convert to tuple and substitute.
    vals = tuple(vals)
    
    string = mask % vals
    string = string.decode("utf-8")
    return string

def parse_mappings(options, card_class):
    fields = card_class.OPTIONS

    card_options = {}
    # Check for mandatory fields.
    for fld in fields:
        if not options.has_key(fld):
            raise ValueError("Option `%s` is mandatory for `%s` card type, but is absent from the config file." % (fld, card_class.__name__))
        else:
            if fld == "filename_field":
                try:
                    int(options[fld])
                except:
                    raise ValueError('Option `%s` for card type `%s` should be an integer.' % (fld, card_class.__name__))

                card_options["filename_field"] = int(options[fld])

            # Make sure every _fields has a matching _mask
            elif fld.endswith("_fields"):
                if not (fld.split("_fields")[0] + "_mask") in fields:
                    raise ValueError('Option `%s` for card type `%s` must have a matching mask option.' % (fld, card_class.__name__))

                # Validate the _fields field. First, try split the list of fields.
                p_int = []
                try:
                    integers = options[fld].split(",")
                    for i in integers:
                        p_int.append(int(i))
                    card_options[fld] = p_int
                except:
                    raise ValueError('Option `%s` for card type `%s` is not a valid list of integers.' % (fld, card_class.__name__))                    

                # Second, make sure the mask has as many %s as we have fields.
                mask = str(options[fld.split("_fields")[0] + "_mask"])
                if mask.count("%s") != len(p_int):
                    raise ValueError('Option `%s` for card type `%s` number of fields doesn\'t match the number of placeholders in the mask' %  \
                    (fld, card_class.__name__))

            else:
                card_options[fld] = options[fld]

    return card_options


def convert_str(string, b_left, b_right, i_left, i_right, u_left, u_right):
    """Replaces meta characters *, _, $ with appropriate substitutes, \ is
       used for escaping."""

    new_string = ""
    skip_proc = False
    skip_char = False

    for cnt, s in enumerate(string):
        # Current character.
        curr_char = s

        # If skip_char is true, it means we skip the character entirely.
        if skip_char == True:
            skip_char = False
            continue

        # If the skip_proc is true, it means we will simply append this character.
        if skip_proc == True:
            skip_proc = False
            new_string += s
            continue

        # Define previous and next character.
        if cnt == 0:
            prev_char = None
        else:
            prev_char = string[cnt - 1]

        if cnt + 1 < len(string):
            next_char = string[cnt + 1]
        else:
            next_char = None

        # If we encounter \, we need to process it as an
        # escape sequence.
        if curr_char == '\\':
            skip_proc = True
            continue
        elif curr_char == r'*' and next_char is not None:
            new_string += b_left + next_char + b_right
            skip_char = True
        elif curr_char == r'$' and next_char is not None:
            new_string += i_left + next_char + i_right
            skip_char = True
        elif curr_char == r'_' and next_char is not None:
            new_string += u_left + next_char + u_right
            skip_char = True
        else:
            new_string += curr_char

    return new_string

def get_abs_path(path, prefix):
    """Returns `path` if it's absolute, returns path + prefix if `path` is
       relative."""
    if os.path.isabs(path):
        return path
    else:
        return os.path.normpath(os.path.join(prefix, path))

if __name__ == "__main__":
    print convert_str('$header', '*', '*', '$', '$', '_', '_')
    print convert_str('*footer', '*', '*', '$', '$', '_', '_')
    print convert_str('_front', '*', '*', '$', '$', '_', '_')
    print convert_str(r'\\b\a\\\\ck \$c\*a\_r*d\\', '*', '*', '$', '$', '_', '_')
