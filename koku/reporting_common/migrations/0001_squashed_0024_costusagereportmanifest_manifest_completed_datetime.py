# Generated by Django 2.2.9 on 2020-01-10 21:50

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import json
import pkgutil


# Functions from the following migrations need manual copying.
# Move them and any dependencies into this file, then update the
# RunPython operations to refer to the local versions:
# reporting_common.migrations.0001_initial_squashed_0007_auto_20190208_0316
def mig_0001_load_report_map_data(apps, schema_editor):
    """Load AWS Cost Usage report to database mapping."""
    ReportColumnMap = apps.get_model('reporting_common', 'ReportColumnMap')

    data = pkgutil.get_data('reporting_common',
                            'data/aws_report_column_map.json')

    data = json.loads(data)

    for entry in data:
        del entry['report_type']
        if entry['database_table'] == "reporting_ocpstoragelineitem":
            continue
        map = ReportColumnMap(**entry)
        map.save()

# reporting_common.migrations.0007_auto_20190208_0316
def mig_0001_reload_ocp_map_0007(apps, schema_editor):
    """Update report to database mapping."""
    ReportColumnMap = apps.get_model('reporting_common', 'ReportColumnMap')
    ocp_items = ReportColumnMap.objects.filter(provider_type='OCP')
    ocp_items.delete()

    data = pkgutil.get_data('reporting_common',
                            'data/ocp_report_column_map.json')

    data = json.loads(data)

    for entry in data:
        map = ReportColumnMap(**entry)
        map.save()

def mig_0001_reload_aws_map(apps, schema_editor):
    """Update report to database mapping."""
    ReportColumnMap = apps.get_model('reporting_common', 'ReportColumnMap')
    aws_items = ReportColumnMap.objects.filter(provider_type='AWS')
    aws_items.delete()

    data = pkgutil.get_data('reporting_common',
                            'data/aws_report_column_map.json')

    data = json.loads(data)

    for entry in data:
        map = ReportColumnMap(**entry)
        map.save()

# reporting_common.migrations.0018_auto_20190923_1838
def mig_0018_reload_azure_map(apps, schema_editor):
    """Update report to database mapping."""
    ReportColumnMap = apps.get_model('reporting_common', 'ReportColumnMap')
    azure_items = ReportColumnMap.objects.filter(provider_type='AZURE')
    azure_items.delete()

    data = pkgutil.get_data('reporting_common',
                            'data/azure_report_column_map.json')

    data = json.loads(data)

    for entry in data:
        map = ReportColumnMap(**entry)
        map.save()

# reporting_common.migrations.0022_add_gcp_column_maps
def mig_0022_load_gcp_column_map(apps, schema_editor):
    """Load GCP column map to database mapping."""
    ReportColumnMap = apps.get_model('reporting_common', 'ReportColumnMap')
    ReportColumnMap.objects.filter(provider_type='GCP').delete()

    data = pkgutil.get_data('reporting_common',
                            'data/gcp_report_column_map.json')

    data = json.loads(data)

    for entry in data:
        map = ReportColumnMap(**entry)
        map.save()


class Migration(migrations.Migration):

    replaces = [('reporting_common', '0001_initial_squashed_0007_auto_20190208_0316'), ('reporting_common', '0008_auto_20190412_1330'), ('reporting_common', '0009_costusagereportstatus_history'), ('reporting_common', '0010_remove_costusagereportstatus_history'), ('reporting_common', '0011_auto_20190723_1655'), ('reporting_common', '0012_auto_20190812_1805'), ('reporting_common', '0013_auto_20190823_1442'), ('reporting_common', '0014_auto_20190820_1513'), ('reporting_common', '0015_auto_20190827_1536'), ('reporting_common', '0016_auto_20190829_2053'), ('reporting_common', '0017_auto_20190923_1410'), ('reporting_common', '0018_auto_20190923_1838'), ('reporting_common', '0019_auto_20191022_1602'), ('reporting_common', '0020_auto_20191022_1620'), ('reporting_common', '0021_auto_20191022_1635'), ('reporting_common', '0022_add_gcp_column_maps'), ('reporting_common', '0023_costusagereportmanifest_task'), ('reporting_common', '0024_costusagereportmanifest_manifest_completed_datetime')]

    initial = True

    dependencies = [
        ('api', '0001_squashed_0041_sources_account_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='CostUsageReportManifest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('assembly_id', models.TextField()),
                ('manifest_creation_datetime', models.DateTimeField(default=django.utils.timezone.now, null=True)),
                ('manifest_updated_datetime', models.DateTimeField(default=django.utils.timezone.now, null=True)),
                ('billing_period_start_datetime', models.DateTimeField()),
                ('num_processed_files', models.IntegerField(default=0)),
                ('num_total_files', models.IntegerField()),
                ('provider', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Provider')),
                ('task',models.UUIDField(null=True)),
                ('manifest_completed_datetime', models.DateTimeField(null=True)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='costusagereportmanifest',
            unique_together={('provider', 'assembly_id')},
        ),
        migrations.CreateModel(
            name='CostUsageReportStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('report_name', models.CharField(max_length=128)),
                ('last_completed_datetime', models.DateTimeField(null=True)),
                ('last_started_datetime', models.DateTimeField(null=True)),
                ('etag', models.CharField(max_length=64, null=True)),
                ('manifest', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='reporting_common.CostUsageReportManifest')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='costusagereportstatus',
            unique_together={('manifest', 'report_name')},
        ),
        migrations.CreateModel(
            name='RegionMapping',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('region', models.CharField(max_length=32, unique=True)),
                ('region_name', models.CharField(max_length=64, unique=True)),
            ],
            options={
                'db_table': 'region_mapping',
            },
        ),
        migrations.CreateModel(
            name='ReportColumnMap',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('provider_type', models.CharField(choices=[('AWS', 'AWS'), ('OCP', 'OCP'), ('AZURE', 'AZURE'), ('GCP', 'GCP'), ('AWS-local', 'AWS-local'), ('AZURE-local', 'AZURE-local'), ('GCP-local', 'GCP-local')], default='AWS', max_length=50)),
                ('provider_column_name', models.CharField(max_length=128)),
                ('database_table', models.CharField(max_length=50)),
                ('database_column', models.CharField(max_length=128)),
                ('report_type', models.CharField(max_length=50, null=True)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='reportcolumnmap',
            unique_together={('report_type', 'provider_column_name')},
        ),
        migrations.CreateModel(
            name='SIUnitScale',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prefix', models.CharField(max_length=12, unique=True)),
                ('prefix_symbol', models.CharField(max_length=1)),
                ('multiplying_factor', models.DecimalField(decimal_places=24, max_digits=49)),
            ],
            options={
                'db_table': 'si_unit_scale',
            },
        ),
        migrations.RunPython(
            code=mig_0001_load_report_map_data,
        ),
        migrations.RunPython(
            code=mig_0001_reload_ocp_map_0007,
        ),
        migrations.RunPython(
            code=mig_0001_reload_aws_map,
        ),
        migrations.RunPython(
            code=mig_0018_reload_azure_map,
        ),
        migrations.RunPython(
            code=mig_0022_load_gcp_column_map,
        ),
    ]
