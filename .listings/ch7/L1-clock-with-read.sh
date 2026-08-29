export TZ=UTC
mkdir work && cd work
: > artifact.txt
echo "== a read with no clock in the capture =="
cat artifact.txt
echo "exit: $?"
echo "== the same read, with the clock captured beside it =="
NOW=$(date +%s)
MTIME=$(stat -c %Y artifact.txt)
echo "age of the observation at capture: $((NOW - MTIME)) seconds"
