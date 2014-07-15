#!/usr/bin/python
# -*- coding: utf-8 -*-

'''usage: pysed [-h] [-v] [-p] [-l] [-r] [-i]

Utility that parses and transforms text

optional arguments:
  -h, --help     : show this help message and exit
  -v, --version  : print version and exit
  -p, --print    : print text
                   e extract/, c chars/, s sum/
  -l, --lines    : print lines
                   'N', '[N-N]', 's step=N/*, all'
                   'c count'
  -r, --replace  : replace text
                   m max=N/, u upper=*/, l lower=*/,
                   s select=[N-N]/, n lines=[N-N]/, /color
  -i, --insert   : insert text
                   m max=N/, s select=[N-N]/, n lines=[N-N]/,
                   /color

N = Number, Options/, 'Pattern'
color = red, green, blue, cyan, yellow, magenta, default

'''


import sys

from .paint import colors
from .args import *
from .files import *


__prog__ = 'pysed'
__author__ = 'dslackw'
__version_info__ = (0, 3, 0)
__version__ = '{0}.{1}.{2}'.format(*__version_info__)
__license__ = 'GNU General Public License v3 (GPLv3)'
__email__ = 'd.zlatanidis@gmail.com'


def replace(read, arg2, arg3):
    '''Replace characters or entire text with another.
        Chose specific areas and to replace
        yet Add color to text'''

    OPTIONS_1 = get_to(arg2, '/')
    arg2 = arg2.replace(OPTIONS_1 + '/', '', 1)

    OPTIONS_2 = get_upside(arg3, '/')
    arg3 = arg3.replace('/' + OPTIONS_2, '', 1)

    find_text = findall(arg2, read)

    nums = get_nums(OPTIONS_1)
    OPTIONS_1 = OPTIONS_1.replace(nums, '')

    if nums == '':
        nums = 0

    if OPTIONS_2 in ['black', 'red', 'green', 'yellow',
                     'cyan', 'blue', 'magenta']:
        color = colors(OPTIONS_2)
        default = colors('default')
    else:
        color = ''
        default = ''

    if OPTIONS_1.startswith('s='):
        nums_all = OPTIONS_1.replace('s=', '')
        OPTIONS_1 = OPTIONS_1.replace(nums_all, '')
        region = select(read, nums_all)
        find_text = findall(arg2, region)
    elif OPTIONS_1.startswith('select='):
        nums_all = OPTIONS_1.replace('select=', '')
        OPTIONS_1 = OPTIONS_1.replace(nums_all, '')
        region = select(read, nums_all)
        find_text = findall(arg2, region)

    if OPTIONS_1.startswith('n='):
        nums_all = OPTIONS_1.replace('n=', '')
        OPTIONS_1 = OPTIONS_1.replace(nums_all, '')
        region = lines(read, nums_all)
        find_text = findall(arg2, region)
    elif OPTIONS_1.startswith('lines='):
        nums_all = OPTIONS_1.replace('lines=', '')
        OPTIONS_1 = OPTIONS_1.replace(nums_all, '')
        region = lines(read, nums_all)
        find_text = findall(arg2, region)

    result = read
    find_text = set(find_text)

    for text in find_text:
        if OPTIONS_1 == 'm=' or OPTIONS_1 == 'max=':
            result = read.replace(text, color + arg3 + default,
                                  int(nums))
        elif OPTIONS_1 == 'u' or OPTIONS_1 == 'upper':
            result = read.replace(text,
                                  color + arg3.upper() + default)
        elif OPTIONS_1 == 'u=*' or OPTIONS_1 == 'upper=*':
            result = color + read.upper() + default
        elif OPTIONS_1 == 'l' or OPTIONS_1 == 'lower':
            result = read.replace(text,
                                  color + arg3.lower() + default)
        elif OPTIONS_1 == 'l=*' or OPTIONS_1 == 'lower=*':
            result = color + read.lower() + default
        elif OPTIONS_1 == 's=' or OPTIONS_1 == 'select=':
            region_original = region
            region = region.replace(text, color + arg3 + default)
            result = result.replace(region_original, region)
        elif OPTIONS_1 == 'n=' or OPTIONS_1 == 'lines=':
            region_original = region
            region = region.replace(text, color + arg3 + default)
            result = result.replace(region_original, region)            
        else:
            result = result.replace(text, color + arg3 + default)

    return result.rstrip()


