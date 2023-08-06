"""
A sample which provide print_lol().
"""


def print_lol(the_list, level):
    """print list"""
    for each_item in the_list:
        if isinstance(each_item, list):
            print_lol(each_item, level+1)
        else:
            print('\t'*level, end='')
            print(each_item)
