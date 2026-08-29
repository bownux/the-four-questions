mkdir work && cd work
mkdir incoming
touch incoming/a.csv incoming/b.csv
find incoming -name "*.json"
echo "exit: $?"
find incoming -name "*.json" | wc -l
