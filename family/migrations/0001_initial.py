# Generated by Django 4.2.4 on 2023-08-18 21:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=30, unique=True)),
                ('first_name', models.CharField(blank=True, max_length=30)),
                ('last_name', models.CharField(blank=True, max_length=30)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('date', models.DateField()),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='family.category')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='family.userprofile')),
            ],
        ),
        migrations.CreateModel(
            name='SavingsGoal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('goal_name', models.CharField(max_length=100)),
                ('target_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('current_amount', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('deadline', models.DateField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='family.userprofile')),
            ],
        ),
        migrations.CreateModel(
            name='Income',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('source', models.CharField(max_length=100)),
                ('date', models.DateField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='family.userprofile')),
            ],
        ),
        migrations.CreateModel(
            name='Expense',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('date', models.DateField()),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='family.category')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='family.userprofile')),
            ],
        ),
    ]