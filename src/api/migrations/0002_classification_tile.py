# Generated by Django 3.2.2 on 2021-05-15 12:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tile',
            fields=[
                ('tid', models.AutoField(primary_key=True, serialize=False)),
                ('x_coordinate', models.IntegerField()),
                ('y_coordinate', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Classification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.IntegerField()),
                ('label', models.CharField(max_length=50)),
                ('classified_by', models.IntegerField()),
                ('tile_id', models.ForeignKey(db_column='tid', on_delete=django.db.models.deletion.CASCADE, to='api.tile')),
            ],
        ),
    ]