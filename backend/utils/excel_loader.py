import pandas as pd
from sqlalchemy.orm import Session
from db.models import Sale

def load_excel_to_db(file_path: str, db: Session):
    df = pd.read_excel(file_path)
    for _, row in df.iterrows():
        sale = Sale(
            product=row.get("product"),
            customer=row.get("customer"),
            date=row.get("date"),
            revenue=row.get("revenue", 0),
            cost=row.get("cost", 0),
        )
        db.add(sale)
    db.commit()