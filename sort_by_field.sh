#!/usr/bin/env bash

_help() {
  echo "Usage: $(basename "$0") FILE FIELD_TO_ORDER_BY DELIMITER OUTPUT_DIR(default .)"
}

if [[ ${#} -lt 3 ]]; then
  _help
  exit 1
fi

file="${1}"
field="${2}"
delimiter="${3}"
output_dir="${4:-"."}"

if [[ ! -f "${file}" ]]; then
  echo "${file} does not exist"
  exit 1
fi 
if [[ ! -d "${output_dir}" ]]; then
  echo "${output_dir} does not exit"
  exit 1
fi

header="$(head -n1 "${file}")"

for test_name in rand-read rand-rw-25 rand-rw-75 rand-write seq-read seq-write; do 
  for volume in cvs-extreme cvs-premium cvs-standard ebs efs; do
    prefix="${test_name}-${volume}-"
    output="${output_dir}/${prefix}sorted.csv"
    echo "${header}" > "${output}"
    grep "${prefix}" "${file}" | sort -k "${field}" -n -t "${delimiter}" >> "${output}"
  done
done