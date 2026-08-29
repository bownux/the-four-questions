mkdir work && cd work
bash -c 'nosuchcommand' 2>&1;    echo "not found:    $?"
printf '#!/bin/sh\necho hi\n' > script.sh
bash -c './script.sh' 2>&1;      echo "not runnable: $?"
timeout 1 sleep 5;               echo "timed out:    $?"
bash -c 'kill -TERM $$' 2>&1;    echo "terminated:   $?"
