# Workflow

Solo project, run like a team project.

## Branches
- `main`: always working and releasable.
- Feature branches, short-lived, one task each:
  - `feat/<thing>` new functionality
  - `fix/<thing>` bug fixes
  - `docs/<thing>` documentation only
  - `test/<thing>` tests only
  - `chore/<thing>` tooling and config

## Commits (Conventional Commits)
```
feat: add estimate endpoint
fix: reject non-numeric sqft
docs: add API error table
test: cover out-of-range rating
chore: pin scikit-learn version
```
Keep commits small and focused. Write in the imperative mood.

## Pull requests
1. Branch from an up-to-date `main`.
2. Push the branch and open a PR using the template.
3. Link the issue with `Closes #<number>`.
4. Check that tests pass and docs are updated.
5. Squash-merge, then delete the branch.

## Daily loop
```bash
git checkout main && git pull
git checkout -b feat/price-form
# work, commit often
git push -u origin feat/price-form
# open PR on GitHub
```

## Releases
After Milestone 5: `git tag v1.0.0 && git push --tags`, then publish a GitHub Release.
