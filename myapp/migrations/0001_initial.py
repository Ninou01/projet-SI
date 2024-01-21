# Generated by Django 5.0.1 on 2024-01-21 23:14

import django.contrib.auth.models
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Medecin',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('Nom', models.CharField(blank=True, max_length=255, null=True)),
                ('Prenom', models.CharField(blank=True, max_length=255, null=True)),
                ('DateNaissance', models.DateField(blank=True, null=True)),
                ('sexe', models.CharField(blank=True, choices=[('M', 'Male'), ('F', 'Female')], max_length=10, null=True)),
                ('Adresse', models.TextField(blank=True, null=True)),
                ('num_tel', models.CharField(blank=True, max_length=20, null=True)),
                ('specialite', models.CharField(blank=True, choices=[('Cardiologue', 'Cardiologue'), ('Neurologue', 'Neurologue'), ('Urologue', 'Urologue'), ('Rhumatologue', 'Rhumatologue'), ('ORL', 'ORL'), ('Generaliste', 'Generaliste')], max_length=30, null=True)),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('Nom', models.CharField(blank=True, max_length=255, null=True)),
                ('Prenom', models.CharField(blank=True, max_length=255, null=True)),
                ('DateNaissance', models.DateField(blank=True, null=True)),
                ('sexe', models.CharField(blank=True, choices=[('M', 'Male'), ('F', 'Female')], max_length=10, null=True)),
                ('Adresse', models.TextField(blank=True, null=True)),
                ('num_tel', models.CharField(blank=True, max_length=20, null=True)),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Salle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='RendezVous',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Date', models.DateField(blank=True, null=True)),
                ('Heure', models.TimeField(blank=True, null=True)),
                ('confirmer', models.BooleanField(default=False)),
                ('medecin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.medecin')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.patient')),
                ('salle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.salle')),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=255)),
                ('chef', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='chef_de_service', to='myapp.medecin')),
            ],
        ),
        migrations.AddField(
            model_name='medecin',
            name='service',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='medecins', to='myapp.service'),
        ),
        migrations.CreateModel(
            name='Tache',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titre', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.service')),
            ],
        ),
    ]