$(document).ready(function () {
    $("#search").click(function (event) {
        if ($("#location").val() == "") {
            $("#location").focus();
        } else if ($("#industry").val() == "") {
            $("#industry").focus();
        } else if ($("#job_title").val() == "") {
            $("#job_title").focus();
        } else {
            event.preventDefault();
            $("#loading-modal").show();
            $.ajax({
                url: "/",
                method: "POST",
                data: JSON.stringify({
                    "location": $("#location").val(),
                    "industry": $("#industry").val(),
                    "job_title": $("#job_title").val()
                }),
                dataType: "json",
                contentType: 'application/json',
                success: function (result, status, xhr) {
                    $("#loading-modal").hide();
                    html = "";
                    for (var i = 0; i < result.data.length; i++) {
                        item = result.data[i];
                        html += `
                        <tr>
                        <td>` + item["company"] + `</td>
                        <td><a href="https://` + item['website'] + `">` + item["website"] + `<a></td>
                        <td><a href="` + item['linkedin_comp'] + `">` + item["linkedin_comp"] + `<a></td>
                        <td>` + item["phone"] + `</td>
                        <td>` + item["address"] + `</td>
                        <td>` + item["state"] + `</td>
                        <td>` + item["city"] + `</td>
                        <td>` + item["code"] + `</td>
                        <td>` + item["country"] + `</td>
                        <td>` + item["fname"] + `</td>
                        <td>` + item["lname"] + `</td>
                        <td>` + item["title"] + `</td>
                        <td><a href="` + item['email'] + `">` + item["email"] + `</td>
                        <td><a href="` + item['linkedin_pers'] + `">` + item["linkedin_pers"] + `</td>
                      </tr>`
                    }
                    $("#tbody-data").html(html);
                    console.log(status, result);
                },
                error: function (xhr, status, error) {
                    $("#loading-modal").hide();
                    console.log(status, error);
                }
            });
        }
    });
    // $("#export").click(function () {
    //     $.ajax({
    //       url: "/export",
    //       method: "POST",
    //       responseType: 'blob',
    //       success: function(response) {
    //         const blob = new Blob([response], { type: 'application/zip' });
    //         const url = URL.createObjectURL(blob);
    //         const link = document.createElement('a');
    //         link.href = url;
    //         link.download = new Date().toString()+'.zip';
    //         link.click();
    //         link.remove();
    //         URL.revokeObjectURL(url);
    //         // link.setAttribute('download', );
    //         // document.body.appendChild(link);
    //         // link.click();
    //         // document.body.removeChild(link);
    //       },
    //       error: function(xhr, textStatus, errorThrown) {
    //         if (xhr.status === 500) {
    //             // Retrieve the error message from the responseText property
    //             var errorMessage = xhr.responseText;
    //             console.log(errorMessage);
    //         } else {
    //             console.log("An error occurred: " + errorThrown);
    //         }
    //       }
    //     });
    // });
    // $("#search").click(function () {
    //   $.ajax({
    //       url: "/",
    //       method: "POST",
    //       headers: {
    //         'X-CSRFToken': getCookie("csrftoken")
    //       },
    //       data: {
    //         loc: $("#location").val(),
    //         ind: $("#industry").val(),
    //         job: $("#job-title").val()
    //       },
    //       contentType: "application/json",
    //       success: function (result, status, xhr) {
    //         try {
    //           suggestedPassword = result.suggested_password;
    //           $('#suggested-password-value').val(result.suggested_password);
    //         } catch (err) {
    //           console.log(err);
    //         }
    //       }
    //     });
    // })
});