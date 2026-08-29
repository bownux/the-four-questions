mkdir work && cd work
printf "level = ERROR\n" > a.conf
grep -n "ERROR" a.conf missing.conf
echo "exit: $?"
