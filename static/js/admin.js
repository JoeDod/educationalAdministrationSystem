//初始化页面
$(document).ready(function () {
    //初始化学生管理页面
    initStudentManagement();
    // 初始化教师管理页面
    initTeacherManagement();
    // 初始化课程管理页面
    initCourseManagement();
    // 初始化成绩管理页面
    initScoreManagement();
    // 初始化搜索和筛选
    searchTable('#studentSearch', '#student-table-body');
    searchTable('#teacherSearch', '#teacher-table-body');
    searchTable('#courseSearch', '#course-table-body');
    searchTable('#gradeSearch', '#grade-table-body');

    filterTable('#studentFilter', '#student-table-body', 0); // 假设筛选学号
    filterTable('#teacherFilter', '#teacher-table-body', 0); // 假设筛选教师编号
    filterTable('#courseFilter', '#course-table-body', 0); // 假设筛选课程编号
    filterTable('#gradeFilter', '#grade-table-body', 0); // 假设筛选学生学号

    //阻止表单默认提交
    $('form').submit(function (e) {
        e.preventDefault();
    });

});

//初始化学生管理页面功能
function initStudentManagement(url) {
    $.getJSON('/get_all_stu_info', function (data) {
        var tableBody = $('#student-table-body');
        tableBody.empty();
        var cnt = 1;
        for (var i = 0; i < data.length; i++) {
            var stu = data[i];
            tableBody.append('<tr>' + '<td>' + cnt + '</td>' + '<td>' + stu.stu_id + '</td>' + '<td>' + stu.stu_name + '</td>' +
                '<td>' + stu.stu_sex + '</td>' + '<td>' + stu.stu_class + '</td>' + '<td>' + stu.stu_major + '</td>' +
                '<td>' + '<button class="btn btn-info btn-sm view_stu" data-toggle="modal" data-target="#viewStudentModal">查看</button>  ' +
                '<button class="btn btn-warning btn-sm edit_stu" data-toggle="modal" data-target="#editStudentModalLabel">修改</button>' +
                '  <button class="btn btn-danger btn-sm del_stu">删除</button>' +
                '</td>' + '</tr>');
            cnt++;
        }
        paginate('#student-table-body', 10);
        stu_but();
    })
}

// 初始化教师管理页面功能
function initTeacherManagement() {
    $.getJSON('/get_all_teacher_info', function (data) {
        var tableBody = $('#teacher-table-body');
        tableBody.empty();
        var cnt = 1;
        for (var i = 0; i < data.length; i++) {
            var teacher = data[i];
            tableBody.append('<tr>' + '<td>' + cnt + '</td>' + '<td>' + teacher.teacher_id + '</td>' + '<td>' + teacher.teacher_name + '</td>' +
                '<td>' + teacher.teacher_sex + '</td>' + '<td>' + teacher.teacher_age + '</td>' + '<td>' + teacher.teacher_title + '</td>' + '<td>' + teacher.email + '</td>'
                + '<td>' + teacher.pwd + '</td>' + '<td>' +
                '<button class="btn btn-warning btn-sm edit_teacher" data-target="editTeacherModal">修改</button>  <button class="btn btn-danger btn-sm delete_teacher">删除</button>' + '</td>' + '</tr>');
            cnt++;
        }
        paginate('#teacher-table-body', 10);
        teacher_but();
    })

}
//初始化课程信息页面功能
function initCourseManagement() {
    $.getJSON('/get_all_course_info', function (data) {
        var tableBody = $('#course-table-body');
        tableBody.empty();
        var cnt = 1;
        //console.log(data);
        for (var i = 0; i < data.length; i++) {
            var course = data[i];
            tableBody.append('<tr>' +
                '<td>' + cnt + '</td>' +
                '<td>' + course.course_id + '</td>' +
                '<td>' + course.teacher_id + '</td>' +
                '<td>' + course.course_name + '</td>' +
                '<td>' + course.class_type + '</td>' +
                '<td>' + course.grade + '</td>' +
                '<td>' + course.credits + '</td>' +
                '<td>' + course.location + '</td>' +
                '<td>' + course.class_time + '</td>' +
                '<td>' + course.start_week + '-' + course.end_week + '</td>' +
                '<td>' + course.class_remain + '/' + course.class_capacity + '</td>' +
                '<td>' + course.class_status + '</td>' +
                '<td>' + '<button class="btn btn-danger btn-sm delete_course">删除</button>' + '</td>' + '</tr>');

            cnt++;
        }
        paginate('#course-table-body', 10);
        course_but();
    })
}

