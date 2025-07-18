
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0002_resource'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='features',
            field=models.TextField(blank=True, help_text='One feature per line'),
        ),
    ]
