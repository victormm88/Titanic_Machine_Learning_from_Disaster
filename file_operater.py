# -*- coding: utf-8 -*-

" load file(training data or test data) "

__author__ = 'Wang Junqi'

import csv;
import numpy as np;

def load_file(file_name):
	data=[];
	temp_file=open(file_name, 'rb');
	csv_file_object = csv.reader(temp_file);
	csv_file_object.next();
	for row in csv_file_object:
		data.append(row);
	data=np.array(data);
	temp_file.close();
	return data;

def write_file(file_name,header,data):
	temp_file=open(file_name, "wb");
	csv_file_object=csv.writer(temp_file);
	csv_file_object.writerow(header);
	for i in xrange(data.shape[0]):
		csv_file_object.writerow(data[i,:]);
	temp_file.close();
