#!/usr/bin/env python
import pcap_to_log
import logs_to_csv
import csv_to_neo4j
import os

def pcap_to_clean_logs(data_dir, pcap):
    """
    Read in pcap that is located in data_dir and process
   through Bro container to crete Bro logs.
    Process Bro logs into clean csv files for import in noe4j.
    :param data_dir: Directory where pacp is located, relative
   to location of script.
    :param pcap: Filename of the pcap to run through Bro.
    :return: 0
    """
    # convert pcap into bro logs
    pcap_to_log.generate_logs(data_dir, pcap)
    # remove excess header and footer from each bro log
    logs = ["conn.log", "dns.log", "http.log"]
    for log in logs:
        pcap_to_log.clean_log(data_dir, log)
    return 0

def import_and_run_neo4j(data_dir):
    """
    Start the neo4j container, execute shell script on the
   container to import nodes and relationships created from
    Bro logs and then restart the neo4j container.
    :param data_dir: Directory that contains node and
   relationship csv's for import in neo4j
    :return: 0
    """
    csv_to_neo4j.start_neo4j(data_dir)
    csv_to_neo4j.run_import()
    csv_to_neo4j.restart_neo4j()
    return 0

def main():
    base_dir = os.getcwd()
    data_dir = os.path.join(base_dir, "data")
    pcap = "maccdc2012_00000.pcap"
    pcap_to_clean_logs(data_dir, pcap)
    logs_to_csv.create_nodes_relationships(data_dir)
    import_and_run_neo4j(data_dir)

if __name__ == '__main__':
    main()
