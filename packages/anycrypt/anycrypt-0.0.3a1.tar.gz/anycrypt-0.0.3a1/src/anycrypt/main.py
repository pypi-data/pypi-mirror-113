# -*- coding: utf-8 -*-
#
#  This file is part of anycrypt.
#
#  Copyright (c) 2020-2021 Georgios (George) Notaras <george@gnotaras.com>
#
#  All Rights Reserved.
#
#  This software has been developed since the 19th of January 2020
#  in an attempt to create a secure way of exchanging classified
#  information. Please note this work is currently proprietary.
#
#  The source code of this work is provided for functionality evaluation
#  and debugging purposes only. Distribution of this source code or
#  building other works on it are currently disallowed, unless there has
#  been a private agreement with a specific third party.
#
#  The distribution points of this source code are:
#
#    * https://codetrax.org/projects/anycrypt/files
#    * https://source.codetrax.org/gnotaras/anycrypt
#    * https://pypi.org/project/anycrypt
#



import sys
import os
import argparse
import StringIO
import json
from pprint import pprint
import base64
import copy
import string
import random


def get_tables(opts):
    # Format tables
    # [
    #   [ # Group0
    #     [ # Table0
    #       [(c0,r0), (c1,r0), (c2,r0)],
    #       [(c0,r1), (c1,r1), (c2,r1)],
    #       [(c0,r2), (c1,r2), (c2,r2)],
    #     ],
    #     [ # Table1
    #       [(c0,r0), (c1,r0), (c2,r0)],
    #       [(c0,r1), (c1,r1), (c2,r1)],
    #       [(c0,r2), (c1,r2), (c2,r2)],
    #     ],
    #   ],
    #   [ # Group1
    #     [ # Table0
    #       [(c0,r0), (c1,r0), (c2,r0)],
    #       [(c0,r1), (c1,r1), (c2,r1)],
    #       [(c0,r2), (c1,r2), (c2,r2)],
    #     ],
    #     [ # Table1
    #       [(c0,r0), (c1,r0), (c2,r0)],
    #       [(c0,r1), (c1,r1), (c2,r1)],
    #       [(c0,r2), (c1,r2), (c2,r2)],
    #     ],
    #   ],
    # ]
    #
    # Input format:
    # - Column items separated by space.
    # - Rows separated by new line.
    # - Tables separated by |.
    # - Groups are separated by --.
    #
    # Example:
    #
    #                         Group 1
    #    Table1         Table2         Table3         Table4
    #  Z  j  t  B  |  c  x  u  b  |  D  d  a  y  |  2  e  A  i 
    #  C  h  M  r  |  s  T  g  X  |  K  o  Q  8  |  S  7  G  4 
    #  m  v  3  6  |  +  R  9  l  |  E  H  n  5  |  q  O  k  p 
    #  f  N  L  /  |  Y  0  W  1  |  I  J  P  V  |  w  z  F  U
    #
    tables = []
    table_data_raw_io = StringIO.StringIO()
    for table_path in opts.tables:
        if not os.path.exists(table_path):
            sys.stderr.write('Table not found: %s' % table_path)
            sys.stderr.flush()
        adding_table_data = False
        with open(table_path, 'rb') as f_in:
            for line in f_in:
                if not line.strip():
                    adding_table_data = False
                    continue
                if not adding_table_data:
                    adding_table_data = True
                    table_data_raw_io.write('--\n')
                table_data_raw_io.write(line)
    # Ensure raw table data ends with a new line.
    table_data_raw_io.write('\n')
    table_data_raw_io.seek(0)
    #print(table_data_raw_io.read())
    
    group_idx = None
    for line in table_data_raw_io:
        #print(line)
        line = line.strip()
        if not line:
            continue
        elif line == '--':
            # Each group is preceded by a line containing: --
            if group_idx is None:
                group_idx = 0
            else:
                group_idx += 1
            tables.append([])
            continue


        # Find total number of tables for group.
        all_tables_row = line.split('|')
        if not tables[group_idx]:
            for table_idx in range(len(all_tables_row)):
                tables[group_idx].append([])

        for table_idx, single_table_row in enumerate(all_tables_row):
            #print table_idx, single_table_row
            items = []
            for item in single_table_row.split():
                item = item.strip()
                if item:
                    items.append(item)
            #print items
            tables[group_idx][table_idx].append(items)
    #pprint(tables)
    
    if not opts.debug:
        return tables

    for group_idx in range(len(tables)):
        if not tables[group_idx]:
            break
        row = 0
        row_max = len(tables[group_idx][0])
        while row < row_max:
            for table_idx in range(len(tables[group_idx])):
                # Test for existing row
                try:
                    tables[group_idx][table_idx][row]
                except IndexError as e:
                    break
                if table_idx > 0:
                    sys.stderr.write(' | ')
                sys.stderr.write('  '.join(tables[group_idx][table_idx][row]))
            sys.stderr.write('\n')
            row += 1
        sys.stderr.write('\n')
    return tables

        
