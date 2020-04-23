#!/usr/bin/env python

# job_counts = [1, 4, 8]
# read_percents = [100, 60, 40, 20]
# block_sizes = ['4k', '16k', '128k', '512k', '1M', '4M']
# io_depths = [1, 8, 16, 32, 64, 128]

job_counts = [4]
read_percents = [60]
block_sizes = ['1M']
io_depths = [16]

base_command = 'fio --ioengine=libaio --invalidate=1 --ramp_time=5 --size=10GB --runtime=30 --time_based --filename=/mnt/ssd/fio-10g'

print 'mkdir results'
print 'cd results'
print 'basedir=`pwd`'

for job_count in job_counts:
    for read_percent in read_percents:
        for block_size in block_sizes:
            for io_depth in io_depths:
                print 'mkdir -p %d/%d/%s/%d/direct' % (job_count, read_percent, block_size, io_depth)
                print 'mkdir -p %d/%d/%s/%d/buffered' % (job_count, read_percent, block_size, io_depth)

                if read_percent == 100:
                    print 'mkdir -p %d/0/%s/%d/direct' % (job_count, block_size, io_depth)
                    print 'mkdir -p %d/0/%s/%d/buffered' % (job_count, block_size, io_depth)


for job_count in job_counts:
    for read_percent in read_percents:
        for block_size in block_sizes:
            for io_depth in io_depths:
                if read_percent == 100:
                    #100% read
                    print 'cd %d/%d/%s/%d/direct' % (job_count, read_percent, block_size, io_depth)
                    print '%s --name=%d_%d_%s_%d_direct --direct=1 --sync=1 --numjobs=%d --iodepth=%d --bs=%s --rw=randread --write_bw_log=%d_%d_%s_%d_direct_bw.results --write_iops_log=%d_%d_%s_%d_direct_iops.results --write_lat_log=%d_%d_%s_%d_direct_lat.results' % (base_command, job_count, read_percent, block_size, io_depth, job_count, io_depth, block_size, job_count, read_percent, block_size, io_depth, job_count, read_percent, block_size, io_depth, job_count, read_percent, block_size, io_depth)
                    print 'cd $basedir'

                    print 'cd %d/%d/%s/%d/buffered' % (job_count, read_percent, block_size, io_depth)
                    print '%s --name=%d_%d_%s_%d_buffered --numjobs=%d --iodepth=%d --bs=%s --rw=randread --write_bw_log=%d_%d_%s_%d_buffered_bw.results --write_iops_log=%d_%d_%s_%d_buffered_iops.results --write_lat_log=%d_%d_%s_%d_buffered_lat.results' % (base_command, job_count, read_percent, block_size, io_depth, job_count, io_depth, block_size, job_count, read_percent, block_size, io_depth, job_count, read_percent, block_size, io_depth, job_count, read_percent, block_size, io_depth)
                    print 'cd $basedir'


                    #0% read
                    print 'cd %d/0/%s/%d/direct' % (job_count, block_size, io_depth)
                    print '%s --name=%d_0_%s_%d_direct --direct=1 --sync=1 --numjobs=%d --iodepth=%d --bs=%s --rw=randwrite --write_bw_log=%d_0_%s_%d_direct_bw.results --write_iops_log=%d_0_%s_%d_direct_iops.results --write_lat_log=%d_0_%s_%d_direct_lat.results' % (base_command, job_count, block_size, io_depth, job_count, io_depth, block_size, job_count, block_size, io_depth, job_count, block_size, io_depth, job_count, block_size, io_depth)
                    print 'cd $basedir'

                    print 'cd %d/0/%s/%d/buffered' % (job_count, block_size, io_depth)
                    print '%s --name=%d_0_%s_%d_buffered --numjobs=%d --iodepth=%d --bs=%s --rw=randwrite --write_bw_log=%d_0_%s_%d_buffered_bw.results --write_iops_log=%d_0_%s_%d_buffered_iops.results --write_lat_log=%d_0_%s_%d_buffered_lat.results' % (base_command, job_count, block_size, io_depth, job_count, io_depth, block_size, job_count, block_size, io_depth, job_count, block_size, io_depth, job_count, block_size, io_depth)
                    print 'cd $basedir'
                else:
                    print 'cd %d/%d/%s/%d/direct' % (job_count, read_percent, block_size, io_depth)
                    print '%s --name=%d_%d_%s_%d_direct --direct=1 --sync=1 --numjobs=%d --iodepth=%d --bs=%s --rw=randrw --rwmixread=%d --write_bw_log=%d_%d_%s_%d_direct_bw.results --write_iops_log=%d_%d_%s_%d_direct_iops.results --write_lat_log=%d_%d_%s_%d_direct_lat.results' % (base_command, job_count, read_percent, block_size, io_depth, job_count, io_depth, block_size, read_percent, job_count, read_percent, block_size, io_depth, job_count, read_percent, block_size, io_depth, job_count, read_percent, block_size, io_depth)
                    print 'cd $basedir'


                    print 'cd %d/%d/%s/%d/buffered' % (job_count, read_percent, block_size, io_depth)
                    print '%s --name=%d_%d_%s_%d_buffered --numjobs=%d --iodepth=%d --bs=%s --rw=randrw --rwmixread=%d --write_bw_log=%d_%d_%s_%d_buffered_bw.results --write_iops_log=%d_%d_%s_%d_buffered_iops.results --write_lat_log=%d_%d_%s_%d_buffered_lat.results' % (base_command, job_count, read_percent, block_size, io_depth, job_count, io_depth, block_size, read_percent, job_count, read_percent, block_size, io_depth, job_count, read_percent, block_size, io_depth, job_count, read_percent, block_size, io_depth)
                    print 'cd $basedir'

print 'cd ..'
