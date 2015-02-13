# -*- coding: utf-8 -*-

" some function of decision tree "


__author__ = 'Wang Junqi'

import numpy as np;
import entity;
import math;
import copy;
import file_operater;

def gain(data,feature,target_feature):
	temp_list=[];
	for i in xrange(len(feature)):
		temp_h_i=0;
		h_a=0;
		for f in feature[i].value:
			num=sum(data[:,feature[i].index]==f);
			if num==0:
				continue;
			temp_h=0;
			for t_f in target_feature.value:
				temp_p=1.0*sum((data[:,target_feature.index]==t_f)&(data[:,feature[i].index]==f))/num;
				# print sum((data[:,target_feature.index]==t_f)&(data[:,feature[i].index]==f));
				if temp_p==0:
					temp_h+=0;
				else:
					temp_h+=temp_p*math.log(temp_p);
			temp_h*=-1.0*num/data.shape[0];
			temp_h_i+=temp_h;
			h_a+=num*1.0/data.shape[0]*math.log(1.0*num/data.shape[0]);
		h_a=-h_a;
		if h_a==0:
			temp_list.append(0);
		else:
			temp_list.append(temp_h_i/h_a);
	index=temp_list.index(min(temp_list));
	return index,min(temp_list);


def generate(tree,node,target_feature,ratio):
	temp_list=[];
	temp_feature_index=0;
	for feature in target_feature.value:
		temp_list.append(sum(node.data_list[:,target_feature.index]==feature));
		temp_feature_index=temp_list.index(max(temp_list));
	# 决策树生成终止条件
	if max(temp_list)==node.data_list.shape[0]:
		node.classification=target_feature.value[temp_feature_index];
		return node.node_id+1;
	if len(node.feature_list)==0:
		node.classification=target_feature.value[temp_feature_index];
		return node.node_id+1;
	feature_index,min_gain=gain(node.data_list,node.feature_list,target_feature);
	# if min_gain<=ratio:
		# node.classification=target_feature.value[temp_feature_index];
		# return node.node_id+1;
	node.feature=node.feature_list[feature_index];
	child_feature=[];
	for i in xrange(len(node.feature_list)):
		if i!=feature_index:
			child_feature.append(node.feature_list[i]);
	tree_index=0;
	for feature in node.feature_list[feature_index].value:
		if len(node.child_list)==0:
			tree_index=node.node_id+1;
		node.child_list.append(tree_index);
		temp_node=entity.node(tree_index,node.data_list[node.data_list[:,node.feature_list[feature_index].index]==feature],child_feature,node.node_id);
		tree.append(temp_node);
		tree_index=generate(tree,temp_node,target_feature,ratio);
	return tree_index;

	
def add_cost(tree,theta,index,target_feature):
	node_cost=0;
	if not hasattr(tree[index],'classification'):
		for i in tree[index].child_list:
			node_cost+=add_cost(tree,theta,i,target_feature);
		tree[index].cost=node_cost;
		return node_cost;
	else:
		num_data=tree[index].data_list.shape[0];
		if num_data==0:
			return 0;
		num_class=[];
		for x in target_feature.value:
			num_class.append(sum(tree[index].data_list[:,target_feature.index]==x));
		num_class=np.array(num_class);
		num_class=num_class*1.0/num_data;
		temp_sum=0;
		for p in num_class:
			if p!=0:
				temp_sum+=-p*math.log(p);
		temp_sum*=num_data;
		tree[index].cost=temp_sum+theta;
		return temp_sum+theta;
		
#决策树剪枝
def prune(tree,theta,index,target_feature):#这个方法执行前，必须先执行add_cost方法
	if not hasattr(tree[index],'classification'):
		num_data=tree[index].data_list.shape[0];
		num_class=[];
		for x in target_feature.value:
			num_class.append(sum(tree[index].data_list[:,target_feature.index]==x));
		num_class=np.array(num_class);
		num_class=num_class*1.0/num_data;
		temp_sum=0;
		for p in num_class:
			if p!=0:
				temp_sum+=-p*math.log(p);
		temp_sum*=tree[index].data_list.shape[0];
		temp_sum+=theta;
		# print temp_sum;
		# print tree[index].cost;
		if temp_sum<tree[index].cost:
			num_class=num_class.tolist();
			tree[index].classification=target_feature.value[num_class.index(max(num_class))];
			return True;
		else:
			for x in tree[index].child_list:
				prune(tree,theta,x,target_feature);
	return False;

	
def predict_classification(tree,person):
	i=0;
	while not hasattr(tree[i],'classification'):
		# print 'cao '+str(i);
		i=tree[i].child_list[tree[i].feature.value.index(person[tree[i].feature.index])];
		# print i;
	return tree[i].classification;

def num_leaf(tree,index):
	leaf=0;
	if not hasattr(tree[index],'classification'):
		for x in tree[index].child_list:
			leaf+=num_leaf(tree,x);
		return leaf;
	else:
		return 1;