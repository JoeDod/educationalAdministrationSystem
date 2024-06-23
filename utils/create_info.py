from faker import Faker
from sql import *

fake = Faker(["zh_CN"])

stu_info = {
    'stu_id': '',
    'stu_name': '',
    'stu_sex': '',
    'stu_age': '',
    'stu_class': '',
    'stu_major': '',
    'stu_grade': '',
    'phone': '',
    'email': '',
    'pwd': '',
    'department': ''
}

teacher_info = {
    'teacher_id': '',
    'teacher_name': '',
    'teacher_sex': '',
    'teacher_age': '',
    'teacher_title': '',
    'pwd': '',
    'email': ''
}
course_info = {
    'course_id': '',
    'course_name': '',
    'course_type': '',
    'credits': '',
    'grade': '',
    'teacher_id': '',
    'location': '',
    'class_time': '',
    'start_week': '1',
    'end_week': '16',
    'class_capacity': '',
    'class_remain': '',
    'class_status': ''
}


def create_stu_info(n: int, start_id: int, major: str, grade: int,
                    department: str, stu_class: str):
    stu_lst = []
    for i in range(n):
        stu_info['stu_id'] = str(start_id + i)
        stu_info['stu_sex'] = fake.random_element(elements=('男', '女'))
        if stu_info['stu_sex'] == '男':
            stu_info['stu_name'] = fake.name_male()
        else:
            stu_info['stu_name'] = fake.name_female()
        stu_info['stu_age'] = fake.random_int(min=18, max=25)
        stu_info['stu_class'] = stu_class
        stu_info['stu_major'] = major
        stu_info['stu_grade'] = grade
        stu_info['phone'] = fake.phone_number()
        stu_info['email'] = fake.email()
        stu_info['pwd'] = '123456'
        stu_info['department'] = department
        stu_lst.append(stu_info.copy())
    return stu_lst


def create_teacher_info(n: int, start_id: int, title: list):
    teacher_lst = []
    for i in range(n):
        teacher_info['teacher_id'] = str(start_id + i)
        teacher_info['teacher_name'] = fake.name()
        teacher_info['teacher_sex'] = fake.random_element(elements=('男', '女'))
        teacher_info['teacher_age'] = fake.random_int(min=30, max=60)
        teacher_info['teacher_title'] = fake.random_element(elements=title)
        teacher_info['pwd'] = '123456'
        teacher_info['email'] = fake.email()
        teacher_lst.append(teacher_info.copy())
    return teacher_lst


def create_course_info(n: int, course_name: str, class_time: str,
                       start_id: int, credits: int, grede: int, location: str):
    course_lst = []
    for i in range(n):
        course_info['course_id'] = str(i + 1)
        course_info['course_name'] = course_name
        course_info['course_credit'] = credits
        course_info['grade'] = grede
        course_info['teacher_id'] = str(start_id + i)
        course_info['course_time'] = class_time
        course_info['location'] = location
        course_info['class_capacity'] = 80
        course_info['class_remain'] = 80
        course_info['class_status'] = '1'
        course_lst.append(course_info.copy())
    return course_lst


if __name__ == '__main__':
    #学生信息
    # stu_lst = create_stu_info(24, 221603020101, '计算机科学与技术', 2022, '计算机工程学院',
    #                           '2216030201')
    # for stu in stu_lst:
    #     if not add_stu_info(Student(**stu)):
    #         print('添加失败', stu)
    # print('添加完成')
    #教师信息
    # teacher_lst = create_teacher_info(50, 100000051, ['教授', '副教授', '讲师'])
    # for teacher in teacher_lst:
    #     if not add_teacher_info(Teacher(**teacher)):
    #         print('添加失败', teacher)
    # print('添加完成')
    lst = create_course_info(5, '数据库原理',
                             '{"Friday": 1, "Monday": 1, "Wednesday": 1}',
                             100000003, 1, 2022, '6A301')
    print(lst)
