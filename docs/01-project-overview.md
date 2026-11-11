# 01 · Project Overview

## Summary
The **House Price Estimator** is a single-page full-stack application. A user enters four house features and instantly receives an estimated market value in INR.

## Purpose
This is a warm-up project for the **BitVision** Bitcoin predictor. It practises the same pipeline on a smaller problem:
- passing structured numeric data from React to Django
- running a scikit-learn regression model behind a REST API
- returning a continuous value to the UI

## Goals
- Working end-to-end flow: form → API → model → result
- Clean input validation and error handling
- A repo that is well-documented and managed on GitHub from day one

## Non-goals
- Real market accuracy (training data is synthetic)
- User accounts, history or saved estimates
- Deployment to production (optional stretch)

## Skills practised
| Skill | Why it matters for BitVision |
|---|---|
| Data formatting | Prevent crashes from strings passed instead of numbers |
| CORS management | React (5173) talking to Django (8000) |
| Stateless API design | Serve ML predictions with no database lookup |

## Bridge to BitVision
| Layer | House Price (this project) | BitVision |
|---|---|---|
| Data source | Synthetic / mock dataset | Live crypto APIs |
| Model | Linear Regression | Time-series (LSTM, ARIMA, Prophet) |
| Frontend | 4 input boxes | Interactive historical charts |

## Tech stack
React (Vite) · Axios · Django · Django REST Framework · django-cors-headers · scikit-learn · joblib · NumPy · pandas

## Success criteria
1. Valid input returns a price within 1 second.
2. Invalid input returns a clear 400 error and the UI shows it.
3. Model metrics (R², MAE) are documented.
4. All 5 milestones complete and `v1.0` tagged.
