# -*- coding: utf-8 -*-

' all classes of the project 2014/11/13'

__author__ = 'Wang Junqi'

class feature(object):
	def __init__(self,index,value):
		self.index=index;
		self.value=value;
	
class node(object):
	def __init__(self,node_id,data_list,feature_list,parent_node):
		self.node_id=node_id;
		self.data_list=data_list;
		self.parent_node=parent_node;
		self.feature_list=feature_list;
		self.child_list=[];
		