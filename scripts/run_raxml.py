#!/usr/bin/env python3
"""
Author : kyclark
Date   : 2019-05-03
Purpose: Run RaxML
"""

import argparse
import os
import sys
import tempfile
import subprocess


# --------------------------------------------------
def get_args():
    """get command-line arguments"""
    parser = argparse.ArgumentParser(
        description='Run RaxML',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument(
        'file', metavar='FILE', nargs='+', help='Input file(s)')

    # parser.add_argument(
    #     '-a',
    #     '--arg',
    #     help='A named string argument',
    #     metavar='str',
    #     type=str,
    #     default='')

    # parser.add_argument(
    #     '-i',
    #     '--int',
    #     help='A named integer argument',
    #     metavar='int',
    #     type=int,
    #     default=0)

    # parser.add_argument(
    #     '-f', '--flag', help='A boolean flag', action='store_true')

    return parser.parse_args()


# --------------------------------------------------
def warn(msg):
    """Print a message to STDERR"""
    print(msg, file=sys.stderr)


# --------------------------------------------------
def die(msg='Something bad happened'):
    """warn() and exit with error"""
    warn(msg)
    sys.exit(1)

# --------------------------------------------------
def line_count(fname):
    """Count the number of lines in a file"""

    n = 0
    for _ in open(fname):
        n += 1

    return n

# --------------------------------------------------
def run_job_file(jobfile, msg='Running job', procs=1):
    """Run a job file if there are jobs"""

    num_jobs = line_count(jobfile)
    warn('{} (# jobs = {})'.format(msg, num_jobs))

    if num_jobs > 0:
        cmd = 'parallel --halt soon,fail=1 -P {} < {}'.format(procs, jobfile)

        try:
            subprocess.run(cmd, shell=True, check=True)
        except subprocess.CalledProcessError as err:
            die('Error:\n{}\n{}\n'.format(err.stderr, err.stdout))
        finally:
            os.remove(jobfile)

    return True

# --------------------------------------------------
def main():
    """Make a jazz noise here"""
    args = get_args()

    jobfile = tempfile.NamedTemporaryFile(delete=False, mode='wt')

    raxml = 'singularity exec raxml-8.2.12.img raxml'
    cmd = '{} -m PROTGAMMAAUTO -s {} -p 12345 -x 12345 -o {} -n TEST -f a -N 1000'

    for file in args.file:
        jobfile.write(cmd.format(raxml, file, 'STR0027663'))

    jobfile.close()

    run_job_file(jobfile=jobfile.name, msg='Running RaxML', procs=12)


# --------------------------------------------------
if __name__ == '__main__':
    main()