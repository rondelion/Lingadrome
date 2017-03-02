#!/bin/sh
for filepath in `find ${1} -type d -depth 1`
do
  echo $filepath
  awk -f pivot1.awk ${filepath}/${2} > ${filepath}/pivot.txt
done
