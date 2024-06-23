$(document).ready(function () {
    var teacher_id = document.getElementById('teacher_id').innerText;

    $.post('search_course_info_by_teacher', { "teacher_id": teacher_id }, function (data) {
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

    // 获取学生成绩
    $.post('get_score_info_by_teacher', { "teacher_id": teacher_id }, function (gradesData) {
        // 动态生成表格行
        // 动态生成表格行
        gradesData.forEach(function (item) {
            var row = '<tr>' +
                '<td>' + item.course_id + '</td>' +
                '<td>' + item.course_name + '</td>' +
                '<td>' + item.student_id + '</td>' +
                '<td>' + item.stu_name + '</td>' +
                '<td class="editable" data-studentid="' + item.student_id + '" data-courseid="' + item.course_id + '">' + item.score + '</td>' +
                '</tr>';
            $('#gradesTableBody').append(row);
        });
    })

    // 添加双击事件，使成绩可编辑
    $('#gradesTable').on('dblclick', '.editable', function () {
        var originalValue = $(this).text().trim();
        var studentId = $(this).data('studentid');
        var courseId = $(this).data('courseid');

        // 替换为输入框
        $(this).html('<input type="text" class="form-control" value="' + originalValue + '">');

        // 监听输入框的回车键事件
        $(this).children().first().focus().keypress(function (e) {
            if (e.which == 13) {
                var newValue = $(this).val().trim();
                $(this).parent().text(newValue);
                // 发送Ajax请求保存成绩
                saveGrade(studentId, courseId, newValue);
            }
        });
    });

    // Ajax保存成绩
    function saveGrade(studentId, courseId, grade) {
        // console.log(studentId, courseId, grade)
        $.post('/update_score_info', { "student_id": studentId, "course_id": courseId, "score": grade }, function (data) {
        })
    }
});