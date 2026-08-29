mkdir work && cd work
cat > report.py <<'SCRIPT'
import os
print("result: 42")
os._exit(0)
SCRIPT
python3 report.py | cat
echo "exit: $?"
python3 -u report.py | cat
echo "exit: $?"
