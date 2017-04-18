var newEntry, table = [],str="";
	
//
//var garr = [12.9255421, 80.11357660000002];
//var garr1 = [13.0526503, 80.2739447];
//var garr2 = [12.9696832, 80.12603759999999];

//var garr = {
//  id: '1',
//  name: 'Bounding-Box-1',
//  coordinate: '13.051353078812106, 80.21846087646486,13.029122526463176, 80.20060174560558'
//};
//var garr1 = {
//  id: '2',
//  name: 'Bounding-Box-2',
//  coordinate: '13.055366494933697, 80.27854235839845,13.033136303313393, 80.26068322753918'
//};
//var garr2 = {
//  id: '3',
//  name: 'Bounding-Box-3',
//  coordinate: '12.997500117240671, 80.1820686645508,12.975264735103725, 80.16420953369152'
//};
//
//// Add the object to the end of the array
//table.push(garr);
//table.push(garr1);
//table.push(garr2);

window.table=table;
creatT(table);

function creatT(table){
	//$(".class").remove();
	document.getElementById("list_Modal").innerHTML = "";
	for (var i in table) {
 //str += table[i].ne + " " +table[i].nw + " " +table[i].se + " " +table[i].sw; //"aa", bb", "cc"
 //str += "<br>"
document.getElementById("list_Modal").innerHTML +=  (i+"> "+"<div class="+"tentry"+" id=t"+i+">"+table[i].name+"</div>"+" "+"<span class="+"close"+" id="+i+">&times;</span>"+"<br>"+"<hr>")
}

}



//document.getElementById("myModal").innerHTML=str; // '22
//document.getElementById("myModal1").innerHTML=table[1].price; // '22


//function to remove an entry from the table
//function removeA(arr) {
 //   var what, a = arguments, L = a.length, ax;
 //   while (L > 1 && arr.length) {
 //       what = a[--L];
 //       while ((ax= arr.indexOf(what)) !== -1) {
 //           arr.splice(ax, 1);
 //       }
  //  }
 //   return arr;
//}

//span.onclick = function() {
//    alert ("removed");
//}

//function to remove an entry from the table
function rA(arr) {
	var a=arguments, indx=a[1];
	console.log(a[1]);
    arr.splice(indx, 1);
return arr;
}


//event trigger for dynamically created clsoe button




//$( "#insertButton" ).click(function() {
//	//var arr1 = [$("#text1").val()];
//	var arr1 = [1,2,3,4];
//    //document.getElementById("my2").innerHTML = arr1;
//    table.push(arr1);
//    creatT(table);
//});

