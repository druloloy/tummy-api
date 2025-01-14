"""empty message

Revision ID: ccdf124ca00c
Revises: b5ce428ecedf
Create Date: 2024-03-30 06:47:54.933149

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ccdf124ca00c'
down_revision = 'b5ce428ecedf'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('_id', sa.UUID(), server_default=sa.text('gen_random_uuid()'), nullable=False),
    sa.Column('_auth_id', sa.String(length=120), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('username', sa.String(length=15), nullable=False),
    sa.Column('first_name', sa.String(length=60), nullable=False),
    sa.Column('last_name', sa.String(length=60), nullable=False),
    sa.Column('dob', sa.Date(), nullable=False),
    sa.Column('is_user_verified', sa.Boolean(), nullable=True),
    sa.Column('gender', sa.Enum('m', 'f', 'a', 'o', name='gender_type'), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('transaction_timestamp()'), nullable=False),
    sa.PrimaryKeyConstraint('_id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username'),
    schema='core'
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users', schema='core')
    # ### end Alembic commands ###
