#!/usr/bin/python3

from typing import Dict, Union, List, Tuple, Any
import pymysql
from pymysql import Error
import configparser

# 数据库连接配置
sql_config = {
    'host': "127.0.0.1",
    'port': 3304,
    'user': "root",
    'password': "123456",
    'database': "mydata"
}


class Student:

    def __init__(self, **kwargs):
        self.stu_id: str = kwargs.get('stu_id', 'null')
        self.stu_name: str = kwargs.get('stu_name', 'null')
        self.stu_sex: str = kwargs.get('stu_sex', '男')
        self.stu_age: int = kwargs.get('stu_age', 0)
        self.stu_class: str = kwargs.get('stu_class', 'null')
        self.stu_major: str = kwargs.get('stu_major', 'null')
        self.stu_grade: int = kwargs.get('stu_grade', 0)
        self.phone: str = kwargs.get('phone', 'null')
        self.email: str = kwargs.get('email', 'null')
        self.pwd: str = kwargs.get('pwd', 'null')
        self.department: str = kwargs.get('department', 'null')


class Teacher:

    def __init__(self, **kwargs):
        self.teacher_id: str = kwargs.get('teacher_id', 'null')
        self.teacher_name: str = kwargs.get('teacher_name', 'null')
        self.teacher_sex: str = kwargs.get('teacher_sex', '男')
        self.teacher_age: int = kwargs.get('teacher_age', 0)
        self.teacher_title: str = kwargs.get('teacher_title', '教授')
        self.pwd: str = kwargs.get('pwd', 'null')
        self.email: str = kwargs.get('email', 'null')


class Admin:

    def __init__(self, **kwargs):
        self.admin_id = kwargs.get('admin_id', 'null')
        self.admin_name = kwargs.get('admin_name', 'null')
        self.email = kwargs.get('email', 'null')
        self.pwd = kwargs.get('pwd', 'null')


class Course:

    def __init__(self, **kwargs):
        self.course_id = kwargs.get('course_id', 'null')
        self.course_name = kwargs.get('course_name', 'null')
        self.class_type = kwargs.get('class_type', 'null')
        self.credits = kwargs.get('credits', 0)
        self.grade = kwargs.get('grade', 'null')
        self.teacher_id = kwargs.get('teacher_id', 'null')
        self.location = kwargs.get('location', 'null')
        self.class_time = kwargs.get('class_time', 'null')
        self.start_week = kwargs.get('start_week', 0)
        self.end_week = kwargs.get('end_week', 0)
        self.class_capacity = kwargs.get('class_capacity', 0)
        self.class_remain = kwargs.get('class_remain', 0)
        self.class_status = kwargs.get('class_status', 'null')


class Score:

    def __init__(self, **kwargs):
        self.student_id = kwargs.get('student_id', 'null')
        self.course_id = kwargs.get('course_id', 'null')
        self.score = kwargs.get('score', 0)


def login_check(usr: str, pwd: str, usr_type: str) -> bool:
    db = pymysql.connect(**sql_config)
    if usr_type == 'admin':
        sql = f'select * from Admin where Admin_id="{usr}" and pwd="{pwd}"'
    elif usr_type == 'student':
        sql = f'select * from Student where stu_id="{usr}" and pwd="{pwd}"'
    else:
        sql = f'select * from Teacher where teacher_id="{usr}" and pwd="{pwd}"'
    cursor = db.cursor()
    cursor.execute(sql)
    data = cursor.fetchone()
    db.close()
    if data:
        return True
    return False


# 获取所有用户信息
def get_all_usr_info(usr_type: str) -> List[Dict]:
    db = pymysql.connect(**sql_config)
    cursor = db.cursor(pymysql.cursors.DictCursor)
    if usr_type == 'admin':
        sql = 'select * from Admin'
    elif usr_type == 'student':
        sql = 'select * from Student ORDER BY CONVERT(stu_id, SIGNED)'
    else:
        sql = 'select * from Teacher  ORDER BY CONVERT(teacher_id, SIGNED)'
    cursor.execute(sql)
    data = cursor.fetchall()
    db.close()
    return data


