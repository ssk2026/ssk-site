from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0011_alter_event_content"),
    ]

    operations = [
        migrations.CreateModel(
            name="AcademicPresentation",
            fields=[],
            options={
                "verbose_name": "학술대회 발표",
                "verbose_name_plural": "학술대회 발표",
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("core.event",),
        ),
    ]
