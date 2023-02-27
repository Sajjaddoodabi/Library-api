# Generated by Django 4.1.7 on 2023-02-27 17:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('library_management', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bookorder',
            name='book',
        ),
        migrations.AddField(
            model_name='bookorder',
            name='status',
            field=models.CharField(choices=[('OPN', 'open'), ('CAN', 'cancelled'), ('DON', 'done')], default='OPN', max_length=100),
        ),
        migrations.CreateModel(
            name='BookOrderDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField()),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_detail', to='library_management.book')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_detail', to='library_management.bookorder')),
            ],
        ),
    ]
