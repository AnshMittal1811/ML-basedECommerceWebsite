console.log("working fine");


$("#commentForm").submit(function(element){
    element.preventDefault();
    $.ajax({
        data: $(this).serialize(),
        method:  $(this).attr("method"),
        url: $(this).attr("action"),
        dataType: "json",
        success: function(response){
            console.log("Comment saved to DB");
            if (response.bool==true){
                $("#review-res").html("Review Added Successfully")
            }
        }
    })
})