mkdir work && cd work
printf "retries = 3\n" > app.conf
printf "port = 8080\n" > net.conf
mkdir -p backup
cp app.conf net.conf backup/;  echo "copy exit:     $?"
ls backup
cmp -s app.conf backup/app.conf && cmp -s net.conf backup/net.conf
echo "read-back:     $?"
