$(document).ready(function () {
    $("#search").click(function (event) {
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
            dataType: "html",
            contentType: 'application/json',
            success: function (result, status, xhr) {
                $("#loading-modal").hide();
                $("html").html("");
                $("html").html(result);
                console.log(status, result);
            },
            error: function (xhr, status, error) {
                $("#loading-modal").hide();
                console.log(status, error);
            }
        });
        // setTimeout(function () {
        //     hideLoadingModal();
        // }, 3000);
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