def append(read, arg2, arg3):
    '''Introduce new characters or the entire text
        with new and can also add color. As with the
        replacement options and you can select specific
         areas'''

    OPTIONS_1 = get_to(arg2, '/')
    arg2 = arg2.replace(OPTIONS_1 + '/', '', 1)

    OPTIONS_2 = get_upside(arg3, '/')
    arg3 = arg3.replace('/' + OPTIONS_2, '', 1)

    find_text = findall(arg2, read)

    nums = get_nums(OPTIONS_1)
    OPTIONS_1 = OPTIONS_1.replace(nums, '')

    if nums == '':
        nums = 0

    if OPTIONS_2 in ['black', 'red', 'green', 'yellow',
                     'cyan', 'blue', 'magenta']:
        color = colors(OPTIONS_2)
        default = colors('default')
    else:
        color = ''
        default = ''

    if OPTIONS_1.startswith('s='):
        nums_all = OPTIONS_1.replace('s=', '')
        OPTIONS_1 = OPTIONS_1.replace(nums_all, '')
        region = select(read, nums_all)
        find_text = findall(arg2, region)
    elif OPTIONS_1.startswith('select='):
        nums_all = OPTIONS_1.replace('select=', '')
        OPTIONS_1 = OPTIONS_1.replace(nums_all, '')
        region = select(read, nums_all)
        find_text = findall(arg2, region)

    if OPTIONS_1.startswith('n='):
        nums_all = OPTIONS_1.replace('n=', '')
        OPTIONS_1 = OPTIONS_1.replace(nums_all, '')
        region = lines(read, nums_all)
        find_text = findall(arg2, region)
    elif OPTIONS_1.startswith('lines='):
        nums_all = OPTIONS_1.replace('lines=', '')
        OPTIONS_1 = OPTIONS_1.replace(nums_all, '')
        region = lines(read, nums_all)
        find_text = findall(arg2, region)

    result = read
    find_text = set(find_text)

    for text in find_text:
        if OPTIONS_1 == 'm=' or OPTIONS_1 == 'max=':
            result = read.replace(text,
                                  color + arg3 + default + text,
                                  int(nums))
        elif OPTIONS_1 == 's=' or OPTIONS_1 == 'select=':
            region_original = region
            region = region.replace(text,
                                    color + arg3 + default + text)
            result = result.replace(region_original, region)
        elif OPTIONS_1 == 'n=' or OPTIONS_1 == 'lines=':
            region_original = region
            region = region.replace(text, 
                                    color + arg3 + default + text)
            result = result.replace(region_original, region)
        else:
            result = result.replace(text,
                                   color + arg3 + default + text)

    return result.rstrip()


def lines(read, argX):
    '''Print all lines of text or specific.
        Printing lines with a step'''

    result = []
    results = []

    OPTIONS_1 = get_to(argX, '/')
    argX = argX.replace(OPTIONS_1 + '/', '', 1)

    step = get_nums(OPTIONS_1)
    OPTIONS_1 = OPTIONS_1.replace(step, '')

    if step == '' or step == "0":
        step = 1

    for line in read.splitlines():
        result.append(line)

    try:
        if argX == '*' or argX == 'all':
            if OPTIONS_1 == 'step=' or OPTIONS_1 == 's=':
                for line in range(0, len(result), int(step)):
                    results.append(result[line])
                result = results
            else:
                result = read,
        elif argX.startswith('[') and argX.endswith(']'):
            argX = argX.replace('[', '', 1)
            argX = argX.replace(']', '', 1)
            line_nums = argX.replace('-', '\n').split()
            if len(line_nums) < 2 or int(
                   line_nums[1]) >= len(result):
                pass
            else:
                for n in range(int(line_nums[0]),
                               int(line_nums[1]) + 1):
                    results.append(result[int(n)])
                result = results
        elif OPTIONS_1 == 'c' or OPTIONS_1 == 'count':
            i = 0
            for line in read.splitlines():
                results.append('{0} <-- {1}'.format(i, line))
                i += 1        
            result = results
        else:
            line_nums = argX.replace(',', '\n').split()
            for num in line_nums:
                if int(num) >= len(result):
                    pass
                else:
                    results.append(result[int(num)])
            result = results
    except ValueError:
            pass

    return '\n'.join(result).rstrip()


def cat(file, arg0, arg1, arg2, arg3):
    '''Print all results before any changes save in a file
        or print statics or extract chars'''

    result = []

    try:
        read = open_file_for_read(file)

        arg_lines = arg1
        OPTIONS_1 = get_to(arg1, '/')

        arg1 = arg1.replace(OPTIONS_1 + '/', '', 1)
        find_text = findall(arg1, read)

        if arg0 == '-p' or arg0 == '--print':
            pass
            if OPTIONS_1 == 's' or OPTIONS_1 == 'sum':
                words = read.split()
                chars = ''.join(words)
                for line in range(len(read.splitlines())):
                    pass
                print ('%d lines' % (line))
                print ('%d characters' % len(chars))
                print ('%d words' % len(words))
                print ('%d blanks' % (len(read) - len(chars)))
            elif OPTIONS_1 == 'c' or OPTIONS_1 == 'chars':
                print ('find %d --> \'%s\'' % (
                    len(find_text), arg1))
            elif OPTIONS_1 == 'e' or OPTIONS_1 == 'extract':
                print (' '.join(find_text))
            else:
                print ('{}'.format(read,).strip())
        elif arg0 == '-l' or arg0 == '--lines':
            result = lines(read, arg_lines)
        elif arg0 == '-r' or arg0 == '--replace':
            result = replace(read, arg2, arg3)

        elif arg0 == '-i' or arg0 == '--insert':
            result = append(read, arg2, arg3)
        else:
            arguments_error(arg0, '')
        if result != []:
            print ('{}'.format(result,))
    except IOError:
        print ("%s: can't read %s: No such file or directory"
               % (__prog__, file))


