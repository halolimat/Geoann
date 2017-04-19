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

//get the modal element
var modal = $("#myModal");

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
    //$('#list_modal').remove();
    $("#myModal").css("display", "none");
    $("#myModal").replaceWith(divClone);
    table=[];
    window.Eflag=0;

    
    //console.log(annWord);
});

$(document).on( "click","#doneButton", function() {
    $("#myModal").css("display", "none");
    //console.log(table);
    
      //window.location.href = "http://127.0.0.1:5000/write/"+[ne,sw];
     $.getJSON('write', {
       wordlist: JSON.stringify(table)
   }, function(data){
       //alert(data.result);
   });
     $("#myModal").replaceWith(divClone);
     table=[];
     window.Eflag=0;
});
$(document).on("click", ".close", function() {
            var id = $(this).attr('id');
            //to get the data boud with this (X) sign
            //var txt = $("#t"+id).text();
            //alert(txt);
            //console.log('match');
            var newT = rA(table, id);
            creatT(newT);
            //removeRectangle();
            //alert(id);
        });

$(document).on( "click","#fetchButton", function() {
    $(".cssload-loader").css("z-index", "1");
});
/////////////////////////////////////////////////////////////////////////////////////////////////////
//$('#list_Modal').keypress(function(e) {
//    if(e.which == 13) {
//        alert('You pressed enter!');
//    }
//});



$('#list_Modal').keydown(function(e){
    if(e.keyCode === 13){
            alert("Enter was pressed");
     }  
});

/////////////////////////////////////////////////////////////////////////////////////////////////////
window.onclick = function(event) {
        //(console.log(event.target.id));
        if (event.target.id == 'myModal') {
        $("#myModal").css("display", "none");
    //console.log(table);
    
      //window.location.href = "http://127.0.0.1:5000/write/"+[ne,sw];
     $.getJSON('write', {
       wordlist: JSON.stringify(table)
   }, function(data){
       //alert(data.result);
   });
     $("#myModal").replaceWith(divClone);
     table=[];
     window.Eflag=0;
   }

  }
