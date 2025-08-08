#!/bin/bash
set -e

if [ $# -eq 0 ]; then
    echo "Usage: $0 <version_type>"
    echo "  version_type: patch, minor, or major"
    exit 1
fi

VERSION_TYPE=$1

echo "🚀 Creating $VERSION_TYPE release..."

echo "📝 Bumping version..."
uvx bump-my-version bump $VERSION_TYPE
uv sync

echo "📋 Adding changes to git..."
git add .
NEW_VERSION=$(uvx bump-my-version show current_version)
git commit -m "Bump version: $(git describe --tags --abbrev=0 HEAD~1) → v$NEW_VERSION"

echo "🏷️ Creating tag..."
git tag v$NEW_VERSION

echo "📚 Generating changelog..."
uvx --with pystache gitchangelog

echo "📋 Amending commit with changelog..."
git add CHANGELOG.txt
git commit --amend --no-edit

echo "🏷️ Updating tag..."
git tag -f v$NEW_VERSION

echo "✅ Release v$NEW_VERSION created successfully!"
echo "💡 To push: git push origin main && git push origin v$NEW_VERSION"
