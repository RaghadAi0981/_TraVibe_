#!/bin/bash
# gitpush.sh — Add, commit, and push in one go

if [ -z "$1" ]; then
  echo "Usage: $0 \"commit message\""
  exit 1
fi

git add .
git commit -m "$1"
git push
# chmod +x gitpush.sh
# ./gitpush.sh "Your commit message"    
    