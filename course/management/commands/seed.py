from django.core.management.base import BaseCommand
import random
from datetime import date

from course.models import *

""" Clear all data and creates addresses """
MODE_REFRESH = 'refresh'

""" Clear all data and do not create any object """
MODE_CLEAR = 'clear'

class Command(BaseCommand):
    help = "seed database for testing and development."

    def add_arguments(self, parser):
        parser.add_argument('--mode', type=str, help="Mode")

    def handle(self, *args, **options):
        self.stdout.write('seeding data...')
        run_seed(self, options['mode'])
        self.stdout.write('done.')

def clear_data():
    """Deletes all the table data"""
    print("Delete all instances")
    Program.objects.all().delete()
    Teacher.objects.all().delete()
    Course.objects.all().delete()
    CourseDetail.objects.all().delete()
    CoursePrice.objects.all().delete()
    CourseCurriculum.objects.all().delete()
    CourseSchedule.objects.all().delete()
    CourseBatch.objects.all().delete()
    CourseFaq.objects.all().delete()
    Testimony.objects.all().delete()

def create_programs():
    """Creates an Program object combining different elements from the list"""
    print("Creating program")
    programs = []
    program_names = ["Carbon Capture Storage", "Executive Learning", "Digital Skills & Talent", "College Preparation", "Trial Class"]
    program_slugs = ["ccs", "el", "dst", "cp", "tc"]

    for i in range(5):
        program = Program.objects.create(
            name=program_names[i],
            slug=program_slugs[i],
        )
        programs.append(program)
        print("{} program created.".format(program))
    return programs

def create_teachers():
    """Creates an Teacher object combining different elements from the list"""
    print("Creating teacher")
    teachers = []
    teacher_names = ["Taufik", "Iqbal", "Adib"]
    teacher_emails = ["taufik@gmail.com", "eureka@gmail.com", "aweu@gmail.com"]
    ocupations = ["Software Engineer", "Developer", "Designer"]

    for i in range(3):
        teacher = Teacher.objects.create(
            name=teacher_names[i],
            email=teacher_emails[i],
            occupation=random.choice(ocupations),
            experience=5
        )
        teachers.append(teacher)
        print("{} teacher created.".format(teacher))
    return teachers

def create_courses(programs, teachers):
    """Creates an Course object combining different elements from the list"""
    print("Creating courses")
    print(teachers)
    courses = []

    course_names = ["Data Science", "Berkebun", "Memasak"]
    status = ['CS', 'AV', 'OG', 'FI']

    for i in range(5):
        course = Course.objects.create(
            program=random.choice(programs),
            # teacher=random.choice(teachers),
            name=random.choice(course_names),
            description="ini course dummy",
            status=random.choice(status),
        )
        course.teacher.set(teachers)
        courses.append(course)
        print("{} course created.".format(course))
    return courses

def create_detail_course(courses):
    """Creates an Course Detail object combining different elements from the list"""
    print("Creating detail courses")

    course_overviews=[
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.", 
        "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat",
        "Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.",
        "Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
    ]

    skills = ["Coding", "Designing"]

    for i in range(5):
        course = CourseDetail.objects.create(
            id=courses[i],
            course_overview=random.choice(course_overviews),
            reason=random.choice(course_overviews),
            result=random.choice(course_overviews),
            skill=random.choice(skills),
        )
        courses.append(course)
        print("{} course created.".format(course))
    return courses

def create_courses_price(courses):
    """Creates an Course Price object combining different elements from the list"""
    print("Creating price courses")

    types=[
        "BL", "SR"
    ]

    for i in range(5):
        course = CoursePrice.objects.create(
            course_id=courses[i],
            type=random.choice(types),
            original_price=1000,
            discounted_price=100,
            discount_percentage=90,
        )
        courses.append(course)
        print("{} price created.".format(course))
    return courses

def create_courses_curicullum(courses):
    """Creates an Course Curicullum object combining different elements from the list"""
    print("Creating curicullum courses")

    titles = [
        "Curicullum 1", "Curicullum 2", "Curicullum 3"
    ]

    detail=[
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.", 
        "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat",
        "Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.",
        "Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
    ]

    for i in range(5):
        course = CourseCurriculum.objects.create(
            course=courses[i],
            title=random.choice(titles),
            detail=random.choice(detail),
        )
        courses.append(course)
        print("{} price created.".format(course))
    return courses

def create_courses_schedule(courses):
    """Creates an Course Schedule object combining different elements from the list"""
    print("Creating schedule courses")

    titles = [
        "Schedule 1", "Schedule 2", "Schedule 3"
    ]

    for i in range(5):
        course = CourseSchedule.objects.create(
            course=courses[i],
            starting_week=1,
            ending_week=14,
            title=random.choice(titles)
        )
        courses.append(course)
        print("{} Schedule created.".format(course))
    return courses

def create_course_batch(courses):
    """Creates an Course Batch object combining different elements from the list"""
    print("Creating batch courses")

    status = [
        "AV", "SO"
    ]

    for i in range(5):
        course = CourseBatch.objects.create(
            course=courses[i],
            status=random.choice(status),
            open_date=date(2020, 12, 31),
            close_date=date(2020, 12, 31),
            start_date=date(2020, 12, 31),
            no=i
        )
        courses.append(course)
        print("{} Schedule created.".format(course))
    return courses

def create_course_faq(courses):
    """Creates an Course Faq object combining different elements from the list"""
    print("Creating faq courses")

    dummy=[
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.", 
        "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat",
        "Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.",
        "Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
    ]

    for i in range(5):
        course = CourseFaq.objects.create(
            course=courses[i],
            order=i,
            question=random.choice(dummy),
            answer=random.choice(dummy),
        )
        courses.append(course)
        print("{} Schedule created.".format(course))
    return courses

def create_course_testimony(courses):
    """Creates an Course Faq object combining different elements from the list"""
    print("Creating testimony courses")

    names = ["Taufik", "Iqbal", "Adib"]
    dummy=[
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.", 
        "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat",
        "Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.",
        "Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
    ]

    for i in range(5):
        course = Testimony.objects.create(
            course=courses[i],
            name=random.choice(names),
            desciption=random.choice(dummy)
        )
        courses.append(course)
        print("{} Testimony created.".format(course))
    return courses

def run_seed(self, mode):
    """ Seed database based on mode

    :param mode: refresh / clear 
    :return:
    """
    # Clear data from tables
    clear_data()
    if mode == MODE_CLEAR:
        return

    programs = create_programs()
    teachers = create_teachers()
    courses = create_courses(programs=programs, teachers=teachers)
    
    create_detail_course(courses)
    create_courses_price(courses)
    create_courses_curicullum(courses)
    create_courses_schedule(courses)
    create_course_batch(courses)
    create_course_faq(courses)
    create_course_testimony(courses)