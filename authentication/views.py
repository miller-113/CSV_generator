from django.forms import modelformset_factory
from django.core import serializers
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import SchemaForm, ColumnForm
import csv
import random
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from .models import Schema, Column, DataSet
from faker import Faker
from django.urls import reverse
from django.http import JsonResponse
from django.http import HttpResponse
from django.core.files import File
from io import StringIO
from django.contrib.auth.views import LoginView
from .forms import MyAuthenticationForm

@login_required
def view_schema(request):
    schemas = Schema.objects.all()
    return render(request, 'schemas/view_schema.html', {'schemas': schemas})


@login_required
def create_schema(request, id=None):
    # obj = get_object_or_404(Schema, id=id, user=request.user)
    schema_form = SchemaForm(request.POST or None)
    column_formset = modelformset_factory(Column, form=ColumnForm, extra=2)
    # qs = obj.objects.all()
    formset = column_formset(request.POST or None, queryset=Column.objects.none())
    context = {
        'schema_form': schema_form,
        'formset': formset,
        # 'obj': obj,
    }
    if all([schema_form.is_valid(), formset.is_valid()]):
        schema_ = schema_form.save(commit=False)
        schema_.owner = request.user
        schema_.save()
        for form in formset:
            column = form.save(commit=False)
            column.schema = schema_
            column.save()
        context['message'] = 'Data saved'
    return render(request, "schemas/create_schema.html", context)


@login_required
def schema_detail(request, schema_id):
    schema = get_object_or_404(Schema, id=schema_id)
    return render(request, 'schemas/detail.html', {'schema': schema})


@csrf_exempt
def generate_data(request, schema_id):
    schema = get_object_or_404(Schema, pk=schema_id)

    if request.method == 'POST':

        fake = Faker()
        # Get the number of records to generate from the form data
        num_records = int(request.POST['num_records'])

        # Get the columns for the schema
        columns = Column.objects.filter(schema=schema).order_by('order')

        # Generate fake data for each column
        data = []
        for i in range(num_records):
            record = {}
            for column in columns:
                # Generate fake data based on the column type
                if column.type == 'full_name':
                    record[column.name] = fake.name()
                elif column.type == 'job':
                    record[column.name] = fake.job()
                elif column.type == 'email':
                    record[column.name] = fake.email()
                elif column.type == 'domain_name':
                    record[column.name] = fake.domain_name()
                elif column.type == 'phone_number':
                    record[column.name] = fake.phone_number()
                elif column.type == 'company_name':
                    record[column.name] = fake.company()
                elif column.type == 'text':
                    num_sentences = random.randint(10, 30)
                    record[column.name] = fake.text(num_sentences)
                elif column.type == 'integer':
                    range_start = int(column.range_start) if column.range_start else 0
                    range_end = int(column.range_end) if column.range_end else 100
                    record[column.name] = random.randint(range_start, range_end)
                elif column.type == 'address':
                    record[column.name] = fake.address()
                elif column.type == 'date':
                    record[column.name] = fake.date_between(start_date='-30d',
                                                            end_date='today')
                else:
                    # Handle unknown column types
                    record[column.name] = ''

            data.append(record)
        data_set = DataSet.objects.create(schema=schema, status=True)
        data_set.name = f'{schema.name}.csv'
        headers = [column.name for column in columns]
        data_set.csv.save(data_set.name, StringIO(f'{schema.column_separator}'
                                                  .join(headers)))
        # csv_file_path = os.path.join(settings.MEDIA_ROOT, f'{schema.name}.csv')

        with data_set.csv.open('w') as f:
            writer = csv.writer(f, delimiter=schema.column_separator,
                                quotechar=schema.column_characters,
                                quoting=csv.QUOTE_MINIMAL)

            # Write the headers
            headers = [column.name for column in columns]
            writer.writerow(headers)

            # Write the data
            for record in data:
                row = [record.get(column.name, '') for column in columns]
                writer.writerow(row)

        # Update the schema status to "ready"
        schema.status = 'ready'
        # schema.dataset = data_set
        schema.save()

        # Return the URL to the generated CSV file in the AJAX response data
        download_link = reverse('schemas:download_csv',
                                kwargs={'dataset_id': data_set.id})
        serialized_dataset = serializers.serialize('json', [data_set])
        data = {'download_link': download_link,
                'data_set': serialized_dataset}

        return JsonResponse(data)


def download_csv(request, dataset_id):
    dataset = get_object_or_404(DataSet, pk=dataset_id)

    # Get the path to the generated CSV file
    # file_path = os.path.join(settings.MEDIA_ROOT, f'{dataset.name}.csv')
    file_path = dataset.csv.path

    # Check if the file exists
    if file_path:
        # Open the file and create an HTTP response with the file content
        with open(file_path, 'rb') as f:
            csv_file = File(f)
            response = HttpResponse(csv_file, content_type='text/csv')
            response['Content-Disposition'] = f'attachment; filename="{dataset.name}.csv"'

        return response

    # If the file does not exist, return a 404 error
    return HttpResponse(status=404)


class CustomLoginView(LoginView):
    authentication_form = MyAuthenticationForm



