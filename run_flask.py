################################################################################
# Author: Hussein S. Al-Olimat      <hussein@knoesis.org>
# License: BSD 3 clause
################################################################################
import googlemaps
import json, os
import numpy as np
from collections import defaultdict
from flask import Flask, request, send_from_directory, render_template_string, render_template, jsonify
import glob
from file import remov
import urllib2
from radius import Ldist
################################################################################
################################################################################
tweet_id=''
word_id = ''
city = ''
default_bb = []
app = Flask(__name__, static_url_path='')
@app.route('/static/<path:path>')
def static_proxy(path):
    # send_static_file will guess the correct MIME type
    return app.send_static_file(path)

################################################################################
################################################################################
@app.route('/location',methods = ['POST', 'GET'])
def result():
    loc = request.args.get('a', 0, type=str)
    print loc

    add = loc
    add = urllib2.quote(add)
    radius = 50000
    a = default_bb[0];
    b = default_bb[1];
    #geocode_url = "https://maps.googleapis.com/maps/api/place/textsearch/json?query=%s&location=%d,%d&radius=%d&key=AIzaSyDA0LEtyiF_1FAyLWpFUUoTtrYkopGKJlI"  % (add,a,b,radius)
    geocode_url = "https://maps.googleapis.com/maps/api/place/textsearch/json?query=%s&location=%d,%d&radius=%d&key=AIzaSyCrw1mGpS8ebkTK8KeXvC9JRZCuEVl3zjk" % (add,a,b,radius)
    print geocode_url
    req = urllib2.urlopen(geocode_url)
    jsonResponse = json.loads(req.read())
    #pprint.pprint(jsonResponse)
    #print jsonResponse.keys()
    #lat=jsonResponse['results'][0]
    #print lat
    packet = []
    data = jsonResponse["results"]
    for entry in data:
        cord = entry["geometry"]["location"]
        name = entry['name']
        name = name.encode('utf-8')
        code = [name,cord['lat'],cord['lng']]
        dist = Ldist(a, b, cord['lat'], cord['lng'])
        if (dist>50):
            continue
        packet.append(code)

    if (packet == []):
        #print (name+"#######################################################")
        #print default_bb
        packet=[["default",default_bb[0],default_bb[1]]];

    return jsonify(response=packet)
################################################################################
def bbread():
    current_path= os.path.dirname(os.path.abspath(__file__))
    data_set=dataset_dir.split("_")
    city=data_set[0]
    fldr=data_set[1]
    path = current_path + "/brat_annotations/" + city + "/" + city + ".ini"
    fo=open(path,"r")
    bb=fo.readlines()
    for b in bb:
        b = b.replace("\n", "").split(",")
    b1= (float(b[0])+float(b[2]))/2
    b2= (float(b[1])+float(b[3]))/2
    b = [b1,b2]
    return b
################################################################################
################################################################################
@app.route('/write', methods=['GET', 'POST'])
def write():
    wordlist = json.loads(request.args.get('wordlist'))
    wrt(wordlist)
    # do some stuff
    #return jsonify(result=wordlist)
    print wordlist
    return jsonify(result="done")

################################################################################
################################################################################


###########################################################################################
def wrt(arr):
    # Open a file
    file = tweet_id+".ann"
    file= file.encode("utf-8")
    current_path= os.path.dirname(os.path.abspath(__file__))
    data_set=dataset_dir.split("_")
    city=data_set[0]
    fldr=data_set[1]
    path = current_path + "/brat_annotations/" + city + "/" + fldr + "/" + file
    remov(path,word_id)
    try:
        fo=open(path,"a")
    except:
        fo = open(path, "w+")
    for i,data in enumerate(arr):
        annId = str(data['annId'])
        crdn = " "+str(data['coordinate'])
        wdata = "G"+str(i+1)+"\t"+annId+"\t"+crdn
        fo.write(wdata+'\n');
        print i

    # Close opend file
    fo.close()
    print tweet_id
##############################################################################################

################################################################################
################################################################################
@app.route('/read', methods=['GET', 'POST'])
def rd():
    wordlist = json.loads(request.args.get('wordlist'))
    crr = read(wordlist)
    # do some stuff
    #return jsonify(result=wordlist)
    print crr
    return jsonify(result=crr)

################################################################################
################################################################################


###########################################################################################
def read(id):
    # Open a file
    global word_id
    word_id=id
    file = tweet_id+".ann"
    file= file.encode("utf-8")
    current_path = os.path.dirname(os.path.abspath(__file__))
    data_set=dataset_dir.split("_")
    city=data_set[0]
    fldr=data_set[1]
    path = current_path + "/brat_annotations/" + city + "/" + fldr + "/" + file
    fo=open(path,"r")
    gnn=fo.readlines()
    rcord=[]

    for g in gnn:
        g = g.replace("\n", "").split("\t")
        if "G" in g[0]:
            if id==g[1]:
                nesw = g[2].split(",")
                print rcord
                rcord.append(nesw)
    return rcord
    # Close opened file
    fo.close()
    print tweet_id
