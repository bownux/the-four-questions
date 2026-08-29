mkdir work && cd work
printf "retries = 3\ntimeout = 30\n" > app.conf
grep -n "timeout" app.conf;   echo "exit: $?"
grep -n "port" app.conf;      echo "exit: $?"
grep -n "port" missing.conf;  echo "exit: $?"
