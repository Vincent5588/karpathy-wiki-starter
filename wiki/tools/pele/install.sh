#!/bin/sh
# 在本機安裝規則 W 用的 Pele（版本照 package-lock.json 固定），裝在 vault 之外。
# 用法：sh wiki/tools/pele/install.sh
# 位置：預設 ~/.local/share/pele-render，可用環境變數 PELE_RENDER_HOME 改。重跑會照鎖定版本重裝。
set -eu
HERE=$(cd "$(dirname "$0")" && pwd)
DEST="${PELE_RENDER_HOME:-$HOME/.local/share/pele-render}"
command -v npm >/dev/null 2>&1 || { echo "[pele-install] 找不到 npm，先裝 Node.js（22 以上）"; exit 1; }
mkdir -p "$DEST"
cp "$HERE/package.json" "$HERE/package-lock.json" "$DEST/"
cd "$DEST"
npm ci --omit=dev --no-audit --no-fund
node -e "const p=require('$DEST/node_modules/pele/package.json');console.log('[pele-install] 已安裝 pele '+p.version+' → $DEST')"
