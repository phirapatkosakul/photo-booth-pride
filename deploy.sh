#!/usr/bin/env bash
# Deploy Photo Booth -> GitHub Pages (รันหลังจาก gh auth login แล้ว)
set -e
REPO="photo-booth-pride"
cd "$(dirname "$0")"

echo "👤 ตรวจสอบบัญชี GitHub…"
USER=$(gh api user --jq .login)
echo "   ล็อกอินเป็น: $USER"

git add -A
git commit -q -m "deploy update" 2>/dev/null || true
git branch -M main

if gh repo view "$USER/$REPO" >/dev/null 2>&1; then
  echo "📦 repo มีอยู่แล้ว — push อัปเดต…"
  git remote get-url origin >/dev/null 2>&1 || git remote add origin "https://github.com/$USER/$REPO.git"
  git push -u origin main
else
  echo "📦 สร้าง repo ใหม่ + push…"
  gh repo create "$REPO" --public --source=. --remote=origin --push
fi

echo "🌐 เปิด GitHub Pages…"
gh api --method POST "repos/$USER/$REPO/pages" \
  -f "source[branch]=main" -f "source[path]=/" >/dev/null 2>&1 \
  || gh api --method PUT "repos/$USER/$REPO/pages" \
       -f "source[branch]=main" -f "source[path]=/" >/dev/null 2>&1 || true

echo ""
echo "=================================================="
echo "  ✅ เสร็จ! เว็บของคุณ (รอ 1-2 นาทีให้ build เสร็จ):"
echo "     https://$USER.github.io/$REPO/"
echo "=================================================="
