mkdir work && cd work
printf "name,role,active\nalice,admin,true\nbob,viewer,false\ncarol,admin,false\n" > users.csv
echo "== count of admins (naive) =="
grep -c admin users.csv
echo "== count of ACTIVE admins (column-aware) =="
awk -F, '$2=="admin" && $3=="true"' users.csv | wc -l
