//$(document).on( "click",'span[id^="e"]', function() {
//    modal.style.display = "block";
//    document.getElementById("model-text").innerHTML=$(this).text();
//    google.maps.event.addDomListener(window, 'load', initMap($(this).text()));
//});


//$('.tweet').click(function() {
//
//    modal.style.display = "block";
//});


// Get the button that submits the model
var donebtn = $("#doneButton");

// Get the <span> element that closes the modal
//var span = $(".close_top:first");
//
//// When the user clicks on <span> (x), close the modal
//span.onclick = function() {
//    console.log("in the function")
//    $("#myModal").css("display", "none");
//}

donebtn.onclick = function() {
    $("#myModal").css("display", "none");
}

$(document).on( "click",".close_top:first", function() {
    $("#myModal").css("display", "none");
    $("#myModal").replaceWith(divClone);
    table=[];
    
    console.log(annWord);
});

$(document).on( "click","#doneButton", function() {
    $("#myModal").css("display", "none");
    console.log(table);
    
      //window.location.href = "http://127.0.0.1:5000/write/"+[ne,sw];
     $.getJSON('http://localhost:8080/write', {
       wordlist: JSON.stringify(table)
   }, function(data){
       alert(data.result);
   });
     $("#myModal").replaceWith(divClone);
     table=[];
});

$(document).on( "click","#fetchButton", function() {
    $(".cssload-loader").css("z-index", "1");
});


 

