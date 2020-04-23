#!/usr/bin/env python

from datetime import datetime
import os
import socket
import csv
import elasticsearch
import elasticsearch.helpers
import elasticsearch.exceptions
import time

hostname = socket.gethostname()

es = elasticsearch.Elasticsearch([{'host': 'effie.laureateinstitute.org'}])

#MAPPING DEFINITION
#scan_name
#num_workers
#read_percent
#block size
#iodepth
#buffered
#direct
#time
#if latency log
##latency in usecs
#elif bandwidth log
##KB/sec
#elif iops log
##iops
#direction
##0 READ
##1 WRITE
##2 TRIM
#io size
request_body = {
            'settings': {
                'index.number_of_shards' : 200,
            },
	    'mappings': {
	        'fio_benchmarks': {
	            'properties': {
	                'name': {'type': 'text'},
                        'host': {'type': 'text'},
                        'num_workers': {'type': 'integer'},
                        'read_percent': {'type': 'integer'},
                        'block_size': {'type': 'keyword'},
                        'io_depth': {'type': 'integer'},
                        'buffered': {'type': 'boolean'},
                        'direct': {'type': 'boolean'},
                        'worker_id': {'type': 'integer'},
                        'data_type': {'type': 'keyword'},
                        'time': {'type': 'integer'},
                        'log_data': {'type': 'long'},
                        'direction': {'type': 'keyword'},
                        'data_size': {'type': 'integer'}
	            }}}
	}
print 'creating fio_benchmarks_index index...'

if not es.indices.exists('fio_benchmarks_index'):
    es.indices.create(index = 'fio_benchmarks_index', body = request_body)
else:
    print 'index already exists'

total_files = 0
for root, dirs, files in os.walk('.', topdown=False):
    for name in files:
        if name != 'benchmark.log' and name.endswith('.log'):
            total_files += 1

time.sleep(10)

progress = 0
for root, dirs, files in os.walk('.', topdown=False):
    for name in files:
        if name != 'benchmark.log' and name.endswith('.log'):
            with open(os.path.join(root, name), 'rb') as log_file:
                logreader = csv.reader(log_file)
                documents = []

                for line in logreader:
                    document = {}
                    document['doc'] = {}
                    document['_type'] = 'fio_benchmarks'
                    document['_index'] = 'fio_benchmarks_index'
                    document['doc']['name'] = name
                    document['doc']['host'] = hostname

                    split_name = name.split('_')
                    document['doc']['num_workers'] = int(split_name[0])
                    document['doc']['read_percent'] = int(split_name[1])
                    document['doc']['block_size'] = split_name[2]
                    document['doc']['io_depth'] = split_name[3]
                    if split_name[4] == 'buffered':
                        document['doc']['buffered'] = True
                        document['doc']['direct'] = False
                    else:
                        document['doc']['buffered'] = False
                        document['doc']['direct'] = True

                    split_name = name.split('.')
                    document['doc']['worker_id'] = split_name[2]

                    if 'bw' in name:
                        document['doc']['data_type'] = 'bw'
                    elif 'iops' in name:
                        document['doc']['data_type'] = 'iops'
                    elif 'clat' in name:
                        document['doc']['data_type'] = 'clat'
                    elif 'slat' in name:
                        document['doc']['data_type'] = 'slat'

                    document['doc']['time'] = int(line[0].replace(' ', '').replace('\t', ''))
                    document['doc']['log_data'] = int(line[1].replace(' ', '').replace('\t', ''))

                    if line[2].replace(' ', '').replace('\t', '') == '0':
                        document['doc']['direction'] = 'read'
                    elif line[2].replace(' ', '').replace('\t', '') == '1':
                        document['doc']['direction'] = 'write'
                    elif line[2].replace(' ', '').replace('\t', '') == '2':
                        document['doc']['direction'] = 'trim'

                    document['doc']['data_size'] = int(line[3].replace(' ', '').replace('\t', ''))

                    documents.append(document)

                success = False

                while not success:
                    try:
                        resp = elasticsearch.helpers.bulk(es, documents)
                        progress += 1
                        print 'progress %d/%d -- %f percent' % (progress, total_files, ((float(progress)/float(total_files))*100.0))
                        success = True
                    except elasticsearch.exceptions.ConnectionTimeout:
                        time.sleep(10)
                        print 'retrying'
                    except elasticsearch.helpers.BulkIndexError:
                        time.sleep(10)
                        print 'retrying'
#1_0_128k_1_buffered_bw.results_bw.1.log      1_0_128k_1_buffered_lat.results_clat.1.log   1_0_128k_1_buffered_lat.results_slat.1.log
#1_0_128k_1_buffered_iops.results_iops.1.log  1_0_128k_1_buffered_lat.results_lat.1.log


#res = es.index(index="test-index", doc_type='tweet', id=1, body=doc)


#
#doc = {
#    'author': 'kimchy',
#    'text': 'Elasticsearch: cool. bonsai cool.',
#    'timestamp': datetime.now(),
#}
#print(res['result'])
#
#res = es.get(index="test-index", doc_type='tweet', id=1)
#print(res['_source'])
#
#es.indices.refresh(index="test-index")
#
#res = es.search(index="test-index", body={"query": {"match_all": {}}})
#print("Got %d Hits:" % res['hits']['total'])
#for hit in res['hits']['hits']:
#    print("%(timestamp)s %(author)s: %(text)s" % hit["_source"])
