mkdir work && cd work
mkdir -p src backup
printf "a\n" > src/one.txt
printf "b\n" > src/two.txt
printf "c\n" > src/three.txt
cat > backup.sh <<'SCRIPT'
#!/bin/sh
cp src/one.txt backup/
cp src/two.txt backup/
echo "Backup complete: 3 files copied to backup/"
SCRIPT
chmod +x backup.sh
./backup.sh
echo "exit: $?"
echo "--- what the directory holds ---"
ls backup
ls backup | wc -l
