"""empty message

Revision ID: 2a92fd3f36a0
Revises: 
Create Date: 2021-09-30 12:10:56.524724

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2a92fd3f36a0'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('Actor', 'name',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('Actor', 'age',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('Actor', 'gender',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('Movie', 'title',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('Movie', 'release_year',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('Movie', 'release_year',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('Movie', 'title',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('Actor', 'gender',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('Actor', 'age',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('Actor', 'name',
               existing_type=sa.VARCHAR(),
               nullable=True)
    # ### end Alembic commands ###
