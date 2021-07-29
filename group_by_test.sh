#!/usr/bin/env bash

_help() {
  echo "Usage: $(basename "$0") DIR(default .)"
}

[[ ${#} -ge 3 ]] || ( _help && exit 1 )

dir="${1:-"."}"
delimiter=";"

[[ -d "${dir}" ]] || ( echo "${output_dir} does not exit" && exit 1 )

iodepth=(1 2 4 8 16 32 64 128 256)
index=0
for test_name in rand-read rand-rw-25 rand-rw-75 rand-write seq-read seq-write; do
  echo "iodepth;cvs-extreme,cvs-premium,cvs-standard,ebs,efs" > "${dir}/${test_name}.csv"
  str_line="${iodepth[i]}"
  for volume in cvs-extreme cvs-premium cvs-standard ebs efs; do
    str_line="${str_line};"
    
  done
done