#!/usr/bin/env bash
#yum install -y fio
apt-get install -y fio

python ssd_bench_generator.py > ssd_bench.sh
sh -x ssd_bench.sh 2>&1 | tee `pwd`/benchmark.log
