from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('code', models.CharField(max_length=200)),
                ('prerequisite', models.BooleanField(default=False)),
                ('credit', models.IntegerField())
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('code', models.CharField(max_length=200)),
                ('clas', models.CharField(max_length=200)),
                ('faculty', models.CharField(max_length=200)),
                ('major', models.CharField(max_length=200))
            ],
        ),
    ]
