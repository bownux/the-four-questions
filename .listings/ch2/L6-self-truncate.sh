mkdir work && cd work
printf "beta\nalpha\ngamma\n" > data.txt
echo "before: $(wc -l < data.txt) lines"
sort data.txt > data.txt
echo "sort exit: $?"
echo "after:  $(wc -l < data.txt) lines"
cat data.txt
echo "(nothing above this line is the file's remaining content)"
