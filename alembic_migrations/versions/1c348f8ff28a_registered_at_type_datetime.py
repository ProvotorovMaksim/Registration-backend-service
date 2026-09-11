"""registered_at_type_DateTime

Revision ID: 1c348f8ff28a
Revises: 530cbf84e76b
Create Date: 2026-09-11 01:16:14.806434

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1c348f8ff28a'
down_revision: Union[str, Sequence[str], None] = '530cbf84e76b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column('users', 'registered_at',
               existing_type=sa.VARCHAR(),
               type_=sa.DateTime(),
               existing_nullable=True,
               postgresql_using='registered_at::timestamp without time zone')


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column('users', 'registered_at',
               existing_type=sa.DateTime(),
               type_=sa.VARCHAR(),
               existing_nullable=True,
               postgresql_using='registered_at::varchar')
