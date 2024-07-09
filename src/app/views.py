import csv
import io

from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from faker import Faker

from .models import Main, Schema, Dataset


@login_required
def new_schema(request):
    if request.method == 'GET':
        return render(request, 'new_schema.html')


@login_required
def download_csv(request, dataset_id):
    try:
        dataset_obj = Dataset.objects.get(id=dataset_id)
        response = HttpResponse(dataset_obj.csv_file, content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{dataset_obj.main.title}.csv"'
        return response
    except Dataset.DoesNotExist:
        return HttpResponse(status=404)


@login_required
def generate(request):
    if request.method == 'POST':
        data = request.POST
        main_id = data.get('main_id')
        num_rows = int(data.get('num_rows', 0))
        try:
            main_obj = Main.objects.get(id=main_id, user=request.user)
            schema_rows = Schema.objects.filter(main=main_obj).order_by('order')
            csv_file = generate_csv_data(schema_rows, num_rows, main_obj.column_separator, main_obj.string_separator)
            dataset = Dataset.objects.create(main=main_obj,
                                             csv_file=ContentFile(csv_file.getvalue(), name=f"{main_obj.title}.csv"))
            return JsonResponse({'message': 'CSV generated successfully', 'dataset_id': dataset.id})
        except Main.DoesNotExist:
            return JsonResponse({'error': 'Main object does not exist'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request'}, status=405)


def generate_csv_data(schema_rows, num_rows, column_separator, string_separator):
    fake = Faker()
    output = io.StringIO()
    writer = csv.writer(output, delimiter=column_separator, quotechar=string_separator, quoting=csv.QUOTE_MINIMAL)
    headers = [schema.name for schema in schema_rows]
    writer.writerow(headers)
    for _ in range(num_rows):
        row = []
        for schema in schema_rows:
            row.append(generate_fake_data(schema, fake))
        writer.writerow(row)
    return output


def generate_fake_data(schema, fake):
    match schema.data_type:
        case 'Integer':
            return str(fake.random_int(min=schema.range_from, max=schema.range_to))
        case 'Name':
            return fake.name()
        case 'Email':
            return fake.email()
        case 'Job':
            return fake.job()
        case 'Address':
            return fake.address()
        case 'Phone':
            return fake.phone_number()
        case _:
            return ''


@login_required
def datasets(request, data_id):
    try:
        main_obj = Main.objects.get(id=data_id, user=request.user)
        schema_rows = Schema.objects.filter(main=main_obj).order_by('order')
        dataset_list = Dataset.objects.filter(main=main_obj)
        context = {
            'main': main_obj,
            'schemas': schema_rows,
            'datasets': dataset_list
        }
        return render(request, 'datasets.html', context)
    except Main.DoesNotExist:
        return HttpResponse(status=404)


@login_required
def edit(request, data_id):
    if request.method == 'GET':
        try:
            main_obj = Main.objects.get(id=data_id, user=request.user)
            schema_rows = Schema.objects.filter(main=main_obj).order_by('order')
            context = {
                'main': main_obj,
                'schemas': schema_rows,
            }
            return render(request, 'edit_schema.html', context)
        except Main.DoesNotExist:
            return HttpResponse(status=404)
    elif request.method == 'POST':
        try:
            main_obj = Main.objects.get(id=data_id, user=request.user)
            main_obj.title = request.POST.get('title')
            main_obj.column_separator = request.POST.get('column_separator')
            main_obj.string_separator = request.POST.get('string_separator')
            main_obj.save()
            # Update or create schemas as needed
            # This part depends on how schema data is sent from the form
            # Assuming schemas are sent as a list of dictionaries in request.POST.get('schemas')
            schemas_data = request.POST.get('schemas')
            for schema_data in schemas_data:
                schema_id = schema_data.get('id')
                if schema_id:
                    schema = Schema.objects.get(id=schema_id, main=main_obj)
                    schema.name = schema_data.get('name')
                    schema.data_type = schema_data.get('data_type')
                    schema.order = schema_data.get('order')
                    schema.range_from = schema_data.get('range_from')
                    schema.range_to = schema_data.get('range_to')
                    schema.save()
                else:
                    Schema.objects.create(
                        main=main_obj,
                        name=schema_data.get('name'),
                        data_type=schema_data.get('data_type'),
                        order=schema_data.get('order'),
                        range_from=schema_data.get('range_from'),
                        range_to=schema_data.get('range_to'),
                    )
            return redirect('datasets', data_id=main_obj.id)
        except Main.DoesNotExist:
            return JsonResponse({'error': 'Main object does not exist'}, status=400)
