#!/usr/bin/env fish

# Pastikan berada di folder repository
echo "Repository: "(pwd)
echo "=============== START PULL ALL BRANCH ==============="

for b in (git branch --format="%(refname:short)")
    echo "=== Switching to $b ==="
    git checkout $b
    echo "=== Pulling $b ==="
    git pull
end

echo "=============== DONE ==============="
