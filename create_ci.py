#!/usr/bin/python
import sys,os
import operator
import itertools
def prepare_attr(info):
	attr = '\tprivate ${attr};\n'
	return attr.format(attr = info)
 
	

def prepare_function(type,info):
	f_name = info[0]
	if (len(info) > 1):
		param_list = info[1].split(',')
	else:
		param_list = []
	if (param_list):
		h_param_c = ' * @param {param_name}\n'
		c_param_c = '\t * @param {param_name}\n'
		if (type == 'helper'):
			param_c = h_param_c
		else:
			param_c = c_param_c
		param = '${param_name},'
	
		param_c_list = [param_c.format(param_name = item)\
											for item in param_list]
		param_c = reduce(operator.concat,param_c_list)
		param_c = param_c[:-1]
		
		param_def = [param.format(param_name=item) for item in param_list]
		param_d = reduce(operator.concat,param_def)
		param_d = param[:-1]
	else:
		param_c = ''
		param_d = ''
	
	file = open( type + '_function.tmpl','r').read()
	file = file.format(	name = f_name,param_comment = param_c,\
											param = param_d)
	return file


def generate_path(type, name_lower):
	created_file_path = '../application/'
	created_file_path = created_file_path + type + 's/' + name_lower
	#equal to created_file_path += type =='view' ? '.tpl' : '.php'
	created_file_path += '.tpl' if type == 'view' else '.php'
	return created_file_path


def prepare_template(type, name, add_info):
	name_lower = name.lower()
	created_file_path = generate_path(type, name_lower)
	def split_by_colon(str):
		return str.split(':')
	template = open(type + '.ci.tmpl', 'r').read()
	if (type != 'model'):
		add_info = [split_by_colon(info) for info in add_info]
		add_info = [prepare_function(type,info) for info in add_info]
		f_list = reduce(operator.concat, add_info) 
		template = template.format(	functions = f_list,\
																name = name,\
																name_lower = name_lower,\
																location = created_file_path)
	else:
		add_info = [prepare_attr(info) for info in add_info]
		a_list = reduce(operator.concat, add_info) 
		template = template.format(	attr = a_list,\
																name = name,\
																name_lower = name_lower,\
																location = created_file_path)
	return template


def create_file(name, option, add_info):
	if(option == '-h' or option == '--helper'):
		type = 'helper'
		template = prepare_template('helper', name, add_info)
	elif (option == '-m' or option == '--model'):
		type = 'model'
		template = prepare_template('model',name,add_info)
	elif (option == '-c' or option == '--controller'):
		type = 'controller'
		template = prepare_template('controller',name,add_info)
	elif (option == '-v' or option == '--view'):
		type = 'view'
		template = open(type + '.ci.tmpl', 'r').read()
	else :
		print "Usage: create.py [OPTION] [NAME] [ADDITIONALS..]"
		return
	created_file_path = generate_path(type)
	if (os.path.isfile(created_file_path)):
		print 'File Existed! Please change the name!'
		return
	created_file = open (created_file_path, 'w')
	created_file.write(template)
	created_file.close()
	print "a {0} file has been created in {1}".format(type,created_file_path)


#main
if (len(sys.argv) < 2):
	print "Usage: create.py [OPTION] [NAME] [ADDITIONALS..]"
else: 
	if (sys.argv[1] == "--help"):
		print """
This is a script to create a Code Igniter 2.0.0 class files or
Smarty 3.0 template file in the default directory with comments.\n
Usage: create.py [OPTION] [NAME] [ADDTIONALS..]\n
The first 2 arguments are mandatory, except for --help.
List of [OPTION]: 
--help
Display this page.
\n
-c,--controller
To create a controller with the [NAME] and methods named in
[ADDITIONALS..]
\n
-m, --model
To create a model class with the [NAME] and attributes named in 
[ADDITIONALS].
\n
v,--view
To create a view template with the [NAME].\n
-h,--helper
To create a helper class with the [NAME] and methods named in
[ADDITIONALS].\n
format of [ADDITIONALS..]:
method_name1:parameter1,parameter2...\n
Example:
./create.py -h foo:x,y bar:a,b
This command create a helper class file with 2 methods:
foo(x,y) and bar (a,b)
		"""
	else:
		option = sys.argv[1]
		name = sys.argv[2]
		add_info = sys.argv[3:]
		create_file(name, option, add_info)

