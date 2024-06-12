from django.core.management import BaseCommand
import os
import time


class Command(BaseCommand):
    def handle(self, *args, **options):
        start_time = time.time()

        os.system("python manage.py makeacademydata")
        os.system("python manage.py makebankdata")
        os.system("python manage.py makebowlingclubdata")
        os.system("python manage.py makebusstopdata")
        os.system("python manage.py makecenterdata")
        os.system("python manage.py makeconveniencestoredata")
        os.system("python manage.py makegasstationdata")
        os.system("python manage.py makehospitaldata")
        os.system("python manage.py makepharmacydata")
        os.system("python manage.py makeschooldata")
        os.system("python manage.py makewelfarecenterdata")
        os.system("python manage.py maketheaterdata")
        os.system("python manage.py makechildwelfarecenterdata")
        os.system("python manage.py makeelectricchargerdata")
        os.system("python manage.py makepolicedata")
        os.system("python manage.py makegymdata")
        os.system("python manage.py makeapartment")

        end_time = time.time()  # command 종료 시간 기록
        elapsed_time = end_time - start_time  # 경과 시간 계산

        print(f"time: {round(elapsed_time, 2)}s")
