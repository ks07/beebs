BEGIN {
   OFS="\t"
}
{
  row[$1,$2]=$3
  if (!($2 in f2)) { header=(header)?header OFS $2:$2;f2[$2]}
  if (col1[c]!=$1)
     col1[++c]=$1
}
END {
  printf("%*s%s\n", length(col1[1])+2, " ",header)
  ncol=split(header,colA,OFS)
  for(i=1;i<=c;i++) {
    printf("%s", col1[i])
    for(j=1;j<=ncol;j++)
      printf("%s%s%c", OFS, row[col1[i],colA[j]], (j==ncol)?ORS:"")
  }
}
