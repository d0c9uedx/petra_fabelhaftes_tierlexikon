"""Fabelwesen-Kategorie und Taxonomie-Felder (Gattung/Familie)

Revision ID: a1f4c8d72b30
Revises: de8e69a98c9a
Create Date: 2026-08-22 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a1f4c8d72b30'
down_revision = 'de8e69a98c9a'
branch_labels = None
depends_on = None


# Enum-Spalte um FABELWESEN erweitern. Auf SQLite steuert der CHECK-Constraint
# die erlaubten Werte; alle bestehenden Werte bleiben gültig, daher reicht das
# Neuanlegen der Spalte ohne Datenmigration.
OLD_CATEGORY_ENUM = sa.Enum(
    'VOGEL', 'FISCH', 'INSEKT', 'SAEUGETIER', 'SONSTIGES_LANDTIER',
    name='animalcategory',
)
NEW_CATEGORY_ENUM = sa.Enum(
    'VOGEL', 'FISCH', 'INSEKT', 'SAEUGETIER', 'SONSTIGES_LANDTIER', 'FABELWESEN',
    name='animalcategory',
)


def upgrade() -> None:
    NEW_CATEGORY_ENUM.create(op.get_bind(), checkfirst=True)

    with op.batch_alter_table('animals') as batch_op:
        batch_op.alter_column(
            'category',
            existing_type=OLD_CATEGORY_ENUM,
            type_=NEW_CATEGORY_ENUM,
            existing_nullable=False,
        )
        # Taxonomie-Felder, bewusst nullable — siehe
        # docs/adr/0009-taxonomie-felder-gattung-familie.md.
        batch_op.add_column(sa.Column('genus', sa.String(length=120), nullable=True))
        batch_op.add_column(sa.Column('family', sa.String(length=120), nullable=True))


def downgrade() -> None:
    with op.batch_alter_table('animals') as batch_op:
        batch_op.drop_column('family')
        batch_op.drop_column('genus')
        batch_op.alter_column(
            'category',
            existing_type=NEW_CATEGORY_ENUM,
            type_=OLD_CATEGORY_ENUM,
            existing_nullable=False,
        )

    # Der Enum-Typ selbst bleibt nach dem Downgrade bestehen (die übrigen Werte
    # werden weiterhin genutzt); ein Entfernen einzelner Werte ist auf Postgres
    # ohnehin nicht vorgesehen.
