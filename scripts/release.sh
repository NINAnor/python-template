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
git commit -m "Bump version: $(git describe --tags --abbrev=0 HEAD~1) → $(git describe --tags --exact-match HEAD 2>/dev/null || echo 'unknown')"

echo "🏷️ Creating tag..."
NEW_VERSION=$(uvx bump-my-version show current_version)
git tag v$NEW_VERSION

echo "📚 Generating changelog..."
uvx gitchangelog

echo "📋 Amending commit with changelog..."
git add CHANGELOG.txt
git commit --amend --no-edit

echo "🏷️ Updating tag..."
git tag -f v$NEW_VERSION

echo "✅ Release v$NEW_VERSION created successfully!"
echo "💡 To push: git push origin main && git push origin v$NEW_VERSION"
