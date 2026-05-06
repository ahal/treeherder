from django.db import migrations, models


def set_accepts_pull_requests(apps, schema_editor):
    Repository = apps.get_model("model", "Repository")
    RepositoryBranch = apps.get_model("model", "RepositoryBranch")
    pr_repo_ids = RepositoryBranch.objects.filter(branch="pull request").values_list(
        "repository_id", flat=True
    )
    Repository.objects.filter(id__in=pr_repo_ids).update(accepts_pull_requests=True)


class Migration(migrations.Migration):
    dependencies = [
        ("model", "0049_multi_branch_support"),
    ]

    operations = [
        migrations.AddField(
            model_name="repository",
            name="accepts_pull_requests",
            field=models.BooleanField(default=False, db_index=True),
        ),
        migrations.RunPython(set_accepts_pull_requests, migrations.RunPython.noop),
    ]
