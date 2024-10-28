with open("db.json", "rb") as f:
    content = f.read()

# Usuń BOM (pierwsze 3 bajty)
if content.startswith(b'\xef\xbb\xbf'):
    content = content[3:]

# Zapisz plik bez BOM
with open("db.json", "wb") as f:
    f.write(content)
