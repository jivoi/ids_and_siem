#!/usr/bin/env python
from subprocess import Popen, PIPE
import os
import time

def start_neo4j(data_dir):
    print("Starting neo4j container...")
    volume = os.path.join(data_dir, ':/var/lib/neo4j/import')
    p = Popen(['docker', 'run', '--publish=7474:7474', '--publish=7687:7687',
               '-v', volume, '--name', 'neo4bro', '-d', 'neo4j'], stdout=PIPE)
    out = p.stdout.read()
    print("neo4j container running")
    time.sleep(5)
    return 0

def run_import():
    print("Importing nodes and relationships into neo4j...")
    p = Popen(['docker', 'exec', 'neo4bro', '/bin/bash',
               '/var/lib/neo4j/import/import_connection.sh'],
              stdout=PIPE)
    out = p.stdout.read()
    print("Import complete")
    return 0

def restart_neo4j():
    print("Restarting neo4j container...")
    p = Popen(['docker', 'restart', 'neo4bro'], stdout=PIPE)
    out = p.stdout.read()
    print("neo4j container restarted")

def main():
    base_dir = os.getcwd()
    data_dir = os.path.join(base_dir, "data")
    start_neo4j(data_dir)
    run_import()
    restart_neo4j()

if __name__ == "__main__":
    main()
