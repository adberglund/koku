# Generated by Django 2.2.9 on 2020-01-10 22:09

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion
import tenant_schemas.postgresql_backend.base
import json
import pkgutil
import uuid


# Functions from the following migrations need manual copying.
# Move them and any dependencies into this file, then update the
# RunPython operations to refer to the local versions:
# api.migrations.0001_initial_squashed_0008_auto_20190305_2015
def mig_0001_migrate_schema_name(apps, schema_editor, model_name):
    Model = apps.get_model('api', model_name)

    for current_model in Model.objects.all():
        cur_schema_name = current_model.schema_name
        org_index = cur_schema_name.index('org')
        if org_index > 0:
            newschema_name = cur_schema_name[:org_index]
            current_model.schema_name = newschema_name
            current_model.save()


def mig_0001_migrate_customer_schema_name(apps, schema_editor):
    mig_0001_migrate_schema_name(apps, schema_editor, 'Customer')

# api.migrations.0010_costmodelmetricsmap
def mig_0010_load_openshift_metric_map(apps, schema_editor):
    """Load AWS Cost Usage report to database mapping."""
    CostModelMetricsMap = apps.get_model('api', 'CostModelMetricsMap')

    data = pkgutil.get_data('api',
                            'metrics/data/cost_models_metric_map.json')

    data = json.loads(data)

    for entry in data:
        map = CostModelMetricsMap(**entry)
        map.save()

# api.migrations.0029_cloud_account_seeder
def mig_0029_seed_cost_management_aws_account_id(apps, schema_editor):
    """Create a cloud account, using the historical CloudAccount model."""
    CloudAccount = apps.get_model('api', 'CloudAccount')
    cloud_account = CloudAccount.objects.create(
            name='AWS', value='589173575009', description="Cost Management's AWS account ID")
    cloud_account.save()

# api.migrations.0040_auto_20191121_2154
def mig_0040_load_openshift_metric_map(apps, schema_editor):
    """Load AWS Cost Usage report to database mapping."""
    CostModelMetricsMap = apps.get_model('api', 'CostModelMetricsMap')
    CostModelMetricsMap.objects.all().delete()

    data = pkgutil.get_data('api',
                            'metrics/data/cost_models_metric_map.json')

    data = json.loads(data)

    for entry in data:
        map = CostModelMetricsMap(**entry)
        map.save()


