#!/bin/sh

job_dir_path=/tmp/siddharth_test_1/methane_test_opt_1
cd $job_dir_path

unset HOSTS_FILE
export TURBODIR=/soft/vanka/TURBOMOLE/TURBOMOLE_6_4/TURBOMOLE
export PATH=$TURBODIR/scripts:$PATH
export PARA_ARCH=MPI
export PATH=$TURBODIR/bin/x86_64-unknown-linux-gnu/:$PATH
export MPI_IC_ORDER="TCP"
export PARNODES=12

NumForce -ri -mfile file > NumForce.out &
