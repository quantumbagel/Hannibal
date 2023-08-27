def dprint(prog='main', *args):
    """
    A very simple function to print logs
    :param prog: the program running
    :param args: other arguments to pass to print
    :return: none
    """
    print(f'[{prog}]', *args)
