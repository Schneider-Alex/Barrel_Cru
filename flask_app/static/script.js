function companyCheck(that) {
    if (that.value == "New") {
        alert("If your company is not listed, Please enter the Correct name below, so that we may add it to our system");
        document.getElementById("newCustomerCompany").style.display = "block";
    } 
    else {
        document.getElementById("newCustomerCompany").style.display = "none";
    }
}