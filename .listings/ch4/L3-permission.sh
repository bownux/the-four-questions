mkdir work && cd work
mkdir -p vault
touch vault/secrets.env
chmod 000 vault
find vault -name "*.env" 2>/dev/null
echo "quiet run exit: $?"
find vault -name "*.env"
echo "loud run exit:  $?"
chmod 755 vault
