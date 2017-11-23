import os,re,sys
import subprocess,signal


def wallpaper_config(pid):
        os.kill(pid,signal.SIGUSR1)

def get_pid_by_name(name):
    cmd = "ps ax | grep '%s" % name+"'"
    f = os.popen(cmd)
    txt = f.readlines()
    if len(txt) == 0:
        print "no process \"%s\"!!" % name
        return
    else:
       for line in txt:
           colum = line.split()
           pid = colum[0]
           if(colum[4] == "python" and colum[5] == "/opt/wallpaper/wallpaper.py"):
                return pid

if __name__ == "__main__":

        pid  = get_pid_by_name("python /opt/wallpaper/wallpaper.py")                                         
	
	if(pid != None):
        	wallpaper_config(int(pid))              