# 增加admin账户
def add_admin_info(admin: Admin) -> bool:
    db = pymysql.connect(**sql_config)
    cursor = db.cursor()
    try:
        sql = (
            f'insert into Admin values("{admin.admin_id}","{admin.admin_name}","{admin.email}",'
            f'"{admin.pwd}")')
        cursor.execute(sql)
        db.commit()
    except Error:
        return False
    db.close()
    return True


# 增加stu账户
def add_stu_info(student: Student) -> bool:
    db = pymysql.connect(**sql_config)
    cursor = db.cursor()
    temp = "insert into Student(stu_id,stu_name,stu_sex,stu_class,stu_major,stu_grade,phone,email,pwd,stu_age,department)values"
    try:
        sql = temp + f'("{student.stu_id}","{student.stu_name}","{student.stu_sex}","{student.stu_class}","{student.stu_major}",{student.stu_grade},"{student.phone}","{student.email}","{student.pwd}",{student.stu_age},"{student.department}")'
        cursor.execute(sql)
        db.commit()
    except Error:
        return False
    db.close()
    return True


# 增加teacher账户
def add_teacher_info(teacher: Teacher) -> bool:
    db = pymysql.connect(**sql_config)
    cursor = db.cursor()
    temp = "insert into Teacher(teacher_id,teacher_name,teacher_sex,teacher_age,teacher_title,pwd,email)values"
    try:
        sql = temp + f'("{teacher.teacher_id}","{teacher.teacher_name}","{teacher.teacher_sex}",{teacher.teacher_age},"{teacher.teacher_title}","{teacher.pwd}","{teacher.email}")'
        cursor.execute(sql)
        db.commit()
    except Error:
        return False
    db.close()
    return True


# 获取一个用户信息
def get_usr_info(usr_type: str, usr_id: str,
                 usr_name: str) -> Union[bool, Dict]:
    db = pymysql.connect(**sql_config)
    cursor = db.cursor(pymysql.cursors.DictCursor)
    usr_type, sql = usr_type.lower(), ''
    if usr_type == 'admin':
        sql = f'SELECT * FROM `Admin` WHERE admin_id = "{usr_id}" AND admin_name ="{usr_name}";'
    elif usr_type == 'student':
        sql = f'SELECT * FROM `Student` WHERE stu_id = "{usr_id}" AND stu_name = "{usr_name}";'
    elif usr_type == 'teacher':
        sql = f'SELECT * FROM Teacher WHERE teacher_id="{usr_id}" AND teacher_name="{usr_name}";'
    try:
        cursor.execute(sql)
        data = cursor.fetchall()
    except Error:
        return False
    if len(data) == 0:
        return False
    db.close()
    return data[0]


#通过id获取信息
def get_info_by_id(usr_type: str, usr_id: str) -> Union[bool, Dict]:
    db = pymysql.connect(**sql_config)
    cursor = db.cursor(pymysql.cursors.DictCursor)
    usr_type, sql = usr_type.lower(), ''
    if usr_type == 'admin':
        sql = f'SELECT * FROM `Admin` WHERE admin_id = "{usr_id}";'
    elif usr_type == 'student':
        sql = f'SELECT * FROM `Student` WHERE stu_id = "{usr_id}";'
    elif usr_type == 'teacher':
        sql = f'SELECT * FROM Teacher WHERE teacher_id="{usr_id}";'
    elif usr_type == 'course':
        sql = f'SELECT * FROM CourseInformation WHERE course_id="{usr_id}";'
    try:
        cursor.execute(sql)
        data = cursor.fetchall()
    except Error:
        return False
    if len(data) == 0:
        return False
    db.close()
    return data[0]