//初始化学生成绩页面功能
function initScoreManagement() {
    $.getJSON('/get_all_score_info', function (data) {
        var tableBody = $('#grade-table-body');
        tableBody.empty();
        var cnt = 1;
        // console.log(data);
        for (var i = 0; i < data.length; i++) {
            var score = data[i];
            tableBody.append('<tr>' +
                '<td>' + cnt + '</td>' +
                '<td>' + score.course_id + '</td>' +
                '<td>' + score.course_name + '</td>' +
                '<td>' + score.student_id + '</td>' +
                '<td>' + score.stu_name + '</td>' +
                '<td>' + score.score + '</td>' +
                '<td>' + '<button class="btn btn-warning btn-sm edit_score" data-toggle="modal" data-target="#editScoreModal">修改</button>  ' +
                '<button class="btn btn-danger btn-sm delete_score">删除</button>' + '</td>' + '</tr>'

            )
            cnt++;
        }
        paginate('#grade-table-body', 10);
        score_but();

    })
}
// 分页功能 
function paginate(tableId, pageSize) {
    var table = $(tableId);
    var rows = table.find('tr');
    var pageCount = Math.ceil(rows.length / pageSize);
    var pagination = $(tableId + '-pagination');

    // 初始化分页按钮
    function renderPagination(currentPage) {
        pagination.html('');
        if (pageCount <= 5) {
            for (var i = 1; i <= pageCount; i++) {
                pagination.append('<li class="page-item"><a class="page-link" href="#" data-page="' + i + '">' + i + '</a></li>');
            }
        } else {
            if (currentPage > 1) {
                pagination.append('<li class="page-item"><a class="page-link" href="#" data-page="' + (currentPage - 1) + '">上一页</a></li>');
            }
            pagination.append('<li class="page-item"><a class="page-link" href="#" data-page="1">1</a></li>');
            if (currentPage > 3) {
                pagination.append('<li class="page-item disabled"><span class="page-link">...</span></li>');
            }
            for (var i = Math.max(2, currentPage - 1); i <= Math.min(pageCount - 1, currentPage + 1); i++) {
                pagination.append('<li class="page-item"><a class="page-link" href="#" data-page="' + i + '">' + i + '</a></li>');
            }
            if (currentPage < pageCount - 2) {
                pagination.append('<li class="page-item disabled"><span class="page-link">...</span></li>');
            }
            pagination.append('<li class="page-item"><a class="page-link" href="#" data-page="' + pageCount + '">' + pageCount + '</a></li>');
            if (currentPage < pageCount) {
                pagination.append('<li class="page-item"><a class="page-link" href="#" data-page="' + (currentPage + 1) + '">下一页</a></li>');
            }
        }

        pagination.find('a').click(function (e) {
            e.preventDefault();
            var page = $(this).data('page');
            renderPage(page);
            renderPagination(page);
        });

        pagination.find('a[data-page="' + currentPage + '"]').parent().addClass('active');
    }

    // 显示指定页
    function renderPage(page) {
        var start = (page - 1) * pageSize;
        var end = start + pageSize;

        rows.hide();
        rows.slice(start, end).show();
    }

    // 跳转功能
    if ($('.jump-to-page').length < 4) {
        pagination.after('<div class="jump-to-page">跳转到 <input type="number" min="1" max="' + pageCount + '" style="width: 50px;" id="jump-page"> 页 <button id="jump-button">跳转</button></div>');
        $('#jump-button').click(function () {
            var page = parseInt($('#jump-page').val());
            if (page >= 1 && page <= pageCount) {
                renderPage(page);
                renderPagination(page);
            }
        });
    }

    // 初始化显示第一页和分页按钮
    renderPage(1);
    renderPagination(1);
}


