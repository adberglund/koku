# Generated by Django 2.2.1 on 2019-05-31 17:25

import json
import pkgutil

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


# Functions from the following migrations need manual copying.
# Move them and any dependencies into this file, then update the
# RunPython operations to refer to the local versions:
# reporting_common.migrations.0002_auto_20180926_1905
def load_report_map_data(apps, schema_editor):
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

# reporting_common.migrations.0003_auto_20180928_1732
def load_ocp_report_map_data(apps, schema_editor):
    """Load OCP Usage report to database mapping."""
    ReportColumnMap = apps.get_model('reporting_common', 'ReportColumnMap')

    data = pkgutil.get_data('reporting_common',
                            'data/ocp_report_column_map.json')

    data = json.loads(data)

    for entry in data:
        del entry['report_type']
        if entry['database_table'] == "reporting_ocpstoragelineitem":
            continue
        map = ReportColumnMap(**entry)
        map.save()

# reporting_common.migrations.0005_auto_20181127_2046
def reload_ocp_map_0005(apps, schema_editor):
    """Update report to database mapping."""
    ReportColumnMap = apps.get_model('reporting_common', 'ReportColumnMap')
    ocp_items = ReportColumnMap.objects.filter(provider_type='OCP')
    ocp_items.delete()

    data = pkgutil.get_data('reporting_common',
                            'data/ocp_report_column_map.json')

    data = json.loads(data)

    for entry in data:
        del entry['report_type']
        if entry['database_table'] == "reporting_ocpstoragelineitem":
            continue
        map = ReportColumnMap(**entry)
        map.save()

# reporting_common.migrations.0007_auto_20190208_0316
def reload_ocp_map_0007(apps, schema_editor):
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

def reload_aws_map(apps, schema_editor):
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


class Migration(migrations.Migration):

    replaces = [('reporting_common', '0001_initial'), ('reporting_common', '0002_auto_20180926_1905'), ('reporting_common', '0003_auto_20180928_1732'), ('reporting_common', '0004_auto_20181003_1859'), ('reporting_common', '0005_auto_20181127_2046'), ('reporting_common', '0006_auto_20190208_0316'), ('reporting_common', '0007_auto_20190208_0316')]

    dependencies = [
        ('api', '0001_initial'),
        ('api', '0002_auto_20180926_1905'),
    ]

    operations = [
        migrations.CreateModel(
            name='CostUsageReportStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('report_name', models.CharField(max_length=128, unique=True)),
                ('cursor_position', models.PositiveIntegerField()),
                ('last_completed_datetime', models.DateTimeField(null=True)),
                ('last_started_datetime', models.DateTimeField(null=True)),
                ('etag', models.CharField(max_length=64, null=True)),
                ('provider', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.Provider')),
            ],
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
                ('provider_type', models.CharField(choices=[('AWS', 'AWS'), ('OCP', 'OCP')], default='AWS', max_length=50)),
                ('provider_column_name', models.CharField(max_length=128, unique=True)),
                ('database_table', models.CharField(max_length=50)),
                ('database_column', models.CharField(max_length=128)),
            ],
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
            code=load_report_map_data,
        ),
        migrations.AlterField(
            model_name='reportcolumnmap',
            name='provider_type',
            field=models.CharField(choices=[('AWS', 'AWS'), ('OCP', 'OCP'), ('AWS-local', 'AWS-local'), ('OCP-local', 'OCP-local')], default='AWS', max_length=50),
        ),
        migrations.RunPython(
            code=load_ocp_report_map_data,
        ),
        migrations.CreateModel(
            name='CostUsageReportManifest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('assembly_id', models.TextField(unique=True)),
                ('manifest_creation_datetime', models.DateTimeField(default=django.utils.timezone.now, null=True)),
                ('manifest_updated_datetime', models.DateTimeField(default=django.utils.timezone.now, null=True)),
                ('billing_period_start_datetime', models.DateTimeField()),
                ('num_processed_files', models.IntegerField(default=0)),
                ('num_total_files', models.IntegerField()),
                ('provider', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Provider')),
            ],
        ),
        migrations.RemoveField(
            model_name='costusagereportstatus',
            name='cursor_position',
        ),
        migrations.RemoveField(
            model_name='costusagereportstatus',
            name='provider',
        ),
        migrations.AddField(
            model_name='costusagereportstatus',
            name='manifest',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='reporting_common.CostUsageReportManifest'),
        ),
        migrations.RunPython(
            code=reload_ocp_map_0005,
        ),
        migrations.AddField(
            model_name='reportcolumnmap',
            name='report_type',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='reportcolumnmap',
            name='provider_column_name',
            field=models.CharField(max_length=128),
        ),
        migrations.AlterUniqueTogether(
            name='reportcolumnmap',
            unique_together={('report_type', 'provider_column_name')},
        ),
        migrations.RunPython(
            code=reload_ocp_map_0007,
        ),
        migrations.RunPython(
            code=reload_aws_map,
        ),
    ]