# 删除一个用户信息
def del_usr_info(usr_type: str, usr_id: str, usr_name: str) -> bool:
    usr_type = usr_type.lower()
    if not get_usr_info(usr_type, usr_id, usr_name):
        return False
    db = pymysql.connect(**sql_config)
    cursor = db.cursor()
    sql = ''
    if usr_type == 'admin':
        sql = f'DELETE FROM `Admin` WHERE admin_id = "{usr_id}";'
    elif usr_type == 'student':
        sql = f'DELETE FROM `Student` WHERE stu_id = "{usr_id}";'
    elif usr_type == 'teacher':
        sql = f'DELETE FROM `Teacher` WHERE teacher_id="{usr_id}";'
    try:
        cursor.execute(sql)
        db.commit()
    except Error:
        return False
    db.close()
    return True


# 修改一个用户信息
def alter_usr_info(user: Union[Admin, Student, Teacher]) -> bool:
    db = pymysql.connect(**sql_config)
    cursor = db.cursor()

    if type(user) == Admin and cursor.execute(
            f'SELECT * FROM `Admin` WHERE admin_id = "{user.admin_id}";'):
        sql = (
            f'UPDATE `Admin` SET admin_name="{user.admin_name}", email="{user.email}",pwd="{user.pwd}" '
            f' WHERE admin_id="{user.admin_id}";')
    elif type(user) == Student and cursor.execute(
            f'SELECT * FROM `Student` WHERE stu_id = "{user.stu_id}";'):
        sql = (
            f'UPDATE `Student` SET stu_name="{user.stu_name}",stu_sex="{user.stu_sex}",'
            f'stu_class="{user.stu_class}",stu_major="{user.stu_major}",'
            f'stu_grade={user.stu_grade},phone="{user.phone}",'
            f'email="{user.email}",pwd="{user.pwd}",stu_age={user.stu_age},'
            f'department="{user.department}" WHERE stu_id="{user.stu_id}";')
    elif type(user) == Teacher and cursor.execute(
            f'SELECT * FROM `Teacher` WHERE teacher_id = "{user.teacher_id}";'
    ):
        sql = (
            f'UPDATE `Teacher` SET teacher_name="{user.teacher_name}",email="{user.email}",pwd="{user.pwd}",'
            f'teacher_sex="{user.teacher_sex}",teacher_age={user.teacher_age}, teacher_title="{user.teacher_title}"'
            f'where teacher_id="{user.teacher_id}";')
    else:
        return False
    try:
        cursor.execute(sql)
        db.commit()
    except Error:
        return False
    db.close()
    return True


#获取所有课程信息
def get_all_course_info() -> list:
    db = pymysql.connect(**sql_config)
    cursor = db.cursor(pymysql.cursors.DictCursor)
    sql = 'SELECT * FROM `CourseInformation` ORDER BY CONVERT(course_id, SIGNED);'
    try:
        cursor.execute(sql)
        data = cursor.fetchall()
    except Error:
        return False
    db.close()
    return data


#增加一个课程信息
def add_course_info(course: Course) -> bool:
    db = pymysql.connect(**sql_config)
    cursor = db.cursor()
    temp = (
        "INSERT INTO `CourseInformation`(course_id,course_name,class_type,credits,grade,teacher_id,location,"
        "class_time,start_week,end_week,class_capacity,class_remain,class_status) VALUE"
    )
    data = f"('{course.course_id}', '{course.course_name}', '{course.class_type}', {course.credits}, {course.grade},'{course.teacher_id}','{course.location}', '{course.class_time}', {course.start_week},{course.end_week}, {course.class_capacity}, {course.class_remain},'{course.class_status}')"
    print(data)
    sql = temp + data
    print(sql)
    try:
        cursor.execute(sql)
        db.commit()
    except Error:
        return False
    db.close()
    return True


#删除一个课程信息
def del_course_info(course_id: str) -> bool:
    db = pymysql.connect(**sql_config)
    cursor = db.cursor()
    sql = f'DELETE FROM `CourseInformation` WHERE course_id = "{course_id}";'
    try:
        cursor.execute(sql)
        db.commit()
        db.close()
        return True
    except Error:
        db.close()
        return False