//增加一个学生
function saveStudentInfo() {
    var form = $('#addStudentForm');
    //console.log(form.serialize());
    $.post('/add_stu_info', form.serialize(), function (response) {
        console.log(response);
        if (response == "success") {
            alert('添加成功');
            location.reload();
            // initStudentManagement();
        } else {
            alert('添加失败：' + response);
        }
    })

}
//修改一个学生
function updateStudent() {
    var form = $('#updateStudentForm');
    console.log(form.serialize());
    $.ajax({
        url: '/update_stu_info',
        type: 'POST',
        data: form.serialize(),
        success: function (response) {
            console.log(response);
            if (response = "success") {
                // 添加成功后刷新页面
                location.reload();
                // initStudentManagement();
                // $('#editStudentModal').hide();
            } else {
                alert('修改失败：' + response);
            }
        }
    })
}
//增加一个教师
function addTeacher() {
    var form = $('#addTeacherForm');
    $.post('/add_teacher_info', form.serialize(), function (response) {
        console.log(response);
        if (response == "success") {
            alert('添加成功');
            location.reload();
        } else {
            alert('添加失败：' + response);
        }
    })
}
//修改一个教师
function updateTeacher() {
    var form = $('#editTeacherForm');
    console.log(form.serialize());
    $.post('/update_teacher_info', form.serialize(), function (response) {
        console.log(response);
        if (response == "success") {
            // 添加成功后刷新页面
            location.reload();
            // initStudentManagement();
            // $('#editStudentModal').hide();
        } else {
            alert('修改失败：' + response);
        }
    })
}
//增加一个课程
function addCourse() {
    var form = $('#addCourseForm');
    console.log(form)
    $.post('/add_course_info', form.serialize(), function (response) {
        if (response == "success") {
            alert('添加成功');
            location.reload();
        }
        else {
            alert('添加失败，请检查输入是否正确');
        }
    })
}
//增加一个成绩
function addScore() {
    var form = $('#addScoreForm');
    $.post('/add_score_info', form.serialize(), function (response) {
        if (response == "success") {
            alert('添加成功');
            location.reload();
        }
        else {
            alert('添加失败：' + response);
        }
    })
}
//修改一个成绩
function editScore() {
    var form = $('#editScoreForm');
    $.post('/update_score_info', form.serialize(), function (response) {
        if (response == "success") {
            alert('修改成功');
            location.reload();
        }
        else {
            alert('修改失败：' + response);
        }
    })

}
// 搜索功能
function findStudent() {
    var stu_id = $('#studentSearch').val();
    //console.log(stu_id);
    $.post('/get_info_by_id', { "id": stu_id, "type": "student" }, function (response) {
        //console.log(response);
        if (response != "false") {
            var tableBody = $('#student-table-body');
            tableBody.empty();
            var stu = response;
            tableBody.append('<tr>' + '<td>' + 1 + '</td>' + '<td>' + stu.stu_id + '</td>' + '<td>' + stu.stu_name + '</td>' +
                '<td>' + stu.stu_sex + '</td>' + '<td>' + stu.stu_class + '</td>' + '<td>' + stu.stu_major + '</td>' +
                '<td>' + '<button class="btn btn-info btn-sm view_stu" data-toggle="modal" data-target="#viewStudentModal">查看</button>  ' +
                '<button class="btn btn-warning btn-sm edit_stu" data-toggle="modal" data-target="#editStudentModalLabel">修改</button>' +
                '  <button class="btn btn-danger btn-sm del_stu">删除</button>' +
                '</td>' + '</tr>');
            paginate('#student-table-body', 10);
            stu_but();
        }
        else {
            alert('查询失败：' + response);
        }
    })
}
function findTeacher() {
    var teacher_id = $('#teacherSearch').val();
    //console.log(teacher_id);
    $.post('/get_info_by_id', { "id": teacher_id, "type": "teacher" }, function (response) {
        if (response != "false") {
            var tableBody = $('#teacher-table-body');
            tableBody.empty();
            var teacher = response;
            tableBody.append('<tr>' + '<td>' + 1 + '</td>' + '<td>' + teacher.teacher_id + '</td>' + '<td>' + teacher.teacher_name + '</td>' +
                '<td>' + teacher.teacher_sex + '</td>' + '<td>' + teacher.teacher_age + '</td>' + '<td>' + teacher.teacher_title + '</td>' + '<td>' + teacher.email + '</td>'
                + '<td>' + teacher.pwd + '</td>' + '<td>' +
                '<button class="btn btn-warning btn-sm edit_teacher" data-target="editTeacherModal">修改</button>  <button class="btn btn-danger btn-sm delete_teacher">删除</button>' + '</td>' + '</tr>');
            paginate('#teacher-table-body', 10);
            teacher_but();
        }
        else {
            alert('查询失败');
        }
    })

}
function findCourse() {
    var course_id = $('#courseSearch').val();
    //console.log(course_id);
    $.post('/get_info_by_id', { "id": course_id, "type": "course" }, function (response) {
        if (response != "false") {
            // console.log(response);
            var tableBody = $('#course-table-body');
            tableBody.empty();
            var course = response;
            tableBody.append('<tr>' +
                '<td>' + 1 + '</td>' +
                '<td>' + course.course_id + '</td>' +
                '<td>' + course.teacher_id + '</td>' +
                '<td>' + course.course_name + '</td>' +
                '<td>' + course.class_type + '</td>' +
                '<td>' + course.grade + '</td>' +
                '<td>' + course.credits + '</td>' +
                '<td>' + course.location + '</td>' +
                '<td>' + course.class_time + '</td>' +
                '<td>' + course.start_week + '-' + course.end_week + '</td>' +
                '<td>' + course.class_remain + '/' + course.class_capacity + '</td>' +
                '<td>' + course.class_status + '</td>' +
                '<td>' + '<button class="btn btn-danger btn-sm delete_course">删除</button>' + '</td>' + '</tr>');

            paginate('#course-table-body', 10);
            course_but();
        }
    })

}
function findScore() {
    var course_id = $('#gradeSearch').val();
    var student_id = $('#studentSearchId').val();
    $.post('search_score_info', { "course_id": course_id, "student_id": student_id }, function (data) {
        if (data != "false") {
            console.log(data);
            var tableBody = $('#grade-table-body');
            tableBody.empty();
            var cnt = 1;
            // console.log(data);
            for (var i = 0; i < data.length; i++) {
                var score = data[i];
                tableBody.append('<tr>' +
                    '<td>' + cnt + '</td>' +
                    '<td>' + score.course_id + '</td>' +
                    '<td>' + score.course_name + '</td>' +
                    '<td>' + score.student_id + '</td>' +
                    '<td>' + score.stu_name + '</td>' +
                    '<td>' + score.score + '</td>' +
                    '<td>' + '<button class="btn btn-warning btn-sm edit_score" data-toggle="modal" data-target="#editScoreModal">修改</button>  ' +
                    '<button class="btn btn-danger btn-sm delete_score">删除</button>' + '</td>' + '</tr>'

                )
                cnt++;
            }
            paginate('#grade-table-body', 10);
            score_but();
        }
        else {
            alert('查询失败');
        }
    })
}

