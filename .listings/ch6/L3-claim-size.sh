mkdir work && cd work
mkdir -p hosts
for h in web01 web02 web03 db01 db02; do
  printf "service: running\n" > "hosts/$h.status"
done
printf "service: stopped\n" > hosts/db02.status
echo "== the check that was run =="
for h in web01 web02; do
  printf "%s: " "$h"; cat "hosts/$h.status"
done
echo "== the fleet the claim covers =="
ls hosts | wc -l
