import json, os
import numpy as np
from bottle import route, run, template
from bottle import static_file
from collections import defaultdict

################################################################################
################################################################################

@route('/<filename:path>')
def send_static(filename):
    return static_file(filename, root='static/')

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
		<title>Fullscreen Pageflip Layout with BookBlock</title>
		<meta name="description" content="Fullscreen Pageflip Layout with BookBlock" />
		<meta name="keywords" content="fullscreen pageflip, booklet, layout, bookblock, jquery plugin, flipboard layout, sidebar menu" />
		<meta name="author" content="Codrops" />
		<link rel="stylesheet" type="text/css" href="css/jquery.jscrollpane.custom.css" />
		<link rel="stylesheet" type="text/css" href="css/bookblock.css" />
		<link rel="stylesheet" type="text/css" href="css/custom.css" />
		<script src="js/modernizr.custom.79639.js"></script>
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

    {{!brat_anns_data}}

    {{!brat_embed_function}}

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

def brat_tweet_annotations_data(id):

    return "var docData"+str(id)+" = {{!annotations}}; "

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

def get_brat_anns_data():

    ann_files, ann_dir = get_ann_files()

    data = list()

    for id, ann_file in enumerate(ann_files):

        id += 1

        data.append(template(brat_tweet_annotations_data(id), {"annotations": get_ann_by_file_name(ann_file)}))

    return '<script type="text/javascript"> ' + "\n".join(data) + ' </script>'

################################################################################

def get_brat_embed_script(len_ann_files):
    ''' Embed function '''

    lines = list()

    for id in range(len_ann_files):

        id += 1

        lines.append("Util.embed('embedding-brat_anns_"+str(id)+"', $.extend({}, collData), $.extend({}, docData"+str(id)+"));")

    t = '''
        <script type="text/javascript">
            head.ready(function() {
                {{!brat_embed_functions}}
            });
        </script>
        '''

    return template(t, {"brat_embed_functions": "\n".join(lines)})

################################################################################
################################################################################
################################################################################

@route('/annotate')
def annotate():

    ann_files, ann_dir = get_ann_files()

    menu_items = ""
    content_items = ""

    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    for idx, ann_file in enumerate(ann_files):

        idx += 1

        menu_items += '''<li>
                            <a href="#item'''+str(idx)+'''">
                                '''+ann_file.replace(ann_dir,"")+'''
                            </a>
                        </li>'''

        content_items += ''' <div class="bb-item" id="item'''+str(idx)+'''">
                                <div class="content">
                                    <div class="scroller">
                                        <div id="embedding-brat_anns_'''+str(idx)+'''">
                                        </div>
                                    </div>
                                </div>
                            </div>'''

    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    brat_embed_script = get_brat_embed_script(len(ann_files))

    return template(html(), {   "menu_items": menu_items,
                                "content_items": content_items,
                                "brat_anns_data": get_brat_anns_data(),
                                "brat_embed_function": brat_embed_script})

################################################################################

if __name__ == "__main__":

    run(host='0.0.0.0', port=8080)