//一些按钮的点击事件
function stu_but() {
    $('.view_stu').click(function () {
        //获取所点击按钮所在行的数据
        var studentId = $(this).closest('tr').find('td:eq(1)').text();
        var studentName = $(this).closest('tr').find('td:eq(2)').text();
        //console.log(studentId, studentName);
        $.post('/get_stu_info', { stu_id: studentId, stu_name: studentName }, function (data) {
            if (data != 'false') {
                $('#viewStudentId').val(data.stu_id);
                $('#viewStudentName').val(data.stu_name);
                $('#viewStudentGender').val(data.stu_sex);
                $('#viewStudentClass').val(data.stu_class);
                $('#viewStudentAge').val(data.stu_age);
                $('#viewStudentPwd').val(data.pwd);
                $('#viewStudentCollege').val(data.department);
                $('#viewStudentMajor').val(data.stu_major);
                $('#viewStudentGrade').val(data.stu_grade);
                $('#viewStudentPhone').val(data.phone);
                $('#viewStudentEmail').val(data.email);
                $('#viewStudentModal').modal('show');
            }
            else {
                alert('该学生不存在');
            }
        })
    })
    //修改按钮
    $('.edit_stu').click(function () {
        //获取所点击按钮所在行的数据
        var studentId = $(this).closest('tr').find('td:eq(1)').text();
        var studentName = $(this).closest('tr').find('td:eq(2)').text();
        //console.log(studentId, studentName);
        $.post('/get_stu_info', { stu_id: studentId, stu_name: studentName }, function (data) {
            console.log(data);
            if (data != 'false') {
                $('#alter_stu_id').val(data.stu_id);
                $('#alter_stu_name').val(data.stu_name);
                $('#alter_stu_sex').val(data.stu_sex);
                $('#alter_stu_class').val(data.stu_class);
                $('#alter_stu_age').val(data.stu_age);
                $('#alter_pwd').val(data.pwd);
                $('#alter_department').val(data.department);
                $('#alter_stu_major').val(data.stu_major);
                $('#alter_stu_grade').val(data.stu_grade);
                $('#alter_phone').val(data.phone);
                $('#alter_email').val(data.email);
                $('#editStudentModal').modal('show');
            } else {
                alert('该学生不存在');
            }
        })

    })
    //删除按钮
    $('.del_stu').click(function () {
        //获取所点击按钮所在行的数据
        var studentId = $(this).closest('tr').find('td:eq(1)').text();
        var studentName = $(this).closest('tr').find('td:eq(2)').text();
        if (confirm('确定要删除该学生吗？\n' + '学号：' + studentId + '\n' + '姓名：' + studentName)) {
            $.post('/delete_stu_info', { stu_id: studentId, stu_name: studentName }, function (data) {
                if (data == 'success') {
                    alert('删除成功');
                    window.location.reload();
                }
                else {
                    alert('删除失败');
                }
            })
        }
    })
}

