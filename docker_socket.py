#!/usr/bin/python
""" docker_socket - A Nagios plugin for watching docker socket and info

Provides a plugin that:
    - checks if docker command exists
    - checks if the docker socket exists
    - provides status and performance in Nagios format

Requires:
    - Python version 2.7+

Author:
    - Joe Harkins <jharkins@gmail.com>

"""

import subprocess
import sys
import argparse


# Helper functions for exiting with correct Nagios status
def ok(message):
    print "OK: {0}".format(message)
    sys.exit(0)


def warn(message):
    print "WARNING: {0}".format(message)
    sys.exit(1)


def critical(message):
    print "CRITICAL: {0}".format(message)
    sys.exit(2)


def unknown(message):
    print "UNKNOWN: {0}".format(message)
    sys.exit(3)


def test_docker():
    """ Test if the docker command exists """

    try:
        subprocess.Popen(['docker'], stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    except OSError:
        critical("docker command not found")


def get_docker_info():
    """ get the information from `docker info` """

    d_process = subprocess.Popen(['docker', 'info'], stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)

    # interact with `docker info`
    result = d_process.communicate()

    # capture docker process issues
    if d_process.returncode is 1:
        # return the stderr from the docker command
        critical(result[1].strip())

    # it worked, return docker inf
    return parse_docker_info(result)


def parse_docker_info(result):
    """ parse the docker info result and return dictionary """

    d_info_raw = [l.strip() for l in result[0].split('\n')]
    d_info = {}

    for row in d_info_raw:
        if row is not "":
            d_info[row.split(':')[0].strip()] = row.split(':')[1].strip()

    return d_info


def format_nagios_performance(docker_info, verbose=False):
    """ format the docker info dict nicely for nagios """

    # key list for things to always display (for non-verbose)
    normal = ['Containers', 'Images', 'Dirs']

    # storage spot for performance line
    nstring = []

    # storage spot for verbose data line
    verb_line = []

    for k in docker_info:
        if k in normal:
            nstring.append("'{0}'={1}".format(k, docker_info[k]))
        else:
            verb_line.append("{0}: {1}".format(k, docker_info[k]))

    if verbose:
        return "docker running | {1}\n{0}".format(", ".join(verb_line),
                                                  " ".join(nstring))
    else:
        return "docker running | {0}".format(" ".join(nstring))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Nagios plugin for watching'
                                     ' docker socket and reporting performance'
                                     ' info.')

    parser.add_argument('-v', '--verbose', dest='verbosity',
                        default=0, action='store_true',
                        help='provides additional docker data')

    args = parser.parse_args()
    test_docker()
    docker_info = get_docker_info()
    ok(format_nagios_performance(docker_info, args.verbosity))
