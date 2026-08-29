mkdir work && cd work
printf "ok\n" > a.txt
printf "ok\n" > b.txt
for f in a.txt b.txt c.txt; do
  grep -q ok "$f" 2>/dev/null && echo "$f: valid" || echo "$f: INVALID"
done
echo "loop exit: $?"