##############################################################################################

def get_files(path):
    files = list()

    for (dirpath, _, filenames) in os.walk(path):
        for filename in filenames:
            files.append(filename)

    return files

################################################################################

def get_ann_files():

    current_path = os.path.dirname(os.path.abspath(__file__))
    data_set=dataset_dir.split("_")
    city=data_set[0]
    fldr=data_set[1]
    ann_dir = current_path + '/brat_annotations/' + city + '/' + fldr  

    list_files = get_files(ann_dir)

    ann_files = set()

    for fname in list_files:
        ann_files.add(ann_dir+fname[:-4])

    return list(ann_files), ann_dir 

################################################################################

def html():

    return '''

    <head>
    <title>GeoAnn</title>
		<meta charset="UTF-8" />
		<meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
		<meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="icon" href="static/favicon.png"/>
		<link rel="stylesheet" type="text/css" href="css/style-vis.css">
        <link rel="stylesheet" type="text/css" href="css/pop-style.css">
        <script type="text/javascript" src="js/head.js"></script>
        <link href="https://fonts.googleapis.com/css?family=Palanquin" rel="stylesheet">
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.1.1/jquery.min.js"></script>
        <script src="https://maps.googleapis.com/maps/api/js?key=AIzaSyA7YOOWjDL1lO3n96oXc4_KPPrJL79ZCpY&libraries=drawing"></script>
    <script type="text/javascript" src="/static/js/client/src/map.js"></script>
        <script type="text/javascript" src = "/static/js/client/src/func.js"></script>
	</head>

    <script>

        var tweets_urls = [{{tweet_urls_array|safe}}];

        function changeTweet(dir) {
            var currentSrc = "{{host|safe}}start?dataset={{div_city|safe}}_{{div_fldr|safe}}&tweet_id={{div_name|safe}}"
            var url = tweets_urls[tweets_urls.indexOf(currentSrc) + (dir || 1)] || tweets_urls[dir ? tweets_urls.length - 1 : 0];
            window.location.href = "http://"+url;
        }

        document.onkeydown = function(e) {
            e = e || window.event;
            if (e.keyCode == '37') {
            //if flag is set commit data to file

            if (Eflag==1) {
            $.getJSON('write', {
       wordlist: JSON.stringify(table)
   }, function(data){
       //alert(data.result);
   });
    }
    changeTweet(-1); //left <- show Prev image
    }
    else if (e.keyCode == '39') {
            //if flag is set commit data to file

    if (Eflag==1) {
    $.getJSON('write', {
    wordlist: JSON.stringify(table)
   }, function(data){
       //alert(data.result);
   });
    }

 // right -> show next image
changeTweet();
    }


    }

        $(document).on("click", "#next", function(){
    changeTweet();
});

$(document).on("click", "#prev", function(){
    changeTweet(-1);
});

    </script>
        <!-- load all the libraries upfront, which takes forever. -->
        <script type="text/javascript" src="js/brat_loader.js"></script>

        <!-- let's do the configuration -->
        <script type="text/javascript">
            var collData = {
                entity_types: [ {
                        type   : 'Location',
                        labels : ['Location', 'Loc'],
                        bgColor: '#17b4ed',
                        borderColor: 'darken'
                } ]
            };
    </script>

    {{brat_anns_data|safe}}

    {{brat_embed_function|safe}}

    <body>
    <div class="main-header">GeoAnnotator</div>
        <div id="{{div_name|safe}}"></div>
        <div id="{{div_city|safe}}"></div>
        <div id="{{div_fldr|safe}}"></div>
        <div class="previous round" id="prev">&#8249;</div>
        <div class="next round" id="next">&#8250;</div>
        </div><div id="myModal" class="modal">
        <!-- Modal content -->
        <div class="modal-content">
            <div class="tops">
            <span id="ann">GeoAnnotator</span>
                <span class="close_top">&times;</span></div>
            <div class="gbox">
            <div class="popup"><span class="popuptext" id="myPopup">Click this Button to Draw Bounding Box.</span>
</div>
                <div id="model-text"></div>
                <input type="text" name="text" placeholder="Location Search......">
                <button id="fetchButton" class="button">Search</button>
                <div class="lcontainer">
                <div class="header">Bbox Entry:</div>
                <div id="list_Modal" class="list_modal"></div></div>
                <br>
                <div class="cssload-loader">
    <div class="cssload-inner cssload-one"></div>
    <div class="cssload-inner cssload-two"></div>
    <div class="cssload-inner cssload-three"></div>
</div>
                <button id="doneButton" class="button">commit to file</button>
                <br>
                <br>
                <div id="map-canvas"></div>
            </div>

        </div>

        <script type="text/javascript" src="/static/js/client/src/tbl.js"></script>
        <script type="text/javascript">
          var btn = document.getElementById('fetchButton');
          google.maps.event.addDomListener(btn, 'click', initMap);
          </script>


    </body>

    '''

