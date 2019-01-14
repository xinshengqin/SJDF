#!/bin/bash
export SJDF_TOPODIR="../../topo"
export SJDF_DTOPODIR="../../dtopo"
export OMP_NUM_THREADS=80
for i in $(seq 0 10); do
    # pad zeros to case id
    printf -v case_name "%06d" $i
    echo "work on case ${case_name}"
    case_dir="run_${case_name}"
    export SJDF_CASEID=${case_name} 

    cp -r template ${case_dir} && cd ${case_dir}
    nice -7 make .plots 2>&1 | tee run.log
    cd ../
done
