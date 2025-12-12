for b in (git branch --format="%(refname:short)")
    echo "=== Pulling $b ==="
    git checkout $b
    git pull
end