function initMap(Sstr) {
    searchStr = "";
    searchStr = $('input[name="text"]').val();
    if (searchStr == "") {
        searchStr = Sstr;
    }

    function callAjax(handleData) {
        $.getJSON('location', {
            a: searchStr
        }, function(data) {
            handleData(data)
        });
    }

    callAjax(function(output) {
        // here you use the output
        var cord = output.response;
        //console.log(cord[0]);
        //var not_found = false;

        //if (cord[0] == null) {
            //$("#map-none").css("display", "table");
            //document.getElementById("map-canvas").innerHTML = "<p>nothing to display!!!</p>";
            //return;

            //TODO: This should be passed automatically as the default search
            //      query. I don't know how you are doing this so I will leave
            //      it to you to figure it out.s
            //cord = [["Chennai",13.0826802,80.2707184]];
           //not_found = true;

        //}

        //console.log("inside map function")
        var map;
        var markArr =[];
        var midLat = 0;
        var midLng = 0;
        var rectangle;
        var isCreated = 0
        var shapes = [];
        var selectedShape = null;
        var bounds = new google.maps.LatLngBounds();
        var mapOptions = {
            mapTypeId: 'roadmap'
        };

        // Display a map on the page
        map = new google.maps.Map(document.getElementById("map-canvas"), mapOptions);
        map.setTilt(45);

        // Multiple Markers
        markers = cord;
        var drawingManager = new google.maps.drawing.DrawingManager({
            //drawingMode: google.maps.drawing.OverlayType.MARKER,
            drawingControl: true,
            drawingControlOptions: {
                position: google.maps.ControlPosition.TOP_RIGHT,
                drawingModes: ['rectangle']
            },
            //markerOptions: {icon: 'https://developers.google.com/maps/documentation/javascript/examples/full/images/beachflag.png'},
            rectangleOptions: {
                fillColor: '#4d81f9',
                fillOpacity: 0.55,
                strokeWeight: 0,
                clickable: true,
                editable: true,
                draggable: true,
                zIndex: 1
            }
        });
        drawingManager.setMap(map);

        // Info Window Content
        var infoWindowContent = [];
        cord.forEach(function(elem) {
            infoWindowContent.push([elem[0]]);
        });

        // Display multiple markers on a map
        var infoWindow = new google.maps.InfoWindow(),
            marker, i;

        // Loop through our array of markers & place each one on the map
        for (i = 0; i < markers.length; i++) {
            var position = new google.maps.LatLng(markers[i][1], markers[i][2]);
            bounds.extend(position);
            marker = new google.maps.Marker({
                position: position,
                map: map,
                title: markers[i][0]
            });
            markArr.push(marker);

            // Allow each marker to have an info window
            google.maps.event.addListener(marker, 'click', (function(marker, i) {
                return function() {
                    infoWindow.setContent(infoWindowContent[i][0]);
                    infoWindow.open(map, marker);
                }
            })(marker, i));

            google.maps.event.addListener(drawingManager, 'overlaycomplete', function(e) {

                var newShape = e.overlay;

                newShape.type = e.type;
                shapes.push(newShape);
                drawingManager.setDrawingMode(null);
                google.maps.event.addListener(newShape, 'bounds_changed', showNewRectInfo);
                selectedShape = newShape;
                showNewRectInfo();
                isCreated = 1;
            });

            google.maps.event.addListener(drawingManager, "drawingmode_changed", function() {
                if (drawingManager.getDrawingMode() != null) {
                    for (var i = 0; i < shapes.length; i++) {
                        shapes[i].setMap(null);
                    }
                    shapes = [];
                    selectedShape = null;
                    if (rectangle != null) {
                        rectangle.setMap(null);
                    }
                }
                infoWindow.close();

            });
            

            ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////
            midLat += markers[i][1];
            window.midLat = midLat;
            midLng += markers[i][2];
            window.midLat = midLat;

            midLng = midLng / i;
            midLat = midLat / i;
            //console.log(midLat, midLng, i);
            ///////////////////////////////////////;///////////////////////////////////////////////////////////////////////////////////////////
        }

        map.fitBounds(bounds);
        zoomChangeBoundsListener =
            google.maps.event.addListenerOnce(map, 'bounds_changed', function(event) {
                if (markers.length < 3){
                    this.setZoom(15);
                }

                if (cord[0][0] == 'default'){
                  map.setZoom(10);
                }
        });
        setTimeout(function(){google.maps.event.removeListener(zoomChangeBoundsListener)}, 2000);

        $(document).on("click", 'div[id^="t"]', function() {
            //console.log($(this).text());
            for (var x = 0; x < table.length; x++) {
                if (table[x].name === $(this).text()) {
                    var y = x;
                }
            }

            var carry = (table[y].coordinate).split(",");

            if (isCreated == 1) {
                removeRectangle();
                addRectangle(carry[0], carry[1], carry[2], carry[3]);
                isCreated = 1;

            } else {
                isCreated = 1;
                addRectangle(carry[0], carry[1], carry[2], carry[3]);

            }
        });

        function showNewRect(event) {
            var ne = rectangle.getBounds().getNorthEast();
            var sw = rectangle.getBounds().getSouthWest();

            var contentString = '<div class="map-info-window">' + '<b>Rectangle moved.</b><br>' +
                'New north-east corner: ' + ne.lat() + ', ' + ne.lng() + '<br>' +
                'New south-west corner: ' + sw.lat() + ', ' + sw.lng() + '</div>';

            // Set the info window's content and position.

            infoWindow.setContent({contentString,
                pixelOffset:1
            });
            infoWindow.setPosition(ne);
            infoWindow.open(map);
        }

        function showNewRectInfo(event) {
            var ne = selectedShape.getBounds().getNorthEast();
            var sw = selectedShape.getBounds().getSouthWest();

            var contentString = '<div class="map-info-window">' + '<button id='+'insertButton'+' class='+'button'+'>Insert </button>' + '</div>';
            //var contentString = '<div ' + 'id='+'insertButton'+' class='+'button'+'>Insert' + '</div>';

            // Set the info window's content and position.

            infoWindow.setContent(contentString);
            infoWindow.setPosition(ne);
            infoWindow.open(map);
        }

        function addRectangle(l1, l2, l3, l4) {

            var arr = [l1, l2, l3, l4];
            latitude = parseFloat(arr[0]);
            longitude = parseFloat(arr[1]);
            //alert(longitude);
            var bounds = {
                north: parseFloat(arr[0]),
                south: parseFloat(arr[2]),
                east: parseFloat(arr[1]),
                west: parseFloat(arr[3])
            };

            // Define the rectangle and set its editable property to true.
            rectangle = new google.maps.Rectangle({
                strokeColor: '#000000',
                strokeOpacity: 1,
                strokeWeight: 0,
                fillColor: '#4d81f9',
                fillOpacity: 0.55,
                bounds: bounds,
                editable: false,
                draggable: false,
                border: '1px'
            });
            rectangle.setMap(map);
            rectangle.addListener('bounds_changed', showNewRect);
            var clat = (parseFloat(arr[0]) + parseFloat(arr[2])) / 2;
            var clng = (parseFloat(arr[1]) + parseFloat(arr[3])) / 2;
            var pos = new google.maps.LatLng(clat, clng);
            map.setCenter(pos);
            map.fitBounds(rectangle.getBounds());
            drawingManager.setDrawingMode(null);
            //shapes.push(rectangle);
            //rectangle.push(rectangle);
        }

        function removeRectangle() {
            for (var i = 0; i < shapes.length; i++) {
                shapes[i].setMap(null);
            }
            shapes = [];
            selectedShape = null;
            if (rectangle != null) {
                rectangle.setMap(null);
            }
            infoWindow.close();
            //console.log(shapes);
        }

        $(document).on( "click","#insertButton", function(event) {
            if (selectedShape != null) {
                var ne = selectedShape.getBounds().getNorthEast();
                var sw = selectedShape.getBounds().getSouthWest();
                var updatearr = "";
                var updatearr = ne.lat() + "," + ne.lng() + "," + sw.lat() + "," + sw.lng();
                for (var i in table) {}
                //console.log(i);
                k = 0;
                if (i >= 0) {
                    j = parseInt(i);
                    j = table[j].id;
                    k = parseInt(j);
                    k += 1;
                }
                //console.log(annId);

                var Nentry = {
                    id: k,
                    annId: annId,
                    name: 'Bounding-Box-' + k,
                    coordinate: updatearr
                };
                table.push(Nentry);
                creatT(table);
                removeRectangle();
            }

        });
        $(document).on("click", ".close", function() {
            var id = $(this).attr('id');
            //to get the data boud with this (X) sign
            //var txt = $("#t"+id).text();
            //alert(txt);
            var newT = rA(table, id);
            creatT(newT);
            removeRectangle();
            //alert(id);
        });
        //document.onkeydown = function(e) {
        //    console.log("keydown");
        //}

        // Override our map zoom level once our fitBounds function runs (Make sure it only runs once)
        //var boundsListener = google.maps.event.addListener((map), 'bounds_changed', function(event) {
        //    this.setZoom(14);
        //    google.maps.event.removeListener(boundsListener);
        //});
        google.maps.event.addListenerOnce(map, 'tilesloaded', function() {
            $(".cssload-loader").css("z-index", "-1");
        });
        google.maps.event.addListener(map, 'click', function() {
            console.log("map clicked");
            var popup = $('.popup');
            popup.css("display", "block");
        });
        if (cord[0][0] == 'default') {
                //console.log(markers);
                for (i = 0; i < markArr.length; i++){
                markArr[i].setMap(null);
                //map.setZoom(1);
            }
            }
    });

    $('.cssload-loader').show();
}
