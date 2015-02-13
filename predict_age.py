#!/usr/bin/env python
# -*- coding: utf-8 -*-

" predict the  attribute 'age' if it is miss "

__author__ = 'Wang Junqi'

import numpy as np;
import entity;
import math;
import copy;
import file_operater;
from decision_tree import *;



def derive_age(data,data_kind='train'):
	tree_index=1;
	tree=[];
	bia=0;
	if data_kind=='train':
		bia=0;
	else:
		bia=-1;
	train_data=data[data[:,5+bia]!=''];
	train_data[train_data[:,5+bia].astype(np.float)<10,5+bia]=5;
	train_data[(train_data[:,5+bia].astype(np.float)>=10) \
			  &(train_data[:,5+bia].astype(np.float)<20),5+bia]=15;
	train_data[(train_data[:,5+bia].astype(np.float)>=20) \
			  &(train_data[:,5+bia].astype(np.float)<30),5+bia]=25;
	train_data[(train_data[:,5+bia].astype(np.float)>=30) \
			  &(train_data[:,5+bia].astype(np.float)<40),5+bia]=35;
	train_data[(train_data[:,5+bia].astype(np.float)>=40) \
			  &(train_data[:,5+bia].astype(np.float)<50),5+bia]=45;
	train_data[(train_data[:,5+bia].astype(np.float)>=50) \
			  &(train_data[:,5+bia].astype(np.float)<60),5+bia]=55;
	train_data[(train_data[:,5+bia].astype(np.float)>=60),5+bia]=70;
	train_data[train_data[:,6+bia].astype(np.int)>=3,6+bia]=3;
	train_data[train_data[:,7+bia].astype(np.int)>=3,7+bia]=3;
	train_data[train_data[:,9+bia].astype(np.float)<10,9+bia]=0;
	train_data[(train_data[:,9+bia].astype(np.float)>=10) \
			  &(train_data[:,9+bia].astype(np.float)<30),9+bia]=10;
	train_data[(train_data[:,9+bia].astype(np.float)>=30) \
			  &(train_data[:,9+bia].astype(np.float)<50),9+bia]=30;
	train_data[train_data[:,9+bia].astype(np.float)>=50,9+bia]=50;
	feature=[];
	feature.append(entity.feature(9+bia,['0','10','30','50']));
	feature.append(entity.feature(11+bia,['S','C','Q']));
	feature.append(entity.feature(2+bia,['1','2','3']));
	feature.append(entity.feature(4+bia,['male','female']));
	feature.append(entity.feature(6+bia,['0','1','2','3']));
	feature.append(entity.feature(7+bia,['0','1','2','3']));
	target_feature=(entity.feature(5+bia,['5','15','25','35','45','55','70']));
	root_node=entity.node(0,train_data,feature,-1);
	tree.append(root_node);
	generate(tree,root_node,target_feature,0.3);
	# x=np.array(['889','0','3','Johnston, Miss. Catherine Helen "Carrie"','female','','0','0','W./C. 6607','0','','S']);
	print len(tree);
	return tree;
	
def new_data(tree,data,data_kind='train',target_feature=entity.feature(5,['5','15','25','35','45','55','70'])):
	if data_kind=='test':
		test_array=np.zeros((data.shape[0],data.shape[1]+1),dtype='S82');
		test_array[:,0]=data[:,0];
		test_array[:,1]=0;
		test_array[:,2:]=data[:,1:];
		data=test_array;
	for row in [data[i] for i in xrange(data.shape[0])]:
		if row[target_feature.index]=='':
			copy_row=copy.copy(row);
			if copy_row[6].astype(np.float)>=3:
				copy_row[6]=str(3);
			if copy_row[7].astype(np.float)>=3:
				copy_row[7]=str(3);
			if copy_row[9]=='':
				copy_row[9]=str(0);
			elif copy_row[9].astype(np.float)<10:
				copy_row[9]=str(0);
			elif copy_row[9].astype(np.float)<30:
				copy_row[9]=str(10);
			elif copy_row[9].astype(np.float)<50:
				copy_row[9]=str(30);
			else:
				copy_row[9]=str(50);
			age=predict_classification(tree,copy_row);
			row[target_feature.index]=str(age);
	return data;