def encode(opts):
    tables = get_tables(opts)
    input_data_io = StringIO.StringIO()
    try:
        if opts.infile == '-':
            f_in = sys.stdin
        else:
            f_in = open(opts.infile, 'rb')
        for line in f_in:
            input_data_io.write(line)
    finally:
        if opts.infile != '-':
            f_in.close()
    input_data_io_base64 = StringIO.StringIO()
    input_data_io.seek(0)
    input_data_io_base64.write(
        base64.b64encode(input_data_io.read()))
    #input_data_io_base64.seek(0)
    #print(input_data_io_base64.read())
    input_data_io_base64.seek(0)
    output = input_data_io_base64.read()
    output_working = []
    ##assert divmod(len(tables), 2)[1] == 1

    line_length = 64

    for idx in range(len(output)):
        obj = output[idx]
        if obj == '=':
            break

        if idx and not divmod(idx, line_length)[1]:
            output_working.append('\n')

        # The character passes through all tables in the following manner.
        # The character is analyzed to table_idx|row_idx|col of the odd
        # groups and reconstructed back to a character through an even group.
        for group in tables:
            if len(obj) == 1:
                # Find coordinates
                col = None
                for table_idx, table in enumerate(group):
                    for row_idx, row_items in enumerate(table):
                        try:
                            col = row_items.index(obj)
                        except ValueError as e:
                            continue
                        if col is not None:
                            break
                    if col is not None:
                        break
                if col is not None:
                    obj = '%d%d%d' % (table_idx, row_idx, col)
            else:   # obj is coordinates
                # Locate character using coordinates in the next group of tables.
                table_idx, row_idx, col = tuple(list(obj))
                #print table_idx, row_idx, col
                obj = group[int(table_idx)][int(row_idx)][int(col)]
        output_working.append(obj)        

    output = copy.copy(output_working)
    output_str = ''.join(output)
    last_line_start_pos = output_str.rfind('\n') + 1
    #padding = divmod(len(output_str), 4)[1]
    padding = line_length - (len(output_str) - last_line_start_pos)
    if padding:
        output_str = '%s%s' % (output_str, '=' * padding)
    #print(output_str)

    if not opts.outfile or opts.outfile == '-':
        print(output_str)
    else:
        f = open(opts.outfile, 'wb')
        f.write(output_str)
        f.close()


def decode(opts):
    tables = get_tables(opts)
    input_data_io = StringIO.StringIO()
    try:
        if opts.infile == '-':
            f_in = sys.stdin
        else:
            f_in = open(opts.infile, 'rb')
        for line in f_in:
            input_data_io.write(line)
    finally:
        if opts.infile != '-':
            f_in.close()
#    input_data_io_base64 = StringIO.StringIO()
#    input_data_io.seek(0)
#    input_data_io_base64.write(
#        base64.b64encode(input_data_io.read()))
#    input_data_io_base64.seek(0)
#    #print(input_data_io_base64.read())
#    output = input_data_io_base64.read()
#    output = input_data_io.read()
    input_data_io.seek(0)
    output = []
    output_working = []
    tables.reverse()
    while True:

        obj = input_data_io.read(1)
        #if not obj.strip():
        # New lines are taken care later by the base64.b64decode function.
        if not obj:
            # Reached the end
            #print('end')
            break
        # The character passes through all tables in the following manner.
        # The character is analyzed to table_idx|row_idx|col of the odd
        # groups and reconstructed back to a character through an even group.
        for group in tables:
            if len(obj) == 1:
                # Find coordinates
                col = None
                for table_idx, table in enumerate(group):
                    for row_idx, row_items in enumerate(table):
                        try:
                            col = row_items.index(obj)
                        except ValueError as e:
                            continue
                        if col is not None:
                            break
                    if col is not None:
                        break
                if col is not None:
                    obj = '%d%d%d' % (table_idx, row_idx, col)
            else:   # obj is coordinates
                # Locate character using coordinates in the next group of tables.
                table_idx, row_idx, col = tuple(list(obj))
                #print table_idx, row_idx, col
                obj = group[int(table_idx)][int(row_idx)][int(col)]
        output_working.append(obj)        

    output = copy.copy(output_working)

    if not opts.outfile or opts.outfile == '-':
        print(base64.b64decode(''.join(output)))
    else:
        f = open(opts.outfile, 'wb')
        f.write(base64.b64decode(''.join(output)))
        f.close()

    """
    output_data_io_base64 = StringIO.StringIO(''.join(output))
    output_data_io = StringIO.StringIO()
    output_data_io.seek(0)
    output_data_io.write(
        base64.b64decode(output_data_io_base64.read()))
    print(output_data_io.read())
#    input_data_io_base64.seek(0)
#    #print(input_data_io_base64.read())
#    output = input_data_io_base64.read()
#    output = input_data_io.read()
    """

