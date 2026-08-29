export TZ=UTC
mkdir work && cd work
mkdir -p srv
printf "version 1.9\n" > srv/app.txt
touch -d "2026-08-29 03:00:00" srv/app.txt
echo "== the evidence the operator showed =="
stat -c "%n  size=%s  modified=%y" srv/app.txt
echo "== the evidence the operator did not show =="
cat srv/app.txt
