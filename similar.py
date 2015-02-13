#!/usr/bin/env python
# -*- coding: utf-8 -*-

" cao "

__author__ = 'Wang Junqi'

import file_operater;

data_my=file_operater.load_file('b.csv');
data_gender=file_operater.load_file('gendermodel.csv');
data_3=file_operater.load_file('genderclassmodel.csv');

num_row=data_gender.shape[0];

my_and_g=0;
my_and_3=0;
for i in xrange(num_row):
	if data_my[i][1]==data_gender[i][1]:
		my_and_g+=1;
	if data_my[i,1]==data_3[i,1]:
		my_and_3+=1;
print 'my_and_g:  '+str(my_and_g*1.0/num_row);
# print 'my_and_3:  '+str(my_and_3*1.0/num_row);