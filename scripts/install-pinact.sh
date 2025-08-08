#!/bin/bash
set -e

echo "🔧 Installing pinact..."

# Install aqua if not already available
if ! command -v aqua &> /dev/null; then
    echo "📦 Installing aqua..."
    curl -sSfL https://raw.githubusercontent.com/aquaproj/aqua-installer/v3.0.1/aqua-installer | bash
fi

# Add aqua to PATH and config in .bashrc if not already present
AQUA_PATH_EXPORT='export PATH="${AQUA_ROOT_DIR:-${XDG_DATA_HOME:-$HOME/.local/share}/aquaproj-aqua}/bin:$PATH"'
AQUA_CONFIG_EXPORT='export AQUA_GLOBAL_CONFIG="${XDG_CONFIG_HOME:-$HOME/.config}/aquaproj-aqua/aqua.yaml"'
if ! grep -qF "aquaproj-aqua" ~/.bashrc 2>/dev/null; then
    echo "🔗 Adding aqua to PATH in ~/.bashrc..."
    echo "$AQUA_PATH_EXPORT" >> ~/.bashrc
    echo "$AQUA_CONFIG_EXPORT" >> ~/.bashrc
fi

# Export for current session
export PATH="${AQUA_ROOT_DIR:-${XDG_DATA_HOME:-$HOME/.local/share}/aquaproj-aqua}/bin:$PATH"
export AQUA_GLOBAL_CONFIG="${XDG_CONFIG_HOME:-$HOME/.config}/aquaproj-aqua/aqua.yaml"

# Create global aqua config and install pinact
echo "📦 Installing pinact..."
mkdir -p ~/.config/aquaproj-aqua
cat > ~/.config/aquaproj-aqua/aqua.yaml << 'EOF'
registries:
- type: standard
  ref: v4.252.0
packages:
- name: suzuki-shunsuke/pinact@v3.3.2
EOF
aqua i -a

echo "✅ pinact installation completed!"
echo "💡 You may need to restart your shell or run: source ~/.bashrc"
