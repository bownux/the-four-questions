mkdir work && cd work
: > app.log
grep "ERROR" app.log
echo "exit: $?"
wc -c app.log
