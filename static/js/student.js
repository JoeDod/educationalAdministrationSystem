$(document).ready(function () {
    var studentId = document.getElementById('studentId').innerText;
    var grade = document.getElementById('grade').innerText;
    // 发送Ajax请求获取学生成绩信息
    console.log(studentId)
    $.post('search_score_info', { "student_id": studentId, "course_id": "" }, function (data) {
        // console.log(data)
        var tableBody = $('#grades-table')
        tableBody.empty()
        for (i in data) {
            var row = $('<tr>')
            row.append($('<td>').text(data[i].course_name))
            row.append($('<td>').text(data[i].score))
            tableBody.append(row)
        }
    })
    $.post('search_course_info', { "student_id": studentId }, function (data) {
        // 遍历返回的课程数据
        data.forEach(course => {
            const { course_name, location, class_time, start_week, end_week } = course;
            const classTimeObj = JSON.parse(class_time);

            Object.keys(classTimeObj).forEach(day => {
                const timeSlot = classTimeObj[day];
                const cellId = `${day}-${timeSlot}`;
                const cell = document.getElementById(cellId);
                if (cell) {
                    // 创建一个新的 div 元素，用于显示课程信息
                    var courseInfoDiv = document.createElement('div');
                    courseInfoDiv.innerHTML = `${course_name}<br>${location}<br>${start_week}-${end_week}周`;

                    // 将新的课程信息追加到现有内容的末尾
                    cell.appendChild(courseInfoDiv);
                }
            });
        });
    });

    $.post('get_available_courses', { "grade": grade }, function (courses) {
        console.log(courses);
        console.log(grade);
        // 获取选课框元素
        var courseSelect = $('#courseSelect');

        // 遍历课程数据并添加到选课框
        courses.forEach(course => {
            const { course_id, course_name, class_type, credits, class_capacity, class_remain } = course;
            var optionText = `${course_name} (${credits}学分, ${class_remain}/${class_capacity}名额)`;
            var option = $('<option>').val(course_id).text(optionText);
            courseSelect.append(option);
        });
    });

    $('form').on('submit', function (event) {
        event.preventDefault();

        // 获取选中的课程号
        var selectedCourses = $('#courseSelect').val();

        // 发送Ajax请求提交选课数据
        $.post('add_course_to_student', {
            "student_id": studentId,
            "course_id": selectedCourses
        }, function (response) {
            // 处理服务器返回的响应
            if (response == 'success') {
                alert('选课成功');
                location.reload();
            } else {
                alert('选课失败');
            }
        }
        );
    });
})

function changePassword() {
    var newPassword = document.getElementById('pwd').value;
    var studentId = document.getElementById('studentId').innerText;
    console.log(newPassword)
    $.post('/change_password', { 'type': 'student', 'password': newPassword, 'id': studentId }, function (data) {
        if (data == 'success') {
            alert('修改成功')
        }
        else {
            alert('修改失败')
        }
    }
    )
}

