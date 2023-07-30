jQuery(document).ready(function ($) {
    $('.user-search').on('keyup', function () {
        const searchUser = $(this).val().toLowerCase();
        $('.user').each(function (idx, item) {
            let tr = $(item).attr("data-user").toLowerCase();
            let id = $(item).attr("data-id").toLowerCase();
            if (tr.includes(searchUser) || id.includes(searchUser) || searchUser.length < 1) {
                $(item).show();
            } else {
                $(item).hide();
            }
        });
    });
});