# Generated by Django 4.1.5 on 2023-05-25 11:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applicantManager', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='applicantrole',
            name='status',
            field=models.CharField(choices=[('Approved', 'Approved'), ('Rejected', 'Rejected'), ('Under Analysis', 'Under Analysis')], default='Under Analysis', max_length=15),
        ),
    ]
