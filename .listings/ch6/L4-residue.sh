mkdir work && cd work
mkdir -p src backup
printf "a\n" > src/one.txt
printf "b\n" > src/two.txt
cp src/one.txt src/two.txt backup/
echo "copy exit: $?"
echo "== residue a true backup claim leaves =="
ls backup
echo "files in src:    $(ls src | wc -l)"
echo "files in backup: $(ls backup | wc -l)"
diff -r src backup > /dev/null; echo "trees identical (diff exit): $?"
