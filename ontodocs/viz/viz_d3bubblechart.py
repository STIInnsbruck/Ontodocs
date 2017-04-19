# !/usr/bin/env python
#  -*- coding: UTF-8 -*-


import os, sys
import json

from ..core import *
from ..core.utils import *
from ..core.builder import *  # loads and sets up Django
from ..core.viz_factory import VizFactory




# ===========
# D3 BUBBLE CHART
# ===========



class D3BubbleChartViz(VizFactory):
    """
    D3 Bubbles

    """


    def __init__(self, ontospy_graph, title=""):
        """
        Init
        """
        super(D3BubbleChartViz, self).__init__(ontospy_graph, title)
        self.static_files = ["libs/d3-v3", "libs/jquery"]


    def _buildTemplates(self):
        """
        OVERRIDING THIS METHOD from Factory
        """

        jsontree_classes = build_D3bubbleChart(0, 99, 1, self.ontospy_graph.toplayer)
        c_total = len(self.ontospy_graph.classes)

        JSON_DATA_CLASSES = json.dumps({'children': jsontree_classes, 'name': 'owl:Thing',})


        extra_context = {
                        "ontograph": self.ontospy_graph,
    					"TOTAL_CLASSES": c_total,
    					'JSON_DATA_CLASSES' : JSON_DATA_CLASSES,
                        }

        # Ontology - MAIN PAGE
        contents = self._renderTemplate("d3/d3_bubblechart.html", extraContext=extra_context)
        FILE_NAME = "index.html"
        main_url = self._save2File(contents, FILE_NAME, self.output_path)

        return main_url




# if called directly, for testing purposes pick a random ontology

if __name__ == '__main__':

    TEST_ONLINE = False
    try:

        g = get_onto_for_testing(TEST_ONLINE)

        v = D3BubbleChartViz(g, title="")
        v.build()
        v.preview()

        sys.exit(0)

    except KeyboardInterrupt as e:  # Ctrl-C
        raise e




#
#
#
# def run(graph, save_on_github=False, main_entity=None):
# 	"""
# 	"""
# 	try:
# 		ontology = graph.ontologies[0]
# 		uri = ontology.uri
# 	except:
# 		ontology = None
# 		uri = ";".join([s for s in graph.sources])
#
# 	# ontotemplate = open("template.html", "r")
# 	ontotemplate = open(ONTODOCS_VIZ_TEMPLATES + "d3_bubblechart.html", "r")
# 	t = Template(ontotemplate.read())
#
# 	c_total = len(graph.classes)
#
# 	mylist = build_D3bubbleChart(0, 99, 1, graph)
# 	# mydict = {'children': mylist, 'name': 'owl:Thing'}
#
# 	JSON_DATA_CLASSES = json.dumps({'children': mylist, 'name': 'owl:Thing',})
#
# 	c = Context({
# 					"ontology": ontology,
# 					"main_uri" : uri,
# 					"STATIC_PATH": ONTODOCS_VIZ_STATIC,
# 					"save_on_github" : save_on_github,
# 					'JSON_DATA_CLASSES' : JSON_DATA_CLASSES,
# 					"TOTAL_CLASSES": c_total,
# 				})
#
# 	rnd = t.render(c)
#
# 	return safe_str(rnd)
#
#
#
#
#
#
#
#
#
# # ===========
# # Utilities
# # ===========
#
#
#
# def build_D3bubbleChart(old, MAX_DEPTH, level=1, g=None):
# 	"""
# 	  Similar to standar d3, but nodes with children need to be duplicated otherwise they are
# 	   not depicted explicitly but just color coded
#
# 	"name": "all",
# 	"children": [
# 		{"name": "Biological Science", "size": 9000},
# 		 {"name": "Biological Science", "children": [
# 			 {"name": "Biological techniques", "size": 6939},
# 			{"name": "Cell biology", "size": 4166},
# 			{"name": "Drug discovery X", "size": 3620, "children": [
# 				{"name": "Biochemistry X", "size": 4585},
# 				{"name": "Biochemistry X", "size": 4585 },
# 			]},
# 			{"name": "Drug discovery Y", "size": 3620, "children": [
# 				{"name": "Biochemistry Y", "size": 4585},
# 				{"name": "Biochemistry Y", "size": 4585 },
# 			]},
# 			{"name": "Drug discovery A", "size": 3620, "children": [
# 				{"name": "Biochemistry A", "size": 4585},
# 			]},
# 			{"name": "Drug discovery B", "size": 3620, },
# 		 ]},
# 		etc...
# 	"""
# 	out = []
# 	if not old:
# 		old = g.toplayer
# 	for x in old:
# 		d = {}
# 		# print "*" * level, x.label
# 		d['qname'] = x.qname
# 		d['name'] = x.bestLabel(quotes=False).replace("_", " ")
# 		d['objid'] = x.id
# 		if x.children() and level < MAX_DEPTH:
# 			duplicate_row = {}
# 			duplicate_row['qname'] = x.qname
# 			duplicate_row['name'] = x.bestLabel(quotes=False).replace("_", " ")
# 			duplicate_row['objid'] = x.id
# 			duplicate_row['size'] = len(x.children()) + 5	 # fake size
# 			duplicate_row['realsize'] = len(x.children())        # real size
# 			out += [duplicate_row]
# 			d['children'] = build_D3bubbleChart(x.children(), MAX_DEPTH, level+1)
# 		else:
# 			d['size'] = 1	 # default size
# 			d['realsize'] = 0	 # default size
# 		out += [d]
#
# 	return out
#
#
#
#
# if __name__ == '__main__':
# 	import sys
# 	try:
# 		# script for testing - must launch this module
# 		# >python -m viz.viz_packh
#
# 		func = locals()["run"] # main func dynamically
# 		run_test_viz(func)
#
# 		sys.exit(0)
#
# 	except KeyboardInterrupt as e: # Ctrl-C
# 		raise e
