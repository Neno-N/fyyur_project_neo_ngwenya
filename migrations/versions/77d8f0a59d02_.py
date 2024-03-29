"""empty message

Revision ID: 77d8f0a59d02
Revises: 2b41e8482f0b
Create Date: 2022-05-31 12:28:41.636957

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '77d8f0a59d02'
down_revision = '2b41e8482f0b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('artist', sa.Column(
        'seeking_venue', sa.Boolean(), nullable=True))
    op.add_column('artist', sa.Column(
        'seeking_description', sa.String(), nullable=True))
    op.add_column('artist', sa.Column(
        'website', sa.String(length=120), nullable=True))
    op.add_column('venue', sa.Column(
        'genres', sa.ARRAY(sa.String(length=120)), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('venue', 'genres')
    op.drop_column('artist', 'website')
    op.drop_column('artist', 'seeking_description')
    op.drop_column('artist', 'seeking_venue')
    # ### end Alembic commands ###
