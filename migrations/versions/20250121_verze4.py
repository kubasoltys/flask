"""verze4

Revision ID: 20250121_verze4
Revises: 20250121_verze3
Create Date: 2025-01-21 18:24:45.929637+00:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '20250121_verze4'
down_revision = '20250121_verze3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('login', sa.Column('trida', sa.String(length=50), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('login', 'trida')
    # ### end Alembic commands ###
