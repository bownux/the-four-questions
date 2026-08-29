export TZ=UTC
mkdir work && cd work
printf "v2\n" > artifact.txt
touch -d "2026-08-29 03:27:10" artifact.txt
stat -c "%n  size=%s  modified=%y" artifact.txt
echo "exit: $?"
