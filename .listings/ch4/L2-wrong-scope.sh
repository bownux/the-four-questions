mkdir work && cd work
mkdir -p data/2026/08 data/2026/07
printf "2026-07-30 ERROR timeout\n" > data/2026/07/events.log
grep -rn "ERROR" data/2026/08
echo "exit: $?"
find data -type f
