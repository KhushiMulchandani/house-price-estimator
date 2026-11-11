# 09 · Testing + Security Plan

## Testing

### ML (`ml_model/`)
| Test | Expectation |
|---|---|
| Model file loads | `joblib.load` succeeds |
| Output shape | One float for one input row |
| Sanity: size | Larger `sqft` gives a higher price, other features fixed |
| Sanity: age | Older house gives a lower or equal price |
| Metrics | R² meets target in [07-ml-model.md](07-ml-model.md) |

### Backend (`python manage.py test`)
| Case | Expected |
|---|---|
| Valid payload | 200 and numeric `estimated_price` |
| Missing field | 400 naming the field |
| String instead of number | 400 |
| Below min / above max for each field | 400 |
| Non-integer bedrooms or rating | 400 |
| GET request | 405 |
| Non-JSON body | 415 |
| Model unavailable | 500 with generic message |

### Frontend (Vitest + React Testing Library)
| Case | Expected |
|---|---|
| Renders four labelled inputs | Pass |
| Valid submit | Calls API once, shows formatted price |
| API 400 | Shows field errors |
| Network failure | Shows connection message |
| Loading | Button disabled while pending |

### Manual end-to-end checklist
- [ ] Backend and frontend both running, no CORS error in the browser console
- [ ] Valid input shows a price formatted as INR
- [ ] Invalid input shows an error, no crash
- [ ] Works at 360 px wide

## Security

| Risk | Mitigation |
|---|---|
| Malformed input crashing the server | DRF serializer validates type and range before the model runs |
| Unsafe pickle loading | Load only the locally trained file; fixed path from settings; never accept uploaded models |
| CORS too open | Allow only the frontend origin; no `CORS_ALLOW_ALL_ORIGINS` |
| Secrets in git | `.env` git-ignored; commit `.env.example` only |
| `DEBUG=True` in production | Read from env; default `False` outside dev |
| Dependency vulnerabilities | Enable GitHub Dependabot alerts |
| Information leakage | Return generic 500 message; log details server-side only |
| Abuse / spam requests | Optional: DRF throttling (e.g. 60 requests/min per IP) |

## CI (optional stretch, Milestone 5)
GitHub Actions workflow running backend tests and frontend build on every pull request.
