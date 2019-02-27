import json

from django.db import IntegrityError
from wbmcrawlr import oms

from oms.models import OmsFill, OmsRun


def create_django_model_from_oms_meta(oms_meta_dict):
    fields = oms_meta_dict['meta']['fields']

    for field in sorted(fields.keys()):
        value = fields[field]

        source_type = value['source_type']
        api_type = value['api_type']
        description = value['description']
        title = value['title']

        django_model = None
        if "float" in source_type:
            django_model = "FloatField("
        elif "varchar" in source_type:
            max_length = source_type.replace("varchar(", "").replace("varchar2(", "").replace(")", "")
            django_model = "CharField(max_length={}, ".format(max_length)
        elif "timestamp" in source_type:
            django_model = "DateTimeField("
        elif "Integer" in api_type:
            django_model = "PositiveIntegerField("
        elif "Fraction" in api_type:
            django_model = "FloatField("
        elif 'String' in api_type:
            django_model = "CharField(max_length=25, "
        elif "Boolean" in api_type:
            django_model = "BooleanField("
        else:
            raise NotImplementedError("Dont know how to handle : {}".format(field))

        print("{} = models.{}help_text='{}', verbose_name='{}')".format(field, django_model, description, title))


def retrieve_fill(fill_number):
    response = oms.get_fills(fill_number, fill_number)[0]

    exclude = ["dump_ready_to_dump_time", "end_stable_beam", "end_time",
               "start_stable_beam", "start_time", "to_dump_ready_time", "to_ready_time"]

    fill_kwargs = {key: value for key, value in response.items() if key not in exclude}

    try:
        return OmsFill.objects.create(**fill_kwargs)
    except IntegrityError:
        return OmsFill.objects.get(fill_number)


def retrieve_run(run_number):
    response = oms.get_runs(run_number, run_number)[0]
    fill_number = response.pop("fill_number")

    exclude = ["start_time", "last_update", "end_time"]

    run_kwargs = {key: value for key, value in response.items() if key not in exclude}

    try:
        fill = OmsFill.objects.get(fill_number=fill_number)
    except OmsFill.DoesNotExist:
        fill = retrieve_fill(fill_number=fill_number)

    try:
        return OmsRun.objects.create(fill=fill, **run_kwargs)
    except IntegrityError:
        return OmsRun.objects.get(run_number=run_number)