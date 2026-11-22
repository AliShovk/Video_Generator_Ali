#!/usr/bin/env bash
set -euo pipefail
GENERATOR_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PIPELINE_HOME="${YOUTUBE_PIPELINE_HOME:-$HOME/youtube-intelligence}"
HERMES_HOME="${HERMES_HOME:-$HOME/.hermes}"
SCOUT="$PIPELINE_HOME/sources/youtube-scout"
WRITER="$PIPELINE_HOME/sources/youtube-agent-skill"

require_bin() { command -v "$1" >/dev/null 2>&1 || { echo "Missing: $1" >&2; exit 2; }; }
clone_pinned() {
  local url="$1" dest="$2" sha="$3"
  mkdir -p "$(dirname "$dest")"
  if [ ! -d "$dest/.git" ]; then
    [ ! -e "$dest" ] || { echo "Refusing to overwrite: $dest" >&2; exit 2; }
    git clone --filter=blob:none "$url" "$dest"
  else
    [ -z "$(git -C "$dest" status --porcelain)" ] || { echo "Local modifications in $dest; refusing reset" >&2; exit 2; }
  fi
  git -C "$dest" fetch --depth 1 origin "$sha"
  git -C "$dest" checkout --detach "$sha"
}
install_skill() {
  local name="$1" src="$GENERATOR_ROOT/youtube_pipeline/hermes_skills/$1/SKILL.md" dst="$HERMES_HOME/skills/$1"
  if [ -d "$dst" ]; then cp -a "$dst" "$dst.backup.$(date +%Y%m%d-%H%M%S)"; fi
  mkdir -p "$dst"; cp "$src" "$dst/SKILL.md"; chmod -R go-rwx "$dst"
}
require_bin git
require_bin python3
python3 -c 'import sys; assert sys.version_info >= (3,10), "Python 3.10+ required"'

echo "[1/5] Install pinned upstream sources"
clone_pinned https://github.com/AgriciDaniel/youtube-scout.git "$SCOUT" 8edb2b66cb2da969d54ece257d0a81047f5f8c8e
clone_pinned https://github.com/Jakeschincariol/youtube-agent-skill.git "$WRITER" a2feb2104981a375ffd4f87ee04f4f5344ac43c6

echo "[2/5] Create isolated Scout environment"
python3 -m venv "$PIPELINE_HOME/.venv"
"$PIPELINE_HOME/.venv/bin/pip" install --upgrade pip
"$PIPELINE_HOME/.venv/bin/pip" install -e "$SCOUT" yt-dlp

echo "[3/5] Install helpers"
mkdir -p "$PIPELINE_HOME/bin" "$PIPELINE_HOME/runs" "$HERMES_HOME/skills"
install -m 0755 "$GENERATOR_ROOT/youtube_pipeline/scout_to_research.py" "$PIPELINE_HOME/bin/scout_to_research.py"
install -m 0755 "$GENERATOR_ROOT/youtube_pipeline/hookscore_ru.py" "$PIPELINE_HOME/bin/hookscore_ru.py"
cp "$WRITER/skills/yt-script/hooks.json" "$PIPELINE_HOME/bin/hooks-21-formulas.json"
cp "$WRITER/skills/yt-script/hookscore.py" "$PIPELINE_HOME/bin/hookscore-en-reference.py"

echo "[4/5] Install Hermes skills with backups"
install_skill youtube-research-agent
install_skill youtube-script-agent
install_skill youtube-shorts-pipeline

echo "[5/5] Prepare secret template and paths"
mkdir -p "$HOME/.config/scout"
if [ ! -f "$HOME/.config/scout/.env" ] && ! printenv YOUTUBE_API_KEY >/dev/null 2>&1; then
  if [ ! -f "$HOME/.config/scout/.env.example" ]; then
    printf '%s\n' 'YOUTUBE_API_KEY=PASTE_YOUTUBE_DATA_API_V3_KEY_HERE' > "$HOME/.config/scout/.env.example"
    chmod 600 "$HOME/.config/scout/.env.example"
  fi
fi
cat > "$PIPELINE_HOME/pipeline.env" <<EOF
YOUTUBE_PIPELINE_HOME=$PIPELINE_HOME
YOUTUBE_SCOUT_HOME=$SCOUT
YOUTUBE_SCOUT_PYTHON=$PIPELINE_HOME/.venv/bin/python
VIDEO_GEN_ROOT=$GENERATOR_ROOT
EOF
chmod 600 "$PIPELINE_HOME/pipeline.env"
echo "Installed. Configure ~/.config/scout/.env, verify /root/tts-bridge, ffmpeg, ffprobe, Node and HyperFrames; then run hermes skills list."
