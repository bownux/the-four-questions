mkdir work && cd work
mkdir logs && touch logs/a.log logs/b.log logs/c.tmp
find logs -name "*.temp" -delete
echo "exit: $?"
ls logs
