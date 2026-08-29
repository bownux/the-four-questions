mkdir work && cd work
cat > timed.log <<'LOG'
2026-08-28T10:00:00Z INFO boot
2026-08-28T10:05:00Z ERROR disk
2026-08-29T01:00:00Z INFO ok
LOG
wc -l < timed.log
echo "exit: $?"
tail -1 timed.log
echo "exit: $?"
