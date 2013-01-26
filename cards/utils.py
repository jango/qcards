#!/usr/bin/python

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

if __name__ == "__main__":
    print convert_str('$header', '*', '*', '$', '$', '_', '_')
    print convert_str('*footer', '*', '*', '$', '$', '_', '_')
    print convert_str('_front', '*', '*', '$', '$', '_', '_')
    print convert_str(r'\\b\a\\\\ck \$c\*a\_r*d\\', '*', '*', '$', '$', '_', '_')
