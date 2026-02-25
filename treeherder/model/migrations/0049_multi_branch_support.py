from django.db import migrations, models
import django.db.models.deletion


def migrate_branches_to_table(apps, schema_editor):
    """Move Repository.branch (comma-separated) to RepositoryBranch rows."""
    Repository = apps.get_model('model', 'Repository')
    RepositoryBranch = apps.get_model('model', 'RepositoryBranch')

    for repo in Repository.objects.exclude(branch__isnull=True).exclude(branch=''):
        for b in repo.branch.split(','):
            b = b.strip()
            if b:
                RepositoryBranch.objects.get_or_create(repository=repo, branch=b)


class Migration(migrations.Migration):
    dependencies = [
        ('model', '0048_alter_failureline_action'),
    ]

    operations = [
        migrations.CreateModel(
            name='RepositoryBranch',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('branch', models.CharField(db_index=True, max_length=255)),
                ('repository', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='branches',
                    to='model.repository',
                )),
            ],
            options={
                'db_table': 'repository_branch',
            },
        ),
        migrations.AlterUniqueTogether(
            name='repositorybranch',
            unique_together={('repository', 'branch')},
        ),
        migrations.RunPython(migrate_branches_to_table, migrations.RunPython.noop),
        migrations.RemoveField(
            model_name='repository',
            name='branch',
        ),
        migrations.AddField(
            model_name='repository',
            name='accepts_all_branches',
            field=models.BooleanField(default=False, db_index=True),
        ),
        migrations.AddField(
            model_name='push',
            name='branch',
            field=models.CharField(blank=True, db_index=True, default='', max_length=255),
        ),
    ]
