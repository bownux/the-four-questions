mkdir work && cd work
mkdir logs
for i in 1 2 3 4 5 6 7 8 9 10 11 12; do
  printf "2026-08-29 request %02d handled\n" "$i" >> logs/app.log
done
printf "2026-08-29 ERROR upstream refused\n" >> logs/app.log
head -5 logs/app.log
echo "--- head -5 above; wc -l below ---"
wc -l < logs/app.log
