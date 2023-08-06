'''
Console arguments handler
'''

from argparse import ArgumentParser, RawTextHelpFormatter


parser = ArgumentParser(
    description=f'''
    Chemical calculators.

    Features:
    - Determines substance composition, mass, etc.
    - Balance chemical reactions
    ''',
    epilog='Last updated: 2020 July 05',
    formatter_class=RawTextHelpFormatter)

parser.add_argument('--reaction', '-r', dest='reaction', required=False,
                    type=str, help='balance reaction')

parser.add_argument('--substance', '-s', dest='substance', required=False,
                    type=str, help='get substance info')

parser.add_argument('--gui', '-g', dest='gui',
                    required=True, type=str, help='enable graphical interface')

args = vars(parser.parse_args())
