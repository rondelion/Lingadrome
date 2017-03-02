#!/bin/sh
for filepath in `find ${1} -type d -depth 1`
do
  echo $filepath
  python MInfo.py ${filepath}/llog.txt 1600 S mode
  python MInfo.py ${filepath}/llog.txt 1600 S llAction mode:act
  python MInfo.py ${filepath}/llog.txt 1600 S luAction mode:react
  python MInfo.py ${filepath}/llog.txt 1600 V mode
  python MInfo.py ${filepath}/llog.txt 1600 V llAction mode:act
  python MInfo.py ${filepath}/llog.txt 1600 V luAction mode:react
  python MInfo.py ${filepath}/llog.txt 1600 A luWord1
  python MInfo.py ${filepath}/llog.txt 1600 A luWord2
done