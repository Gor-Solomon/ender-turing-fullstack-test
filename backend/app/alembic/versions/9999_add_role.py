"""add role"""
from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes

revision = '9999'
down_revision = 'fe56fa70289e'
branch_labels = None
depends_on = None

def upgrade():
    op.add_column('user', sa.Column('role', sa.String(length=50), server_default='member', nullable=False))

def downgrade():
    op.drop_column('user', 'role')
