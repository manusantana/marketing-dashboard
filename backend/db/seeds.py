import random
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from .session import SessionLocal, Base, engine
from .models import Sale

# Crear schema si no existe
Base.metadata.create_all(bind=engine)

def seed_sales(db: Session, n=100):
    products = ["Producto A", "Producto B", "Producto C", "Producto D"]
    customers = ["Cliente X", "Cliente Y", "Cliente Z", "Cliente W"]

    for _ in range(n):
        product = random.choice(products)
        customer = random.choice(customers)
        date = datetime.today() - timedelta(days=random.randint(0, 180))
        revenue = round(random.uniform(50, 500), 2)
        cost = round(revenue * random.uniform(0.3, 0.7), 2)

        sale = Sale(
            product=product,
            customer=customer,
            date=date.date(),
            revenue=revenue,
            cost=cost,
        )
        db.add(sale)

    db.commit()


if __name__ == "__main__":
    db = SessionLocal()
    seed_sales(db, n=200)
    db.close()
    print("✅ Datos de prueba insertados en la tabla sales")
