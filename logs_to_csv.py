#!/usr/bin/env python
from subprocess import Popen, PIPE
import os
import re

def generate_logs(pcap_dir, pcap):
    """
    Process PCAP through a Bro container
    :param pcap_dir: Full directory path to location of PCAP
    :param pcap: PCAP filename
    :return: 0
    """
    volume = os.path.join(pcap_dir, ':/pcap:rw')
    container_name = 'bro'
    print("Starting bro container to process {}".format(pcap))
    print("NOTE: This can take some time depending on size of pcap")
    print("NOTE: bro will display Errors in screen")
    print("\n")
    p = Popen(['docker', 'run', '--rm', '--name',
               container_name,
               '-v', volume, 'blacktop/bro', '-r', pcap,
               'local'],
              stdout=PIPE)
    out = p.stdout.read()
    print("\n")
    print("{} processed.".format(pcap))
    print("\n")
    return 0

def clean_log(log_dir, filename):
    """
    Removes excess header and footer information from Bro logs
   to support import as CSV
    :param log_dir: Path to log files
    :param filename: Filename of log file
    :return: 0
    """
    print("Cleaning {}".format(filename))
    log_file = os.path.join(log_dir, filename)
    clean_file = os.path.join(log_dir, filename + '.clean')
    with open(log_file) as original:
        lines = original.readlines()
    with open(clean_file, 'w') as cleaned:
        cleaned.writelines(lines[6][8:])
        cleaned.writelines(lines[9:-1])
    # this is to fix errors in http log due to random " in some
    # of the User Agent strings
    if filename == "http.log":
        with open(clean_file, "r") as sources:
            lines = sources.readlines()
        with open(clean_file, "w") as sources:
            for line in lines:
                sources.write(re.sub(r'\t"', '\t', line))
    return 0

def main():
    base_dir = os.getcwd()
    data_dir = os.path.join(base_dir, "data")
    pcap = 'maccdc2012_00000.pcap'
    logs = ['conn.log', 'dns.log', 'http.log']
    # convert pcap into bro logs
    generate_logs(data_dir, pcap)
    # remove excess header and footer from each bro log
    for log in logs:
        clean_log(data_dir, log)

if __name__ == '__main__':
    main()
