import json, os
import numpy as np
from bottle import route, run, template
from bottle import static_file
from collections import defaultdict

################################################################################
################################################################################

def show_dialog_box():

    db = '''

    <h1>Welcome to Geoann</h1>

    <h2>Choose a file to start annotating</h2>

    <input id="selectedFile" name="files[]" accept=".txt" type="file" style="position:absolute;visibility:hidden;"/>
    <input type="button" id="browseButton" value="Select a tweet" onclick="selectedFile.click()">

    <output id="list"></output>

    <script>
        function handleFileSelect(evt) {
            var files = evt.target.files; // FileList object

            // files is a FileList of File objects. List some properties.
            var output = [];
            for (var i = 0, f; f = files[i]; i++) {
                output.push('<li><strong>', escape(f.name), '</strong> (', f.type || 'n/a', ') - ',
                          f.size, ' bytes, last modified: ',
                          f.lastModifiedDate ? f.lastModifiedDate.toLocaleDateString() : 'n/a',
                          '</li>');
            }

            document.getElementById('list').innerHTML = '<ul>' + output.join('') + '</ul>';
        }

        document.getElementById('selectedFile').addEventListener('change', handleFileSelect, false);

    </script>

    '''

    return db

################################################################################

def page_flips():

    return '''

    <head>
		<meta charset="UTF-8" />
		<meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
		<meta name="viewport" content="width=device-width, initial-scale=1.0">
		<title>Fullscreen Pageflip Layout with BookBlock</title>
		<meta name="description" content="Fullscreen Pageflip Layout with BookBlock" />
		<meta name="keywords" content="fullscreen pageflip, booklet, layout, bookblock, jquery plugin, flipboard layout, sidebar menu" />
		<meta name="author" content="Codrops" />
		<link rel="stylesheet" type="text/css" href="css/jquery.jscrollpane.custom.css" />
		<link rel="stylesheet" type="text/css" href="css/bookblock.css" />
		<link rel="stylesheet" type="text/css" href="css/custom.css" />
		<script src="js/modernizr.custom.79639.js"></script>
	</head>

    <div id="container" class="container">

        <div class="menu-panel">
            <h3>List of Tweets</h3>

            <ul id="menu-toc" class="menu-toc">
                {{!menu_items}}
            </ul>

        </div>

        <div class="bb-custom-wrapper">
            <div id="bb-bookblock" class="bb-bookblock">
                {{!content_items}}
            </div>

            <nav>
                <span id="bb-nav-prev">&larr;</span>
                <span id="bb-nav-next">&rarr;</span>
            </nav>

            <span id="tblcontents" class="menu-button">Table of Contents</span>

        </div>

    </div><!-- /container -->
    <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.8.3/jquery.min.js"></script>
    <script src="js/jquery.mousewheel.js"></script>
    <script src="js/jquery.jscrollpane.min.js"></script>
    <script src="js/jquerypp.custom.js"></script>
    <script src="js/jquery.bookblock.js"></script>
    <script src="js/page.js"></script>
    <script>
        $(function() {

            Page.init();

        });
    </script>

    '''

################################################################################

@route('/annotate')
def annotate():

    ann_dir = 'Chennai/Chennai_Tweets/'

    list_files = get_files(ann_dir)

    ann_files = set()

    for fname in list_files:
        ann_files.add(ann_dir+fname[:-4])

    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    menu_items = ""
    content_items = ""

    for idx, ann_file in enumerate(ann_files):

        menu_items += '<li><a href="#item'+str(idx)+'">'+ann_file.replace(ann_dir,"")+'</a></li>'

        content_items += '<div class="bb-item" id="item'+str(idx)+'"><div class="content"><div class="scroller">'+get_ann_by_file_name(ann_file)+'</div></div></div>}'

    return template(page_flips(), {"menu_items": menu_items, "content_items": content_items})

################################################################################

def get_files(path):
    files = list()

    for (dirpath, _, filenames) in os.walk(path):
        for filename in filenames:
            files.append(filename)

    return files

################################################################################

@route('/<filename:path>')
def send_static(filename):
    return static_file(filename, root='static/')

def brat_template():

    return '''
        <head>
            <meta http-equiv="content-type" content="text/html; charset=UTF-8">
            <link rel="stylesheet" type="text/css" href="css/style-vis.css">
            <script type="text/javascript" src="js/head.js"></script>
        </head>

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

        <!-- we simply call it inside a script element -->
        <script type="text/javascript">
            var docData = {{!annotations}};
        </script>

        <!-- the visualization will be embedded here. we'll just need to tell
        brat the div ID in a Util.embed() call-->
        <div id="embedding-entity-example"></div>


        <script type="text/javascript">
            head.ready(function() {
                // Evaluate the code from the example (with ID
                // 'embedding-entity-example') and show it to the user
                Util.embed('embedding-entity-example', $.extend({}, collData),
                        $.extend({}, docData));//, webFontURLs);
            });
        </script>

        '''

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

    temp = "{text:'"+tweet[0]+"',entities:["+entities+"],}"

    return template(brat_template(), {"annotations": temp})

################################################################################

@route('/geoann')
def index():

    ann_dir = 'Chennai/Chennai_Tweets/'

    list_files = get_files(ann_dir)

    ann_files = set()

    for fname in list_files:
        ann_files.add(ann_dir+fname[:-4])

    for x in ann_files:
        return get_ann_by_file_name(x)

################################################################################

@route('/g')
def temp():

    my_dict={'number': '123', 'street': 'Fake St.', 'city': 'Fakeville'}

    return template('I live at {{number}} {{street}}, {{city}}', **my_dict)

################################################################################

from bottle import route, request

@route('/login')
def login():
    return '''
        <form action="/login" method="post">
            Username: <input name="username" type="text" />
            Password: <input name="password" type="password" />
            <input value="Login" type="submit" />
        </form>
    '''

@route('/login', method='POST')
def do_login():
    username = request.forms.get('username')
    password = request.forms.get('password')
    if check_login(username, password):
        return "<p>Your login information was correct.</p>"
    else:
        return "<p>Login failed.</p>"

################################################################################

if __name__ == "__main__":

    run(host='0.0.0.0', port=8080)
