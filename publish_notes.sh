#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

VAULT_ROOT="/home/lukasz/Documents/ObsidianVault"
VENV_PYTHON="${VAULT_ROOT}/.venv/bin/python"
MKDOCS_BIN="${VAULT_ROOT}/.venv/bin/mkdocs"

# Step 1: Run the Python script to prepare the documentation
echo "
--- Running documentation build script ---"
"${VENV_PYTHON}" "${VAULT_ROOT}/_build_docs.py"

# Step 2: Stage and commit changes to the main branch
echo "
--- Staging and committing changes to main branch ---"
cd "${VAULT_ROOT}"
git add .

# Check if there are any changes to commit
if git diff-index --quiet HEAD --;
then
  echo "No changes detected in main branch to commit."
else
  git commit -m "Automated notes refresh for GitHub Pages"
  echo "Pushing changes to origin/main..."
  git push origin main
fi

# Step 3: Deploy to GitHub Pages
echo "
--- Deploying to GitHub Pages ---"
"${MKDOCS_BIN}" gh-deploy

echo "
--- GitHub Pages refresh complete ---"
