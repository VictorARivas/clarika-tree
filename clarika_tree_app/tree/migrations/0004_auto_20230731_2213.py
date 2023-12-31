# Generated by Django 2.2.28 on 2023-07-31 22:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tree', '0003_subtree'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subtree',
            name='tree',
        ),
        migrations.AddField(
            model_name='subtree',
            name='tree_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='tree.Tree'),
        ),
        migrations.AlterField(
            model_name='subtree',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='tree.SubTree'),
        ),
        migrations.AlterField(
            model_name='subtree',
            name='state',
            field=models.CharField(default='active', max_length=8),
        ),
    ]
