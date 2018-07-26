"""Add tv and animation table and media table add bilibili_id column

Revision ID: 1b2d2f1a1d56
Revises: cc825dd0b55a
Create Date: 2016-02-21 22:24:43.509991

"""

# revision identifiers, used by Alembic.
revision = '1b2d2f1a1d56'
down_revision = 'cc825dd0b55a'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('animation_genres',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('animations',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id'], ['videos.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tvs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id'], ['videos.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('animations_genres_association',
    sa.Column('animation_id', sa.Integer(), nullable=True),
    sa.Column('animation_genre_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['animation_genre_id'], ['animation_genres.id'], ),
    sa.ForeignKeyConstraint(['animation_id'], ['animations.id'], )
    )
    op.create_table('tvs_genres_association',
    sa.Column('tv_id', sa.Integer(), nullable=True),
    sa.Column('tv_genre_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['tv_genre_id'], ['tv_genres.id'], ),
    sa.ForeignKeyConstraint(['tv_id'], ['tvs.id'], )
    )
    with op.batch_alter_table('media', schema=None) as batch_op:
        batch_op.add_column(sa.Column('bilibili_id', sa.String(), nullable=True))

    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('media', schema=None) as batch_op:
        batch_op.drop_column('bilibili_id')

    op.drop_table('tvs_genres_association')
    op.drop_table('animations_genres_association')
    op.drop_table('tvs')
    op.drop_table('animations')
    op.drop_table('animation_genres')
    ### end Alembic commands ###
