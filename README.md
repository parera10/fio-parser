#Note: Only tested with fio version 3.x

# forked from mchad1/fio-parser

# fio-parser.py
This repository contains code used to parse fio normal output (as in non json)
As well as instructions for installing and running fio in both single and multi instance mode

usage: fio-parser.py [-h] [--directory DIRECTORY]

optional arguments:
  -h, --help            show this help message and exit
  --directory DIRECTORY, -d DIRECTORY
                        Specify the directory with fio output files to parse.
                        If none if provided, ./ is used

Output looks something like this

fio_file,operation,io_depth,reads,read_bw(MiB/s),read_lat(ms),writes,write_bw(MIB/s),write_lat(ms)
rand-read-vol-1-8k-randread-1,randread,1,2060,16.1,0.48451,,,
rand-read-vol-1-8k-randread-128,randread,128,2999,23.5,42.649910000000006,,,
rand-read-vol-1-8k-randread-16,randread,16,2999,23.4,5.33292,,,
rand-read-vol-1-8k-randread-2,randread,2,2999,23.4,0.6659299999999999,,,
rand-read-vol-1-8k-randread-256,randread,256,2999,23.5,85.23973,,,
rand-read-vol-1-8k-randread-32,randread,32,2999,23.4,10.66778,,,
rand-read-vol-1-8k-randread-4,randread,4,2999,23.4,1.33267,,,
rand-read-vol-1-8k-randread-64,randread,64,2999,23.4,21.332259999999998,,,
rand-read-vol-1-8k-randread-8,randread,8,2999,23.4,2.66603,,,
rand-write-vol-1-8k-randwrite-1,randwrite,1,,,,1313,10.3,0.7605599999999999
rand-write-vol-1-8k-randwrite-128,randwrite,128,,,,2998,23.5,42.65049
rand-write-vol-1-8k-randwrite-16,randwrite,16,,,,2999,23.4,5.33303
rand-write-vol-1-8k-randwrite-2,randwrite,2,,,,2515,19.6,0.79438
rand-write-vol-1-8k-randwrite-256,randwrite,256,,,,2998,23.5,85.24201
rand-write-vol-1-8k-randwrite-32,randwrite,32,,,,2998,23.4,10.668
rand-write-vol-1-8k-randwrite-4,randwrite,4,,,,2999,23.4,1.33267
rand-write-vol-1-8k-randwrite-64,randwrite,64,,,,2998,23.4,21.33459
rand-write-vol-1-8k-randwrite-8,randwrite,8,,,,2999,23.4,2.6660999999999997
seq-read-vol-1-64k-read-1,read,1,1199,74.0,0.83274,,,
seq-read-vol-1-64k-read-128,read,128,2049,128,62.389269999999996,,,
seq-read-vol-1-64k-read-16,read,16,2049,128,7.80324,,,
seq-read-vol-1-64k-read-2,read,2,2050,128,0.97476,,,
seq-read-vol-1-64k-read-256,read,256,2049,129,124.65,,,
seq-read-vol-1-64k-read-32,read,32,2049,128,15.60933,,,
seq-read-vol-1-64k-read-4,read,4,2050,128,1.9501300000000001,,,
seq-read-vol-1-64k-read-64,read,64,2049,128,31.21343,,,
seq-read-vol-1-64k-read-8,read,8,2050,128,3.9010100000000003,,,
seq-write-vol-1-64k-write-1,write,1,,,,886,55.4,1.12784
seq-write-vol-1-64k-write-128,write,128,,,,2049,128,62.39
seq-write-vol-1-64k-write-16,write,16,,,,2049,128,7.80307
seq-write-vol-1-64k-write-2,write,2,,,,1686,105,1.18495
seq-write-vol-1-64k-write-256,write,256,,,,2049,129,125.41
seq-write-vol-1-64k-write-32,write,32,,,,2049,128,15.60868
seq-write-vol-1-64k-write-4,write,4,,,,2050,128,1.9501300000000001
seq-write-vol-1-64k-write-64,write,64,,,,2049,128,31.21011
seq-write-vol-1-64k-write-8,write,8,,,,2050,128,3.90108


