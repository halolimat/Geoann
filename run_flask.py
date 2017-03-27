################################################################################
# Author: Hussein S. Al-Olimat      <hussein@knoesis.org>
# License: BSD 3 clause
################################################################################

import json, os
import numpy as np
from collections import defaultdict
from flask import Flask, request, send_from_directory, render_template_string

################################################################################
################################################################################

app = Flask(__name__, static_url_path='')

@app.route('/static/<path:path>')
def static_proxy(path):
    # send_static_file will guess the correct MIME type
    return app.send_static_file(path)

################################################################################
################################################################################

def get_files(path):
    files = list()

    for (dirpath, _, filenames) in os.walk(path):
        for filename in filenames:
            files.append(filename)

    return files

################################################################################

def get_ann_files():

    ann_dir = 'Chennai/Chennai_Tweets/'

    list_files = get_files(ann_dir)

    ann_files = set()

    for fname in list_files:
        ann_files.add(ann_dir+fname[:-4])

    return list(ann_files), ann_dir

################################################################################

def html():

    return '''

    <head>
		<meta charset="UTF-8" />
		<meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
		<meta name="viewport" content="width=device-width, initial-scale=1.0">
		<link rel="stylesheet" type="text/css" href="css/style-vis.css">
        <script type="text/javascript" src="js/head.js"></script>
	</head>

    <script>

        var tweets_urls = [{{tweet_urls_array|safe}}];

        function changeTweet(dir) {
            var currentSrc = "{{host|safe}}start?tweet_id={{div_name|safe}}"
            var url = tweets_urls[tweets_urls.indexOf(currentSrc) + (dir || 1)] || tweets_urls[dir ? tweets_urls.length - 1 : 0];
            window.location.href = "http://"+url;
        }

        document.onkeydown = function(e) {
            e = e || window.event;
            if (e.keyCode == '37') {
                changeTweet(-1) //left <- show Prev image
            } else if (e.keyCode == '39') {
                // right -> show next image
                changeTweet()
            }
        }

    </script>
        <!-- load all the libraries upfront, which takes forever. -->
        <script type="text/javascript" src="js/brat_loader.js"></script>

        <!-- let's do the configuration -->
        <script type="text/javascript">
            var collData = {
                entity_types: [ {
                        type   : 'Location',
                        labels : ['Location', 'Loc'],
                        bgColor: '#FF866C',
                        borderColor: 'darken'
                } ]
            };
    </script>

    {{brat_anns_data|safe}}

    {{brat_embed_function|safe}}

    <body>
        <div id="{{div_name|safe}}">
        </div>
    </body>

    '''

################################################################################

def brat_tweet_annotations_data(id):

    return "var docData"+str(id)+" = {{annotations|safe}}; "

################################################################################

def get_ann_by_file_name(fname):

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

        print '"'+request_host+"start?tweet_id="+ann_file+'"'

        urls.append('"'+request_host+"start?tweet_id="+ann_file+'"')

    return ", ".join(urls)

################################################################################

@app.route('/start')
def start():

    tweet_id = request.args.get('tweet_id')

    if not tweet_id:
        return "you should choose the tweet id from the set of files in the folder"

    ann_files, ann_dir = get_ann_files()

    # remove the full directory name from each file name
    ann_files = [x.replace(ann_dir,"") for x in ann_files]

    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    request_host = request.host_url.replace("http://", "")

    return render_template_string(html(),
                brat_anns_data=get_brat_anns_data(tweet_id),
                brat_embed_function=get_brat_embed_script(tweet_id),
                tweet_urls_array=get_tweet_urls_array(ann_files),
                div_name=tweet_id,
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
