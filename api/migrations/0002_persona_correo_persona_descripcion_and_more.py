# Generated by Django 4.2 on 2024-02-09 06:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='persona',
            name='correo',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='persona',
            name='descripcion',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='persona',
            name='numero_celular',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.CreateModel(
            name='Profesional',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('biografia', models.TextField(blank=True)),
                ('imagen_perfil', models.ImageField(blank=True, null=True, upload_to='imagenes/')),
                ('persona', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profesional', to='api.persona')),
            ],
        ),
    ]
