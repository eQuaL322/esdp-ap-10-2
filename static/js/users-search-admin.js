jQuery(document).ready(function ($) {
    $('.user-search').on('keyup', function () {
        const searchUser = $(this).val().toLowerCase();
        $('.user').each(function (idx, item) {
            let student = $(item).attr("data-student").toLowerCase();
            let teacher = $(item).attr("data-teacher").toLowerCase();
            let studentID = $(item).attr("data-student-id").toLowerCase();;
            let teacherID = $(item).attr("data-teacher-id").toLowerCase();;
            if (student.includes(searchUser) || teacher.includes(searchUser) || studentID.includes(searchUser) || teacherID.includes(searchUser) || searchUser.length < 1) {
                $(item).show();
            } else {
                $(item).hide();
            }
        });
    });
});