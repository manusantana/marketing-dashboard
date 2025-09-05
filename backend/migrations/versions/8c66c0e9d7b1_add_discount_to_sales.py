"""add discount column to sales

Revision ID: 8c66c0e9d7b1
Revises: b0e877608ad6
Create Date: 2025-09-01 00:00:00.000000
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "8c66c0e9d7b1"
down_revision = "b0e877608ad6"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "sales",

        sa.Column("discount", sa.Float(), nullable=False, server_default=sa.text("0")),
    )
    # remove server default now that existing rows are populated
    op.alter_column("sales", "discount", server_default=None, existing_type=sa.Float())



def downgrade() -> None:
    op.drop_column("sales", "discount")

