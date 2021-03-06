from __future__ import unicode_literals

from django.db import models

class Measurements(models.Model):
    id = models.IntegerField(primary_key=True)
    value = models.FloatField(blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    time = models.DateTimeField(blank=True, null=True)
    timezone_offset = models.IntegerField(blank=True, null=True)
    stream = models.ForeignKey('Streams', models.DO_NOTHING, blank=True, null=True)
    milliseconds = models.IntegerField(blank=True, null=True)
    measured_value = models.FloatField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    ward = models.ForeignKey('Wards', models.DO_NOTHING, blank=True, null=True)
    neighborhood = models.ForeignKey('Neighborhoods', models.DO_NOTHING, blank=True, null=True)
    tract = models.ForeignKey('Tracts', models.DO_NOTHING, blank=True, null=True)
    hexagon = models.ForeignKey('Hexagons', models.DO_NOTHING, blank=True, null=True)
    zipcode = models.ForeignKey('Zipcodes', models.DO_NOTHING, blank=True, null=True)
	
    class Meta:
        managed = False
        db_table = 'measurements'
        unique_together = (('id', 'stream'),)
        verbose_name_plural = 'measurements'


class Notes(models.Model):
    id = models.IntegerField(primary_key=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)
    text = models.TextField(blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    session = models.ForeignKey('Sessions', models.DO_NOTHING, blank=True, null=True)
    photo_file_name = models.CharField(max_length=40, blank=True, null=True)
    photo_content_type = models.CharField(max_length=40, blank=True, null=True)
    photo_file_size = models.IntegerField(blank=True, null=True)
    photo_updated_at = models.DateTimeField(blank=True, null=True)
    number = models.IntegerField(blank=True, null=True)
    photo = models.TextField(blank=True, null=True)
    photo_thumbnail = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'notes'
        verbose_name_plural = 'notes'


class Sessions(models.Model):
    id = models.IntegerField(primary_key=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    user = models.ForeignKey('Users', models.DO_NOTHING, blank=True, null=True)
    uuid = models.CharField(max_length=40, blank=True, null=True)
    url_token = models.CharField(max_length=40, blank=True, null=True)
    title = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    calibration = models.IntegerField(blank=True, null=True)
    contribute = models.IntegerField(blank=True, null=True)
    data_type = models.CharField(max_length=40, blank=True, null=True)
    instrument = models.CharField(max_length=40, blank=True, null=True)
    phone_model = models.CharField(max_length=40, blank=True, null=True)
    os_version = models.CharField(max_length=40, blank=True, null=True)
    offset_60_db = models.CharField(max_length=40, blank=True, null=True)
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    measurements_count = models.IntegerField(blank=True, null=True)
    timezone_offset = models.IntegerField(blank=True, null=True)
    start_time_local = models.DateTimeField(blank=True, null=True)
    end_time_local = models.DateTimeField(blank=True, null=True)
    type = models.CharField(max_length=40)
    is_indoor = models.IntegerField(blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    last_measurement_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sessions'
        verbose_name_plural = 'sessions'


class Streams(models.Model):
    id = models.IntegerField(primary_key=True)
    sensor_name = models.CharField(max_length=40, blank=True, null=True)
    unit_name = models.CharField(max_length=40, blank=True, null=True)
    measurement_type = models.CharField(max_length=40, blank=True, null=True)
    measurement_short_type = models.CharField(max_length=40, blank=True, null=True)
    unit_symbol = models.CharField(max_length=40, blank=True, null=True)
    threshold_very_low = models.IntegerField(blank=True, null=True)
    threshold_low = models.IntegerField(blank=True, null=True)
    threshold_medium = models.IntegerField(blank=True, null=True)
    threshold_high = models.IntegerField(blank=True, null=True)
    threshold_very_high = models.IntegerField(blank=True, null=True)
    session = models.ForeignKey(Sessions, models.DO_NOTHING, blank=True, null=True)
    sensor_package_name = models.CharField(max_length=40)
    measurements_count = models.IntegerField()
    min_latitude = models.FloatField(blank=True, null=True)
    max_latitude = models.FloatField(blank=True, null=True)
    min_longitude = models.FloatField(blank=True, null=True)
    max_longitude = models.FloatField(blank=True, null=True)
    average_value = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'streams'
        verbose_name_plural = 'streams'


class Users(models.Model):
    id = models.IntegerField(blank=True, null=True)
    username = models.CharField(primary_key=True, max_length=40)
    display = models.CharField(max_length=40)
    private = models.BooleanField(default=False)

    class Meta:
        managed = False
        db_table = 'users'
        verbose_name_plural = 'users'

class Tracts(models.Model):
    id = models.BigIntegerField(primary_key=True)
    display = models.CharField(max_length=40, blank=True, null=True)
    geo = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tracts'
        verbose_name_plural = 'tracts'

class Neighborhoods(models.Model):
    id = models.IntegerField(primary_key=True)
    display = models.CharField(max_length=40, blank=True, null=True)
    geo = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'neighborhoods'
        verbose_name_plural = 'neighborhoods'

class Wards(models.Model):
    id = models.IntegerField(primary_key=True)
    display = models.CharField(max_length=40, blank=True, null=True)
    geo = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'wards'
        verbose_name_plural = 'wards'

class Hexagons(models.Model):
    id = models.IntegerField(primary_key=True)
    display = models.CharField(max_length=40, blank=True, null=True)
    geo = models.TextField(blank=True, null=True)
    counts = models.IntegerField(blank=True, null=True)
    harmful = models.IntegerField(blank=True, null=True)
    good = models.IntegerField(blank=True, null=True)
    average = models.FloatField(blank=True, null=True)
    health_score = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'hexagons'
        verbose_name_plural = 'hexagons'

class Zipcodes(models.Model):
    id = models.IntegerField(primary_key=True)
    display = models.CharField(max_length=40, blank=True, null=True)
    geo = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'zipcodes'
        verbose_name_plural = 'zipcodes'
