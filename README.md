# House Price Estimator

A single-page full-stack app: enter a house's square footage, bedrooms, age and location rating, and get an instant estimated price.

**Stack:** React (Vite) · Django + Django REST Framework · scikit-learn (LinearRegression / RandomForestRegressor)

> **Note:** The model is trained on synthetic data. The output is a learning-project estimate, not a real market valuation.

## How it works

```
[ React Form ] --> POST /api/v1/estimate/ --> [ Django API View ] --> [ house_model.pkl ] --> { "estimated_price": 350230.50 }
```

The API is stateless: no database is needed to serve a prediction.

## Repository layout

```
house-price-estimator/
├── backend/       # Django + DRF API (port 8000)
├── frontend/      # React + Vite app (port 5173)
├── ml_model/      # train.py, evaluation, house_model.pkl
├── docs/          # project documents 01-09
├── scripts/       # GitHub setup helper
└── .github/       # PR and issue templates
```

## Documentation

| # | Document |
|---|---|
| 1 | [Project Overview](docs/01-project-overview.md) |
| 2 | [SRS + Features](docs/02-srs.md) |
| 3 | [System Architecture](docs/03-architecture.md) |
| 4 | [Database Design](docs/04-database-design.md) |
| 5 | [UI/UX + Flows](docs/05-ui-ux.md) |
| 6 | [API Specification](docs/06-api-spec.md) |
| 7 | [ML Dataset + Model](docs/07-ml-model.md) |
| 8 | [Project Plan](docs/08-project-plan.md) |
| 9 | [Testing + Security](docs/09-testing-security.md) |
| 10 | This README (setup below) |

## Setup

> Commands below are the target setup. Folders are filled in as milestones are completed.

### Prerequisites
- Python 3.11+
- Node.js 20+
- Git

### 1. Clone
```bash
git clone https://github.com/<your-username>/house-price-estimator.git
cd house-price-estimator
```

### 2. Train the model
```bash
cd ml_model
python -m venv ../venv
source ../venv/bin/activate        # Windows: ..\venv\Scripts\activate
pip install -r requirements.txt
python train.py                    # writes house_model.pkl and prints metrics
```

### 3. Run the backend
```bash
cd ../backend
pip install -r requirements.txt
python manage.py runserver         # http://localhost:8000
```

### 4. Run the frontend
```bash
cd ../frontend
npm install
npm run dev                        # http://localhost:5173
```

### 5. Run tests
```bash
cd backend && python manage.py test
cd ../frontend && npm test
```

## Git workflow

See [CONTRIBUTING.md](CONTRIBUTING.md): short-lived feature branches, Conventional Commits, pull requests into `main`.

## Roadmap

Next project built on the same stack: **BitVision**, a Bitcoin price predictor with live data and time-series models.

## License

MIT (add a LICENSE file when you publish).