def write_replace_text(file, arg1, arg2):
    '''Replace the text and save changes to the file'''

    result = []

    try:
        file = open_file_for_read_and_write(file)
        read = file.read()
        result = replace(read, arg1, arg2)
        if result != []:
            write_to_file(file, result)
    except IOError:
        print ("%s: can't read %s: No such file or directory"
               % (__prog__, file))


def write_append_text(file, arg1, arg2):
    '''Insert text and save changes to the file'''

    result = []

    try:
        file = open_file_for_read_and_write(file)
        read = file.read()
        result = append(read, arg1, arg2)
        if result != []:
            write_to_file(file, result)
    except IOError:
        print ("%s: can't read %s: No such file or directory"
               % (__prog__, file))


def version():
    '''Print version, license and email'''

    print ('version : {}'.format(__version__))
    print ('License : {}'.format(__license__))
    print ('Email   : {}'.format(__email__))


def arguments_view():
    '''Print arguments options'''

    print ('usage: pysed [-h] [-v] [-p] [-l] [-r] [-i]\n')
    print ('Utility that parses and transforms text\n')
    print ('optional arguments:')
    print ('  -h, --help     : show this help message and exit')
    print ('  -v, --version  : print version and exit')
    print ('  -p, --print    : print text')
    print ('                   e extract/, c chars/, s sum/')
    print ('  -l, --lines    : print lines')
    print ('                   \'N\', \'[N-N]\', \'s step=N/*, all\',')
    print ('                   \'c count\'')
    print ('  -r, --replace  : replace text')
    print ('                   m max=N/, u upper=*/, l lower=*/,')
    print ('                   s select=[N-N]/, n lines=[N-N]/, /color')
    print ('  -i, --insert   : insert text')
    print ('                   m max=N/, s select=[N-N]/, n lines=[N-N]/,')
    print ('                   /color\n')
    print ('N = Number, Options/, \'Pattern\'')
    print ('color = black, red, green, blue, cyan, yellow, magenta, default')


def arguments_error(arg0, argx):
    '''Print errors arguments'''

    print ('usage: %s [-h] [-v] [-p] [-l] [-r] [-i]\n' % __prog__)

    if arg0 == '':
        print ('%s: error: argument: expected one argument' % __prog__)
    elif arg0 in ['-p', '--print',
                  '-l', '--lines',
                  '-r', '--replace',
                  '-i', '--insert']:
        print ('%s: argument %s: expected at least one argument'
               % (__prog__, arg0))
    else:
        print ('%s: error: unrecognized arguments: %s %s'
               % (__prog__, arg0, ' '.join(argx)))


def main():
    arg = sys.argv
    arg.pop(0)

    if len(arg) == 2:
        file = arg[1]
    elif len(arg) == 3:
        file = arg[2]
    elif len(arg) == 4:
        file = arg[3]
    elif len(arg) == 5:
        file = arg[4]

    if len(arg) == 0:
        arguments_error('', '')
    elif (len(arg) == 1 and arg[0] == '-h' or len(arg) == 1
                        and arg[0] == '--help'):
        arguments_view()
    elif (len(arg) == 1 and arg[0] == '-v' or len(arg) == 1 
                        and arg[0] == '--version'):
        version()
    elif (len(arg) == 2 and arg[0] == '-p' or len(arg) == 2 
                        and arg[0] == '--print'):
        cat(file, arg[0], '', '', '')
    elif (len(arg) == 3 and arg[0] == '-p' or len(arg) == 3
                        and arg[0] == '--print'):
        cat(file, arg[0], arg[1], '', '')
    elif (len(arg) == 5 and arg[1] == '-p' or len(arg) == 5
                        and arg[1] == '--print'):
        cat(file, arg[0], arg[1], arg[2], arg[3])
    elif (len(arg) == 3 and arg[0] == '-l' or len(arg) == 3
                        and arg[0] == '--lines'):
        cat(file, arg[0], arg[1], '', '')
    elif (len(arg) == 4 and arg[0] == '-r' or len(arg) == 4
                        and arg[0] == '--replace'):
        write_replace_text(file, arg[1], arg[2])
    elif (len(arg) == 4 and arg[0] == '-i' or len(arg) == 4
                        and arg[0] == '--insert'):
        write_append_text(file, arg[1], arg[2])
    elif not any(
        [len(arg) == 1 and arg[0] == '-p', len(arg) == 1 and arg[0] == '--print',
         len(arg) == 1 and arg[0] == '-l', len(arg) == 1 and arg[0] == '--lines',
         len(arg) == 1 and arg[0] == '-r', len(arg) == 1 and arg[0] == '--replace',
         len(arg) == 1 and arg[0] == '-i', len(arg) == 1 and arg[0] == '--insert', ]):
        arguments_error(arg[0], arg[1:])
    else:
        arguments_error(arg[0], arg[1:])

if __name__ == '__main__':
    main()
