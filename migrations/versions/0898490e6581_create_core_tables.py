"""create core tables

Revision ID: 0898490e6581
Revises: 
Create Date: 2025-09-30 20:07:20.476090

"""
from __future__ import annotations

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = '0898490e6581'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    batch_status = sa.Enum('open', 'closed', 'cancelled', name='batch_status', native_enum=False)
    slice_status = sa.Enum('available', 'reserved', 'sold', 'discarded', name='slice_status', native_enum=False)
    order_status = sa.Enum('pending', 'confirmed', 'cancelled', 'completed', name='order_status', native_enum=False)

    op.create_table(
        'stores',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column('name', sa.String(length=150), nullable=False),
        sa.Column('slug', sa.String(length=150), nullable=False),
        sa.Column('timezone', sa.String(length=64), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.text('TRUE')),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.Column('created_by', sa.String(length=64), nullable=False),
        sa.Column('updated_by', sa.String(length=64), nullable=True),
        sa.UniqueConstraint('slug', name='uq_stores_slug'),
    )

    op.create_table(
        'menu_items',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column('store_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('name', sa.String(length=150), nullable=False),
        sa.Column('slug', sa.String(length=150), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('price', sa.Numeric(10, 2), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.text('TRUE')),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.Column('created_by', sa.String(length=64), nullable=False),
        sa.Column('updated_by', sa.String(length=64), nullable=True),
        sa.ForeignKeyConstraint(['store_id'], ['stores.id'], ondelete='CASCADE', name='fk_menu_items_store_id_stores'),
        sa.UniqueConstraint('store_id', 'slug', name='uq_menu_items_store_slug'),
    )
    op.create_index('ix_menu_items_store_id', 'menu_items', ['store_id'])

    op.create_table(
        'orders',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column('store_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('order_code', sa.String(length=32), nullable=False),
        sa.Column('status', order_status, nullable=False, server_default='pending'),
        sa.Column('customer_name', sa.String(length=150), nullable=True),
        sa.Column('customer_phone', sa.String(length=32), nullable=True),
        sa.Column('reserved_until', sa.DateTime(timezone=True), nullable=True),
        sa.Column('total_amount', sa.Numeric(12, 2), nullable=False, server_default='0'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.Column('created_by', sa.String(length=64), nullable=False),
        sa.Column('updated_by', sa.String(length=64), nullable=True),
        sa.ForeignKeyConstraint(['store_id'], ['stores.id'], ondelete='CASCADE', name='fk_orders_store_id_stores'),
        sa.UniqueConstraint('store_id', 'order_code', name='uq_orders_store_code'),
    )
    op.create_index('ix_orders_store_id', 'orders', ['store_id'])
    op.create_index('ix_orders_status', 'orders', ['status'])

    op.create_table(
        'pizza_batches',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column('store_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('menu_item_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('reference', sa.String(length=64), nullable=False),
        sa.Column('total_slices', sa.Integer(), nullable=False),
        sa.Column('opened_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.Column('closed_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('status', batch_status, nullable=False, server_default='open'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.Column('created_by', sa.String(length=64), nullable=False),
        sa.Column('updated_by', sa.String(length=64), nullable=True),
        sa.ForeignKeyConstraint(['store_id'], ['stores.id'], ondelete='CASCADE', name='fk_pizza_batches_store_id_stores'),
        sa.ForeignKeyConstraint(['menu_item_id'], ['menu_items.id'], ondelete='RESTRICT', name='fk_pizza_batches_menu_item_id_menu_items'),
        sa.UniqueConstraint('store_id', 'reference', name='uq_pizza_batches_store_reference'),
    )
    op.create_index('ix_pizza_batches_store_id', 'pizza_batches', ['store_id'])
    op.create_index('ix_pizza_batches_menu_item_id', 'pizza_batches', ['menu_item_id'])
    op.create_index('ix_pizza_batches_status', 'pizza_batches', ['status'])

    op.create_table(
        'order_items',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column('store_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('order_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('menu_item_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('quantity', sa.Integer(), nullable=False, server_default='1'),
        sa.Column('unit_price', sa.Numeric(12, 2), nullable=False),
        sa.Column('notes', sa.String(length=250), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.Column('created_by', sa.String(length=64), nullable=False),
        sa.Column('updated_by', sa.String(length=64), nullable=True),
        sa.ForeignKeyConstraint(['store_id'], ['stores.id'], ondelete='CASCADE', name='fk_order_items_store_id_stores'),
        sa.ForeignKeyConstraint(['order_id'], ['orders.id'], ondelete='CASCADE', name='fk_order_items_order_id_orders'),
        sa.ForeignKeyConstraint(['menu_item_id'], ['menu_items.id'], ondelete='RESTRICT', name='fk_order_items_menu_item_id_menu_items'),
        sa.UniqueConstraint('order_id', 'menu_item_id', name='uq_order_items_order_menu_item'),
    )
    op.create_index('ix_order_items_store_id', 'order_items', ['store_id'])
    op.create_index('ix_order_items_order_id', 'order_items', ['order_id'])

    op.create_table(
        'slices',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column('store_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('batch_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('sequence_number', sa.Integer(), nullable=False),
        sa.Column('status', slice_status, nullable=False, server_default='available'),
        sa.Column('reserved_until', sa.DateTime(timezone=True), nullable=True),
        sa.Column('order_item_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.Column('created_by', sa.String(length=64), nullable=False),
        sa.Column('updated_by', sa.String(length=64), nullable=True),
        sa.ForeignKeyConstraint(['store_id'], ['stores.id'], ondelete='CASCADE', name='fk_slices_store_id_stores'),
        sa.ForeignKeyConstraint(['batch_id'], ['pizza_batches.id'], ondelete='CASCADE', name='fk_slices_batch_id_pizza_batches'),
        sa.ForeignKeyConstraint(['order_item_id'], ['order_items.id'], ondelete='SET NULL', name='fk_slices_order_item_id_order_items'),
        sa.UniqueConstraint('batch_id', 'sequence_number', name='uq_slices_batch_sequence'),
    )
    op.create_index('ix_slices_store_id', 'slices', ['store_id'])
    op.create_index('ix_slices_status', 'slices', ['status'])
    op.create_index('ix_slices_order_item_id', 'slices', ['order_item_id'])


def downgrade() -> None:
    op.drop_index('ix_slices_order_item_id', table_name='slices')
    op.drop_index('ix_slices_status', table_name='slices')
    op.drop_index('ix_slices_store_id', table_name='slices')
    op.drop_table('slices')

    op.drop_index('ix_order_items_order_id', table_name='order_items')
    op.drop_index('ix_order_items_store_id', table_name='order_items')
    op.drop_table('order_items')

    op.drop_index('ix_pizza_batches_status', table_name='pizza_batches')
    op.drop_index('ix_pizza_batches_menu_item_id', table_name='pizza_batches')
    op.drop_index('ix_pizza_batches_store_id', table_name='pizza_batches')
    op.drop_table('pizza_batches')

    op.drop_index('ix_orders_status', table_name='orders')
    op.drop_index('ix_orders_store_id', table_name='orders')
    op.drop_table('orders')

    op.drop_index('ix_menu_items_store_id', table_name='menu_items')
    op.drop_table('menu_items')

    op.drop_table('stores')
