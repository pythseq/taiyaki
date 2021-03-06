#!/usr/bin/env python3
# Combine mapped-read files in HDF5 format into a single file

import argparse
from taiyaki import mapped_signal_files
from taiyaki.cmdargs import Positive

parser = argparse.ArgumentParser(
    description='Combine HDF5 mapped-read files into a single file')
parser.add_argument('output',help='Output filename')
parser.add_argument('inputs', nargs='*', help='One or more input files')
parser.add_argument('--version', default=mapped_signal_files._version, type=Positive(int),
                    help='Version number for mapped read format')

#To convert to any new mapped read format (e.g. mapped_signal_files.SQL)
#we should be able to just change MAPPED_READ_CLASS to equal the new class.
MAPPED_READ_CLASS = mapped_signal_files.HDF5


if __name__ == '__main__':
    args = parser.parse_args()
    reads_written = set()
    print("Writing reads to ", args.output)
    with  MAPPED_READ_CLASS(args.output, "w") as hout:
        hout.write_version_number(args.version)
        for infile in args.inputs:
            copied_from_this_file = 0
            with MAPPED_READ_CLASS(infile, "r") as hin:
                in_version = hin.get_version_number()
                if in_version != args.version:
                    raise Exception("Version number of files should be {} but version number of {} is {}".format(args.version, infile, in_version))
                for read_id in hin.get_read_ids():
                    if read_id in reads_written:
                        print("* Read",read_id,"already present: not copying from",infile)
                    else:
                        hout.write_read(read_id, hin.get_read(read_id))
                        reads_written.add(read_id)
                        copied_from_this_file += 1
            print("Copied",copied_from_this_file,"reads from",infile)
    print("Copied",len(reads_written),"reads in total")
                        