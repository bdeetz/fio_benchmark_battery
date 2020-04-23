#!/usr/bin/env python

job_counts = [1]
read_percents = [60]
block_sizes = ['1M']
io_depths = [16]
num_devices = 24
file_size = "5GB"

devices = []
for i in range(0, num_devices):
    device_prefix = "sd"
    device_suffix = chr(ord("f") + i)
    
    if not device_suffix.isalpha():
        i = i - 21
        device_prefix = "sda"
        device_suffix = chr(ord("a") + i)
        
    devices.append('%s%s' % (device_prefix, device_suffix))

base_command = 'fio --ioengine=libaio --invalidate=1 --ramp_time=5 --size=%s --runtime=600 --time_based' % (file_size)
print('#!/usr/bin/env bash')
print('mkdir results')
print('cd results')
print('basedir=`pwd`')

for job_count in job_counts:
    for read_percent in read_percents:
        for block_size in block_sizes:
            for io_depth in io_depths:
                for device in devices:
                    print('mkdir -p %s/%d/%d/%s/%d/direct' % (device, job_count, read_percent, block_size, io_depth))


for job_count in job_counts:
    for read_percent in read_percents:
        for block_size in block_sizes:
            for io_depth in io_depths:
                print('pids=()')
                for device in devices:
                    print('cd %s/%d/%d/%s/%d/direct' % (device, job_count, read_percent, block_size, io_depth))
                    print('%s --filename=/mnt/%s/fio-5g --name=%d_%d_%s_%d_direct --direct=1 --sync=1 --numjobs=%d --iodepth=%d --bs=%s --rw=randrw --rwmixread=%d --write_bw_log=%d_%d_%s_%d_direct_bw.results --write_iops_log=%d_%d_%s_%d_direct_iops.results --write_lat_log=%d_%d_%s_%d_direct_lat.results&' % (base_command, device, job_count, read_percent, block_size, io_depth, job_count, io_depth, block_size, read_percent, job_count, read_percent, block_size, io_depth, job_count, read_percent, block_size, io_depth, job_count, read_percent, block_size, io_depth))
                    print('pids+=($?)')
                    print('cd $basedir')
                    
                print('pids=()')

                print('for pid in ${pids[@]}')
                print('do')
                print('    ret=`kill -0 ${pid}`')	
                print('    while [[ ${ret} -ne 0 ]]')
                print('    do')
                print('        sleep 1')
                print('        ret=`kill -0 ${pid}`')
                print('    done')
                print('done')

print('cd ..')
