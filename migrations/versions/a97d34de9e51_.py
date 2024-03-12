"""empty message

Revision ID: a97d34de9e51
Revises: 
Create Date: 2024-03-11 23:45:20.797203

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a97d34de9e51'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('roles',
    sa.Column('role_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('about', sa.String(), nullable=False),
    sa.Column('job', sa.String(), nullable=False),
    sa.Column('relation', sa.String(), nullable=False),
    sa.Column('behavior', sa.String(), nullable=False),
    sa.Column('hobby', sa.String(), nullable=False),
    sa.Column('dark_side', sa.String(), nullable=False),
    sa.Column('gift', sa.String(), nullable=False),
    sa.Column('additional', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.Column('first_fact', sa.String(), nullable=False),
    sa.Column('second_fact', sa.String(), nullable=False),
    sa.Column('third_fact', sa.String(), nullable=False),
    sa.Column('token', sa.String(), nullable=False),
    sa.Column('is_dead', sa.Boolean(), nullable=False),
    sa.Column('is_registered', sa.Boolean(), nullable=False),
    sa.Column('opened', sa.String(), nullable=False),
    sa.Column('user', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('role_id'),
    sa.UniqueConstraint('token')
    )
    op.create_table('telegram',
    sa.Column('tg_id', sa.String(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('tg_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('telegram')
    op.drop_table('roles')
    op.drop_table('users')
    # ### end Alembic commands ###
