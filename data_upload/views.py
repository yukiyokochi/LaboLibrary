from django.shortcuts import render
from search.models import LaboratoryInfo
from mypage.models import UniversityArea, University, Faculty, Department, Laboratory
import csv
from io import TextIOWrapper, StringIO
from django.utils import timezone
from django.db.utils import IntegrityError, DataError


def upload(request):
    if 'csv' in request.FILES:
        form_data = TextIOWrapper(request.FILES['csv'].file, encoding='utf-8')
        csv_file = csv.reader(form_data)
        for line in csv_file:
            try:
                try:
                    if line[0] == '0':
                        try:
                            UniversityArea.objects.get(university_area=line[1])
                            print('UniversityArea objects already exist.')
                        except UniversityArea.DoesNotExist:
                            univ_area = UniversityArea.objects.create(university_area=line[1])
                            univ_area.save()
                            print('UniversityArea objects registered.')
                        pass
                    elif line[0] == '1':
                        try:
                            University.objects.get(
                                university=line[2],
                            )
                            print('University objects already exist.')
                        except University.DoesNotExist:
                            univ = University.objects.create(
                                university=line[2],
                                university_system=0,
                                university_area=UniversityArea.objects.get(university_area=line[1])
                            )
                            univ.university_area = UniversityArea.objects.get(university_area=line[1])
                            univ.university_system = 0
                            univ.save()
                            print('University objects registered.')
                        pass
                    elif line[0] == '2':
                        print(University.objects.filter(university=line[1]))
                        try:
                            i = Faculty.objects.get(
                                faculty=line[2],
                                belong_university=University.objects.get(university=line[1])
                            )
                            print(f'Faculty objects already exist. Faculty : {i}')
                        except Faculty.DoesNotExist:
                            faculty = Faculty.objects.create(
                                faculty=line[2],
                                belong_university=University.objects.get(university=line[1])
                            )
                            faculty.save()
                            print('Faculty objects registered.')
                        pass
                    elif line[0] == '3':
                        # print(Faculty.objects.get(faculty=line[2]))
                        print(line[2])
                        print(line[3])
                        try:
                            check = Department.objects.get(
                                department=line[3], belong_faculty=Faculty.objects.get(faculty=line[2])
                            )
                            print(check)
                            print('Department objects already exist.')
                        except Department.DoesNotExist:
                            belong_faculty = Faculty.objects.get(faculty=line[2])
                            print(belong_faculty)
                            department = Department.objects.create(
                                department=line[3], belong_faculty=belong_faculty
                            )
                            department.save()
                            print('Department objects registered.')
                        pass
                    elif line[0] == '4':
                        try:
                            Laboratory.objects.get(
                                laboratory_name=line[4],
                                belong_university=University.objects.get(university=line[1]),
                                belong_faculty=Faculty.objects.get(faculty=line[2]),
                                belong_department=Department.objects.get(department=line[3])
                            )
                            print('Laboratory objects already exist.')
                        except Laboratory.DoesNotExist:
                            lab = Laboratory.objects.create(
                                laboratory_name=line[4],
                                belong_university=University.objects.get(university=line[1]),
                                belong_faculty=Faculty.objects.get(faculty=line[2]),
                                belong_department=Department.objects.get(department=line[3])
                            )
                            lab.save()
                            print('Laboratory objects registered.')

                        except Department.DoesNotExist:
                            print(f'department : {line[3]}')

                        pass
                    elif line[0] == '5':
                        if len(line[8]) > 99:
                            print(f'Too long information Error --- Laboratory :{line[4]}')
                            keywords = line[8]
                            line[8] = keywords[:90] + '...'
                            print(f'{line[8]}')
                        try:
                            i = LaboratoryInfo.objects.get(
                                laboratory=Laboratory.objects.filter(
                                    laboratory_name=line[4]
                                ).filter(
                                    belong_department=Department.objects.get(department=line[3])
                                )[0],
                                professor_name=line[5],
                                research_info=line[6],
                                laboratory_website=line[7],
                                research_keywords=line[8],
                                information_source=line[9]
                            )
                            print('LaboratoryInfo objects already exist.')
                        except DataError:
                            print(f'DataError LaboratoryInfo : {i}')
                        except LaboratoryInfo.DoesNotExist:
                            lab_info = LaboratoryInfo.objects.create(
                                laboratory=Laboratory.objects.filter(
                                    laboratory_name=line[4]
                                ).filter(
                                    belong_department=Department.objects.get(department=line[3])
                                )[0],
                                professor_name=line[5],
                                research_info=line[6],
                                laboratory_website=line[7],
                                research_keywords=line[8],
                                information_source=line[9]
                            )
                            lab_info.save()
                            print('LaboratoryInfo objects registered.')
                        except Department.DoesNotExist:
                            print(f'department : {line[3]}')
                except IntegrityError as e:
                    print(f'Error={e}')
                    pass
            except IndexError:
                pass
            # print(line)
            # laboratory = LaboratoryInfo.objects.create(laboratory_name=line[0])
            # laboratory.laboratory_name = line[0]
            # laboratory.university = line[1]
            # laboratory.department = line[2]
            # laboratory.professor_name = line[3]
            # laboratory.research_keywords = line[4]
            # laboratory.research_info = line[5]
            # laboratory.laboratory_website = line[6]
            # laboratory.information_source = line[7]
            # laboratory.create_date = timezone.now
            # laboratory.update_date = timezone.now
            #
            # laboratory.save()

        return render(request, 'data_upload/upload.html')

    else:
        return render(request, 'data_upload/upload.html')
