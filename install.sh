#!/usr/bin/env bash
set -e
 
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV="$DIR/.venv"
BIN="/usr/local/bin/eventhorizon"
 
command -v python3 >/dev/null || { echo "python3 not found."; exit 1; }
 
[ -x "$VENV/bin/pip" ] || python3 -m venv "$VENV"
 
[ -f "$DIR/requirements.txt" ] && "$VENV/bin/pip" install -q -r "$DIR/requirements.txt"
 
sudo tee "$BIN" > /dev/null << EOF
#!/usr/bin/env bash
exec "$VENV/bin/python" "$DIR/main.py" "\$@"
EOF
sudo chmod +x "$BIN"
 
echo "Installed. Run 'eventhorizon --help'."