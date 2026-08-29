mkdir work && cd work
cat > convert.sh <<'SCRIPT'
#!/bin/sh
echo "warning: input has no header row" >&2
echo "converted 14 records"
SCRIPT
chmod +x convert.sh
./convert.sh 2>/dev/null
echo "--- without the commentary channel: the line above is all you see"
./convert.sh 2>&1
echo "exit: $?"
