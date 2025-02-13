"""Criando tabelas

Revision ID: ba39ed5c86f1
Revises: 
Create Date: 2025-02-11 20:23:48.483720

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ba39ed5c86f1'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=50), nullable=False),
    sa.Column('password', sa.String(length=255), nullable=False),
    sa.Column('saldo', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    op.create_table('transacao',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('usuario_id', sa.Integer(), nullable=False),
    sa.Column('valor', sa.Float(), nullable=False),
    sa.Column('tipo', sa.String(length=10), nullable=False),
    sa.Column('data', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['usuario_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('transacao')
    op.drop_table('user')
    # ### end Alembic commands ###
