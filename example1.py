import elasticsearch
import requests
import base64
import glob
import os
import queue
import sys
from yapsy.PluginManager import PluginManager
import logging
logging.basicConfig(level=logging.DEBUG)
from yapsy.IPlugin import IPlugin
from plugins.plugin1 import PluginOne
import threading


class myClass(threading.Thread):
    def __init__(self,thread_id,chunk_size,chunk_size_inc,q):
        threading.Thread.__init__(self)
        self.thread_id=thread_id
        self.chunk_size = chunk_size
        self.chunk_size_inc=chunk_size_inc
        self.q=q
        
    def run(self):
        global data
        print(threading.current_thread().getName(),"Starting")
        fo=f.read(self.chunk_size_inc)
        self.q.put(fo)
        f.seek(self.chunk_size)
        print("contents: ",fo,"\n\n\n")
        return                                 
                        
es = elasticsearch.Elasticsearch() # by default it takes 9200
print(es.cat.health())



body = {
  "description" : "Extract attachment information",
  "processors" : [
    {
      "attachment" : {
        "field" : "data"
      }
    }
  ]
}


def main():   
    global p1
    #  Load the plugins from the plugin directory.
    manager = PluginManager()
    manager.setPluginPlaces(["plugins"])
    manager.collectPlugins()
    # Loop round the plugins and print their names.
    for plugin in manager.getAllPlugins():
        print("==========>  ",format(plugin.plugin_object))
        #p="C:\Python34\directory1"
        #print("path is:======>",p)
        p1=plugin.plugin_object.print_name()
        print(p1) 
        p2=PluginOne()
        p2.g()
       
        
if __name__ == "__main__":
    main()
threads=[]
data1=" "
my_queue = queue.Queue()
glob.glob(p1)
os.chdir(p1) 
for file in glob.glob("*.txt"):
        with open(file, 'r') as f:
                file_size = os.path.getsize(file)
                print('File size: {}'.format(file_size))
                filesize='File size: {}'.format(file_size)
                chunk_size =(int)(file_size/10)
                print("chunk_size is",chunk_size)
                chunk_size_inc=chunk_size
                print("==>",f)
                data=" "
                data1=" "
                for i in range(10):
                    t1= myClass(i,chunk_size,chunk_size_inc,my_queue) 
                    t1.start()
                    chunk_size=chunk_size+chunk_size_inc
                    threads.append(t1)
                    data=my_queue.get()
                    data1=data1+data
                    #print("data ",data)
                for x in threads: 
                    x.join()
        data = base64.b64encode(bytes(data1,'utf-8')).decode('ascii');
        result2 = es.index(index='my_index', doc_type='my_type', pipeline='attachment',body={'data': data})    
        print ("Exiting Main Thread")
        f.close()
        
     #   
       

