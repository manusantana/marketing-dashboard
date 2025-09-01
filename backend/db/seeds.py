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
        amount = round(random.uniform(50, 500), 2)
        margin = round(random.uniform(0.1, 0.4), 2)  # porcentaje
        discount = round(random.uniform(0, 0.2), 2)  # porcentaje
        quantity = random.randint(1, 5)

        sale = Sale(
            product=product,
            customer=customer,
            date=date.date(),
            amount=amount,
            margin=margin,
            discount=discount,
            quantity=quantity,
            batch_id="seed",
        )
        db.add(sale)

    db.commit()


if __name__ == "__main__":
    db = SessionLocal()
    seed_sales(db, n=200)
    db.close()
    print("✅ Datos de prueba insertados en la tabla sales")
