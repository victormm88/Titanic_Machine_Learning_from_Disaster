#!/usr/bin/env python
# -*- coding: utf-8 -*-

" predict the survive in the test file "

__author__ = 'Wang Junqi'

import numpy as np;
import entity;
import predict_age;
import file_operater;
import decision_tree;
import average_age;

train_data=file_operater.load_file('train.csv');
tree=predict_age.derive_age(train_data);
target_feature=(entity.feature(5,['5','15','25','35','45','55','70']));
decision_tree.add_cost(tree,1.9,0,target_feature);
decision_tree.prune(tree,1.9,0,target_feature);
print decision_tree.num_leaf(tree,0);
train_data=predict_age.new_data(tree,train_data);


test_data=file_operater.load_file('test.csv');
test_data=predict_age.new_data(tree,test_data,data_kind='test');

# train_data,xdsd=average_age.t_data();
# print train_data;
# test_data=average_age.s_data();

tree_index=1;
tree=[];

train_data[train_data[:,5].astype(np.float)<10,5]=5;
train_data[(train_data[:,5].astype(np.float)>=10) \
		  &(train_data[:,5].astype(np.float)<20),5]=15;
train_data[(train_data[:,5].astype(np.float)>=20) \
		  &(train_data[:,5].astype(np.float)<30),5]=25;
train_data[(train_data[:,5].astype(np.float)>=30) \
		  &(train_data[:,5].astype(np.float)<40),5]=35;
train_data[(train_data[:,5].astype(np.float)>=40) \
		  &(train_data[:,5].astype(np.float)<50),5]=45;
train_data[(train_data[:,5].astype(np.float)>=50) \
		  &(train_data[:,5].astype(np.float)<60),5]=55;
train_data[(train_data[:,5].astype(np.float)>=60),5]=70;
train_data[train_data[:,6].astype(np.int)>=3,6]=3;
train_data[train_data[:,7].astype(np.int)>=3,7]=3;
train_data[train_data[:,9].astype(np.float)<10,9]=0;
train_data[(train_data[:,9].astype(np.float)>=10) \
		  &(train_data[:,9].astype(np.float)<30),9]=10;
train_data[(train_data[:,9].astype(np.float)>=30) \
		  &(train_data[:,9].astype(np.float)<50),9]=30;
train_data[train_data[:,9].astype(np.float)>=50,9]=50;

feature=[];
feature.append(entity.feature(9,['0','10','30','50']));
feature.append(entity.feature(11,['S','C','Q']));
feature.append(entity.feature(2,['1','2','3']));
feature.append(entity.feature(4,['male','female']));
feature.append(entity.feature(6,['0','1','2','3']));
feature.append(entity.feature(7,['0','1','2','3']));
feature.append(entity.feature(5,['5','15','25','35','45','55','70']));
target_feature=entity.feature(1,['1','0']);
root_node=entity.node(0,train_data,feature,-1);
tree.append(root_node);
decision_tree.generate(tree,root_node,target_feature,0.1);
# x=np.array(['889','0','3','Johnston, Miss. Catherine Helen "Carrie"','male','35','0','0','W./C. 6607','0','','S']);
# print decision_tree.predict_classification(tree,x);
# write_line('b.csv',['PassengerId','Survived']);
decision_tree.add_cost(tree,1.329,0,target_feature);
decision_tree.prune(tree,1.329,0,target_feature);
for row in [test_data[i] for i in xrange(test_data.shape[0])]:
	if row[6].astype(np.float)>3:
		row[6]=str(3);
	if row[7].astype(np.float)>3:
		row[7]=str(3);
	if row[9]=='':
		row[9]=str(0);
	elif row[9].astype(np.float)<10:
		row[9]=str(0);
	elif row[9].astype(np.float)<30:
		row[9]=str(10);
	elif row[9].astype(np.float)<50:
		row[9]=str(30);
	else:
		row[9]=str(50); 
	if row[5].astype(np.float)<10:
		row[5]=str(5);
	elif row[5].astype(np.float)<20:
		row[5]=str(15);
	elif row[5].astype(np.float)<30:
		row[5]=str(25);
	elif row[5].astype(np.float)<40:
		row[5]=str(35);
	elif row[5].astype(np.float)<50:
		row[5]=str(45);
	elif row[5].astype(np.float)<60:
		row[5]=str(55);
	else:
		row[5]=70;
	survived=decision_tree.predict_classification(tree,row);
	row[target_feature.index]=str(survived);
test_data=test_data[:,:2];
print len(tree);
print decision_tree.num_leaf(tree,0);
# for x in tree:
	# print x.cost;
file_operater.write_file('b.csv',['PassengerId','Survived'],test_data);