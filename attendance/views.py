from django.shortcuts import render

# Create your views here.
def attendance_sheet(request):
    return render(request, 'attendance/attendance_sheet.html')