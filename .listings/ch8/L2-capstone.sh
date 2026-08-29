export TZ=UTC
mkdir work && cd work
mkdir -p release hosts/app01 hosts/app02 hosts/app03
printf "v2\n" > release/app.bin
cat > deploy.sh <<'SCRIPT'
#!/bin/sh
for h in app01 app02; do
  cp release/app.bin "hosts/$h/app.bin"
done
echo "warning: app03 unreachable, skipped" >&2
echo "Deploy complete: v2 on 3 hosts"
SCRIPT
chmod +x deploy.sh
./deploy.sh
echo "exit: $?"
echo "== health check as run by the operator =="
grep -l "v2" hosts/app01/app.bin
echo "exit: $?"
echo "== the denominator =="
ls hosts | wc -l
