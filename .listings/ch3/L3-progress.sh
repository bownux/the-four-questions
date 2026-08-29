mkdir work && cd work
cat > fetch.sh <<'SCRIPT'
#!/bin/sh
echo "fetching 1/3..." >&2
echo "fetching 2/3..." >&2
echo "fetching 3/3..." >&2
echo '{"status": "complete", "items": 3}'
SCRIPT
chmod +x fetch.sh
./fetch.sh > result.json 2> progress.log
echo "exit: $?"
cat result.json
cat progress.log
