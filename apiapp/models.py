from django.db import models


# Create your models here.
class Plant(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class DataPoint(models.Model):
    """
      here I divided the datetime to date and hour for better controll: for example:
      - easier to get observed energy between 23h and 24h of(which is 00 of next date)4
      - maybe also  reports with lesser calculations when working with dates
    """
    plant = models.ForeignKey(Plant,
                              related_name='plant_data',
                              on_delete=models.CASCADE)
    data_date = models.DateField()
    data_hour = models.CharField(max_length=10)
    energy_expected = models.FloatField(null=True, default=0)
    energy_observed = models.FloatField(null=True, default=0)
    irradiation_expected = models.FloatField(null=True, default=0)
    irradiation_observed = models.FloatField(null=True, default=0)

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        unique_together = ['plant', 'data_date', 'data_hour']  # in case some update needed, we make sure about unicity


# class DailyReport(models.Model):
#     plant = models.ForeignKey(Plant,
#                               related_name='plant_daily_reports',
#                               on_delete=models.CASCADE)
#
#     data_date = models.CharField(max_length=10)
#     energy_expected = models.FloatField(default=0)
#     energy_observed = models.FloatField(default=0)
#     irradiation_expected = models.FloatField(default=0)
#     irradiation_observed = models.FloatField(default=0)


# class MonthlyReport(models.Model):
#     plant = models.ForeignKey(Plant,
#                               related_name='plant_monthly_reports',
#                               on_delete=models.CASCADE)
#
#     data_year = models.CharField(max_length=10)
#     data_month = models.CharField(max_length=10)
#     energy_expected = models.FloatField(default=0)
#     energy_observed = models.FloatField(default=0)
#     irradiation_expected = models.FloatField(default=0)
#     irradiation_observed = models.FloatField(default=0)


# class YearlyReport(models.Model):
#     plant = models.ForeignKey(Plant,
#                               related_name='plant_yearly_reports',
#                               on_delete=models.CASCADE)
#
#     data_year = models.CharField(max_length=10)
#     energy_expected = models.FloatField(default=0)
#     energy_observed = models.FloatField(default=0)
#     irradiation_expected = models.FloatField(default=0)
#     irradiation_observed = models.FloatField(default=0)
