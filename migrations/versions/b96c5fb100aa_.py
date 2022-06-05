"""empty message

Revision ID: b96c5fb100aa
Revises: 
Create Date: 2022-05-31 11:30:11.726500

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b96c5fb100aa'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('artist',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.String(), nullable=True),
                    sa.Column('city', sa.String(length=120), nullable=True),
                    sa.Column('state', sa.String(length=120), nullable=True),
                    sa.Column('phone', sa.String(length=120), nullable=True),
                    sa.Column('genres', sa.ARRAY(
                        sa.String(length=120)), nullable=True),
                    sa.Column('image_link', sa.String(
                        length=500), nullable=True),
                    sa.Column('facebook_link', sa.String(
                        length=120), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('venue',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.String(), nullable=True),
                    sa.Column('city', sa.String(length=120), nullable=True),
                    sa.Column('state', sa.String(length=120), nullable=True),
                    sa.Column('address', sa.String(length=120), nullable=True),
                    sa.Column('phone', sa.String(length=120), nullable=True),
                    sa.Column('image_link', sa.String(
                        length=500), nullable=True),
                    sa.Column('facebook_link', sa.String(
                        length=120), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('venue')
    op.drop_table('artist')
    # ### end Alembic commands ###
