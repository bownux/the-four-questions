mkdir work && cd work
printf "max_conn = 50\nlog_level = info\n" > server.conf
sed -i "s/max_connections = .*/max_connections = 200/" server.conf
echo "exit: $?"
cat server.conf