function teacher_but() {
    //修改按钮
    $('.edit_teacher').click(function () {
        //获取所点击按钮所在行的数据
        var teacherId = $(this).closest('tr').find('td:eq(1)').text();
        var teacherName = $(this).closest('tr').find('td:eq(2)').text();
        //console.log(teacherId, teacherName);
        $.post('/get_teacher_info', { teacher_id: teacherId, teacher_name: teacherName }, function (data) {

            if (data != 'false') {
                // console.log(data);
                //将获取到的数据填充到修改模态框的输入框中
                $('#edit_teacher_id').val(data.teacher_id);
                $('#edit_teacher_name').val(data.teacher_name);
                $('#edit_teacher_sex').val(data.teacher_sex);
                $('#edit_teacher_age').val(data.teacher_age);
                $('#edit_teacher_title').val(data.teacher_title);
                $('#edit_pwd').val(data.pwd);
                $('#edit_email').val(data.email);
                $('#editTeacherModal').modal('show');

            } else {
                alert('该教师不存在');
            }
        })
    })
    // 删除按钮
    $('.delete_teacher').click(function () {
        //获取所点击按钮所在行的数据
        var teacherId = $(this).closest('tr').find('td:eq(1)').text();
        var teacherName = $(this).closest('tr').find('td:eq(2)').text();
        //console.log(teacherId, teacherName);
        $.post('/delete_teacher', { teacher_id: teacherId, teacher_name: teacherName }, function (data) {
            if (data == 'success') {
                alert('删除成功');
                location.reload();
            } else {
                alert('删除失败');
            }
        })
    })
}

function course_but() {
    //修改按钮
    $('.delete_course').click(function () {
        //获取所点击按钮所在行的数据
        var course_id = $(this).closest('tr').find('td:eq(1)').text();
        $.post('/delete_course', { course_id: course_id }, function (data) {
            if (data == 'success') {
                alert('删除成功');
                location.reload();
            }
            else {
                alert('删除失败');
            }
        })
    })
}

function score_but() {
    $('.edit_score').click(function () {
        //获取所点击按钮所在行的数据
        var course_id = $(this).closest('tr').find('td:eq(1)').text();
        var student_id = $(this).closest('tr').find('td:eq(3)').text();
        var score = $(this).closest('tr').find('td:eq(5)').text();
        console.log(course_id, student_id, score);
        $('#student_id').val(student_id);
        $('#courseId').val(course_id);
        $('#score').val(score);

    })
    // 删除按钮
    $('.delete_score').click(function () {
        //获取所点击按钮所在行的数据
        var course_id = $(this).closest('tr').find('td:eq(1)').text();
        var student_id = $(this).closest('tr').find('td:eq(3)').text();
        $.post('/delete_score', { course_id: course_id, stuent_id: student_id }, function (data) {
            if (data == 'success') {
                alert('删除成功');
                location.reload();
            }
            else {
                alert('删除失败');
            }
        })
    })
}