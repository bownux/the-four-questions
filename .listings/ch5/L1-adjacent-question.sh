mkdir work && cd work
mkdir -p etc docs
printf "listen_port = 9090\n" > etc/service.conf
printf "The service listens on port 8080 by default.\n" > docs/README.txt
echo "== the question: is the service configured for port 8080? =="
grep -rn "8080" .
echo "exit: $?"
