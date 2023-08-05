import csv

from django.forms import model_to_dict
from django.http import HttpResponse

def generate_csv_from_queryset(queryset, csv_name = "query_csv"):
    """
    Genera un file csv a partire da un oggetto di tipo QuerySet
    :param queryset: oggetto di tipo QuerySet
    :param csv_name: campo opzionale per indicare il nome di output del csv
    :return: oggetto response
    """
    try:

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=' + csv_name + '.csv'

        model_field_names = []
        writer = csv.writer(response, delimiter=';')

        if isinstance(queryset.first(), dict):
            fields = queryset.first().keys()
        else:
            fields = [field.attname.split('_id')[0] if field.attname.endswith('_id') else field.attname for field in queryset.first()._meta.local_fields]

        for field in fields:
            model_field_names.append(field)
        writer.writerow(model_field_names)

        for query in queryset:
            csv_row = []
            for field in fields:
                csv_row.append(query[field] if isinstance(query, dict) else model_to_dict(query)[field])

            writer.writerow(csv_row)

        return response
    except Exception as e:
        return e