mkdir work && cd work
printf '#!/bin/sh\nsleep 5\n' > svc.sh
chmod +x svc.sh
./svc.sh > /dev/null 2>&1 & SVC=$!
sleep 1
echo "== while the service runs =="
ps ax -o args= | grep "svc.sh"
echo "match count: $(ps ax -o args= | grep -c "svc.sh")"
kill "$SVC" 2>/dev/null; wait "$SVC" 2>/dev/null
echo "== after the service is stopped =="
ps ax -o args= | grep "svc.sh"
echo "match count: $(ps ax -o args= | grep -c "svc.sh")"
pgrep -f "svc.sh" > /dev/null; echo "pgrep exit: $?"
