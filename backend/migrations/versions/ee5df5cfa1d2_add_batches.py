"""add batches table and batch_id to sales

Revision ID: ee5df5cfa1d2
Revises: cdb7a72fc2d2
Create Date: 2025-10-20 00:00:00.000000
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "ee5df5cfa1d2"
down_revision: Union[str, Sequence[str], None] = "cdb7a72fc2d2"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "batches",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_batches_id"), "batches", ["id"], unique=False)
    op.add_column("sales", sa.Column("batch_id", sa.Integer(), nullable=True))
    op.create_index(op.f("ix_sales_batch_id"), "sales", ["batch_id"], unique=False)
    op.create_foreign_key(
        None, "sales", "batches", ["batch_id"], ["id"], ondelete="CASCADE"
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(None, "sales", type_="foreignkey")
    op.drop_index(op.f("ix_sales_batch_id"), table_name="sales")
    op.drop_column("sales", "batch_id")
    op.drop_index(op.f("ix_batches_id"), table_name="batches")
    op.drop_table("batches")
