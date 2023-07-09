console.log("working fine");
const MonthNames = ["Jan", "Feb", "Mar", "April", "May", "June",
    "July", "Aug", "Sept", "Oct", "Nov", "Dec"
];

// For Comment-Reviews
$("#commentForm").submit(function(element){
    element.preventDefault();
    let date = new Date();
    let time = date.getDay() + " " + MonthNames[date.getUTCMonth()] + ", " + date.getFullYear()
    $.ajax({
        data: $(this).serialize(),
        method:  $(this).attr("method"),
        url: $(this).attr("action"),
        dataType: "json",
        success: function(response){
            console.log("Comment saved to DB...");
            if (response.bool==true){
                $("#review-res").html("Review Added Successfully")
                $(".hide-comment-form").hide()
                $(".add-review").hide()

                let _html = '<div class="single-comment justify-content-between d-flex mb-30">'
                    _html += '<div class="user justify-content-between d-flex">'
                    _html += '<div class="thumb text-center">'
                    _html += '<img src="https://commons.wikimedia.org/wiki/File:Windows_10_Default_Profile_Picture.svg" alt="" />'
                    _html += '<a href="#" class="font-heading text-brand">'+ response.context.user+'</a>'
                    _html += '</div>'

                    _html += '<div class="desc">'
                    _html += '<div class="d-flex justify-content-between mb-10">'
                    _html += '<div class="d-flex align-items-center">'
                    _html += '<span class="font-xs text-muted">' + time +'</span>'
                    _html += '</div>'

                    for(let i=1; i <= response.context.ratings; i++){
                        _html += '<i class="fas fa-star text-warning"></i>'
                    }

                    _html += '</div>'
                    _html += '<!-- <a href="#" class="reply">Reply</a> -->'

                    _html += '<p class="mb-10">'+ response.context.review +'</p>'
                    _html += '</div>'
                    _html += '</div>'
                    _html += '</div>'
                    $(".comment-list").prepend(_html)
            }
        }
    })
})

// For Filtering based on Categories and Vendors
$(document).ready(function (){
    $(".filter-checkbox, #price-filter-btn").on("click", function(){
        console.log("A checkbox have been clicked");
        let filter_object = {}

        let min_price = $("#max_price").attr("min")
        let max_price = $("#max_price").val()

        filter_object.min_price = min_price
        filter_object.max_price = max_price

        $(".filter-checkbox").each(function(){
            let filter_value = $(this).val()
            let filter_key = $(this).data("filter") // vendor, or category
            // console.log("Filter value is:", filter_value);
            // console.log("Filter Key is:", filter_key);    

            filter_object[filter_key] = Array.from(document.querySelectorAll('input[data-filter=' + filter_key +']:checked')).map(function(element){
                return element.value
            })
        })
        console.log("Filter object is:", filter_object);
        $.ajax({
            url: '/filter-products', //Can be done using Django URL template for core
            data: filter_object,
            dataType: 'json',
            beforeSend: function(){
                console.log("Filtering Product...");
            },
            success: function(response){
                console.log(response);
                console.log("Data filtered successfully...");
                $("#filtered-product").html(response.data)
            }
        })
    })
    // Changing the price bar in real time
    $("#max_price").on("blur", function(){
        let min_price = $(this).attr('min')
        let max_price = $(this).attr('max')

        let main_value = $(this).val()

        // console.log("Value is:", main_value);
        // console.log("Max value is:", min_price);
        // console.log("Min value is:", max_price);

        if(main_value<parseInt(min_price) || main_value>parseInt(max_price)){
            console.log("Price Error Occurred...");
            min_price = Math.round(min_price * 100 ) / 100;
            max_price = Math.round(max_price * 100 ) / 100;

            // console.log("************************");
            // console.log("************************");
            // console.log("************************");
            // console.log("Max value is:", min_Price);
            // console.log("Min value is:", max_Price);
            alert("Price must be between $" + min_price + ' and $' + max_price + '!!');
            $(this).val(min_price)
            $("#range").val(min_price)
            $(this).focus

            return false
        }
    })

    // Add to cart functionality
    $(".add-to-cart-btn").on("click", function(){
        let this_val = $(this)
        let index = this_val.attr("data-index")

        let quantity = $(".product-quantity-"+index).val()
        let product_title = $(".product-title-"+index).val()
        let product_id = $(".product-id-"+index).val()
        let product_price = $(".current-product-price-"+index).text()
        let product_p_id = $(".product-pid-"+index).val()
        let product_image = $(".product-image-"+index).val()

        console.log("Quantity: ", quantity);
        console.log("Title: ", product_title);
        console.log("Price: ", product_price);
        console.log("Product ID: ", product_id);
        console.log("Product PID: ", product_p_id);
        console.log("Product Image", product_image);
        console.log("Index", index);
        console.log("Current Element", this_val);

        $.ajax({
            url: '/add-to-cart',
            data: {
                'id': product_id,
                'p_id': product_p_id,
                'image': product_image,
                'qty': quantity,
                'title': product_title,
                'price': product_price,
            },
            dataType: 'json',
            beforeSend: function(){
                console.log("Adding Product to Cart...");
            },
            success: function(response){
                this_val.html("✓")
                console.log("Added Product to Cart");
                $(".cart-items-count").text(response.totalcartitems)
            }
        })
    })


    $(".delete-product").on("click", function(){
        let product_id =  $(this).attr("data-product")
        let this_val = $(this)

        // console.log("Product ID:", product_id);

        $.ajax({
            url: "/delete-from-cart",
            data: {
                "id": product_id,
            },
            dataType: "json",
            beforeSend: function(){
                this_val.hide()
            },
            success: function(response){
                this_val.show()
                $(".cart-items-count").text(response.totalcartitems)
                $("#cart-list").html(response.data)
            }
        })
    })

})


// $(".add-to-cart-btn").on("click", function(){
//     let quantity = $("#product-quantity").val()
//     let product_title = $(".product-title").val()
//     let product_id = $(".product-id").val()
//     let product_price = $("#current-product-price").text()
//     let this_val = $(this)

//     console.log("Quantity", quantity);
//     console.log("Product Title", product_title);
//     console.log("Product ID", product_id);
//     console.log("Product Price", product_price);
//     console.log("Current Element", this_val);

//     $.ajax({
//         url: '/add-to-cart',
//         data: {
//             'id': product_id,
//             'qty': quantity,
//             'title': product_title,
//             'price': product_price,
//         },
//         dataType: 'json',
//         beforeSend: function(){
//             console.log("Adding Product to Cart...");
//         },
//         success: function(response){
//             this_val.html("Item Added to Cart")
//             console.log("Added Product to Cart");
//             $(".cart-items-count").text(response.totalcartitems)
//         }
//     })
// })