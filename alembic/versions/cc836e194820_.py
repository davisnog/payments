"""empty message

Revision ID: cc836e194820
Revises: 
Create Date: 2023-07-30 13:38:05.456887

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cc836e194820'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('bank_slip',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('email', sa.String(255), nullable=False),
        sa.Column('government_id', sa.String(11), nullable=False),
        sa.Column('debt_amount', sa.Double(10), nullable=False),
        sa.Column('debt_due_date', sa.Date(), nullable=False),
        sa.Column('debt_id', sa.Integer(), nullable=False),
        sa.Column('paid_at', sa.DateTime(), nullable=True),
        sa.Column('paid_by', sa.String(255), nullable=True),
        sa.Column('paid_amount', sa.Double(10), nullable=True),
        sa.Column('inserted_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('idx_id'), 'bank_slip', ['id'], unique=True)
    op.create_index(op.f('idx_debit_id'), 'bank_slip', ['debt_id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('idx_id'), table_name='bank_slip')
    op.drop_index(op.f('idx_debit_id'), table_name='bank_slip')
    op.drop_table('bank_slip')
