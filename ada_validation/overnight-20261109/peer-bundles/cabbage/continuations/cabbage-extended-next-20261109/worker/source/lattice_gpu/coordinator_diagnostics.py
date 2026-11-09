#!/usr/bin/env python3
"""Serial scratch profiling and serialized-payload diagnostic, not timed trials."""
import argparse
import cProfile
import io
import json
from pathlib import Path
import pickle
import pstats
import statistics
import time

import coordinator_pipeline as pipeline
import overnight_search as night


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source',type=Path,default=Path(__file__).resolve().parents[1]/'lattice_prototype')
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    night.initialize(args.source.resolve())
    window=pipeline.Window(100_000_000_001,200_000_000_000,3751385984,3751386240,bits=222)
    specs=window.specifications()
    profile=cProfile.Profile()
    profile.enable()
    fused=[pipeline.prepare_certified(spec) for spec in specs]
    profile.disable()
    text=io.StringIO()
    pstats.Stats(profile,stream=text).sort_stats('tottime').print_stats(30)
    # Isolate primitive argument/result payloads. Real Pool framing/chunk headers
    # differ, so these bytes are not advertised as measured IPC transport bytes.
    tasks=[r[0] for r in fused]
    prepared=[(r[0],r[2][0],r[2][1]) for r in fused]
    certified=[(r[1],r[2][2],r[2][3]) for r in fused]
    packets={'baseline':(specs,prepared,tasks,certified),'fused':(specs,fused)}
    timings={}
    for mode,values in packets.items():
        samples=[]
        for _ in range(21):
            start=time.perf_counter()
            buffers=[pickle.dumps(value) for value in values]
            for blob in buffers:pickle.loads(blob)
            samples.append(time.perf_counter()-start)
        timings[mode]=dict(payload_pickle_bytes=sum(len(blob) for blob in buffers),
                          encode_decode_median_seconds=statistics.median(samples))
    args.output.mkdir(parents=True,exist_ok=False)
    (args.output/'profile.txt').write_text(text.getvalue())
    (args.output/'payloads.json').write_text(json.dumps(dict(window=window.identity(),metrics=timings,
        note='Serial diagnostic only. Payload serialization excludes multiprocessing framing and is not actual IPC latency.'),indent=2)+'\n')


if __name__=='__main__':main()
