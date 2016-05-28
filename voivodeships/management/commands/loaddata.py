# coding=utf-8
import os

from django.core.management.base import BaseCommand
from django.conf import settings

from django.contrib.gis.utils import LayerMapping
from django.contrib.gis import geos

from voivodeships.models import Voivodeship, Point


voivodeship_mapping = {
    'iip_przest' : 'iip_przest',
    'iip_identy' : 'iip_identy',
    'iip_wersja' : 'iip_wersja',
    'jpt_sjr_ko' : 'jpt_sjr_ko',
    'jpt_kod_je' : 'jpt_kod_je',
    'jpt_nazwa_field' : 'jpt_nazwa_',
    'jpt_nazw01' : 'jpt_nazw01',
    'jpt_organ_field' : 'jpt_organ_',
    'jpt_orga01' : 'jpt_orga01',
    'jpt_jor_id' : 'jpt_jor_id',
    'wazny_od' : 'wazny_od',
    'wazny_do' : 'wazny_do',
    'jpt_wazna_field' : 'jpt_wazna_',
    'wersja_od' : 'wersja_od',
    'wersja_do' : 'wersja_do',
    'jpt_powier' : 'jpt_powier',
    'jpt_kj_iip' : 'jpt_kj_iip',
    'jpt_kj_i01' : 'jpt_kj_i01',
    'jpt_kj_i02' : 'jpt_kj_i02',
    'jpt_kod_01' : 'jpt_kod_01',
    'id_bufora_field' : 'id_bufora_',
    'id_bufor01' : 'id_bufor01',
    'id_technic' : 'id_technic',
    'jpt_opis' : 'jpt_opis',
    'jpt_sps_ko' : 'jpt_sps_ko',
    'gra_ids' : 'gra_ids',
    'status_obi' : 'status_obi',
    'opis_bledu' : 'opis_bledu',
    'typ_bledu' : 'typ_bledu',
    'geom' : 'MULTIPOLYGON',
}

class Command(BaseCommand):
    help = 'Load inital data from data folder'

    def handle(self, *args, **options):
        voivodeship_shp = os.path.abspath(
            os.path.join(
                settings.BASE_DIR,
                'data',
                'PRG_jednostki_administracyjne_v10',
                'województwa.shp'
            )
        )
        point_csv = os.path.abspath(
            os.path.join(
                settings.BASE_DIR,
                'data',
                'points.csv'
            )
        )

        # load shp file
        lm = LayerMapping(Voivodeship, voivodeship_shp, voivodeship_mapping,
                          transform=False, encoding='iso-8859-1')
        lm.save(strict=True, verbose=True)

        self.stdout.write(
            self.style.SUCCESS('Sucessfully loaded shp file from %s')
            % voivodeship_shp
        )

        # load csv file
        with open(point_csv) as point_file:
            for line in point_file:
                name, lon, lat = line.split(',')
                point = "POINT(%s %s)" % (lat.strip(), lon.strip())
                Point.objects.create(name=name, geom=geos.fromstr(point))

        self.stdout.write(
            self.style.SUCCESS('Sucessfully loaded points from %s')
            % point_csv
        )
