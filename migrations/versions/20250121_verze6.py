"""verze6

Revision ID: 20250121_verze6
Revises: 20250121_verze5
Create Date: 2025-01-21 18:55:58.061491+00:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '20250121_verze6'
down_revision = '20250121_verze5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('logins',
    sa.Column('logins_id', sa.Integer(), nullable=False),
    sa.Column('jmeno', sa.String(length=50), nullable=False),
    sa.Column('prijmeni', sa.String(length=50), nullable=False),
    sa.Column('trida', sa.String(length=50), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.PrimaryKeyConstraint('logins_id')
    )
    op.drop_table('login')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('login',
    sa.Column('login_id', sa.INTEGER(), nullable=False),
    sa.Column('jmeno', sa.VARCHAR(length=50), nullable=False),
    sa.Column('prijmeni', sa.VARCHAR(length=50), nullable=False),
    sa.Column('created_at', sa.DATETIME(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.Column('trida', sa.VARCHAR(length=50), nullable=False),
    sa.PrimaryKeyConstraint('login_id')
    )
    op.drop_table('logins')
    # ### end Alembic commands ###