#获取所有成绩信息
def get_all_score_info() -> list:
    db = pymysql.connect(**sql_config)
    cursor = db.cursor(pymysql.cursors.DictCursor)
    sql = 'SELECT `Score`.course_id,`CourseInformation`.course_name,`Score`.student_id,`Student`.stu_name,`Score`.score FROM `Score` INNER JOIN `CourseInformation` ON `Score`.course_id = `CourseInformation`.course_id INNER JOIN `Student` ON `Score`.student_id = `Student`.stu_id '
    try:
        cursor.execute(sql)
        data = cursor.fetchall()
    except Error:
        return False
    db.close()
    return data


#增加一个成绩信息
def add_score_info(score: Score) -> bool:
    db = pymysql.connect(**sql_config)
    cursor = db.cursor()
    temp = ("INSERT INTO `Score`(course_id,student_id,score) VALUE")
    data = f"('{score.course_id}', '{score.student_id}', {score.score})"
    sql = temp + data
    # print(sql)
    try:
        cursor.execute(sql)
        db.commit()
        db.close()
        return True
    except Error:
        db.close()
        return False


# 修改一个成绩信息
def update_score_info(score: Score) -> bool:
    db = pymysql.connect(**sql_config)
    cursor = db.cursor()
    sql = f'UPDATE `Score` SET score = {score.score} WHERE course_id = "{score.course_id}" AND student_id = "{score.student_id}";'
    try:
        cursor.execute(sql)
        db.commit()
        db.close()
        return True
    except Error:
        db.close()
        return False


#删除一个成绩信息
def del_score_info(course_id: str, stuent_id: str) -> bool:
    db = pymysql.connect(**sql_config)
    cursor = db.cursor()
    sql = f'DELETE FROM `Score` WHERE course_id = "{course_id}" AND student_id = "{stuent_id}";'
    try:
        cursor.execute(sql)
        db.commit()
        db.close()
        return True
    except Error:
        db.close()
        return False


#查找一个成绩信息
def get_score_info(course_id: str, stuent_id: str) -> list:
    if len(course_id) == 0 and len(stuent_id) == 0:
        return get_all_score_info()
    db = pymysql.connect(**sql_config)
    cursor = db.cursor(pymysql.cursors.DictCursor)
    if len(course_id) != 0 and len(stuent_id) != 0:
        sql = (
            f'SELECT `Score`.course_id, `CourseInformation`.course_name, `Score`.student_id, `Student`.stu_name, '
            f'`Score`.score FROM `Score` INNER JOIN `CourseInformation` ON `Score`.course_id = '
            f'`CourseInformation`.course_id INNER JOIN `Student` ON `Score`.student_id = `Student`.stu_id WHERE '
            f'`Score`.student_id ="{stuent_id}" AND `Score`.course_id = "{course_id}";'
        )
    elif len(course_id) != 0:
        sql = (
            f'SELECT `Score`.course_id, `CourseInformation`.course_name, `Score`.student_id, `Student`.stu_name, '
            f'`Score`.score FROM `Score` INNER JOIN `CourseInformation` ON `Score`.course_id = '
            f'`CourseInformation`.course_id INNER JOIN `Student` ON `Score`.student_id = `Student`.stu_id WHERE '
            f'`Score`.course_id = "{course_id}";')
    elif len(stuent_id) != 0:
        sql = (
            f'SELECT `Score`.course_id, `CourseInformation`.course_name, `Score`.student_id, `Student`.stu_name, '
            f'`Score`.score FROM `Score` INNER JOIN `CourseInformation` ON `Score`.course_id = '
            f'`CourseInformation`.course_id INNER JOIN `Student` ON `Score`.student_id = `Student`.stu_id WHERE '
            f'`Score`.student_id ="{stuent_id}";')
    try:
        cursor.execute(sql)
        result = cursor.fetchall()
        db.close()
        if len(result) == 0:
            return False
        return result

    except Error:
        db.close()
        return None


