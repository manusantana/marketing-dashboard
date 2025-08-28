# API - Endpoints actuales

## Health
- `GET /api/v1/health` → Status del backend.

## Upload
- `POST /api/v1/upload`  
  - **Body**: archivo (CSV/XLSX).  
  - **Response**: `{ "rows_inserted": int }`.

## KPIs
- `GET /api/v1/kpis/overview`  
  - **Response**:  
    ```json
    {
      "total_leads": 100,
      "conversion_rate": 0.25,
      "revenue": 25000,
      "avg_ticket": 250
    }
    ```
- `GET /api/v1/kpis/timeseries`
- `GET /api/v1/kpis/top?by=channel`
