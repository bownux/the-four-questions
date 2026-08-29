mkdir work && cd work
printf "retries = 3\n" > app.conf
printf "port = 8080\n" > net.conf
cp app.conf backup;  echo "first copy:  $?"
cp net.conf backup;  echo "second copy: $?"
ls
cat backup
