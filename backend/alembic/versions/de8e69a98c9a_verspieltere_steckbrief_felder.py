"""verspieltere Steckbrief-Felder (Umbenennungen + Liebesleben)

Revision ID: de8e69a98c9a
Revises: d51ceba2a034
Create Date: 2026-08-18 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'de8e69a98c9a'
down_revision = 'd51ceba2a034'
branch_labels = None
depends_on = None


relationship_status_enum = sa.Enum(
    'MONOGAMOUS', 'MULTIPLE_PARTNERS', 'HAREM', name='relationshipstatus'
)


def upgrade() -> None:
    # Neuen Enum-Typ vorab anlegen (No-op auf SQLite, notwendig auf Postgres).
    relationship_status_enum.create(op.get_bind(), checkfirst=True)

    with op.batch_alter_table('animals') as batch_op:
        # Umbenennungen (Spaltenname, JSON-Key und UI-Label ziehen gemeinsam mit,
        # siehe docs/adr/0006-neue-steckbrief-felder-nullable.md).
        batch_op.alter_column('habitat', new_column_name='home_turf',
                               existing_type=sa.Text(), existing_nullable=False)
        batch_op.alter_column('offspring_count', new_column_name='offspring_brood',
                               existing_type=sa.String(length=60), existing_nullable=False)
        batch_op.alter_column('gestation_period', new_column_name='baby_wait_time',
                               existing_type=sa.String(length=60), existing_nullable=False)
        batch_op.alter_column('diet', new_column_name='favorite_food',
                               existing_type=sa.Text(), existing_nullable=False)
        batch_op.alter_column('natural_enemies', new_column_name='arch_enemies',
                               existing_type=sa.Text(), existing_nullable=False)
        batch_op.alter_column('social_behavior', new_column_name='social_life',
                               existing_type=sa.Enum('SOLITARY', 'HERD', name='socialbehavior'),
                               existing_nullable=False)
        batch_op.alter_column('character_traits', new_column_name='personality',
                               existing_type=sa.Text(), existing_nullable=False)

        # Neue, bewusst nullable Zusatzfelder.
        batch_op.add_column(sa.Column('fun_fact', sa.Text(), nullable=True))
        batch_op.add_column(sa.Column('superpower', sa.Text(), nullable=True))
        batch_op.add_column(sa.Column('mating_season', sa.Text(), nullable=True))
        batch_op.add_column(sa.Column('nest_building', sa.Text(), nullable=True))
        batch_op.add_column(sa.Column('courtship_dance', sa.Text(), nullable=True))
        batch_op.add_column(sa.Column('relationship_status', relationship_status_enum, nullable=True))


def downgrade() -> None:
    with op.batch_alter_table('animals') as batch_op:
        batch_op.drop_column('relationship_status')
        batch_op.drop_column('courtship_dance')
        batch_op.drop_column('nest_building')
        batch_op.drop_column('mating_season')
        batch_op.drop_column('superpower')
        batch_op.drop_column('fun_fact')

        batch_op.alter_column('personality', new_column_name='character_traits',
                               existing_type=sa.Text(), existing_nullable=False)
        batch_op.alter_column('social_life', new_column_name='social_behavior',
                               existing_type=sa.Enum('SOLITARY', 'HERD', name='socialbehavior'),
                               existing_nullable=False)
        batch_op.alter_column('arch_enemies', new_column_name='natural_enemies',
                               existing_type=sa.Text(), existing_nullable=False)
        batch_op.alter_column('favorite_food', new_column_name='diet',
                               existing_type=sa.Text(), existing_nullable=False)
        batch_op.alter_column('baby_wait_time', new_column_name='gestation_period',
                               existing_type=sa.String(length=60), existing_nullable=False)
        batch_op.alter_column('offspring_brood', new_column_name='offspring_count',
                               existing_type=sa.String(length=60), existing_nullable=False)
        batch_op.alter_column('home_turf', new_column_name='habitat',
                               existing_type=sa.Text(), existing_nullable=False)

    relationship_status_enum.drop(op.get_bind(), checkfirst=True)
