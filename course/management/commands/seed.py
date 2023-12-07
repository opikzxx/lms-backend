from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model

import datetime
from datetime import date
import random
from decimal import Decimal

# from authentication.models import User
from lms.models import *
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
    User = get_user_model()
    User.objects.filter(email='tito123@gmail.com').delete()
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
    
    Enrollment.objects.all().delete()
    CourseAssignment.objects.all().delete()
    AssignmentAttachment.objects.all().delete()
    CourseQuiz.objects.all().delete()
    QuizQuestion.objects.all().delete()
    QuizOption.objects.all().delete()
    QuizUser.objects.all().delete()
    QuizUserAnswer.objects.all().delete()
    CourseSession.objects.all().delete()
    LastAccess.objects.all().delete()

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

    reason= {
            "overview": "Digital marketing adalah suatu bidang yang berfokus pada pemasaran dan promosi produk atau layanan menggunakan platform digital seperti internet, media sosial, email, mesin pencari, dan berbagai kanal online lainnya. Ini adalah upaya untuk menjangkau audiens target dan membangun hubungan dengan mereka melalui berbagai metode dan strategi digital.",
            "content": [
                {
                    "title": "Permintaan yang Terus Meningkat",
                    "detail": "Dalam era digital yang terus berkembang, permintaan akan profesional digital marketing terus tumbuh. Bisnis dari berbagai industri mengandalkan digital marketing untuk mencapai audiens mereka secara efektif dan berkompetitif di pasar."
                },
                {
                    "title": "Peluang Karier yang Luas",
                    "detail": "Digital marketing mencakup SEO, email marketing, periklanan online, dan analisis data. Ini memberikan banyak peluang karier yang beragam dan memungkinkan untuk mengejar jalur yang sesuai dengan minat dan kompetensi."
                }
            ]
        }
    

    result = {
        "content": [
            {
                "title": "Real Protofolio",
                "detail": "Lorem ipsum dolor sit amet. Sit quia maiores qui error labore qui suscipit illo et quia sequi sit dolore, "
            },
            {
                "title": "Job Placement Recomendation",
                "detail": "Lorem ipsum dolor sit amet. Sit quia maiores qui error labore qui suscipit illo et quia sequi sit dolore, "
            }
        ]
    }

    skills = ["Marketing;Sales;", "Komunikasi;Data Analisis;Sosial;Media;Advertising;Kepemimpina;Manajemen;Strategi;", ";Brand;Management;Komunikasi Bisnis;"]

    for i in range(5):
        course = CourseDetail.objects.create(
            id=courses[i],
            course_overview=random.choice(course_overviews),
            reason=reason,
            result=result,
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

    benefits= {
            "content": [
                {
                    "title": "lorem ipsum",
                    "detail": True
                },
                {
                    "title": "lorem ipsum",
                    "detail": True
                },
                {
                    "title": "lorem ipsum",
                    "detail": True
                },
                {
                    "title": "lorem ipsum",
                    "detail": True
                },
                {
                    "title": "lorem ipsum",
                    "detail": False
                },
                {
                    "title": "lorem ipsum",
                    "detail": False
                }
            ]
        }

    for i in range(5):
        course = CoursePrice.objects.create(
            course_id=courses[i],
            type=random.choice(types),
            original_price=1000,
            discounted_price=100,
            discount_percentage=90,
            description="Ini deskripsinya",
            benefits=benefits
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

    course_batchs = []

    for i in range(5):
        course = CourseBatch.objects.create(
            course=courses[i],
            status=random.choice(status),
            open_date=date(2020, 12, 31),
            close_date=date(2020, 12, 31),
            start_date=date(2020, 12, 31),
            end_date=date(2020, 12, 31),
            no=i
        )
        course_batchs.append(course)
        print("{} Schedule created.".format(course))
    return course_batchs

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


def create_enrollments(user, course_batchs):
    """Creates an enrollment object combining different elements from the list"""
    print("Creating enrollment")
    enrollments = []
    types = ['BL', 'SR']
    dummy=[
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.", 
        "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat",
        "Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.",
        "Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
    ]

    for i in range(5):
        enrollment = Enrollment.objects.create(
            course_batch=course_batchs[i],
            user=user,
            enrollment_type=random.choice(types),
        )
        enrollments.append(enrollment)
        print("{} enrollment created.".format(enrollment))
    return enrollments

def create_course_assignment(course_batchs):
    """Creates an course assignment object combining different elements from the list"""
    print("Creating course assignment")
    course_assignments = []
    accessibilities = ['OP', 'CL']
    dummy=[
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.", 
        "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat",
        "Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.",
        "Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
    ]

    for i in range(5):
        assignment = CourseAssignment.objects.create(
            course_batch=course_batchs[i],
            accesibility=random.choice(accessibilities),
            title='assignment ' + str(i),
            file=random.choice(dummy),
            ordering=i,
            deadline=date(2020, 12, 31),
        )
        course_assignments.append(assignment)
        print("{} assignment created.".format(assignment))
    return course_assignments

def create_assignment_attachment(user, course_assignments):
    """Creates an Course object combining different elements from the list"""
    print("Creating assignment attachment")

    assignments = []

    status = ['BS', 'RV', 'SL']

    for i in range(5):
        assignment = AssignmentAttachment.objects.create(
            user=user,
            assignment=course_assignments[i],
            status=random.choice(status),
        )
        assignments.append(assignment)
        print("{} assignment created.".format(assignment))
    return assignments

def create_course_quiz(course_batchs):
    """Creates an Course quiz object combining different elements from the list"""
    print("Creating quiz courses")
    quizs=[]
    accesibilities = ['OP', 'CL']
    status = ['DR', 'FN']
    
    questions=[
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.", 
        "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat",
        "Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.",
        "Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
    ]

    answers=[
        "Nunc sed augue lacus viverra vitae congue.",
        "Nulla facilisi etiam dignissim diam quis enim."
        "Pellentesque elit eget gravida cum sociis natoque penatibus et.",
        "Sed elementum tempus egestas sed sed risus pretium quam vulputate."
    ]

    for i in range(5):
        quiz = CourseQuiz.objects.create(
            course_batch=course_batchs[i],
            title=f'quiz {i}',
            duration=10,
            minimum_score=Decimal('50.00'),
            accessibility=random.choice(accesibilities),
            status=random.choice(status),
            ordering=i,
            deadline=date(2020, 12, 31),
        )
        quizs.append(quiz)
        print("{} quiz created.".format(quiz))
        
        for j in range(10):
            question = QuizQuestion.objects.create(
                course_quiz=quiz,
                question=random.choice(questions),
                ordering=j
            )

            for k in range(4):
                if(k==3):
                    QuizOption.objects.create(
                        question=question,
                        value=random.choice(answers),
                        is_correct=True
                    )
                else:
                    QuizOption.objects.create(
                        question=question,
                        value=random.choice(answers),
                    )
    return quizs

def create_course_session(course_batchs):
    """Creates an course session object combining different elements from the list"""
    print("Creating course session")
    sessions = []
    
    dummy=[
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.", 
        "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat",
        "Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.",
        "Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
    ]

    for i in range(5):
        session = CourseSession.objects.create(
            course_batch=course_batchs[i],
            title=random.choice(dummy),
            time=datetime.datetime.now(),
            ordering=1
        )
        sessions.append(session)
        print("{} course session created.".format(session))
    return sessions

def run_seed(self, mode):
    """ Seed database based on mode

    :param mode: refresh / clear 
    :return:
    """
    # Clear data from tables
    clear_data()
    if mode == MODE_CLEAR:
        return
    User = get_user_model()
    user = User.objects.create(
        email='tito123@gmail.com',
        username='tito123',
        password=make_password('tito123'),
        birth_date=date(2000, 11, 11),
        gender='L',
        account_type='PR',
        phone_number='1234567889',
        role='US'
    )

    programs = create_programs()
    teachers = create_teachers()
    courses = create_courses(programs=programs, teachers=teachers)
    
    create_detail_course(courses)
    create_courses_price(courses)
    create_courses_curicullum(courses)
    create_courses_schedule(courses)
    course_batchs = create_course_batch(courses)
    create_course_faq(courses)
    create_course_testimony(courses)

    create_enrollments(user, course_batchs)
    course_assignments = create_course_assignment(course_batchs)
    create_assignment_attachment(user, course_assignments)
    create_course_quiz(course_batchs)
    create_course_session(course_batchs)