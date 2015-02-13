#!/usr/bin/env python
# -*- coding: utf-8 -*-

" predict the  attribute 'age' if it is miss with a average"

__author__ = 'Wang Junqi'

import file_operater;
import numpy as np;

def t_data():
	data=file_operater.load_file('train.csv');
	num_hasage=sum(data[:,5]!='');
	sum_age=sum(data[data[:,5]!='',5].astype(np.float));
	average=sum_age/num_hasage;
	for x in [data[i] for i in xrange(data.shape[0])]:
		if x[5]=='':
			x[5]=str(average);
	return data,average;

def s_data():
	data,average=t_data();
	data=file_operater.load_file('test.csv');
	test_array=np.zeros((data.shape[0],data.shape[1]+1),dtype='S82');
	test_array[:,0]=data[:,0];
	test_array[:,1]=0;
	test_array[:,2:]=data[:,1:];
	data=test_array;
	for x in [data[i] for i in xrange(data.shape[0])]:
		if x[5]=='':
			x[5]=str(average);
	return data;