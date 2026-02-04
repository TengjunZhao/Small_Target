from django.db import migrations, models
import django.db.models.deletion


def seed_kana(apps, schema_editor):
    Kana = apps.get_model('kana', 'Kana')
    User = apps.get_model('auth', 'User')
    # Seed basic kana list (a, i, u, e, o, ka, ki, ku, ke, ko, ...)
    data = [
        ('あ','ア','a',5), ('い','イ','i',5), ('う','ウ','u',5), ('え','エ','e',5), ('お','オ','o',5),
        ('か','カ','ka',5), ('き','キ','ki',5), ('く','ク','ku',5), ('け','ケ','ke',5), ('こ','コ','ko',5),
        ('さ','サ','sa',5), ('し','シ','shi',5), ('す','ス','su',5), ('せ','セ','se',5), ('そ','ソ','so',5),
        ('た','タ','ta',5), ('ち','チ','chi',5), ('つ','ツ','tsu',5), ('て','テ','te',5), ('と','ト','to',5),
        ('な','ナ','na',5), ('に','ニ','ni',5), ('ぬ','ヌ','nu',5), ('ね','ネ','ne',5), ('の','ノ','no',5),
        ('は','ハ','ha',5), ('ひ','ヒ','hi',5), ('ふ','フ','fu',5), ('へ','ヘ','he',5), ('ほ','ホ','ho',5),
        ('ま','マ','ma',5), ('み','ミ','mi',5), ('む','ム','mu',5), ('め','メ','me',5), ('も','モ','mo',5),
        ('や','ヤ','ya',5), ('ゆ','ユ','yu',5), ('よ','ヨ','yo',5),
        ('ら','ラ','ra',5), ('り','リ','ri',5), ('る','ル','ru',5), ('れ','レ','re',5), ('ろ','ロ','ro',5),
        ('わ','ワ','wa',5), ('を','ヲ','wo',5), ('ん','ン','n',5),
    ]
    for hira, kata, romaji, w in data:
        Kana.objects.create(hira=hira, kata=kata, romaji=romaji, base_weight=w)

    # create a guest user if not exists (for API access)
    UserModel = User
    guest, created = UserModel.objects.get_or_create(username='guest')
    if created:
        guest.set_unusable_password()
        guest.save()


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Kana',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hira', models.CharField(max_length=2)),
                ('kata', models.CharField(max_length=2)),
                ('romaji', models.CharField(max_length=10, unique=True)),
                ('base_weight', models.IntegerField(default=5)),
            ],
        ),
        migrations.CreateModel(
            name='KanaProgress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weight', models.IntegerField(null=True, blank=True)),
                ('errors', models.IntegerField(default=0)),
                ('kana', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kana.kana')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.user')),
            ],
            options={
                'unique_together': {('user', 'kana')},
            },
        ),
        migrations.RunPython(seed_kana,
            reverse_code=lambda apps, schema_editor: None,
        ),
    ]
