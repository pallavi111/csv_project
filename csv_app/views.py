from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from .forms import CSVUploadForm
from .models import CSVUpload, Person
import pandas as pd
import time
from django.db import IntegrityError
from django.shortcuts import render, get_object_or_404
from .models import CSVUpload
import pandas as pd
import time 

def upload_csv(request):
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_instance = form.save(commit=False)
            csv_instance.status = 'PROCESSING'
            csv_instance.save()

            start_time = time.time()
            try:
                # Read CSV file
                df = pd.read_csv(csv_instance.file)

                total_records = len(df)
                duplicate_count = 0

                # Track duplicates within this CSV upload
                seen = set()

                for _, row in df.iterrows():
                    key = (row['Email'], row['Phone'])
                    is_duplicate = False

                    # Duplicate inside CSV
                    if key in seen:
                        is_duplicate = True
                        duplicate_count += 1
                    else:
                        seen.add(key)

                    # Handle blank Age
                    age_value = row['Age']
                    if pd.isna(age_value):
                        age_value = 0

                    # Always create a new Person record
                    Person.objects.create(
                        first_name=row['FirstName'],
                        last_name=row['LastName'],
                        email=row['Email'],
                        phone=row['Phone'],
                        age=int(age_value),
                        city=row['City'],
                        country=row['Country'],
                        upload=csv_instance,
                        is_duplicate=is_duplicate
                    )

                end_time = time.time()
                # Update CSVUpload instance
                csv_instance.total_records = total_records
                csv_instance.duplicate_count = duplicate_count
                csv_instance.processing_time = round(end_time - start_time, 2)
                csv_instance.status = 'COMPLETED'
                csv_instance.save()

            except Exception as e:
                csv_instance.status = 'FAILED'
                csv_instance.save()
                print("CSV Processing Error:", e)

            return redirect('dashboard')
    else:
        form = CSVUploadForm()
    return render(request, 'csv_app/upload.html', {'form': form})


def dashboard(request):
    uploads = CSVUpload.objects.all().order_by('-uploaded_at')
    return render(request, 'csv_app/dashboard.html', {'uploads': uploads})

def upload_detail(request, upload_id):
    upload = get_object_or_404(CSVUpload, id=upload_id)
    # Filter only duplicates for this upload
    duplicates = upload.people.filter(is_duplicate=True).order_by('id')
    all_records = upload.people.all().order_by('id')
    return render(request, 'csv_app/upload_detail.html', {
        'upload': upload,
        'all_records': all_records,
        'duplicates': duplicates
    })

