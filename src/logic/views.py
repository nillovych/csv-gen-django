from django.shortcuts import render
import io
from django.core.files.uploadedfile import InMemoryUploadedFile
from .models import schema, main, dataset
import json
from django.http import JsonResponse, FileResponse
from datetime import date
from django.contrib.auth.decorators import login_required
from faker import Faker
import csv
import random


@login_required
def new_schema(request):
    return render(request, 'new_schema.html')

def download_csv(request, dataset_id):
    dataset_obj = dataset.objects.get(id=dataset_id)
    file_path = dataset_obj.csv_file.path
    file_name = f"{dataset_obj.main.Title}.csv"
    response = FileResponse(open(file_path, 'rb'))
    response['Content-Disposition'] = f'attachment; filename="{file_name}"'
    return response

def generate(request):
    fake = Faker()
    if request.method == 'POST':
        data = json.loads(request.POST['values'])
        main_rows = main.objects.filter(id=data['main_id'])
        schema_rows = schema.objects.filter(main_id = data['main_id']).order_by('Order')

        csv_full = []
        col_names = []

        for i in range(len(schema_rows)):
            col_names.append(schema_rows[i].Name)
        csv_full.append(col_names)

        for i in range(int(data['num_gen'])):
            temp_arr=[]
            for j in range(len(schema_rows)):
                if schema_rows[j].Type == 'Integer':
                    temp_arr.append(random.randint(schema_rows[j].From, schema_rows[j].To))
                elif schema_rows[j].Type == 'Name':
                    temp_arr.append(fake.name())
                elif schema_rows[j].Type == 'Email':
                    temp_arr.append(fake.email(domain='gmail.com'))
                elif schema_rows[j].Type == 'Job':
                    temp_arr.append(fake.job())
                elif schema_rows[j].Type == 'Address':
                    temp_arr.append(fake.address())
                elif schema_rows[j].Type == 'Phone':
                    temp_arr.append(fake.phone_number())
            csv_full.append(temp_arr)
        output = io.StringIO()
        writer = csv.writer(output, delimiter=main_rows[0].Colmn_Sep, quotechar=main_rows[0].Strng_Sep)
        for row in csv_full:
            writer.writerow(row)

        file = InMemoryUploadedFile(output, 'csv_file', f'{main_rows[0].Title}.csv', 'text/csv', len(output.getvalue()), None)

        new_dataset = dataset.objects.create(main=main_rows[0], csv_file=file)
        new_dataset.save()
        dataset_id = dataset.objects.last().id
    return JsonResponse({'message': 'Correct!', 'dataset_id': dataset_id})

def datasets(request, data_id):
    schema_rows = schema.objects.filter(main__id=data_id).order_by('Order')
    main_rows = main.objects.filter(id=data_id)
    datasets = dataset.objects.filter(main__id=data_id)
    context = {
        'schema_rows': schema_rows,
        'main_rows': main_rows,
        'datasets': datasets
    }
    return render(request, 'datasets.html', context)

def edit(request, data_id):
    schema_rows = schema.objects.filter(main__id=data_id)
    main_rows = main.objects.filter(id=data_id)
    print(schema_rows)
    context = {
        'schema_rows': schema_rows,
        'main_rows': main_rows,
    }
    return render(request, 'edit.html', context)

def main_view(request):
    main_data = main.objects.filter(user_id=request.user)
    context = {
        'main_data': main_data
    }
    return render(request, 'home.html', context)

def delete_row(request):
  if request.method == "POST":
    row_id = request.POST.get("row_id")
    main.objects.filter(id=row_id).delete()
    return JsonResponse({"success": True})
  else:
    return JsonResponse({"success": False})

def getting(request):
    if request.method == 'POST':
        data = json.loads(request.POST['values'])
        data_list = list(data.items())
        info_main = main(
            Title=data['name'],
            Colmn_Sep=data['sep'],
            Strng_Sep=data['stch'],
            user=request.user,
        )
        info_main.save()
        del data_list[:3]
        for i in range(len(data_list)):
            if list(data_list[i])[0] == 'Integer':
                info_schema = schema(
                    Name=list(data_list[i])[1]['col_name'],
                    Type=list(data_list[i])[0],
                    Order=int(list(data_list[i])[1]['order']),
                    From=int(list(data_list[i])[1]['input1']),
                    To=int(list(data_list[i])[1]['input2']),
                    main=info_main
                )
                info_schema.save()
            else:
                info_schema = schema(
                    Name=list(data_list[i])[1]['col_name'],
                    Type=list(data_list[i])[0],
                    Order=int(list(data_list[i])[1]['order']),
                    main=info_main
                )
                info_schema.save()
        return JsonResponse({'message': 'Correct!'})

def getting_edit(request):
    if request.method == 'POST':
        data = json.loads(request.POST['values'])
        data_list = list(data.items())
        main.objects.filter(id=data['main_id']).update(
            Title=data['name'],
            Colmn_Sep=data['sep'],
            Strng_Sep=data['stch'],
            Date=date.today(),
        )
        del data_list[:4]
        schema.objects.filter(main_id=data['main_id']).delete()
        for i in range(len(data_list)):
            if list(data_list[i])[0] == 'Integer':
                info_schema = schema(
                    Name=list(data_list[i])[1]['col_name'],
                    Type=list(data_list[i])[0],
                    Order=int(list(data_list[i])[1]['order']),
                    From=int(list(data_list[i])[1]['input1']),
                    To=int(list(data_list[i])[1]['input2']),
                    main_id=data['main_id']
                )
                info_schema.save()
            else:
                info_schema = schema(
                    Name=list(data_list[i])[1]['col_name'],
                    Type=list(data_list[i])[0],
                    Order=int(list(data_list[i])[1]['order']),
                    main_id=data['main_id']
                )
                info_schema.save()


    return JsonResponse({'message': 'Correct!'})