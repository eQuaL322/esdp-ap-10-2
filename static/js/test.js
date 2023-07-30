$(document).ready(function () {
    let json = {
        "limit": 10,
        "offset": 0
    };

    let content = JSON.stringify(json);
    let base = btoa(content);
    let postData = {
        "user": "798fa12deb050afabfd1c6bd481c8633",
        "key": "578b341dea8d2c84b714923bdd11736e",
        "action": "webinars-list",
        "content": base
    };

    $.ajax({
        type: "POST",
        dataType: "json",
        url: "https://pruffme.com/api/",
        data: postData,
        success: function (data) {
            console.log(data);

            let list_web = document.getElementById('list');
            list_web.innerHTML = '';

            if (data.result && data.result.length > 0) {
                for (let i = 0; i < data.result.length; i++) {
                    let webinar = data.result[i];

                    function createWebinarElement(webinar, i) {
                        let webinarElement = document.createElement('div');
                        webinarElement.innerHTML =
                            '<h3>Webinar ' + i + '</h3>' +
                            '<p>Name: ' + webinar.name + '</p>' +
                            '<p>Creationdate: ' + webinar.creationdate + '</p>' +
                            '<p>has_questions: ' + webinar.has_questions + '</p>' +
                            '<p>id: ' + webinar.id + '</p>' +
                            '<p>landing: ' + webinar.landing + '</p>' +
                            '<p>password: ' + webinar.password + '</p>' +
                            '<p>Hash: ' + webinar.hash + '</p>';
                        return webinarElement;
                    }

                    list_web.appendChild(createWebinarElement(webinar, i)
                    )
                }
            } else {
                let noWebinars = document.createElement('p');
                noWebinars.textContent = 'No webinars found.';
                list_web.appendChild(noWebinars);
            }
        },
        error: function (e) {
            console.log(e.message);
        }
    });

    $('#createWebinarForm').submit(function (event) {
        event.preventDefault();

        let webinarName = encodeURIComponent($('#webinarName').val());
        let webinarDate = $('#webinarDate').val();
        let webinarPass = encodeURIComponent($('#webinarPass').val());
        let webinarType = $('#webinarType').val();

        console.log(webinarName);
        console.log(webinarDate);
        console.log(webinarType);

        let createWebinarData = {
            "name": webinarName,
            "type": webinarType,
            "password": webinarPass,
            "publish": 1,
            "use_record": 0,
            "time": {
                "selected_date": webinarDate,
                "duration": 60,
                "zone_offset": -180
            },
            "questions": [
                {
                    "name": "",
                    "type": 1 // Тип вопроса ( 1 - Имя,3 - Email,4 - телефон, 0 - Любой другой)
                }
            ],
        };

        let content = JSON.stringify(createWebinarData);
        let base = btoa(content);
        let postData = {
            "user": "798fa12deb050afabfd1c6bd481c8633",
            "key": "578b341dea8d2c84b714923bdd11736e",
            "action": "webinar-create",
            "content": base
        };

        $.ajax({
            type: "POST",
            dataType: "json",
            url: "https://pruffme.com/api/",
            data: postData,
            success: function (response) {
                console.log(response);
                let meetingURL = response.webinar.landing;

                let iframe = document.createElement('iframe');
                iframe.src = meetingURL;
                iframe.width = "600";
                iframe.height = "400";

                let meetingFrame = document.getElementById('meetingFrame');
                meetingFrame.innerHTML = '';
                meetingFrame.appendChild(iframe);
                $('#webinarName').val('');
                $('#webinarDate').val('');
                $('#webinarPass').val('');
            },
            error: function (e) {
                console.log(e.message);
            }
        });
    });
});

let webinarsList = [];

function getRecentWebinars() {

    let json = {
        "limit": 10,
        "offset": 0
    };

    let content2 = JSON.stringify(json);
    let base2 = btoa(content2);
    let postData2 = {
        "user": "798fa12deb050afabfd1c6bd481c8633",
        "key": "578b341dea8d2c84b714923bdd11736e",
        "action": "webinars-list",
        "content": base2
    };

    $.ajax({
        type: "POST",
        dataType: "json",
        url: "https://pruffme.com/api/",
        data: postData2,
        success: function (response) {
            console.log(response);

            webinarsList = response.result;

            $('#webinarSelect').empty();

            webinarsList.forEach(function (webinar) {
                let option = $('<option></option>')
                    .attr('value', webinar.hash)
                    .text(webinar.name);
                $('#webinarSelect').append(option);
            });
        },
        error: function (e) {
            console.log(e.message);
        }
    });
}

getRecentWebinars();

$('#webinarSelect').change(function () {
    let selectedHash = $(this).val();

    let selectedWebinar = webinarsList.find(function (webinar) {
        return webinar.hash === selectedHash;
    });

    if (selectedWebinar) {

        let json =
            {
                "hash": selectedHash,
            };

        let content3 = JSON.stringify(json);
        let base3 = btoa(content3);
        let postData3 = {
            "user": "798fa12deb050afabfd1c6bd481c8633",
            "key": "578b341dea8d2c84b714923bdd11736e",
            "action": "webinar-delete",
            "content": base3
        };

        $.ajax({
            type: "POST",
            dataType: "json",
            url: "https://pruffme.com/api/",
            data: postData3,

            success: function (response) {
                console.log("deleted success " + response.result);

                getRecentWebinars();
            },
            error: function (e) {
                console.log(e.message);
            }
        });
    }
});
