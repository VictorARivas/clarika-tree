# Generated by Django 2.2.28 on 2023-07-31 19:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tree', '0002_auto_20230731_1756'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubTree',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valor', models.CharField(max_length=30)),
                ('state', models.CharField(choices=[('active', 'Active'), ('deleted', 'Deleted')], default='active', max_length=8)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='children', to='tree.SubTree')),
                ('tree', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='nodes', to='tree.Tree')),
            ],
        ),
    ]