"""Add Roles and Permissios functional

Revision ID: 0003
Revises: 0002
Create Date: 2024-09-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0002'
down_revision = '0001'
branch_labels = None
depends_on = None

def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('role',
        sa.Column(name='id',
                type_=sa.Integer(),
                nullable=False),
        sa.Column(name="title",
                type_=sa.String(length=255),
                nullable=False,
                comment="Роль"
                ),
        sa.PrimaryKeyConstraint('id')
        )
    
    op.create_table(
        'permission',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('internal_name', sa.String(), nullable=False, unique=True, index=True),
        sa.Column('title', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    # Шаг 1: Добавление столбца с nullable=True
    op.add_column('role', sa.Column('internal_name', sa.String(), nullable=True, unique=True))

    # Шаг 2: Заполнение столбца для существующих строк
    op.execute("UPDATE role SET internal_name = 'default_value' WHERE internal_name IS NULL")

    # Шаг 3: Изменение столбца на NOT NULL
    op.alter_column('role', 'internal_name', nullable=False)

    # Создание индекса для нового столбца
    op.create_index(op.f('ix_role_internal_name'), 'role', ['internal_name'], unique=True)

    op.create_table('role_permission_link',
                    sa.Column('role_id', sa.Integer(), nullable=False),
                    sa.Column('permission_id', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['role_id'], ['role.id'], ),
                    sa.ForeignKeyConstraint(['permission_id'], ['permission.id'], ),
                    sa.PrimaryKeyConstraint('role_id', 'permission_id')
                    )
    

    # ### end Alembic commands ###

def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('permission')
    op.drop_table('role')
    op.drop_table('role_permission_link')
    # ### end Alembic commands ###