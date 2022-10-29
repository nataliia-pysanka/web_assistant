"""empty message

Revision ID: 595235bb0f37
Revises: 63e8c4d8a626
Create Date: 2022-10-28 18:12:45.365138

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '595235bb0f37'
down_revision = '63e8c4d8a626'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('contact_group',
    sa.Column('contact_id', sa.Integer(), nullable=True),
    sa.Column('group_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['contact_id'], ['contact_table.id'], ),
    sa.ForeignKeyConstraint(['group_id'], ['group_table.id'], )
    )
    op.drop_table('association_table')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('association_table',
    sa.Column('contact_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('group_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['contact_id'], ['contact_table.id'], name='association_table_contact_id_fkey'),
    sa.ForeignKeyConstraint(['group_id'], ['group_table.id'], name='association_table_group_id_fkey'),
    sa.PrimaryKeyConstraint('contact_id', 'group_id', name='association_table_pkey')
    )
    op.drop_table('contact_group')
    # ### end Alembic commands ###