class Migration(migrations.Migration):

    replaces = [('api', '0001_initial_squashed_0008_auto_20190305_2015'), ('api', '0009_providerstatus'), ('api', '0010_costmodelmetricsmap'), ('api', '0011_auto_20190613_1554'), ('api', '0012_auto_20190723_1655'), ('api', '0013_auto_20190812_1815'), ('api', '0014_auto_20190807_1420'), ('api', '0015_dataexportrequest'), ('api', '0016_dataexportrequest_bucket_name'), ('api', '0017_auto_20190823_1442'), ('api', '0018_auto_20190827_1536'), ('api', '0019_auto_20190912_1853'), ('api', '0020_sources'), ('api', '0021_auto_20190917_1757'), ('api', '0022_auto_20190923_1410'), ('api', '0023_auto_20190923_1810'), ('api', '0024_auto_20190925_1914'), ('api', '0025_sources_endpoint_id'), ('api', '0026_auto_20191003_2339'), ('api', '0027_auto_20191008_1905'), ('api', '0028_cloud_account'), ('api', '0029_cloud_account_seeder'), ('api', '0030_auto_20191022_1602'), ('api', '0031_auto_20191022_1615'), ('api', '0032_auto_20191022_1620'), ('api', '0033_auto_20191022_1635'), ('api', '0034_provider_active'), ('api', '0035_auto_20191108_1914'), ('api', '0036_auto_20191113_2029'), ('api', '0037_auto_20191120_1538'), ('api', '0038_sources_source_uuid'), ('api', '0039_auto_20191121_2154'), ('api', '0040_auto_20191121_2154'), ('api', '0041_sources_account_id')]

    initial = True

    dependencies = [
#        ('reporting_common', '0019_auto_20191022_1602'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('account_id', models.CharField(max_length=150, null=True, unique=True)),
                ('schema_name', models.TextField(default='public', unique=True)),
            ],
            options={
                'ordering': ['schema_name'],
            },
        ),
        migrations.CreateModel(
            name='ProviderAuthentication',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('provider_resource_name', models.TextField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProviderBillingSource',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('bucket', models.CharField(max_length=63)),
            ],
        ),
        migrations.CreateModel(
            name='Tenant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('schema_name', models.CharField(max_length=63, unique=True, validators=[tenant_schemas.postgresql_backend.base._check_schema_name])),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('username', models.CharField(max_length=150, unique=True)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.NullBooleanField(default=True)),
                ('customer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.Customer')),
            ],
            options={
                'ordering': ['username'],
            },
        ),
        migrations.CreateModel(
            name='UserPreference',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('preference', django.contrib.postgres.fields.jsonb.JSONField(default=dict)),
                ('name', models.CharField(default=uuid.uuid4, max_length=255)),
                ('description', models.CharField(max_length=255, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.User')),
            ],
            options={
                'ordering': ('name',),
                'unique_together': {('name', 'user')},
            },
        ),
        migrations.CreateModel(
            name='Provider',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('name', models.CharField(max_length=256)),
                ('type', models.CharField(choices=[('AWS', 'AWS'), ('OCP', 'OCP'), ('AWS-local', 'AWS-local'), ('OCP-local', 'OCP-local')], default='AWS', max_length=50)),
                ('setup_complete', models.BooleanField(default=False)),
                ('authentication', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='api.ProviderAuthentication')),
                ('billing_source', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='api.ProviderBillingSource')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.User')),
                ('customer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='api.Customer')),
            ],
            options={
                'ordering': ['name'],
                'unique_together': {('authentication', 'billing_source')},
            },
        ),
        migrations.AddField(
            model_name='provider',
            name='created_timestamp',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='provider',
            name='type',
            field=models.CharField(choices=[('AWS', 'AWS'), ('OCP', 'OCP')], default='AWS', max_length=50),
        ),
        migrations.AlterField(
            model_name='provider',
            name='type',
            field=models.CharField(choices=[('AWS', 'AWS'), ('OCP', 'OCP'), ('AWS-local', 'AWS-local'), ('OCP-local', 'OCP-local')], default='AWS', max_length=50),
        ),
        migrations.AlterField(
            model_name='provider',
            name='type',
            field=models.CharField(choices=[('AWS', 'AWS'), ('OCP', 'OCP'), ('AZURE', 'AZURE')], default='AWS', max_length=50),
        ),
        migrations.AlterField(
            model_name='provider',
            name='type',
            field=models.CharField(choices=[('AWS', 'AWS'), ('OCP', 'OCP'), ('AZURE', 'AZURE'), ('AWS-local', 'AWS-local'), ('OCP-local', 'OCP-local')], default='AWS', max_length=50),
        ),
        migrations.AlterField(
            model_name='provider',
            name='type',
            field=models.CharField(choices=[('AWS', 'AWS'), ('OCP', 'OCP'), ('AZURE', 'AZURE'), ('AWS-local', 'AWS-local'), ('AZURE-local', 'AZURE-local')], default='AWS', max_length=50),
        ),
        migrations.AlterField(
            model_name='provider',
            name='type',
            field=models.CharField(choices=[('AWS', 'AWS'), ('OCP', 'OCP'), ('AZURE', 'AZURE')], default='AWS', max_length=50),
        ),
        migrations.AlterField(
            model_name='provider',
            name='type',
            field=models.CharField(choices=[('AWS', 'AWS'), ('OCP', 'OCP'), ('AZURE', 'AZURE'), ('GCP', 'GCP'), ('AWS-local', 'AWS-local'), ('AZURE-local', 'AZURE-local'), ('GCP-local', 'GCP-local')], default='AWS', max_length=50),
        ),
        migrations.RemoveField(
            model_name='providerstatus',
            name='provider',
        ),
        migrations.RunSQL(
            sql=['ALTER TABLE api_provider DROP CONSTRAINT api_provider_pkey'],
            state_operations=[migrations.RemoveField(
                model_name='provider',
                name='id',
            )],
        ),
        migrations.AlterField(
            model_name='provider',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False),
        ),
        migrations.AddField(
            model_name='providerstatus',
            name='provider',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.Provider'),
        ),
        migrations.AlterField(
            model_name='providerstatus',
            name='provider',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Provider'),
        ),
        migrations.AddField(
            model_name='provider',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='provider',
            name='infrastructure',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.ProviderInfrastructureMap'),
        ),
        migrations.RunPython(
            code=mig_0001_migrate_customer_schema_name,
        ),
        migrations.AlterField(
            model_name='userpreference',
            name='preference',
            field=django.contrib.postgres.fields.jsonb.JSONField(),
        ),
        migrations.CreateModel(
            name='ProviderStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.IntegerField(choices=[(0, 'New'), (1, 'Ready'), (33, 'Warning'), (98, 'Disabled: Error'), (99, 'Disabled: Admin')], default=0)),
                ('last_message', models.CharField(max_length=256)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('retries', models.IntegerField(default=0)),
                ('provider', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Provider')),
            ],
        ),
        migrations.CreateModel(
            name='CostModelMetricsMap',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source_type', models.CharField(choices=[('AWS', 'AWS'), ('OCP', 'OCP'), ('AWS-local', 'AWS-local'), ('OCP-local', 'OCP-local')], max_length=50)),
                ('metric', models.CharField(choices=[('cpu_core_usage_per_hour', 'cpu_core_usage_per_hour'), ('cpu_core_request_per_hour', 'cpu_core_request_per_hour'), ('memory_gb_usage_per_hour', 'memory_gb_usage_per_hour'), ('memory_gb_request_per_hour', 'memory_gb_request_per_hour'), ('storage_gb_usage_per_month', 'storage_gb_usage_per_month'), ('storage_gb_request_per_month', 'storage_gb_request_per_month')], max_length=256)),
                ('label_metric', models.CharField(max_length=256)),
                ('label_measurement', models.CharField(max_length=256)),
                ('label_measurement_unit', models.CharField(max_length=64)),
            ],
            options={
                'db_table': 'cost_models_metrics_map',
                'unique_together': {('source_type', 'metric')},
            },
        ),
        migrations.RunPython(
            code=mig_0010_load_openshift_metric_map,
        ),
        migrations.RemoveField(
            model_name='providerstatus',
            name='provider_uuid',
        ),
        migrations.AlterField(
            model_name='costmodelmetricsmap',
            name='source_type',
            field=models.CharField(choices=[('AWS', 'AWS'), ('OCP', 'OCP')], max_length=50),
        ),
        migrations.AlterField(
            model_name='costmodelmetricsmap',
            name='source_type',
            field=models.CharField(choices=[('AWS', 'AWS'), ('OCP', 'OCP'), ('AWS-local', 'AWS-local'), ('OCP-local', 'OCP-local')], max_length=50),
        ),
        migrations.AddField(
            model_name='providerauthentication',
            name='credentials',
            field=django.contrib.postgres.fields.jsonb.JSONField(default=dict, null=True),
        ),
        migrations.AddField(
            model_name='providerbillingsource',
            name='data_source',
            field=django.contrib.postgres.fields.jsonb.JSONField(default=dict, null=True),
        ),
        migrations.AlterField(
            model_name='costmodelmetricsmap',
            name='source_type',
            field=models.CharField(choices=[('AWS', 'AWS'), ('OCP', 'OCP'), ('AZURE', 'AZURE')], max_length=50),
        ),
        migrations.AlterField(
            model_name='providerauthentication',
            name='provider_resource_name',
            field=models.TextField(null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='providerbillingsource',
            name='bucket',
            field=models.CharField(max_length=63, null=True),
        ),
        migrations.AddConstraint(
            model_name='providerauthentication',
            constraint=models.CheckConstraint(check=models.Q(models.Q(('provider_resource_name', None), ('credentials', {})), _negated=True), name='credentials_and_resource_name_both_null'),
        ),
        migrations.AddConstraint(
            model_name='providerauthentication',
            constraint=models.CheckConstraint(check=models.Q(models.Q(models.Q(_negated=True, provider_resource_name=None), models.Q(_negated=True, credentials={})), _negated=True), name='credentials_and_resource_name_both_not_null'),
        ),
        migrations.AddConstraint(
            model_name='providerbillingsource',
            constraint=models.CheckConstraint(check=models.Q(models.Q(('bucket', None), ('data_source', {})), _negated=True), name='bucket_and_data_source_both_null'),
        ),
        migrations.AddConstraint(
            model_name='providerbillingsource',
            constraint=models.CheckConstraint(check=models.Q(models.Q(models.Q(_negated=True, bucket=None), models.Q(_negated=True, data_source={})), _negated=True), name='bucket_and_data_source_both_not_null'),
        ),
        migrations.AlterField(
            model_name='providerstatus',
            name='timestamp',
            field=models.DateTimeField(),
        ),
        migrations.CreateModel(
            name='DataExportRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('created_timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated_timestamp', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('complete', 'Complete')], default='pending', max_length=32)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.User')),
                ('bucket_name', models.CharField(default='', max_length=63)),
            ],
            options={
                'ordering': ('created_timestamp',),
            },
        ),
        migrations.AlterField(
            model_name='costmodelmetricsmap',
            name='source_type',
            field=models.CharField(choices=[('AWS', 'AWS'), ('OCP', 'OCP'), ('AZURE', 'AZURE'), ('AWS-local', 'AWS-local'), ('OCP-local', 'OCP-local')], max_length=50),
        ),
        migrations.AlterField(
            model_name='costmodelmetricsmap',
            name='source_type',
            field=models.CharField(choices=[('AWS', 'AWS'), ('OCP', 'OCP'), ('AZURE', 'AZURE'), ('AWS-local', 'AWS-local'), ('AZURE-local', 'AZURE-local')], max_length=50),
        ),
        migrations.RemoveConstraint(
            model_name='providerbillingsource',
            name='bucket_and_data_source_both_not_null',
        ),
        migrations.AddConstraint(
            model_name='providerbillingsource',
            constraint=models.CheckConstraint(check=models.Q(models.Q(models.Q(models.Q(('bucket', None), ('bucket', ''), _connector='OR'), _negated=True), models.Q(_negated=True, data_source={})), _negated=True), name='bucket_and_data_source_both_not_null'),
        ),
        migrations.AlterField(
            model_name='costmodelmetricsmap',
            name='source_type',
            field=models.CharField(choices=[('AWS', 'AWS'), ('OCP', 'OCP'), ('AZURE', 'AZURE')], max_length=50),
        ),
        migrations.AlterField(
            model_name='dataexportrequest',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('processing', 'Processing'), ('complete', 'Complete'), ('error', 'Error')], default='pending', max_length=32),
        ),
        migrations.AlterField(
            model_name='costmodelmetricsmap',
            name='source_type',
            field=models.CharField(choices=[('AWS', 'AWS'), ('OCP', 'OCP'), ('AZURE', 'AZURE'), ('GCP', 'GCP'), ('AWS-local', 'AWS-local'), ('AZURE-local', 'AZURE-local'), ('GCP-local', 'GCP-local')], max_length=50),
        ),
        migrations.CreateModel(
            name='Sources',
            fields=[
                ('source_id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=256, null=True)),
                ('source_type', models.CharField(max_length=50)),
                ('authentication', django.contrib.postgres.fields.jsonb.JSONField(default=dict)),
                ('billing_source', django.contrib.postgres.fields.jsonb.JSONField(default=dict, null=True)),
                ('koku_uuid', models.CharField(max_length=512, null=True)),
                ('auth_header', models.TextField(null=True)),
                ('pending_delete', models.BooleanField(default=False)),
                ('offset', models.IntegerField()),
                ('endpoint_id', models.IntegerField(null=True)),
            ],
            options={
                'db_table': 'api_sources',
            },
        ),
        migrations.RemoveConstraint(
            model_name='providerauthentication',
            name='credentials_and_resource_name_both_not_null',
        ),
        migrations.RemoveConstraint(
            model_name='providerbillingsource',
            name='bucket_and_data_source_both_not_null',
        ),
        migrations.AddField(
            model_name='sources',
            name='pending_update',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='dataexportrequest',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('processing', 'Processing'), ('waiting', 'Waiting'), ('complete', 'Complete'), ('error', 'Error')], default='pending', max_length=32),
        ),
        migrations.CreateModel(
            name='CloudAccount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='The name of the attribute', max_length=255)),
                ('value', models.TextField(null=True)),
                ('description', models.TextField(null=True)),
                ('updated_timestamp', models.DateTimeField(auto_now=True, null=True)),
            ],
        ),
        migrations.RunPython(
            code=mig_0029_seed_cost_management_aws_account_id,
        ),
        migrations.AddField(
            model_name='providerstatus',
            name='provider_uuid',
            field=models.UUIDField(null=True),
        ),
        migrations.RunSQL(
            sql='\n                UPDATE api_providerstatus AS ps\n                    SET provider_uuid = p.uuid\n                FROM api_provider AS p\n                WHERE p.id = ps.provider_id\n            ',
        ),
        migrations.RunSQL(
            sql='\n                UPDATE api_providerstatus AS ps\n                    SET provider_id = provider_uuid\n            ',
        ),
        migrations.CreateModel(
            name='ProviderInfrastructureMap',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('infrastructure_type', models.CharField(choices=[('AWS', 'AWS'), ('AZURE', 'AZURE'), ('GCP', 'GCP'), ('AWS-local', 'AWS-local'), ('AZURE-local', 'AZURE-local'), ('GCP-local', 'GCP-local')], max_length=50)),
                ('infrastructure_provider', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Provider')),
            ],
        ),
        migrations.AlterField(
            model_name='sources',
            name='koku_uuid',
            field=models.CharField(max_length=512, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='sources',
            name='source_uuid',
            field=models.UUIDField(null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='costmodelmetricsmap',
            name='metric',
            field=models.CharField(choices=[('cpu_core_usage_per_hour', 'cpu_core_usage_per_hour'), ('cpu_core_request_per_hour', 'cpu_core_request_per_hour'), ('memory_gb_usage_per_hour', 'memory_gb_usage_per_hour'), ('memory_gb_request_per_hour', 'memory_gb_request_per_hour'), ('storage_gb_usage_per_month', 'storage_gb_usage_per_month'), ('storage_gb_request_per_month', 'storage_gb_request_per_month'), ('node_cost_per_month', 'node_cost_per_month')], max_length=256),
        ),
        migrations.RunPython(
            code=mig_0040_load_openshift_metric_map,
        ),
        migrations.AddField(
            model_name='sources',
            name='account_id',
            field=models.CharField(max_length=150, null=True),
        ),
    ]
