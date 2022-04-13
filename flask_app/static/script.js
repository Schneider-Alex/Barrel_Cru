function companyCheck(that) {
    if (that.value == "New") {
        alert("If your company is not listed, Please enter the Correct name below, so that we may add it to our system");
        document.getElementById("newCustomerCompany").style.display = "block";
    } 
    else {
        document.getElementById("newCustomerCompany").style.display = "none";
    }
}
function orderButton(id){
    document.getElementById(`order${id}`).innerHTML=`<form action="/customer/add_to_cart" method="post">
    <input type="hidden" name="product_id" value="${id}"
    <label for"quantity">Quantity:</label>
    <input type="number" value="0" name="quantity">
    <input type="submit" value="Add to Cart">
    </form>`
    console.log(id)
}
