# Generated by Django 3.0.5 on 2020-04-29 10:33

from decimal import Decimal
from django.conf import settings
import django.contrib.postgres.fields.jsonb
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import django_measurement.models
import kda.core.utils.json_serializer
import kda.core.weight
import measurement.measures.mass


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Fulfillment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('private_metadata', django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict, encoder=kda.core.utils.json_serializer.CustomJsonEncoder, null=True)),
                ('metadata', django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict, encoder=kda.core.utils.json_serializer.CustomJsonEncoder, null=True)),
                ('fulfillment_order', models.PositiveIntegerField(editable=False)),
                ('status', models.CharField(choices=[('fulfilled', 'Fulfilled'), ('canceled', 'Canceled')], default='fulfilled', max_length=32)),
                ('tracking_number', models.CharField(blank=True, default='', max_length=255)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ('pk',),
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('private_metadata', django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict, encoder=kda.core.utils.json_serializer.CustomJsonEncoder, null=True)),
                ('metadata', django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict, encoder=kda.core.utils.json_serializer.CustomJsonEncoder, null=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('status', models.CharField(choices=[('draft', 'Draft'), ('unfulfilled', 'Unfulfilled'), ('partially fulfilled', 'Partially fulfilled'), ('fulfilled', 'Fulfilled'), ('canceled', 'Canceled')], default='unfulfilled', max_length=32)),
                ('language_code', models.CharField(default='en-us', max_length=35)),
                ('tracking_client_id', models.CharField(blank=True, editable=False, max_length=36)),
                ('user_email', models.EmailField(blank=True, default='', max_length=254)),
                ('currency', models.CharField(default='KES', max_length=3)),
                ('shipping_method', models.CharField(blank=True, default=None, editable=False, max_length=255, null=True)),
                ('shipping_method_name', models.CharField(blank=True, default=None, editable=False, max_length=255, null=True)),
                ('shipping_price_net_amount', models.DecimalField(decimal_places=2, default=0, editable=False, max_digits=12)),
                ('shipping_price_gross_amount', models.DecimalField(decimal_places=2, default=0, editable=False, max_digits=12)),
                ('token', models.CharField(blank=True, max_length=36, unique=True)),
                ('checkout_token', models.CharField(blank=True, max_length=36)),
                ('total_net_amount', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('total_gross_amount', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('discount_amount', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('discount_name', models.CharField(blank=True, max_length=255, null=True)),
                ('translated_discount_name', models.CharField(blank=True, max_length=255, null=True)),
                ('display_gross_prices', models.BooleanField(default=True)),
                ('customer_note', models.TextField(blank=True, default='')),
                ('weight', django_measurement.models.MeasurementField(default=kda.core.weight.zero_weight, measurement=measurement.measures.mass.Mass)),
                ('billing_address', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='account.Address')),
                ('shipping_address', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='account.Address')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-pk',),
                'permissions': (('manage_orders', 'Manage orders.'),),
            },
        ),
        migrations.CreateModel(
            name='OrderLine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('digital_content_url', models.CharField(max_length=255)),
                ('product_name', models.CharField(max_length=386)),
                ('variant_name', models.CharField(blank=True, default='', max_length=255)),
                ('translated_product_name', models.CharField(blank=True, default='', max_length=386)),
                ('translated_variant_name', models.CharField(blank=True, default='', max_length=255)),
                ('product_sku', models.CharField(max_length=255)),
                ('is_shipping_required', models.BooleanField()),
                ('quantity', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('quantity_fulfilled', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('currency', models.CharField(default='KES', max_length=3)),
                ('unit_price_net_amount', models.DecimalField(decimal_places=2, max_digits=12)),
                ('unit_price_gross_amount', models.DecimalField(decimal_places=2, max_digits=12)),
                ('tax_rate', models.DecimalField(decimal_places=2, default=Decimal('0.0'), max_digits=5)),
                ('order', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='lines', to='order.Order')),
            ],
            options={
                'ordering': ('pk',),
            },
        ),
        migrations.CreateModel(
            name='OrderEvent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('type', models.CharField(choices=[('DRAFT_CREATED', 'draft_created'), ('DRAFT_ADDED_PRODUCTS', 'draft_added_products'), ('DRAFT_REMOVED_PRODUCTS', 'draft_removed_products'), ('PLACED', 'placed'), ('PLACED_FROM_DRAFT', 'placed_from_draft'), ('OVERSOLD_ITEMS', 'oversold_items'), ('CANCELED', 'canceled'), ('ORDER_MARKED_AS_PAID', 'order_marked_as_paid'), ('ORDER_FULLY_PAID', 'order_fully_paid'), ('UPDATED_ADDRESS', 'updated_address'), ('EMAIL_SENT', 'email_sent'), ('PAYMENT_CAPTURED', 'payment_captured'), ('PAYMENT_REFUNDED', 'payment_refunded'), ('PAYMENT_VOIDED', 'payment_voided'), ('PAYMENT_FAILED', 'payment_failed'), ('FULFILLMENT_CANCELED', 'fulfillment_canceled'), ('FULFILLMENT_RESTOCKED_ITEMS', 'fulfillment_restocked_items'), ('FULFILLMENT_FULFILLED_ITEMS', 'fulfillment_fulfilled_items'), ('TRACKING_UPDATED', 'tracking_updated'), ('NOTE_ADDED', 'note_added'), ('OTHER', 'other')], max_length=255)),
                ('parameters', django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict, encoder=kda.core.utils.json_serializer.CustomJsonEncoder)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='events', to='order.Order')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('date',),
            },
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=255)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('url', models.URLField(max_length=2048)),
                ('order', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='order.Order')),
            ],
        ),
        migrations.CreateModel(
            name='FulfillmentLine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField()),
                ('fulfillment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lines', to='order.Fulfillment')),
                ('order_line', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='order.OrderLine')),
            ],
        ),
        migrations.AddField(
            model_name='fulfillment',
            name='order',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='fulfillments', to='order.Order'),
        ),
    ]
