export TZ=UTC
mkdir work && cd work
printf "2026-08-29T09:58:00Z ERROR upstream refused\n" > app.log
echo "== the incident window's evidence, before rotation =="
grep -c ERROR app.log
mv app.log app.log.1
: > app.log
echo "== the same command, run after rotation =="
grep -c ERROR app.log
echo "exit: $?"
echo "== what the directory holds =="
ls
wc -c app.log app.log.1
