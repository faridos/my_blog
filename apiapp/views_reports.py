from rest_framework import generics
from rest_framework import status
from django.http import JsonResponse
from django.db.models import Avg, Count, Min, Sum

from .serializers import DataPointSerializer
from .models import Plant, DataPoint
from .utils import *
from .tasks import run_monthly_report_generator_pdf


def get_report_name(number_x, monthly=None, yearly=None):
    # generate random file name
    return "my_report"


class MonthlyReportsCreateView(generics.CreateAPIView):
    """
     API to get the reports of high consuming energy plants in a specific month of a specific solar plant
     here we use normal DataPoint Table, not the MonthlyReport Table,
    """
    serializer_class = DataPointSerializer
    permission_classes = ()

    def get(self, request, *args, **kwargs):
        number_x_months = kwargs["last_x_months"]
        last_x_months_date = TODAY - timedelta(number_x_months * 365 / 12)
        # we get the stuff filtered by  last_x_months_date
        qs = DataPoint.objects.select_related().filter(data_date__gte=last_x_months_date)
        # we sum all energy numbers for each plant name
        result = (qs.objects.values('plant__name').annotate(sum_energy_expected=Sum('energy_expected'),
                                                            sum_energy_observed=Sum('energy_observed'),
                                                            sum_irradiation_expected=Sum('irradiation_expected'),
                                                            sum_irradiation_observed=Sum('irradiation_observed'),
                                                            ).order_by())

        # TODO we generate pdf report/someplotting with pandas/ matplotlib,
        #  save it and fetch it later by its name via another api
        file_name = get_report_name(number_x_months, monthly=True)
        run_monthly_report_generator_pdf.delay(pdf_file_name=file_name
                                               )
        return JsonResponse(result, status=status.HTTP_200_OK)