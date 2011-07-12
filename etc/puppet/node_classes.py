#!/bin/env python
import json
import os

ROOT = os.path.dirname(__file__)


def main(hostname):
  hostfile = os.path.join(ROOT, 'hosts', hostname)
  host_info = json.load(open(hostfile))
  cluster = host_info['options'].get('cluster')
  clusterfile = os.path.join(ROOT, 'clusters', cluster)
  cluster_info = json.load(open(clusterfile))

  options = cluster_info.get('options', {}).copy()
  options.update(host_info.get('options', {}))

  classes = cluster_info.get('classes', [])[:]
  classes.extend(host_info.get('classes', []))

  print json.dumps({'options': options, 'classes': list(set(classes))})


if __name__ == '__main__':
  import sys
  main(sys.argv[1])
