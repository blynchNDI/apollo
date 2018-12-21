"""empty message

Revision ID: 872591ee58b4
Revises: 
Create Date: 2018-12-18 13:20:00.714150

"""
from uuid import uuid4

from alembic import op
from flask_principal import Permission
from flask_security.utils import encrypt_password
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from sqlalchemy.sql import text
import sqlalchemy_utils

from apollo.frontend import permissions
from apollo.models import (
    Form, Message, Participant, Submission, SubmissionVersion)

# revision identifiers, used by Alembic.
revision = '872591ee58b4'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('deployment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('hostnames', postgresql.ARRAY(sa.String()), nullable=False),
    sa.Column('allow_observer_submission_edit', sa.Boolean(), nullable=True),
    sa.Column('logo', sa.String(), nullable=True),
    sa.Column('include_rejected_in_votes', sa.Boolean(), nullable=True),
    sa.Column('is_initialized', sa.Boolean(), nullable=True),
    sa.Column('dashboard_full_locations', sa.Boolean(), nullable=True),
    sa.Column('uuid', postgresql.UUID(as_uuid=True), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('phone',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('number', sa.String(), nullable=False),
    sa.Column('uuid', postgresql.UUID(as_uuid=True), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('number')
    )
    op.create_table('form_set',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('slug', sa.String(), nullable=True),
    sa.Column('deployment_id', sa.Integer(), nullable=False),
    sa.Column('uuid', postgresql.UUID(as_uuid=True), nullable=False),
    sa.ForeignKeyConstraint(['deployment_id'], ['deployment.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('location_set',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('slug', sa.String(), nullable=True),
    sa.Column('deployment_id', sa.Integer(), nullable=False),
    sa.Column('uuid', postgresql.UUID(as_uuid=True), nullable=False),
    sa.ForeignKeyConstraint(['deployment_id'], ['deployment.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('permission',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('deployment_id', sa.Integer(), nullable=False),
    sa.Column('uuid', postgresql.UUID(as_uuid=True), nullable=False),
    sa.ForeignKeyConstraint(['deployment_id'], ['deployment.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('resource',
    sa.Column('resource_id', sa.Integer(), nullable=False),
    sa.Column('resource_type', sa.String(), nullable=False),
    sa.Column('deployment_id', sa.Integer(), nullable=False),
    sa.Column('uuid', postgresql.UUID(as_uuid=True), nullable=False),
    sa.ForeignKeyConstraint(['deployment_id'], ['deployment.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('resource_id')
    )
    op.create_table('role',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('deployment_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('uuid', postgresql.UUID(as_uuid=True), nullable=False),
    sa.ForeignKeyConstraint(['deployment_id'], ['deployment.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('deployment_id', 'name')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('deployment_id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('last_name', sa.String(), nullable=True),
    sa.Column('first_name', sa.String(), nullable=True),
    sa.Column('active', sa.Boolean(), nullable=True),
    sa.Column('confirmed_at', sa.DateTime(), nullable=True),
    sa.Column('current_login_at', sa.DateTime(), nullable=True),
    sa.Column('last_login_at', sa.DateTime(), nullable=True),
    sa.Column('current_login_ip', sa.String(), nullable=True),
    sa.Column('last_login_ip', sa.String(), nullable=True),
    sa.Column('login_count', sa.Integer(), nullable=True),
    sa.Column('uuid', postgresql.UUID(as_uuid=True), nullable=False),
    sa.ForeignKeyConstraint(['deployment_id'], ['deployment.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('form',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('prefix', sa.String(), nullable=False),
    sa.Column('form_type', sqlalchemy_utils.types.choice.ChoiceType(Form.FORM_TYPES), nullable=False),
    sa.Column('require_exclamation', sa.Boolean(), nullable=True),
    sa.Column('data', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('version_identifier', sa.String(), nullable=True),
    sa.Column('form_set_id', sa.Integer(), nullable=False),
    sa.Column('resource_id', sa.Integer(), nullable=True),
    sa.Column('quality_checks', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('party_mappings', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('calculate_moe', sa.Boolean(), nullable=True),
    sa.Column('accredited_voters_tag', sa.String(), nullable=True),
    sa.Column('quality_checks_enabled', sa.Boolean(), nullable=True),
    sa.Column('invalid_votes_tag', sa.String(), nullable=True),
    sa.Column('registered_voters_tag', sa.String(), nullable=True),
    sa.Column('blank_votes_tag', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['form_set_id'], ['form_set.id'], ),
    sa.ForeignKeyConstraint(['resource_id'], ['resource.resource_id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('location_data_field',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('location_set_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('label', sa.String(), nullable=False),
    sa.Column('visible_in_lists', sa.Boolean(), nullable=True),
    sa.Column('resource_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['location_set_id'], ['location_set.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['resource_id'], ['resource.resource_id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('location_type',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('is_administrative', sa.Boolean(), nullable=True),
    sa.Column('is_political', sa.Boolean(), nullable=True),
    sa.Column('has_registered_voters', sa.Boolean(), nullable=True),
    sa.Column('slug', sa.String(), nullable=True),
    sa.Column('location_set_id', sa.Integer(), nullable=False),
    sa.Column('uuid', postgresql.UUID(as_uuid=True), nullable=False),
    sa.ForeignKeyConstraint(['location_set_id'], ['location_set.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('participant_set',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('slug', sa.String(), nullable=True),
    sa.Column('location_set_id', sa.Integer(), nullable=False),
    sa.Column('deployment_id', sa.Integer(), nullable=False),
    sa.Column('uuid', postgresql.UUID(as_uuid=True), nullable=False),
    sa.ForeignKeyConstraint(['deployment_id'], ['deployment.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['location_set_id'], ['location_set.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('role_resource_permissions',
    sa.Column('role_id', sa.Integer(), nullable=False),
    sa.Column('resource_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['resource_id'], ['resource.resource_id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['role_id'], ['role.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('role_id', 'resource_id')
    )
    op.create_table('roles_permissions',
    sa.Column('role_id', sa.Integer(), nullable=False),
    sa.Column('permission_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['permission_id'], ['permission.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['role_id'], ['role.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('role_id', 'permission_id')
    )
    op.create_table('roles_users',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('role_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['role_id'], ['role.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('user_id', 'role_id')
    )
    op.create_table('sample',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('location_set_id', sa.Integer(), nullable=False),
    sa.Column('uuid', postgresql.UUID(as_uuid=True), nullable=False),
    sa.ForeignKeyConstraint(['location_set_id'], ['location_set.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_resource_permissions',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('resource_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['resource_id'], ['resource.resource_id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('user_id', 'resource_id')
    )
    op.create_table('user_upload',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('deployment_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('upload_filename', sa.String(), nullable=True),
    sa.Column('uuid', postgresql.UUID(as_uuid=True), nullable=False),
    sa.ForeignKeyConstraint(['deployment_id'], ['deployment.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users_permissions',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('permission_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['permission_id'], ['permission.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('user_id', 'permission_id')
    )
    op.create_table('event',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('start', sa.DateTime(), nullable=False),
    sa.Column('end', sa.DateTime(), nullable=False),
    sa.Column('form_set_id', sa.Integer(), nullable=True),
    sa.Column('resource_id', sa.Integer(), nullable=True),
    sa.Column('location_set_id', sa.Integer(), nullable=True),
    sa.Column('participant_set_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['form_set_id'], ['form_set.id'], ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['location_set_id'], ['location_set.id'], ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['participant_set_id'], ['participant_set.id'], ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['resource_id'], ['resource.resource_id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('location',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('code', sa.String(), nullable=False),
    sa.Column('registered_voters', sa.Integer(), nullable=True),
    sa.Column('location_set_id', sa.Integer(), nullable=False),
    sa.Column('location_type_id', sa.Integer(), nullable=False),
    sa.Column('lat', sa.Float(), nullable=True),
    sa.Column('lon', sa.Float(), nullable=True),
    sa.Column('extra_data', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('uuid', postgresql.UUID(as_uuid=True), nullable=False),
    sa.ForeignKeyConstraint(['location_set_id'], ['location_set.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['location_type_id'], ['location_type.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('location_set_id', 'code')
    )
    op.create_index(op.f('ix_location_code'), 'location', ['code'], unique=False)
    op.create_table('location_type_path',
    sa.Column('location_set_id', sa.Integer(), nullable=False),
    sa.Column('ancestor_id', sa.Integer(), nullable=False),
    sa.Column('descendant_id', sa.Integer(), nullable=False),
    sa.Column('depth', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['ancestor_id'], ['location_type.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['descendant_id'], ['location_type.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['location_set_id'], ['location_set.id']),
    sa.PrimaryKeyConstraint('ancestor_id', 'descendant_id')
    )
    op.create_index('location_type_paths_ancestor_idx', 'location_type_path', ['ancestor_id'], unique=False)
    op.create_index('location_type_paths_descendant_idx', 'location_type_path', ['descendant_id'], unique=False)
    op.create_table('participant_data_field',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('participant_set_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('label', sa.String(), nullable=False),
    sa.Column('visible_in_lists', sa.Boolean(), nullable=True),
    sa.Column('resource_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['participant_set_id'], ['participant_set.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['resource_id'], ['resource.resource_id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('participant_group_type',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('participant_set_id', sa.Integer(), nullable=False),
    sa.Column('uuid', postgresql.UUID(as_uuid=True), nullable=False),
    sa.ForeignKeyConstraint(['participant_set_id'], ['participant_set.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('participant_partner',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('participant_set_id', sa.Integer(), nullable=False),
    sa.Column('uuid', postgresql.UUID(as_uuid=True), nullable=False),
    sa.ForeignKeyConstraint(['participant_set_id'], ['participant_set.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('participant_role',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('participant_set_id', sa.Integer(), nullable=False),
    sa.Column('uuid', postgresql.UUID(as_uuid=True), nullable=False),
    sa.ForeignKeyConstraint(['participant_set_id'], ['participant_set.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('location_path',
    sa.Column('location_set_id', sa.Integer(), nullable=False),
    sa.Column('ancestor_id', sa.Integer(), nullable=False),
    sa.Column('descendant_id', sa.Integer(), nullable=False),
    sa.Column('depth', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['ancestor_id'], ['location.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['descendant_id'], ['location.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['location_set_id'], ['location_set.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('ancestor_id', 'descendant_id')
    )
    op.create_index('location_paths_ancestor_idx', 'location_path', ['ancestor_id'], unique=False)
    op.create_index('location_paths_descendant_idx', 'location_path', ['descendant_id'], unique=False)
    op.create_table('participant',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('participant_id', sa.String(), nullable=True),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.Column('partner_id', sa.Integer(), nullable=True),
    sa.Column('supervisor_id', sa.Integer(), nullable=True),
    sa.Column('gender', sqlalchemy_utils.types.choice.ChoiceType(Participant.GENDER), nullable=True),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('location_id', sa.Integer(), nullable=True),
    sa.Column('participant_set_id', sa.Integer(), nullable=False),
    sa.Column('message_count', sa.Integer(), nullable=True),
    sa.Column('accurate_message_count', sa.Integer(), nullable=True),
    sa.Column('completion_rating', sa.Float(), nullable=True),
    sa.Column('device_id', sa.String(), nullable=True),
    sa.Column('password', sa.String(), nullable=True),
    sa.Column('extra_data', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('uuid', postgresql.UUID(as_uuid=True), nullable=False),
    sa.ForeignKeyConstraint(['location_id'], ['location.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['participant_set_id'], ['participant_set.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['partner_id'], ['participant_partner.id'], ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['role_id'], ['participant_role.id'], ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['supervisor_id'], ['participant.id'], ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('participant_group',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('group_type_id', sa.Integer(), nullable=False),
    sa.Column('participant_set_id', sa.Integer(), nullable=False),
    sa.Column('uuid', postgresql.UUID(as_uuid=True), nullable=False),
    sa.ForeignKeyConstraint(['group_type_id'], ['participant_group_type.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['participant_set_id'], ['participant_set.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('samples_locations',
    sa.Column('sample_id', sa.Integer(), nullable=False),
    sa.Column('location_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['location_id'], ['location.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['sample_id'], ['sample.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('sample_id', 'location_id')
    )
    op.create_table('participant_groups_participants',
    sa.Column('group_id', sa.Integer(), nullable=False),
    sa.Column('participant_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['group_id'], ['participant_group.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['participant_id'], ['participant.id'], ondelete='CASCADE')
    )
    op.create_table('participant_phone',
    sa.Column('participant_id', sa.Integer(), nullable=False),
    sa.Column('phone_id', sa.Integer(), nullable=False),
    sa.Column('last_seen', sa.DateTime(), nullable=True),
    sa.Column('verified', sa.Boolean(), nullable=True),
    sa.Column('uuid', postgresql.UUID(as_uuid=True), nullable=False),
    sa.ForeignKeyConstraint(['participant_id'], ['participant.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['phone_id'], ['phone.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('participant_id', 'phone_id')
    )
    op.create_table('submission',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('deployment_id', sa.Integer(), nullable=False),
    sa.Column('event_id', sa.Integer(), nullable=False),
    sa.Column('form_id', sa.Integer(), nullable=False),
    sa.Column('participant_id', sa.Integer(), nullable=True),
    sa.Column('location_id', sa.Integer(), nullable=False),
    sa.Column('data', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('extra_data', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('submission_type', sqlalchemy_utils.types.choice.ChoiceType(Submission.SUBMISSION_TYPES), nullable=True),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('updated', sa.DateTime(), nullable=True),
    sa.Column('sender_verified', sa.Boolean(), nullable=True),
    sa.Column('quarantine_status', sqlalchemy_utils.types.choice.ChoiceType(Submission.QUARANTINE_STATUSES), nullable=True),
    sa.Column('verification_status', sqlalchemy_utils.types.choice.ChoiceType(Submission.VERIFICATION_STATUSES), nullable=True),
    sa.Column('incident_description', sa.String(), nullable=True),
    sa.Column('incident_status', sqlalchemy_utils.types.choice.ChoiceType(Submission.INCIDENT_STATUSES), nullable=True),
    sa.Column('overridden_fields', postgresql.ARRAY(sa.String()), nullable=True),
    sa.Column('conflicts', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('uuid', postgresql.UUID(as_uuid=True), nullable=False),
    sa.ForeignKeyConstraint(['deployment_id'], ['deployment.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['event_id'], ['event.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['form_id'], ['form.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['location_id'], ['location.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['participant_id'], ['participant.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('submission_data_idx', 'submission', ['data'], unique=False, postgresql_using='gin')
    op.create_table('message',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('direction', sqlalchemy_utils.types.choice.ChoiceType(Message.DIRECTIONS), nullable=False),
    sa.Column('recipient', sa.String(), nullable=True),
    sa.Column('sender', sa.String(), nullable=True),
    sa.Column('text', sa.String(), nullable=True),
    sa.Column('received', sa.DateTime(), nullable=True),
    sa.Column('delivered', sa.DateTime(), nullable=True),
    sa.Column('deployment_id', sa.Integer(), nullable=False),
    sa.Column('event_id', sa.Integer(), nullable=False),
    sa.Column('submission_id', sa.Integer(), nullable=True),
    sa.Column('participant_id', sa.Integer(), nullable=True),
    sa.Column('uuid', postgresql.UUID(as_uuid=True), nullable=False),
    sa.ForeignKeyConstraint(['deployment_id'], ['deployment.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['event_id'], ['event.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['participant_id'], ['participant.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['submission_id'], ['submission.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_message_received'), 'message', ['received'], unique=False)
    op.create_table('submission_comment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('submission_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('comment', sa.String(), nullable=True),
    sa.Column('submit_date', sa.DateTime(), nullable=True),
    sa.Column('deployment_id', sa.Integer(), nullable=False),
    sa.Column('uuid', postgresql.UUID(as_uuid=True), nullable=False),
    sa.ForeignKeyConstraint(['deployment_id'], ['deployment.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['submission_id'], ['submission.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('submission_version',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('submission_id', sa.Integer(), nullable=False),
    sa.Column('data', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('channel', sqlalchemy_utils.types.choice.ChoiceType(SubmissionVersion.CHANNEL_CHOICES), nullable=True),
    sa.Column('deployment_id', sa.Integer(), nullable=False),
    sa.Column('identity', sa.String(), nullable=False),
    sa.Column('uuid', postgresql.UUID(as_uuid=True), nullable=False),
    sa.ForeignKeyConstraint(['deployment_id'], ['deployment.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['submission_id'], ['submission.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )

    # ----- initial fixtures -----
    conn = op.get_bind()
    conn.execute(text("""INSERT INTO deployment (
        id, name, hostnames, allow_observer_submission_edit,
        include_rejected_in_votes, is_initialized, dashboard_full_locations,
        uuid)
        VALUES (1, 'Default', '{\"localhost\"}', 't', 'f', 'f', 't',
        :uuid)"""), uuid=uuid4().hex)
    op.execute("""
    SELECT nextval(pg_get_serial_sequence('deployment', 'id'))
    """)
    conn.execute(text("""INSERT INTO resource (
        resource_id, resource_type, deployment_id, uuid)
        VALUES (1, 'event', 1, :uuid)"""), uuid=uuid4().hex)
    op.execute("""
    SELECT nextval(pg_get_serial_sequence('resource', 'resource_id'))
    """)
    op.execute("""INSERT INTO event (
        id, name, start, \"end\", resource_id)
        VALUES (1, 'Default', '1970-01-01 00:00:00', '1970-01-01 00:00:00', 1)
        """)
    op.execute("""
    SELECT nextval(pg_get_serial_sequence('event', 'id'))
    """)
    conn.execute(text("""INSERT INTO role (
        id, deployment_id, name, uuid) VALUES (1, 1, 'admin', :uuid)"""),
                 uuid=uuid4().hex)
    op.execute("""
    SELECT nextval(pg_get_serial_sequence('role', 'id'))
    """)
    conn.execute(text("""INSERT INTO role (
        id, deployment_id, name, uuid) VALUES (2, 1, 'analyst', :uuid)"""),
                 uuid=uuid4().hex)
    op.execute("""
    SELECT nextval(pg_get_serial_sequence('role', 'id'))
    """)
    conn.execute(text("""INSERT INTO role (
        id, deployment_id, name, uuid) VALUES (3, 1, 'manager', :uuid)"""),
                 uuid=uuid4().hex)
    op.execute("""
    SELECT nextval(pg_get_serial_sequence('role', 'id'))
    """)
    conn.execute(text("""INSERT INTO role (
        id, deployment_id, name, uuid) VALUES (4, 1, 'clerk', :uuid)"""),
        uuid=uuid4().hex)
    op.execute("""
    SELECT nextval(pg_get_serial_sequence('role', 'id'))
    """)
    password = encrypt_password('admin')
    conn.execute(text("""INSERT INTO \"user\" (
        id, deployment_id, email, username, password, active, uuid)
        VALUES (1, 1, 'root@localhost', 'admin',
        :password, 't', :uuid)"""), password=password, uuid=uuid4().hex)
    op.execute("INSERT INTO roles_users (user_id, role_id) VALUES (1, 1)")
    op.execute("""
    SELECT nextval(pg_get_serial_sequence('user', 'id'))
    """)

    for name in dir(permissions):
        item = getattr(permissions, name, None)
        if isinstance(item, Permission):
            for need in item.needs:
                if need.method == 'action':
                    conn.execute(text("""INSERT INTO permission (name, deployment_id, uuid)
                                 VALUES (:value, 1, :uuid)"""), uuid=uuid4().hex,
                                 value=need.value)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('submission_version')
    op.drop_table('submission_comment')
    op.drop_index(op.f('ix_message_received'), table_name='message')
    op.drop_table('message')
    op.drop_index('submission_data_idx', table_name='submission')
    op.drop_table('submission')
    op.drop_table('participant_phone')
    op.drop_table('participant_groups_participants')
    op.drop_table('samples_locations')
    op.drop_table('participant_group')
    op.drop_table('participant')
    op.drop_index('location_paths_descendant_idx', table_name='location_path')
    op.drop_index('location_paths_ancestor_idx', table_name='location_path')
    op.drop_table('location_path')
    op.drop_table('participant_role')
    op.drop_table('participant_partner')
    op.drop_table('participant_group_type')
    op.drop_table('participant_data_field')
    op.drop_index('location_type_paths_descendant_idx', table_name='location_type_path')
    op.drop_index('location_type_paths_ancestor_idx', table_name='location_type_path')
    op.drop_table('location_type_path')
    op.drop_index(op.f('ix_location_code'), table_name='location')
    op.drop_table('location')
    op.drop_table('event')
    op.drop_table('users_permissions')
    op.drop_table('user_upload')
    op.drop_table('user_resource_permissions')
    op.drop_table('sample')
    op.drop_table('roles_users')
    op.drop_table('roles_permissions')
    op.drop_table('role_resource_permissions')
    op.drop_table('participant_set')
    op.drop_table('location_type')
    op.drop_table('location_data_field')
    op.drop_table('form')
    op.drop_table('user')
    op.drop_table('role')
    op.drop_table('resource')
    op.drop_table('permission')
    op.drop_table('location_set')
    op.drop_table('form_set')
    op.drop_table('phone')
    op.drop_table('deployment')
    # ### end Alembic commands ###