def get_version():
    return '0.1.0'

def main():

    usage = '''%s [general-options] command [command-specific-options]''' % os.path.basename(sys.argv[0])

    parser = argparse.ArgumentParser(usage=usage, version=get_version())

    parser.set_defaults(
        debug = False,
        infile = '-',
        outfile = '-',
    )

    parser.add_argument('-d', '--debug', action='store_true', dest='debug', \
        help= '''Prints all messages.''')

    parser.add_argument('-i', '--infile', action='store', dest='infile', metavar='PATH', \
        help='''Path to input file.''')

    parser.add_argument('-o', '--outfile', action='store', dest='outfile', metavar='PATH', \
        help='''Path to output file.''')

    #parser.add_argument('tables', metavar='PATH', nargs='+',
    #    help='Paths to table files in required order.')

    subparsers = parser.add_subparsers(help='sub-command help')

    # Subcommand encode

    parser_encode = subparsers.add_parser('encode', help='Encode text using provided NxN tables in order.')
    parser_encode.set_defaults(command='encode')

    parser_encode.add_argument('tables', metavar='PATH', nargs='+',
        help='Paths to table files in required order.')

    # Subcommand decode

    parser_decode = subparsers.add_parser('decode', help='Decode text using provided NxN tables in order.')
    parser_decode.set_defaults(command='decode')

    parser_decode.add_argument('tables', metavar='PATH', nargs='+',
        help='Paths to table files in required order.')

    opts = parser.parse_args()

    #print(opts)
    #return opts
    
    if opts.command == 'encode':
        encode(opts)
    elif opts.command == 'decode':
        decode(opts)


"""
Generates NxN tables

This source code has been moved here from gentables.py, part of
the initial project.
"""

pool = string.uppercase + string.lowercase + string.digits + '/+'
assert len(pool) == 64

def shuffle(counts=100):
    pool_shuffled = list(pool)
    for count in range(counts):
        pool_work = []
        idx_pool = [i for i in range(len(pool))]
        while len(idx_pool):
            idx = random.choice(idx_pool)
            if random.choice([0,1,0,0,1]):
                continue
            pool_work.append(pool_shuffled[idx])
            idx_pool.pop(idx_pool.index(idx))
        assert len(pool_work) == 64
        pool_shuffled = copy.copy(pool_work)
    assert len(set(pool_shuffled)) == len(pool)
    #print(pool)
    #print(''.join(pool_shuffled))
    return pool_shuffled


def gentables(nr_tables=4):
    pool_shuffled = shuffle()
    nr_group_items, remnant = divmod(len(pool_shuffled), nr_tables)
    for i in range(2, nr_group_items + 1):
        cols, remnant = divmod(nr_group_items, i**2)
        if remnant < i**2:
            break
    sys.stdout.write('\n')
    for c, char in enumerate(pool_shuffled):
        sys.stdout.write(' %s ' % char)
        if not divmod(c + 1, nr_tables * cols)[1]:
            sys.stdout.write('\n')
        elif not divmod(c + 1, cols)[1]:
            sys.stdout.write(' | ')
    sys.stdout.write('\n')
    sys.stdout.flush()


def main_tables():
    nr_groups = 1
    nr_tables = 4
    if len(sys.argv) > 1:
        nr_tables = int(sys.argv[1])
    if len(sys.argv) > 2:
        nr_groups = int(sys.argv[2])
    for i in range(nr_groups):
        gentables(nr_tables=nr_tables)



if __name__ == '__main__':
    main()



