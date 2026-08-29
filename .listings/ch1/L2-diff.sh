mkdir work && cd work
printf "a\nb\n" > one.txt
cp one.txt two.txt
diff one.txt two.txt; echo "same:    $?"
printf "a\nB\n" > two.txt
diff one.txt two.txt; echo "differ:  $?"
diff one.txt three.txt; echo "trouble: $?"