#通过学号找课表
def get_course_info_by_id(stuent_id: str) -> list:
    db = pymysql.connect(**sql_config)
    cursor = db.cursor(pymysql.cursors.DictCursor)
    sql = f'SELECT course_id FROM `Score` WHERE student_id = "{stuent_id}";'
    try:
        cursor.execute(sql)
        result = cursor.fetchall()
        if len(result) == 0:
            return []
    except Error:
        return []
    ret = []
    for i in result:
        course_id = i['course_id']
        sql = f'SELECT course_name,location, class_time,start_week,end_week FROM `CourseInformation` WHERE course_id = "{course_id}";'
        cursor.execute(sql)
        ret.append(cursor.fetchone())
    db.close()
    return ret


#通过id修改密码
def changePassword(usr_type: str, id: str, new_password: str):
    db = pymysql.connect(**sql_config)
    cursor = db.cursor()
    if usr_type == 'student':
        sql = f'UPDATE `Student` SET `pwd` = "{new_password}" WHERE `stu_id` = "{id}";'
    elif usr_type == 'teacher':
        sql = f'UPDATE `Teacher` SET `pwd` = "{new_password}" WHERE `teacher_id` = "{id}";'
    try:
        cursor.execute(sql)
        db.commit()
        db.close()
        return True
    except Error:
        db.close()
        return False


#查询可选课程
def get_available_courses(grade) -> list:
    db = pymysql.connect(**sql_config)
    sql = f"SELECT course_id,course_name,class_type,credits,class_capacity,class_remain FROM `CourseInformation` WHERE grade='{grade}' AND class_status = '1'"
    cursor = db.cursor(pymysql.cursors.DictCursor)
    try:
        cursor.execute(sql)
        result = cursor.fetchall()
        db.close()
        if len(result) == 0:
            return False
        return result
    except Error:
        db.close()


#选课
def selece_course(stu_id, course_id) -> bool:
    db = pymysql.connect(**sql_config)
    cursor = db.cursor()
    sql = f'INSERT INTO `Score` VALUES ("{stu_id}", "{course_id}", 0)'
    try:
        cursor.execute(sql)
        db.commit()
        db.close()
        return True
    except Error:
        db.close()
        return False


#教师课表
def teacher_course_table(teacher_id) -> list:
    db = pymysql.connect(**sql_config)
    cursor = db.cursor(pymysql.cursors.DictCursor)
    sql = f'SELECT course_name,location, class_time,start_week,end_week FROM `CourseInformation` WHERE teacher_id = "{teacher_id}";'
    try:
        cursor.execute(sql)
        result = cursor.fetchall()
        db.close()
        if len(result) == 0:
            return False
        return result
    except Error:
        db.close()
        return []


#教师名下的学生信息
def get_stu_info_by_teacher_id(teacher_id) -> list:
    db = pymysql.connect(**sql_config)
    cursor = db.cursor(pymysql.cursors.DictCursor)
    sql = (
        f'SELECT `Score`.course_id, `CourseInformation`.course_name, `Score`.student_id, `Student`.stu_name, '
        f'`Score`.score FROM `Score` INNER JOIN `CourseInformation` ON `Score`.course_id = '
        f'`CourseInformation`.course_id INNER JOIN `Student` ON `Score`.student_id = `Student`.stu_id WHERE '
        f'`CourseInformation`.teacher_id = "{teacher_id}";')
    try:
        cursor.execute(sql)
        result = cursor.fetchall()
        db.close()
        if len(result) == 0:
            return []
        return result
    except Error:
        db.close()
        return []


if __name__ == '__main__':
    # print(get_score_info(stuent_id="221603030103"))
    # print(get_info_by_id('student', "221603030415"))
    # print(get_course_info_by_id('221603030415'))
    # print(changePassword('teacher', '100000001', '1111'))
    print(teacher_course_table('100000001'))
    print(get_stu_info_by_teacher_id('100000001'))
