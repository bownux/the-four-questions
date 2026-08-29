mkdir work && cd work
cat > response.json <<'JSON'
{"status": "error", "message": "quota exceeded", "records": [], "expires": null}
JSON
echo "== well-formed? =="
python3 -m json.tool response.json > /dev/null; echo "parse exit: $?"
echo "== what a naive extraction reports =="
python3 -c '
import json
d = json.load(open("response.json"))
print("records returned:", len(d["records"]))
print("expires:", d.get("expires"))
print("renewed:", d.get("renewed"))
print("expires present?", "expires" in d, " renewed present?", "renewed" in d)
print("status:", d["status"], "-", d["message"])
'
