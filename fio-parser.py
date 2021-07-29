#!/usr/bin/env python3
from os import listdir
from os.path import isfile, join
import argparse
import os


def command_line():
    parser = argparse.ArgumentParser(prog='fio-parser.py', description='%(prog)s is used to parse fio output files')
    parser.add_argument('--directory',
                        '-d',
                        type=str,
                        help='Specify the directory with fio output files to parse.  If none if provided, ./ is used')
    parser.add_argument('--delimiter', '-D', type=str, help='Specify output separator. Default ",".', default=',')
    # parser.add_argument('--output',
    # '-rod',
    # type=str,
    # help='Specify the output file to dump results.  If none, output is to screen')
    arg = vars(parser.parse_args())

    if not arg['directory']:
        directory = os.getcwd()
    else:
        directory = arg['directory']
    '''
    if arg['output']:
       if '/' in arg['output']:
           dir = '/'.join(arg['output'].split('/')[:-1])
           output_file = arg['output'].split('/')[-1]
           if ! output_file:
              print('--output %s missing file name, exiting' % (arg['output'])
              exit()
       else:
           dir='./'
           output_file = arg['output']

       if isdir(dir):
    '''

    f_list = get_file_list(directory)
    return f_list, arg['delimiter']


def get_file_list(directory):
    """
    extract the contents of the current file if present to only overwrite the section in play
    """

    if os.path.exists(directory):
        f_list = []
        only_files = [files for files in listdir(directory) if isfile(join(directory, files))]
        # Check for non binary files and make a list of them
        for files in only_files:
            abs_path = ('%s/%s' % (directory, files))
            # with open( abs_path,'rb') as fh:
            with open(abs_path, 'r') as fh:
                if 'fio-parser.py' not in files and 'IO depths' in fh.read():
                    f_list.append('%s/%s' % (directory, files))
        if (len(f_list)) > 0:
            return sorted(f_list)
        else:
            print('No text files found')
            exit()
    else:
        print(('Directory %s invalid' % directory))
        exit()


def parse_files(f_list, d):
    total_output_list = \
        [('fio_file{0}operation{0}io_depth{0}reads{0}read_bw(MiB/s){0}read_lat(ms){0}writes{0}write_bw(MIB/s){0}'
          'write_lat(ms)').format(d)]
    for working_file in f_list:
        with open(working_file, 'r') as fh:
            file_content = fh.readlines()
        # extract_content(file_content, working_file, total_output_list)
        parsed_content = extract_content(file_content)
        total_output(parsed_content, total_output_list, working_file, delimiter)
    return total_output_list


def bandwidth_conversion(b_line):
    bandwidth = (b_line.split(','))[1].split(' ')[1].split('=')[1]
    if 'Mi' in bandwidth:
        bandwidth = bandwidth.split('M')[0]
    elif 'Ki' in bandwidth:
        bandwidth = int(bandwidth.split('K')[0]) / 2**10
    elif 'Gi' in bandwidth:
        bandwidth = int(bandwidth.split('G')[0]) * 2**20
    elif 'Ti' in bandwidth:
        bandwidth = int(bandwidth.split('T')[0]) * 2**30
    return bandwidth


def io_conversion(io_line):
    io = io_line.split(',')[0].split('=')[1]
    if 'k' in io:
        io = int(float(io[0:-1]) * 10**3)
    elif 'm' in io:
        io = int(float(io[0:-1]) * 10**6)
    return io


def iodepth_conversion(depth_line):
    return depth_line.split(' ')[10].split('=')[1]


def lat_conversion(lat_line):
    lat = (float(lat_line.split(',')[2].split('=')[1]))
    if lat_line[5] == 'u':
        lat = lat / 10**3
    elif lat_line[5] == 'n':
        lat = lat / 10**6
    elif lat_line[5] == 's':
        lat = lat * 10**3
    return lat


def operation_conversion(op_line):
    return op_line.split(' ')[2].split('=')[1][0:-1]


# look for 'All clients in file', if found, this file contains
# The contents ofd a multi host job
def single_or_multi_job(content):
    for job_line in content:
        if 'All clients:' in job_line:
            return True
    return False


def search(parsed_content, s_line):
    if 'read: IOP' in s_line:
        parsed_content['read_iop'] = io_conversion(s_line)
        parsed_content['read_bw'] = bandwidth_conversion(s_line)
    if 'read_iop' in list(parsed_content.keys()) and \
            s_line[0:3] == 'lat' and \
            'read_lat' not in list(parsed_content.keys()):
        parsed_content['read_lat'] = lat_conversion(s_line)

    if 'write: IOP' in s_line:
        parsed_content['write_iop'] = io_conversion(s_line)
        parsed_content['write_bw'] = bandwidth_conversion(s_line)
    if 'write_iop' in list(parsed_content.keys()) and \
            s_line[0:3] == 'lat' and \
            'write_lat' not in list(parsed_content.keys()):
        parsed_content['write_lat'] = lat_conversion(s_line)

    if 'rw=' in s_line:
        parsed_content['operation'] = operation_conversion(s_line)
    if 'iodepth=' in s_line:
        parsed_content['iodepth'] = iodepth_conversion(s_line)


def extract_content(content):
    multihost = single_or_multi_job(content)
    parsed_content = {}
    if multihost:
        begin_search = False
    else:
        begin_search = True

    for c_line in content:
        c_line = c_line.strip()
        if multihost and 'All clients:' in c_line:
            begin_search = True
        if begin_search:
            search(parsed_content, c_line)
        # Exit search here
        if begin_search and 'IO depths' in c_line:
            return parsed_content


def total_output(parsed_content, total_output_list, working_file, d):
    out = working_file.split('/')[-1]
    out += '{0}{1}{0}{2}'.format(d, parsed_content['operation'], parsed_content['iodepth'])
    if 'read_iop' in list(parsed_content.keys()):
        out += '{0}{1}{0}{2:.3f}'.format(d, parsed_content['read_iop'], float(parsed_content['read_bw']))
    else:
        out += '{0}{0}'.format(d)
    if 'read_lat' in list(parsed_content.keys()):
        out += '{0}{1:.3f}'.format(d, parsed_content['read_lat'])
    else:
        out += '{0}'.format(d)
    if 'write_iop' in list(parsed_content.keys()):
        out += '{0}{1}{0}{2:.3f}'.format(d, parsed_content['write_iop'], float(parsed_content['write_bw']))
    else:
        out += '{0}{0}'.format(d)
    if 'write_lat' in list(parsed_content.keys()):
        out += '{0}{1:.3f}'.format(d, parsed_content['write_lat'])
    else:
        out += d
    total_output_list.append(out)


file_list, delimiter = command_line()
output = parse_files(file_list, delimiter)
for line in output:
    print(line)
