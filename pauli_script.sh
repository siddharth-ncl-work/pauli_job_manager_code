#!/bin/bash

keep_running=yes

job_list="
/tmp/siddharth_test_1/rand_mol_1_test_opt_1
/tmp/siddharth_test_1/rand_mol_1_test_num_1
/tmp/siddharth_test_1/benzene_test_opt_1
/tmp/siddharth_test_1/benzene_test_num_1
/tmp/siddharth_test_1/rand_mol_2_test_opt_1
/tmp/siddharth_test_1/rand_mol_2_test_num_1
/tmp/siddharth_test_1/butane_test_opt_1
/tmp/siddharth_test_1/butane_test_opt_1
/tmp/siddharth_test_1/rand_mol_3_test_opt_1
/tmp/siddharth_test_1/rand_mol_3_test_num_1
/tmp/siddharth_test_1/rand_mol_4_test_opt_1
/tmp/siddharth_test_1/rand_mol_4_test_num_1
/tmp/siddharth_test_1/cacl2_test_opt_1
/tmp/siddharth_test_1/cacl2_test_opt_1
/tmp/siddharth_test_1/rand_mol_5_test_opt_1
/tmp/siddharth_test_1/rand_mol_5_test_num_1
/tmp/siddharth_test_1/methane_test_opt_1
/tmp/siddharth_test_1/methane_test_opt_1
"

job_type="
opt
numforce
opt
numforce
opt
numforce
opt
numforce
opt
numforce
opt
numforce
opt
numforce
opt
numforce
opt
numforce
"


###################################***DO NOT MODIFY BELOW THIS LINE***##########################################
code_dir_path='core_code'
cd $code_dir_path
is_running=$(python source/check_running_code.py check)
if [ $is_running == 'True' ]
then
  python source/check_running_code.py info
  tail output/output.log
elif [ $is_running == 'False' ]
then
  job_count=$(python source/get_job_count.py $job_list)
  echo 'TOTAL JOBS = '$job_count
  nohup python -u manager.py $keep_running $job_count $job_list $job_type | tee output/output.log &
fi

#waiting for working status from others
