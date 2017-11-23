#! /usr/bin/python2.7
import ConfigParser
import os,stat,sys
import time 
from ftplib import FTP
import socket
import getpass
import re 
import json
import signal
from xml.etree.ElementTree import ElementTree,Element 

current_user_name = os.path.expanduser('~')

CHANGE_SIGN_CONFIG = 0

IF_BREAK = 0

def readconf(conf_path):
        with open(conf_path,"r") as load_f:
            load_dict = json.load(load_f)
        return load_dict

def get_datapath(current_user_name):
	return current_user_name+"/picture_ftp/"

def mkdir_ftp(datapath):
	flag = False
        if ( (os.path.exists(datapath)) == flag ):
		os.makedirs(datapath)


def readLocalFile(directory):
	FileList = read_picture_url(directory)
	loop_picture(FileList)

def readFtpFile(ftp_address,directory_ftp):
	ftp=FTP()             
	ftp.connect(ftp_address) 
	ftp.login("","")      
	ftp.cwd(directory_ftp) 
	ftp.dir()   
	FileList_ftp = ftp.nlst()
        count = 0
	imageListfrom_ftp = []
	datapath = get_datapath(current_user_name)
	while (count < len(FileList_ftp)):
    		picture_filename = FileList_ftp[count]
    		localpath = datapath+picture_filename
                write_local_from_ftp(localpath,picture_filename,ftp_address,directory_ftp)
    		count = count + 1

	FileList = read_picture_url(datapath)
        loop_picture(FileList)

def change_wallpaper(picture_filename):
	cmd='dconf write /org/mate/desktop/background/picture-filename \"\''+picture_filename+'\'\"'
	info=os.system(cmd)

def change_login_background(picture_filename):
	tree = read_xml("/usr/share/backgrounds/f21/default/f21.xml")
        text_nodes_1920 = get_node_by_keyvalue(find_nodes(tree, "static/file/size"), {"width":"1920"})
        text_nodes_2048 = get_node_by_keyvalue(find_nodes(tree, "static/file/size"), {"width":"2048"})
        text_nodes_1280 = get_node_by_keyvalue(find_nodes(tree, "static/file/size"), {"width":"1280"})
	change_node_text(text_nodes_1920, picture_filename)
        change_node_text(text_nodes_2048, picture_filename)
        change_node_text(text_nodes_1280, picture_filename)
	reload(sys)
        sys.setdefaultencoding('utf8')
        write_xml(tree, "/usr/share/backgrounds/f21/default/f21.xml")


def loop_picture(FileList):
	intervals = readconf(current_user_name+"/.wallpaper.conf")['intervals']
	count = 0
        while (count < len(FileList)):
	    global CHANGE_SIGN_CONFIG
	    global IF_BREAK
	    if(CHANGE_SIGN_CONFIG == 1):
		IF_BREAK = 1
	        break;
	    else:
            	picture_filename = FileList[count]
	    	change_wallpaper(picture_filename)
	    	change_login_background(picture_filename)
            	time.sleep(int(intervals))
            	count = count + 1

def read_picture_url(datapath):
	FileList = []
	for file in os.listdir(datapath) :
       		file_path = os.path.join(datapath, file)
                FileList.append(file_path)
	FileList.sort()
	return FileList

def write_local_from_ftp(localpath,picture_filename,ftp_address,directory_ftp):
        ftp=FTP()
        ftp.connect(ftp_address)
        ftp.login("","")
        #bufsize=1024
        ftp.cwd(directory_ftp)
	fp = open(localpath,"wb").write
        filename = 'RETR '+picture_filename
        ftp.retrbinary(filename,fp)


def read_xml(in_path):  
	tree = ElementTree()  
	tree.parse(in_path)  
	return tree

def find_nodes(tree, path):   
	return tree.findall(path) 

def if_match(node, kv_map):  
	for key in kv_map:  
    	  if node.get(key) != kv_map.get(key):  
      	     return False  
  	return True

def get_node_by_keyvalue(nodelist, kv_map):  
	result_nodes = []  
	for node in nodelist:  
		if if_match(node, kv_map):  
	  	   result_nodes.append(node)  
	return result_nodes

def change_node_text(nodelist, text, is_add=False, is_delete=False):  
	for node in nodelist:  
	    if is_add:  
                node.text += text  
            elif is_delete:  
      	        node.text = ""  
    	    else:  
                node.text = text 

def write_xml(tree, out_path):  
	tree.write(out_path, encoding="utf-8",xml_declaration=True)  


def change_by_signal():
	global IF_BREAK
        global CHANGE_SIGN_CONFIG
        if(IF_BREAK == 1):
        	CHANGE_SIGN_CONFIG = 0
		IF_BREAK = 0
                loopreadconf()


def loopreadconf():
	load_dict = readconf(current_user_name+"/.wallpaper.conf")
        count = 0
        while(count < len(load_dict['directorys'])):
                if( str(load_dict['directorys'][count]['type']) == "directory"):
                        directory = load_dict['directorys'][count]['value']
                        readLocalFile(str(directory));
			change_by_signal()

                elif( str(load_dict['directorys'][count]['type']) == "url"):
			datapath= get_datapath(current_user_name)
                        mkdir_ftp(datapath)
                        url = load_dict['directorys'][count]['value']
                        compile_rule = re.compile(r'\d+[\.]\d+[\.]\d+[\.]\d+')
                        ftp_address_list = re.findall(compile_rule, url)
                        ftp_address = ftp_address_list[0]
                        directory_include = url.split('.')[-1]
                        directory_ftp = directory_include[directory_include.index("/")+1:len(directory_include)]
                        readFtpFile(ftp_address,directory_ftp);
			change_by_signal()

                if count == len(load_dict['directorys'])-1:
                        loopreadconf()
		count = count + 1


def myHandler(signum, frame):
	global CHANGE_SIGN_CONFIG
	CHANGE_SIGN_CONFIG = 1

if __name__ == "__main__":	
	signal.signal(signal.SIGUSR1,myHandler)
	loopreadconf();	


