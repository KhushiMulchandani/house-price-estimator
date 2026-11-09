#!/usr/bin/env bash
# Creates labels, milestones and issues for the House Price Estimator repo.
#
# Prerequisites:
#   1. Install GitHub CLI: https://cli.github.com
#   2. Run: gh auth login
#   3. Create the (empty) repo on GitHub and push this folder to it
#   4. Run this script from inside the repo folder:  bash scripts/setup_github.sh
#
# Run it ONCE. Running it again creates duplicate issues.

set -euo pipefail

if ! command -v gh >/dev/null 2>&1; then
  echo "GitHub CLI (gh) not found. Install it first: https://cli.github.com" >&2
  exit 1
fi

REPO="$(gh repo view --json nameWithOwner -q .nameWithOwner)"
echo "Setting up: $REPO"

# ---------- Labels ----------
make_label() { gh label create "$1" --color "$2" --description "$3" --force >/dev/null; }
make_label "docs"     "0075ca" "Documentation"
make_label "ml"       "8250df" "Machine learning"
make_label "backend"  "1a7f37" "Django / DRF"
make_label "frontend" "bf3989" "React"
make_label "testing"  "fbca04" "Tests"
make_label "chore"    "6e7781" "Tooling and config"

# ---------- Milestones ----------
make_milestone() {
  gh api "repos/$REPO/milestones" -f title="$1" -f description="$2" >/dev/null
}
M1="1 - Docs and repo setup"
M2="2 - ML model"
M3="3 - Backend API"
M4="4 - Frontend"
M5="5 - Integration and polish"

make_milestone "$M1" "README, SRS, API spec, architecture"
make_milestone "$M2" "Training script, metrics, saved model"
make_milestone "$M3" "DRF endpoint, validation, CORS, tests"
make_milestone "$M4" "Form, Axios call, result display, error states"
make_milestone "$M5" "End-to-end test, README screenshots, tag v1.0"

# ---------- Issues ----------
# usage: issue "title" "label" "milestone" "body"
issue() {
  gh issue create --title "$1" --label "$2" --milestone "$3" --body "$4" >/dev/null
  echo "  + $1"
}

echo "Creating issues..."

# Milestone 1
issue "Finalize README and project overview"            "docs"  "$M1" "See docs/01-project-overview.md"
issue "Finalize SRS with validation ranges"             "docs"  "$M1" "Confirm ranges in docs/02-srs.md"
issue "Finalize API specification"                      "docs"  "$M1" "See docs/06-api-spec.md"
issue "Finalize architecture and folder layout"         "docs"  "$M1" "See docs/03-architecture.md"
issue "Configure repo: templates and branch protection" "chore" "$M1" "Protect main, require PRs, enable Dependabot alerts"

# Milestone 2
issue "Write train.py with synthetic data generator"    "ml"      "$M2" "Seed 42, ~2000 rows, formula in docs/07-ml-model.md"
issue "Train and compare LinearRegression vs RandomForest" "ml"   "$M2" "Report R2, MAE, RMSE on the 20% test set"
issue "Save house_model.pkl and pin scikit-learn version"  "ml"   "$M2" "Same pinned version in ml_model and backend requirements"
issue "Record model metrics in docs/07-ml-model.md"     "docs"    "$M2" "Fill in actual results"
issue "Add model sanity tests"                          "testing" "$M2" "Output shape, sqft monotonic, age effect"

# Milestone 3
issue "Create Django project and estimator app with DRF"   "backend"  "$M3" "Project: config, app: estimator"
issue "Add serializer with type and range validation"      "backend"  "$M3" "Ranges from docs/02-srs.md"
issue "Load model once at startup (ml.py)"                 "backend"  "$M3" "joblib.load at import; path from MODEL_PATH"
issue "Implement POST /api/v1/estimate/"                   "backend"  "$M3" "Contract in docs/06-api-spec.md"
issue "Configure CORS for localhost:5173"                  "backend"  "$M3" "django-cors-headers, specific origin only"
issue "Write API tests for success and all error cases"    "testing"  "$M3" "See docs/09-testing-security.md"

# Milestone 4
issue "Scaffold React app with Vite"                       "frontend" "$M4" "Dev server on port 5173"
issue "Build PriceEstimatorForm with single state object"  "frontend" "$M4" "Fields: sqft, bedrooms, age, location_rating"
issue "Add Axios client and submit handler"                "frontend" "$M4" "Base URL from VITE_API_URL"
issue "Build ResultBox with USD formatting"                "frontend" "$M4" "toLocaleString en-US currency"
issue "Add loading, validation and error states"           "frontend" "$M4" "See docs/05-ui-ux.md"
issue "Make layout responsive and accessible"              "frontend" "$M4" "Works at 360px, labelled inputs, role=alert"

# Milestone 5
issue "End-to-end manual test of full flow"            "testing" "$M5" "Checklist in docs/09-testing-security.md"
issue "Add screenshots to README"                      "docs"    "$M5" "Empty, success and error states"
issue "Add .env.example files and verify clean-clone setup" "chore" "$M5" "Follow README steps on a fresh clone"
issue "Review docs against final code"                 "docs"    "$M5" "Update API spec, ML metrics, architecture"
issue "Tag v1.0 and publish GitHub Release"            "chore"   "$M5" "git tag v1.0.0 && git push --tags"

echo "Done. Open https://github.com/$REPO/issues"
