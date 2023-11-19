# Generated by Django 4.2.5 on 2023-11-19 17:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import shop.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='Nom')),
                ('hexa', models.CharField(max_length=7, verbose_name='Hex')),
            ],
            options={
                'verbose_name': 'Couleur',
            },
        ),
        migrations.CreateModel(
            name='Garment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(help_text='50 caractères max', max_length=50, verbose_name='Description')),
                ('reference', models.UUIDField(blank=True, default=uuid.uuid4, verbose_name='Référence')),
                ('slug', models.SlugField(blank=True)),
                ('price', models.IntegerField(verbose_name="Prix d'achat")),
                ('size', models.CharField(choices=[('16', '16'), ('17', '17'), ('18', '18'), ('19', '19'), ('20', '20'), ('21', '21'), ('22', '22'), ('23', '23'), ('24', '24'), ('25', '25'), ('26', '26'), ('27', '27'), ('28', '28'), ('29', '29'), ('30', '30'), ('31', '31'), ('32', '32'), ('33', '33'), ('34', '34'), ('35', '35'), ('36', '36'), ('37', '37'), ('38', '38'), ('39', '39'), ('40', '40'), ('41', '41'), ('42', '42'), ('43', '43'), ('44', '44'), ('45', '45'), ('46', '46'), ('47', '47'), ('48', '48'), ('49', '49'), ('50', '50'), ('51', '51'), ('52', '52'), ('53', '53'), ('54', '54'), ('55', '55'), ('56', '56'), ('57', '57'), ('58', '58'), ('59', '59'), ('60', '60'), ('61', '61'), ('62', '62'), ('63', '63'), ('64', '64'), ('65', '65'), ('66', '66'), ('67', '67'), ('68', '68'), ('69', '69'), ('70', '70')], max_length=10, verbose_name='Taille')),
                ('year', models.CharField(blank=True, choices=[('1900', '1900'), ('1901', '1901'), ('1902', '1902'), ('1903', '1903'), ('1904', '1904'), ('1905', '1905'), ('1906', '1906'), ('1907', '1907'), ('1908', '1908'), ('1909', '1909'), ('1910', '1910'), ('1911', '1911'), ('1912', '1912'), ('1913', '1913'), ('1914', '1914'), ('1915', '1915'), ('1916', '1916'), ('1917', '1917'), ('1918', '1918'), ('1919', '1919'), ('1920', '1920'), ('1921', '1921'), ('1922', '1922'), ('1923', '1923'), ('1924', '1924'), ('1925', '1925'), ('1926', '1926'), ('1927', '1927'), ('1928', '1928'), ('1929', '1929'), ('1930', '1930'), ('1931', '1931'), ('1932', '1932'), ('1933', '1933'), ('1934', '1934'), ('1935', '1935'), ('1936', '1936'), ('1937', '1937'), ('1938', '1938'), ('1939', '1939'), ('1940', '1940'), ('1941', '1941'), ('1942', '1942'), ('1943', '1943'), ('1944', '1944'), ('1945', '1945'), ('1946', '1946'), ('1947', '1947'), ('1948', '1948'), ('1949', '1949'), ('1950', '1950'), ('1951', '1951'), ('1952', '1952'), ('1953', '1953'), ('1954', '1954'), ('1955', '1955'), ('1956', '1956'), ('1957', '1957'), ('1958', '1958'), ('1959', '1959'), ('1960', '1960'), ('1961', '1961'), ('1962', '1962'), ('1963', '1963'), ('1964', '1964'), ('1965', '1965'), ('1966', '1966'), ('1967', '1967'), ('1968', '1968'), ('1969', '1969'), ('1970', '1970'), ('1971', '1971'), ('1972', '1972'), ('1973', '1973'), ('1974', '1974'), ('1975', '1975'), ('1976', '1976'), ('1977', '1977'), ('1978', '1978'), ('1979', '1979'), ('1980', '1980'), ('1981', '1981'), ('1982', '1982'), ('1983', '1983'), ('1984', '1984'), ('1985', '1985'), ('1986', '1986'), ('1987', '1987'), ('1988', '1988'), ('1989', '1989'), ('1990', '1990'), ('1991', '1991'), ('1992', '1992'), ('1993', '1993'), ('1994', '1994'), ('1995', '1995'), ('1996', '1996'), ('1997', '1997'), ('1998', '1998'), ('1999', '1999'), ('2000', '2000'), ('2001', '2001'), ('2002', '2002'), ('2003', '2003'), ('2004', '2004'), ('2005', '2005'), ('2006', '2006'), ('2007', '2007'), ('2008', '2008'), ('2009', '2009'), ('2010', '2010'), ('2011', '2011'), ('2012', '2012'), ('2013', '2013'), ('2014', '2014'), ('2015', '2015'), ('2016', '2016'), ('2017', '2017'), ('2018', '2018'), ('2019', '2019'), ('2020', '2020'), ('2021', '2021'), ('2022', '2022'), ('2023', '2023')], max_length=4, verbose_name='Année')),
                ('category', models.CharField(choices=[('ch', 'Chaussures'), ('pa', 'Pantalons'), ('ha', 'Hauts')], max_length=20, verbose_name='Catégorie')),
                ('state', models.CharField(choices=[('b', 'Bon état'), ('tb', 'Très bon état'), ('cn', 'Comme neuf')], max_length=20, verbose_name='Etat')),
                ('type', models.CharField(choices=[('h', 'Homme'), ('f', 'Femme'), ('e', 'Enfant')], max_length=10, verbose_name='Sexe')),
                ('pics_1', models.ImageField(upload_to=shop.models.user_directory_path, verbose_name='Photo 1')),
                ('pics_2', models.ImageField(blank=True, null=True, upload_to=shop.models.user_directory_path, verbose_name='Photo 2')),
                ('pics_3', models.ImageField(blank=True, null=True, upload_to=shop.models.user_directory_path, verbose_name='Photo 3')),
                ('published', models.DateTimeField(auto_now_add=True, verbose_name='Date de publication')),
                ('activate', models.BooleanField(default=False, verbose_name='Activé')),
                ('bought', models.BooleanField(default=False, verbose_name='Acheté')),
                ('color', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='shop.color', verbose_name='Couleur')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='garments', to=settings.AUTH_USER_MODEL, verbose_name='Utilisateur')),
            ],
            options={
                'verbose_name': 'Vêtement',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reference', models.UUIDField(default=uuid.uuid4, verbose_name='Référence')),
                ('ordered', models.BooleanField(default=False, verbose_name='Commandée')),
                ('ordered_date', models.DateTimeField(blank=True, null=True)),
                ('validation', models.BooleanField(default=False, verbose_name='Validation du deal')),
                ('garment', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='shop.garment', verbose_name='Vêtements')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Utilisateur')),
            ],
            options={
                'verbose_name': 'Commande',
            },
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_date', models.DateTimeField(auto_now_add=True, verbose_name='Date de création')),
                ('orders', models.ManyToManyField(to='shop.order', verbose_name='Vêtements')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Utilisateur')),
            ],
            options={
                'verbose_name': 'Panier',
            },
        ),
    ]
