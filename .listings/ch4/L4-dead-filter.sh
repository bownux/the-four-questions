mkdir work && cd work
printf "2026-08-28 Error: disk nearly full\n2026-08-28 started ok\n" > service.log
grep "ERROR" service.log
echo "exit: $?"
grep -i "ERROR" service.log
echo "exit: $?"
