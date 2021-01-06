# Generated by Django 2.1.5 on 2019-01-13 09:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GeneralSubject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject_code', models.CharField(blank=True, max_length=50)),
                ('description', models.CharField(max_length=75)),
                ('units', models.PositiveSmallIntegerField()),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('prerequisite', models.ManyToManyField(blank=True, to='grading_system.GeneralSubject')),
            ],
            options={
                'verbose_name_plural': 'Curriculum',
            },
        ),
        migrations.CreateModel(
            name='SemesterFinalGrade',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('semester', models.CharField(choices=[('First Semester', 'First Semester'), ('Second Semester', 'Second Semester'), ('Summer Semester', 'Summer Semester')], default='First Semester', max_length=25)),
                ('grade', models.CharField(blank=True, default='', max_length=10)),
                ('school_year', models.CharField(choices=[('2010-2011', '2010-2011'), ('2011-2012', '2011-2012'), ('2012-2013', '2012-2013'), ('2013-2014', '2013-2014'), ('2014-2015', '2014-2015'), ('2015-2016', '2015-2016'), ('2016-2017', '2016-2017'), ('2017-2018', '2017-2018'), ('2018-2019', '2018-2019'), ('2019-2020', '2019-2020'), ('2020-2021', '2020-2021'), ('2021-2022', '2021-2022'), ('2022-2023', '2022-2023'), ('2023-2024', '2023-2024'), ('2024-2025', '2024-2025'), ('2025-2026', '2025-2026'), ('2026-2027', '2026-2027'), ('2027-2028', '2027-2028'), ('2028-2029', '2028-2029'), ('2029-2030', '2029-2030'), ('2030-2031', '2030-2031'), ('2031-2032', '2031-2032'), ('2032-2033', '2032-2033'), ('2033-2034', '2033-2034')], default='2019-2020', max_length=25)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('student', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='semester_grade', to='account.StudentProfile')),
            ],
            options={
                'verbose_name_plural': 'Semester Final Grade',
            },
        ),
        migrations.CreateModel(
            name='SubjectGrade',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('semester', models.CharField(choices=[('First Semester', 'First Semester'), ('Second Semester', 'Second Semester'), ('Summer Semester', 'Summer Semester')], default='First Semester', max_length=25)),
                ('school_year', models.CharField(choices=[('2010-2011', '2010-2011'), ('2011-2012', '2011-2012'), ('2012-2013', '2012-2013'), ('2013-2014', '2013-2014'), ('2014-2015', '2014-2015'), ('2015-2016', '2015-2016'), ('2016-2017', '2016-2017'), ('2017-2018', '2017-2018'), ('2018-2019', '2018-2019'), ('2019-2020', '2019-2020'), ('2020-2021', '2020-2021'), ('2021-2022', '2021-2022'), ('2022-2023', '2022-2023'), ('2023-2024', '2023-2024'), ('2024-2025', '2024-2025'), ('2025-2026', '2025-2026'), ('2026-2027', '2026-2027'), ('2027-2028', '2027-2028'), ('2028-2029', '2028-2029'), ('2029-2030', '2029-2030'), ('2030-2031', '2030-2031'), ('2031-2032', '2031-2032'), ('2032-2033', '2032-2033'), ('2033-2034', '2033-2034')], default='2019-2020', max_length=15)),
                ('final_grade', models.CharField(blank=True, choices=[('1.00', '1.00'), ('1.25', '1.25'), ('1.50', '1.50'), ('1.75', '1.75'), ('2.00', '2.00'), ('2.25', '2.25'), ('2.50', '2.50'), ('2.75', '2.75'), ('3.00', '3.00'), ('4.00', '4.00'), ('5.00', '5.00'), ('P', 'P'), ('D', 'D'), ('INC', 'INC'), ('W', 'W'), ('NOT S', 'NOT S')], max_length=15)),
                ('grade_status', models.CharField(blank=True, editable=False, max_length=10)),
                ('is_finalized', models.BooleanField(default=False, help_text='Once finalized, you can no longer make any more changes.', verbose_name='Finalized?')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student_grade', to='account.StudentProfile')),
            ],
            options={
                'verbose_name_plural': 'Subject Grades',
            },
        ),
        migrations.CreateModel(
            name='SubjectInstance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('school_year', models.CharField(choices=[('2010-2011', '2010-2011'), ('2011-2012', '2011-2012'), ('2012-2013', '2012-2013'), ('2013-2014', '2013-2014'), ('2014-2015', '2014-2015'), ('2015-2016', '2015-2016'), ('2016-2017', '2016-2017'), ('2017-2018', '2017-2018'), ('2018-2019', '2018-2019'), ('2019-2020', '2019-2020'), ('2020-2021', '2020-2021'), ('2021-2022', '2021-2022'), ('2022-2023', '2022-2023'), ('2023-2024', '2023-2024'), ('2024-2025', '2024-2025'), ('2025-2026', '2025-2026'), ('2026-2027', '2026-2027'), ('2027-2028', '2027-2028'), ('2028-2029', '2028-2029'), ('2029-2030', '2029-2030'), ('2030-2031', '2030-2031'), ('2031-2032', '2031-2032'), ('2032-2033', '2032-2033'), ('2033-2034', '2033-2034')], default='2019-2020', max_length=15)),
                ('semester', models.CharField(choices=[('First Semester', 'First Semester'), ('Second Semester', 'Second Semester'), ('Summer Semester', 'Summer Semester')], default='First Semester', max_length=25)),
                ('schedule', models.TextField(blank=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('instructor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='given_grade', to='account.FacultyProfile')),
                ('subject', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='subject_instance', to='grading_system.GeneralSubject', verbose_name='Subject')),
                ('year_and_section', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='subjects', to='account.YearAndSection')),
            ],
            options={
                'verbose_name_plural': 'Subjects',
            },
        ),
        migrations.AddField(
            model_name='subjectgrade',
            name='subject_instance',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='subject_grade', to='grading_system.SubjectInstance', verbose_name='Subject'),
        ),
        migrations.AddField(
            model_name='semesterfinalgrade',
            name='subject_grades',
            field=models.ManyToManyField(blank=True, related_name='semester_subject_grades', to='grading_system.SubjectGrade'),
        ),
        migrations.AlterUniqueTogether(
            name='subjectinstance',
            unique_together={('subject', 'instructor', 'school_year', 'year_and_section', 'semester')},
        ),
        migrations.AlterUniqueTogether(
            name='subjectgrade',
            unique_together={('student', 'subject_instance', 'semester', 'school_year')},
        ),
        migrations.AlterUniqueTogether(
            name='semesterfinalgrade',
            unique_together={('student', 'semester', 'school_year')},
        ),
        migrations.AlterUniqueTogether(
            name='generalsubject',
            unique_together={('subject_code', 'description')},
        ),
    ]