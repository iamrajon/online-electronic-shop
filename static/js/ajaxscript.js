

// // ajax call to increase quantity in cart
$('.plus-cart').click(function(){
    console.log("plus button clicked..")
    const id = $(this).attr("pid").toString();
    // console.log("pid: ", id);
    const quant_eml = this.parentNode.children[2];

    // ajax call
    $.ajax({
        type: "GET",
        url: "http://127.0.0.1:8000/plus-cart/",
        data: {
            product_id: id,
        },
        success: function(data){
            console.log(data);
            quant_eml.innerText = data.quantity

            document.getElementById('amount').innerText = data.amount;
            document.getElementById('totalamount').innerText = data.total_amount;
        }
    })
})

// ajax call for decreasing quantity
$('.minus-cart').click(function(){
    console.log("minus button clicked..")
    const id = $(this).attr("pid").toString();
    // console.log("pid: ", id);
    const quant_eml = this.parentNode.children[2];

    // ajax call
    $.ajax({
        type: "GET",
        url: "http://127.0.0.1:8000/minus-cart/",
        data: {
            product_id: id,
        },
        success: function(data){
            console.log(data);
            quant_eml.innerText = data.quantity

            document.getElementById('amount').innerText = data.amount;
            document.getElementById('totalamount').innerText = data.total_amount;
        }
    })
})


// ajax call for remove cart
$('.remove-cart').click(function(){
    console.log("remove button clicked..")
    const id = $(this).attr("pid").toString();
    // console.log("pid: ", id);
    const rem = this

    // ajax call
    $.ajax({
        type: "GET",
        url: "http://127.0.0.1:8000/remove-cart/",
        data: {
            product_id: id,
        },
        success: function(data){
            console.log(data);
            // quant_eml.innerText = data.quantity

            document.getElementById('amount').innerText = data.amount;
            document.getElementById('totalamount').innerText = data.total_amount;
            rem.parentNode.parentNode.parentNode.parentNode.remove();
        }
    })
})

