from flask import Flask, render_template, request, session, redirect, url_for, jsonify
from utils.sql import *
from utils.codeImage import *
import io

app = Flask(__name__)
app.secret_key = 'abc123'
app.permanent_session_lifetime = 100000


#检查登录状态，未登录重定向到登录页面
@app.before_request
def before_request():
    if request.endpoint not in ['login', 'static', 'captcha'
                                ] and 'id' not in session:
        return redirect(url_for('login'))


@app.route('/')
def index():
    if 'usr_type' in session:
        if session['usr_type'] == 'admin':
            return render_template('admin.html', username=session['id'])
        elif session['usr_type'] == 'student':
            data = get_info_by_id("student", session['id'])
            return render_template('student.html',
                                   name=data['stu_name'],
                                   id=data['stu_id'],
                                   major=data['stu_major'],
                                   grade=data['stu_grade'],
                                   pwd=data['pwd'])

        else:
            data = get_info_by_id("teacher", session['id'])
            return render_template('teacher.html',
                                   name=data['teacher_name'],
                                   id=data['teacher_id'],
                                   pwd=data['pwd'],
                                   email=data['email'])

    else:
        return redirect(url_for('login'))


#登录
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        code = request.form['captcha']
        if code.upper() != session['code']:
            return render_template('login.html', error='验证码错误')
        usr_id, pwd, usr_type, = request.form['usr_id'], request.form[
            'pwd'], request.form['role'],
        if login_check(usr_id, pwd, usr_type):
            session['id'] = usr_id
            session['usr_type'] = usr_type
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error='账号或密码错误')
    return render_template('login.html')


#验证码
@app.route('/captcha', methods=['GET'])
def captcha():
    image, code = check_code()
    session['code'] = code.upper()
    buffer = io.BytesIO()
    image.save(buffer, 'JPEG')
    return buffer.getvalue()


#登出
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


#获取所有学生信息
@app.route('/get_all_stu_info')
def get_all_stu_info():
    return get_all_usr_info('student')


#获取所有教师信息
@app.route('/get_all_teacher_info')
def get_all_teacher_info():
    return get_all_usr_info('teacher')


#获取一个学生信息
@app.route('/get_stu_info', methods=['POST'])
def get_stu_info():
    stu_id = request.form['stu_id']
    stu_name = request.form['stu_name']
    return get_usr_info('student', stu_id, stu_name)


#增加一个学生信息
@app.route('/add_stu_info', methods=['POST'])
def add_stu():
    if add_stu_info(Student(**request.form)):
        return "success"
    else:
        return "false"


#更新一个学生信息
@app.route('/update_stu_info', methods=['POST'])
def update_stu_info():
    if alter_usr_info(Student(**request.form)):
        return "success"
    return "请检查后再试"


#删除一个学生信息
@app.route('/delete_stu_info', methods=['POST'])
def delete_stu_info():
    if del_usr_info("student", request.form['stu_id'],
                    request.form['stu_name']):
        return "success"
    return "请检查后再试"


#增加一个教师信息
@app.route('/add_teacher_info', methods=['POST'])
def add_teacher():
    if add_teacher_info(Teacher(**request.form)):
        return "success"
    return "false"


#获取一个教师信息
@app.route('/get_teacher_info', methods=['POST'])
def get_teacher():
    return get_usr_info('teacher', request.form['teacher_id'],
                        request.form['teacher_name'])


#更新一个教师信息
@app.route('/update_teacher_info', methods=['POST'])
def update_teacher_info():

    if alter_usr_info(Teacher(**request.form)):
        return "success"
    print(request.form)
    return "请检查后再试"


#删除一个教师信息
@app.route('/delete_teacher', methods=['POST'])
def delete_teacher():
    if del_usr_info("teacher", request.form['teacher_id'],
                    request.form['teacher_name']):
        return "success"
    return "请检查后再试"


#获取所有课程信息
@app.route('/get_all_course_info', methods=['GET'])
def all_course_info():
    return get_all_course_info()


#增加一个课程信息
@app.route('/add_course_info', methods=['POST'])
def add_course():
    if add_course_info(Course(**request.form)):
        return "success"
    return "false"


#删除一个课程信息
@app.route('/delete_course', methods=['POST'])
def delete_course():
    if del_course_info(request.form['course_id']):
        return "success"
    return "请检查后再试"


#获取所有成绩信息
@app.route('/get_all_score_info', methods=['GET'])
def all_score_info():
    # print(get_all_score_info())
    return get_all_score_info()


#删除一个成绩信息
@app.route('/delete_score', methods=['POST'])
def delete_score():
    if del_score_info(request.form['course_id'], request.form['stuent_id']):
        return "success"
    return "请检查后再试"


#增加一个成绩信息
@app.route('/add_score_info', methods=['POST'])
def add_score():
    if add_score_info(Score(**request.form)):
        return "success"
    return "false"


#修改一个成绩信息
@app.route('/update_score_info', methods=['POST'])
def update_score():
    if update_score_info(Score(**request.form)):
        return "success"
    return "false"


#通过id获取信息
@app.route('/get_info_by_id', methods=['POST'])
def get_info():
    if get_info_by_id(request.form['type'], request.form['id']):
        return get_info_by_id(request.form['type'], request.form['id'])
    return "false"


#查找成绩信息
@app.route('/search_score_info', methods=['POST'])
def search_score():
    msg = get_score_info(request.form['course_id'], request.form['student_id'])
    if msg:
        return msg
    return "false"


#学生课表
@app.route('/search_course_info', methods=['POST'])
def search_course():
    msg = get_course_info_by_id(request.form['student_id'])
    if msg:
        return msg
    return "false"


#修改密码
@app.route('/change_password', methods=['POST'])
def change_password():
    if changePassword(request.form['type'], request.form['id'],
                      request.form['password']):
        return "success"
    return "false"


#课程选择查询
@app.route('/get_available_courses', methods=['POST'])
def available_courses():
    msg = get_available_courses(request.form['grade'])
    if msg:
        return msg
    return "false"


#选课
@app.route('/add_course_to_student', methods=['POST'])
def add_course_to_student():
    if selece_course(request.form['student_id'],
                     request.form.getlist('course_id[]')[0]):
        return "success"
    return "false"


#教师课表
@app.route('/search_course_info_by_teacher', methods=['POST'])
def search_course_by_teacher():
    print(request.form)
    mas = teacher_course_table(request.form['teacher_id'])
    print(mas)
    if mas:
        return mas
    return "false"


#通过教师获取学生成绩
@app.route('/get_score_info_by_teacher', methods=['POST'])
def get_score_info_by_teacher():
    msg = get_stu_info_by_teacher_id(request.form['teacher_id'])
    if msg:
        return msg
    return "false"


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)
