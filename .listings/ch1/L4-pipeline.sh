mkdir work && cd work
printf "one\ntwo\nthree\n" > lines.txt
grep zebra lines.txt | wc -l;  echo "pipeline exit: $?"
grep zebra lines.txt | wc -l;  echo "PIPESTATUS: ${PIPESTATUS[@]}"
set -o pipefail
grep zebra lines.txt | wc -l;  echo "with pipefail: $?"
