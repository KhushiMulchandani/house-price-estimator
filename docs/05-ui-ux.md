# 05 · UI/UX Design + User Flows

## Page layout (single page)

```
┌──────────────────────────────────────────┐
│  House Price Estimator                   │
│  Enter details to get an estimate        │
├──────────────────────────────────────────┤
│  Square footage     [ 1500            ]  │
│  Bedrooms           [ 3               ]  │
│  House age (years)  [ 10              ]  │
│  Location rating    [ 4   (1 to 5)    ]  │
│                                          │
│            [ Estimate Price ]            │
├──────────────────────────────────────────┤
│  Estimated price                         │
│  $350,230.50                             │
│  Demo estimate based on synthetic data.  │
└──────────────────────────────────────────┘
```

## Components
| Component | Role |
|---|---|
| `App` | Page shell and title |
| `PriceEstimatorForm` | Four inputs, submit button, owns the state object |
| `ResultBox` | Shows the formatted price, rendered only when a price exists |
| `ErrorMessage` | Shows API or network errors |

## UI states
| State | Behaviour |
|---|---|
| Empty | Placeholders visible, result box hidden |
| Client-invalid | Inline hint under the offending field, submit blocked |
| Loading | Button disabled, label "Estimating..." |
| Success | Result box shows currency string |
| Server error (400) | Field-level messages from the API response |
| Network error | "Could not reach the server. Is the backend running?" |

## User flow
1. Open page → empty form.
2. Fill four fields → click **Estimate Price**.
3. Loading state → success or error state.
4. Edit any field and resubmit; the old result clears while loading.

## Accessibility and responsiveness
- Every input has a visible `<label>`.
- Numeric inputs use `type="number"` with `min`/`max`/`step`.
- Error text is announced with `role="alert"`.
- Layout is a single column that works from 360 px wide up.
