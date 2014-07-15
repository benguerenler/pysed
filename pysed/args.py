#!/usr/bin/python
# -*- coding: utf-8 -*-


import re

def select(read, nums_all):
    '''Select a region to modify'''

    nums_all = nums_all.replace('[', '')
    nums_all = nums_all.replace(']', '')
    try:
        begin = int(get_to(nums_all, '-').replace('-', ''))
        end = int(get_upside(nums_all, '-').replace('-', ''))
        result = read[begin:end]
    except ValueError:
        result = ''
        
    return result


def get_to(arg, char):
    '''Get any string before char /'''

    result = []
    for c in arg:
        result.append(c)
        if c == char:
            break

    return ''.join(result).replace('/', '')


def get_upside(arg, char):
    '''Get any string after char /'''

    i = 0
    result = []
    for c in range(len(arg)):
        i -= 1
        result.append(arg[i])
        if arg[i] == char:
            break

    return ''.join(result[::-1]).replace('/', '')


def get_nums(text):
    '''Grep numbers from a string'''

    nums = '0123456789'

    result = []
    for t in text:
        for n in nums:
            if n == t:
                result.append(n)

    return ''.join(result)


def findall(argX, read):
    '''Find text from string'''

    try:
        find_text = re.findall(argX, read)

        if find_text == []:
            find_text == ''
    except re.error:
        find_text = ''

    return find_text
