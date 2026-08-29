mkdir work && cd work
cat > steps.py <<'SCRIPT'
import sys
print("step 1 done")
print("note: step 2 used the fallback path", file=sys.stderr)
print("step 2 done")
print("step 3 done")
SCRIPT
python3 steps.py 2>&1 | cat
