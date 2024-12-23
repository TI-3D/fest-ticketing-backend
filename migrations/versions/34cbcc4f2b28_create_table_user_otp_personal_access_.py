"""create table user, otp, personal access token, provider and event organizer

Revision ID: 4e992fd6cef9
Revises: 34cbcc4f2b28
Create Date: 2024-11-27 00:57:43.371404

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes


# revision identifiers, used by Alembic.
revision: str = '34cbcc4f2b28'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('user_id', sa.Uuid(), nullable=False),
    sa.Column('full_name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('email', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('gender', sa.Enum('MALE', 'FEMALE', name='gender'), nullable=False),
    sa.Column('birth_date', sa.DateTime(), nullable=True),
    sa.Column('phone_number', sqlmodel.sql.sqltypes.AutoString(length=16), nullable=True),
    sa.Column('nik', sqlmodel.sql.sqltypes.AutoString(length=16), nullable=True),
    sa.Column('address', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('role', sa.Enum('ADMIN', 'USER', 'EO', name='role'), nullable=False),
    sa.Column('password_hash', sqlmodel.sql.sqltypes.AutoString(length=255), nullable=False),
    sa.Column('profile_picture', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('email_verified_at', sa.DateTime(), nullable=True),
    sa.Column('embedding', type_=sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('user_id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('nik')
    )
    op.create_table('eventorganizers',
    sa.Column('organizer_id', sa.Uuid(), nullable=False),
    sa.Column('profile_picture', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('company_name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('company_pic', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
     sa.Column('company_email', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
     sa.Column('company_phone', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
     sa.Column('company_experience', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
     sa.Column('company_portofolio', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('company_address', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('status', sa.Enum('PENDING', 'ACTIVE', 'INACTIVE', name='organizerstatus'), nullable=False),
    sa.Column('user_id', sa.Uuid(), nullable=False),
    sa.Column('verified_at', sa.DateTime(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ),
    sa.PrimaryKeyConstraint('organizer_id')
    )
    op.create_table('otps',
    sa.Column('otp_id', sa.Integer(), nullable=False),
    sa.Column('otp_code', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('user_id', sa.Uuid(), nullable=False),
    sa.Column('hashed_otp', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('token_type', sa.Enum('REGISTRATION', 'LOGIN', 'PASSWORD_RESET', name='verificationtype'), nullable=False),
    sa.Column('expires_in', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ),
    sa.PrimaryKeyConstraint('otp_id')
    )
    op.create_index(op.f('ix_otps_otp_code'), 'otps', ['otp_code'], unique=False)
    op.create_table('personal_access_tokens',
    sa.Column('token_id', sa.Integer(), nullable=False),
    sa.Column('device_id', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('access_token', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('user_id', sa.Uuid(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('expires_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ),
    sa.PrimaryKeyConstraint('token_id')
    )
    op.create_index(op.f('ix_personal_access_tokens_access_token'), 'personal_access_tokens', ['access_token'], unique=True)
    op.create_table('providers',
    sa.Column('provider_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Uuid(), nullable=False),
    sa.Column('provider_name', sa.Enum('EMAIL', 'GOOGLE', 'FACEBOOK', 'TWITTER', name='providername'), nullable=False),
    sa.Column('external_provider_id', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ),
    sa.PrimaryKeyConstraint('provider_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('providers')
    op.drop_index(op.f('ix_personal_access_tokens_access_token'), table_name='personal_access_tokens')
    op.drop_table('personal_access_tokens')
    op.drop_index(op.f('ix_otps_otp_code'), table_name='otps')
    op.drop_table('otps')
    op.drop_table('eventorganizers')
    op.drop_table('users')
    
    op.execute("DROP TYPE IF EXISTS verificationtype")
    op.execute("DROP TYPE IF EXISTS gender")
    op.execute("DROP TYPE IF EXISTS role")
    op.execute("DROP TYPE IF EXISTS organizerstatus")
    op.execute("DROP TYPE IF EXISTS providername")    
    # ### end Alembic commands ###