################################################################################

def brat_tweet_annotations_data(id):

    return "var docData"+str(id)+" = {{annotations|safe}}; "

################################################################################

def get_ann_by_file_name(fname):

    fname = fname.replace("//", "/")

    with open(fname+".ann") as f:
        ann = f.readlines()
    with open(fname+".txt") as f:
        tweet = f.readlines()

    '''
    {
      text     : "I study at WSU, Dayton, USA.",
      entities : [
        ['T1', 'Location', [[11, 14]]],
        ['T2', 'Location', [[16, 22]]],
        ['T3', 'Location', [[24, 27]]],
      ],
    }
    '''

    #  ['T1', 'Imp-Top 61 85', 'Vivekananda Nagar Street']

    entities = ""

    for a in ann:
        a = a.replace("\n", "").split("\t")
        if "T" in a[0]:
            offsets = a[1].split()
            start_idx = offsets[1]
            end_idx = offsets[2]
            entities += "['"+a[0]+"', 'Location', [["+str(start_idx)+", "+str(end_idx)+"]]],"

    return "{text:'"+tweet[0]+"',entities:["+entities+"],} "

################################################################################

def get_brat_anns_data(tweet_id):

    ann_files, ann_dir = get_ann_files()

    temp = brat_tweet_annotations_data(tweet_id)
    anns = get_ann_by_file_name(ann_dir+"/"+tweet_id)

    data = render_template_string(temp, annotations=anns)

    return '<script type="text/javascript"> ' + data + ' </script>'

################################################################################

def get_brat_embed_script(tweet_id):
    ''' Embed function '''

    embed_func = "Util.embed('"+tweet_id+"', $.extend({}, collData), $.extend({}, docData"+tweet_id+"));"

    t = '''
        <script type="text/javascript">
            head.ready(function() {
                {{brat_embed_functions|safe}}
            });
        </script>
        '''

    return render_template_string(t, brat_embed_functions=embed_func)

################################################################################
################################################################################
################################################################################

def get_tweet_urls_array(ann_files):

    urls = list()

    # NOTE: example http://localhost:8080/start?tweet_id=671934506450861952
    for ann_file in ann_files:

        request_host = request.host_url.replace("http://", "")

        data_set=dataset_dir.split("_")
        city=data_set[0]
        fldr=data_set[1]

        print '"'+request_host+"start?dataset="+city+"_"+fldr+"&tweet_id="+ann_file+'"'

        urls.append('"'+request_host+"start?dataset="+city+"_"+fldr+"&tweet_id="+ann_file+'"')

    return ", ".join(urls)

################################################################################

@app.route('/start')
def start():
    global tweet_id, dataset_dir
    tweet_id = request.args.get('tweet_id')
    dataset_dir=request.args.get('dataset')

    if not dataset_dir:
        return "you should type the dataset that the tweet belongs to"
        #dataset=chennai_set1;

    if not tweet_id:
        return "you should choose the tweet id from the set of files in the folder"
        #tweet_id = '671935055137116032';

    ann_files, ann_dir = get_ann_files()

    data_set=dataset_dir.split("_")
    city=data_set[0]
    fldr=data_set[1]

    # remove the full directory name from each file name
    ann_files = [x.replace(ann_dir,"") for x in ann_files]
    global default_bb
    default_bb = bbread()
    #print default_bb

    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    request_host = request.host_url.replace("http://", "")

    return render_template_string(html(),
                brat_anns_data=get_brat_anns_data(tweet_id),
                brat_embed_function=get_brat_embed_script(tweet_id),
                tweet_urls_array=get_tweet_urls_array(ann_files),
                div_name=tweet_id,
                div_city=city,
                div_fldr=fldr,
                host=request_host)

################################################################################

@app.route('/ignore')
def opendialog():
    ''' Leave for later ..
    This should allow us to choose the files for annotations, sets the working directory.
    The code below is client side.. Do not work!
    '''

    return '''

        <head>
            <script type="text/javascript" src="//code.jquery.com/jquery-1.8.3.js"></script>

            <script type="text/javascript">
                $(window).load(function(){
                    var input = document.getElementById('ann');

                    input.onchange = function () {
                        var filename = this.value.substring(12);
                    };
                });

            </script>

        </head>

        <body>
            <input type='file' id="ann" style="visibility: hidden; width: 1px; height: 1px" accept=".ann" />
            <a href="" onclick="document.getElementById('ann').click(); return false">Start Annotating</a>
        </body>
    '''

if __name__ == "__main__":

    app.run(host='0.0.0.0', port=8080)
