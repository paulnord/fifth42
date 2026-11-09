import argparse
import host_probe as h
import speed_options
original_initialize=h.initialize
def initialize(source,cpus,variant):
    if variant=='reference':return original_initialize(source,cpus,'reference')
    if variant!='recommended':raise ValueError('Unknown recommended-path variant')
    return speed_options.initialize(source,cpus)
h.initialize=initialize
if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('--variant',choices=['reference','recommended'],required=True)
    a.add_argument('--width',type=int,default=8);a.add_argument('--patches',type=int,default=2048);a.add_argument('--first',type=int,default=0)
    a.add_argument('--ratio-num',type=int,default=3);a.add_argument('--ratio-den',type=int,default=10)
    a.add_argument('--workers',type=int,default=16);a.add_argument('--map-chunksize',type=int,default=8);a.add_argument('--output',required=True)
    h.trial(a.parse_args())
