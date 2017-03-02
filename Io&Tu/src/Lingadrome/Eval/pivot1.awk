BEGIN { cnt = 1 }
{ if (NR>1 && $1!="") {
    buf1[NR-1]=$1
    buf2[NR-1]=$2
    cnt = cnt + 1
    }
}
END {
  for (i = 1; i < cnt; i++) 
	printf "%s\t", buf1[i]
  print ""
  for (i = 1; i < cnt; i++) 
	printf "%s\t", buf2[i]
  print ""
}
