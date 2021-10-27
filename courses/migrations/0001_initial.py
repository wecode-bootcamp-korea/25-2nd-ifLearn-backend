# Generated by Django 3.2.7 on 2021-10-19 08:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(default=None)),
                ('name', models.CharField(max_length=20)),
            ],
            options={
                'db_table': 'categories',
            },
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(default=None)),
                ('name', models.CharField(max_length=20)),
                ('summary', models.TextField()),
                ('detail', models.TextField()),
                ('thumbnail_url', models.TextField()),
                ('visible', models.IntegerField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('learning_period_month', models.IntegerField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Hashtag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(default=None)),
                ('name', models.CharField(max_length=20)),
            ],
            options={
                'db_table': 'hashtags',
            },
        ),
        migrations.CreateModel(
            name='InfoType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(default=None)),
                ('name', models.CharField(max_length=20)),
            ],
            options={
                'db_table': 'info_types',
            },
        ),
        migrations.CreateModel(
            name='Lecture',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(default=None)),
                ('name', models.CharField(max_length=20)),
                ('storage_key', models.CharField(max_length=200)),
                ('storage_path', models.CharField(max_length=200)),
                ('priority', models.IntegerField()),
                ('play_time', models.IntegerField()),
            ],
            options={
                'db_table': 'lectures',
            },
        ),
        migrations.CreateModel(
            name='Level',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(default=None)),
                ('name', models.CharField(max_length=20)),
            ],
            options={
                'db_table': 'levels',
            },
        ),
        migrations.CreateModel(
            name='SubCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(default=None)),
                ('name', models.CharField(max_length=20)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sub_categories', to='courses.category')),
            ],
            options={
                'db_table': 'sub_categories',
            },
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(default=None)),
                ('name', models.CharField(max_length=20)),
                ('objectives', models.CharField(max_length=20)),
                ('priority', models.IntegerField()),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sections', to='courses.course')),
            ],
            options={
                'db_table': 'sections',
            },
        ),
        migrations.CreateModel(
            name='LectureCompletion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(default=None)),
                ('lecture', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lecture_completion_by_lecture', to='courses.lecture')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lecture_completion_by_user', to='users.user')),
            ],
            options={
                'db_table': 'lecture_completions',
            },
        ),
        migrations.AddField(
            model_name='lecture',
            name='section',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lecture', to='courses.section'),
        ),
        migrations.CreateModel(
            name='CourseInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(default=None)),
                ('name', models.CharField(max_length=100)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cousre_info_by_course', to='courses.course')),
                ('info_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cousre_info_by_type', to='courses.infotype')),
            ],
            options={
                'db_table': 'course_info',
            },
        ),
        migrations.CreateModel(
            name='CourseHashtag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(default=None)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='coursehashtag_by_course', to='courses.course')),
                ('hashtag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='coursehashtag_by_hashtag', to='courses.hashtag')),
            ],
            options={
                'db_table': 'coursehashtags',
            },
        ),
        migrations.AddField(
            model_name='course',
            name='level',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='courses_by_level', to='courses.level'),
        ),
        migrations.AddField(
            model_name='course',
            name='sharer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='courses_by_user', to='users.user'),
        ),
        migrations.AddField(
            model_name='course',
            name='subcatgory',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='courses_by_subcategory', to='courses.subcategory'),
        ),
    ]
