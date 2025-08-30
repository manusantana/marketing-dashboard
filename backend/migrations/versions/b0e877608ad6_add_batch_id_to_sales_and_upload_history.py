"""add batch_id to sales and upload_history

Revision ID: b0e877608ad6
Revises: cdb7a72fc2d2
Create Date: 2025-08-28 23:42:22.082664
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "b0e877608ad6"          # ← usa el de la cabecera
down_revision = "cdb7a72fc2d2"     # ← el “Revises” de la cabecera (tu última mig previa)
branch_labels = None
depends_on = None

def upgrade():
    # 1) sales.batch_id
    op.add_column("sales", sa.Column("batch_id", sa.String(length=36), nullable=True))
    op.create_index("ix_sales_batch_id", "sales", ["batch_id"], unique=False)

    # 2) índice compuesto útil para reporting
    op.create_index("ix_sales_date_customer_product", "sales", ["date","customer","product"], unique=False)

    # 3) rellenar batch_id en registros existentes y poner NOT NULL
    conn = op.get_bind()
    conn.execute(sa.text(
        "UPDATE sales SET batch_id = '00000000-0000-0000-0000-000000000000' WHERE batch_id IS NULL"
    ))
    op.alter_column("sales", "batch_id", nullable=False)

    # 4) tabla upload_history
    op.create_table(
        "upload_history",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("batch_id", sa.String(length=36), nullable=False),
        sa.Column("filename", sa.String(), nullable=False),
        sa.Column("mode", sa.Enum("append","replace", name="upload_mode"), nullable=False),
        sa.Column("rows", sa.Integer, nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
    )
    op.create_index("ix_upload_history_batch_id", "upload_history", ["batch_id"], unique=True)

def downgrade():
    op.drop_index("ix_upload_history_batch_id", table_name="upload_history")
    op.drop_table("upload_history")
    op.drop_index("ix_sales_date_customer_product", table_name="sales")
    op.drop_index("ix_sales_batch_id", table_name="sales")
    op.drop_column("sales", "batch_id")
    op.execute("DROP TYPE IF EXISTS upload_mode")
