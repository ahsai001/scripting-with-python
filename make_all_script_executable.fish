#!/usr/bin/env fish

# Dapatkan direktori lokasi script saat ini
set SCRIPT_DIR (dirname (status --current-filename))

echo "=== Fixing files in: $SCRIPT_DIR ==="

# Loop semua file di folder yang sama
for f in $SCRIPT_DIR/*
    if test -f "$f"
        echo "Processing: $f"

        # ---- Remove CRLF ----
        # Mac & Linux sama-sama valid pakai format ini
        sed -i '' -e 's/\r$//' "$f"

        # ---- Set executable ----
        chmod +x "$f"

        echo "Fixed: $f"
    end
end

echo "=== DONE ==="
