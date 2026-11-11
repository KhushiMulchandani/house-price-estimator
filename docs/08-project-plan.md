# 08 · Project Plan + Task Allocation

Work is tracked as **GitHub milestones and issues**. Run `scripts/setup_github.sh` once to create them.

Owner for all tasks: you (solo project).

## Milestone 1 · Docs and repo setup
| # | Task |
|---|---|
| 1.1 | Finalize README and project overview |
| 1.2 | Finalize SRS with validation ranges |
| 1.3 | Finalize API specification |
| 1.4 | Finalize architecture and folder layout |
| 1.5 | Configure repo: `.gitignore`, templates, branch protection on `main` |

## Milestone 2 · ML model
| # | Task |
|---|---|
| 2.1 | Write `ml_model/train.py` with synthetic data generator (seed 42) |
| 2.2 | Train LinearRegression and RandomForest, compare R², MAE, RMSE |
| 2.3 | Save `house_model.pkl` and pin scikit-learn version |
| 2.4 | Record metrics in `docs/07-ml-model.md` |
| 2.5 | Add model sanity tests (shape, monotonic sqft, sensible range) |

## Milestone 3 · Backend API
| # | Task |
|---|---|
| 3.1 | Create Django project and `estimator` app, add DRF |
| 3.2 | Add serializer with type and range validation |
| 3.3 | Load model once at startup (`ml.py`) |
| 3.4 | Implement `POST /api/v1/estimate/` |
| 3.5 | Configure CORS for `localhost:5173` |
| 3.6 | Write API tests for success and every error case |

## Milestone 4 · Frontend
| # | Task |
|---|---|
| 4.1 | Scaffold React app with Vite |
| 4.2 | Build `PriceEstimatorForm` with single state object |
| 4.3 | Add Axios client and submit handler |
| 4.4 | Build `ResultBox` with INR formatting |
| 4.5 | Add loading, validation and error states |
| 4.6 | Make layout responsive and accessible |

## Milestone 5 · Integration and polish
| # | Task |
|---|---|
| 5.1 | End-to-end manual test of the full flow |
| 5.2 | Add screenshots to README |
| 5.3 | Add `.env.example` files and verify setup steps from a clean clone |
| 5.4 | Review docs against the final code |
| 5.5 | Tag `v1.0` and publish a GitHub Release |

## Git workflow
- `main` is always working. Work on short-lived branches:
  `feat/estimate-endpoint`, `feat/price-form`, `docs/api-spec`, `fix/cors-error`.
- Open a pull request for every change, even solo. Link the issue with `Closes #N`.
- Commit style: Conventional Commits (`feat:`, `fix:`, `docs:`, `test:`, `chore:`, `refactor:`).
- Squash-merge PRs to keep `main` history clean.

## Definition of done (per task)
Code works locally · tests added or updated · docs updated if behaviour changed · PR merged · issue closed.
