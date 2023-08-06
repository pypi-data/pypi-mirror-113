from datetime import datetime
import json
import numpy
import platform
import boto3
import os


class MetricBoard():

    def __init__(self,name,param_list,nb_trials,description="No description"):
        self.param_list = param_list
        self.nb_trials = nb_trials
        self.start_time = None
        self.stop_time = None
        self.description = description
        self.status = 0
        self.name = name
        self._current_simulation = None
        self._category_list = {}
        self._simulation_list = {}
        self._folder = "."
        self._filename = "data.csv"
        self._ACL = "private"
        self.start()

    def set_backend(self,folder,filename,ACL="private"):
        self._folder = folder 
        self._filename = filename
        self._ACL = ACL

    def add_category_metric(self,name,metric_name_list):
        category = Category_Metric(name,metric_name_list,xlabel=self.name)
        self._category_list[name] = category

    def start(self):
        self.status = 1
        self.start_time = datetime.now().time().strftime("%Y-%m-%d %H:%M:%S")

    def stop(self):
        self.status = 2
        self.stop_time = datetime.now().time().strftime("%Y-%m-%d %H:%M:%S")

    def start_simulation(self,key):
        simulation = Simulation(self.nb_trials)
        simulation.start()
        self._simulation_list[key] = simulation

    def increment_simulation(self,key):
        self._simulation_list[key].increment()

    def stop_simulation(self,key):
        self._simulation_list[key].stop()

    def add_category_metric_values(self,category_name,key,metric_name_list,value_list):
        self._category_list[category_name].add_values(key,metric_name_list,value_list)
  
    def export_sys_info(self):
        data = {}
        try:
            computer = platform.uname()
            data = {}
            data["system"] = computer[0]
            data["user"] = computer[1]
            data["release"] = computer[2]
            data["version"] = computer[3]
            data["machine"] = computer[4]
            data["processor"] = computer[5]
        except:
            data = {}

        return data


    def export(self):
        data_sys_info = self.export_sys_info()
        data = {"name":self.name,"sys":data_sys_info,"status":self.status,"start_time":self.start_time,"stop_time":self.stop_time}
        data_simulation = []

        for key in self._simulation_list:
            simulation = self._simulation_list[key]
            data_simulation.append({"name":key,"data":simulation.export()})
        
        data["simulations"] = data_simulation

        data_category_metric = []
        for key in self._category_list:
            category = self._category_list[key]
            data_category_metric.append({"name":key,"data":category.export()})

        data["category_metrics"] = data_category_metric
        return data


    def save(self):

        def convert(o):
            if isinstance(o, numpy.int64): return int(o)  
            raise TypeError

        data = self.export()

        if "s3://" in self._folder:
            bucket = self._folder.replace("s3://","")
            s3 = boto3.resource('s3')
            s3object = s3.Object(bucket,self._filename)
            s3object.put(Body=(bytes(json.dumps(data, default=convert).encode('UTF-8'))),ACL=self._ACL)
        else:
            filename = os.path.join(self._folder,self._filename)
            with open(filename, 'w') as outfile:
                json.dump(data, outfile, default=convert)

class Simulation():

    def __init__(self,nb_trials,name="simulation"):
        self.current_trial = None
        self.nb_trials = nb_trials
        self.status = 0
        self.start_time = None
        self.stop_time = None
        self.name = name

    def start(self):
        self.status = 1
        self.start_time = datetime.now().time().strftime("%Y-%m-%d %H:%M:%S")
        self.current_trial = 0

    def stop(self):
        self.status = 2
        self.stop_time = datetime.now().time().strftime("%Y-%m-%d %H:%M:%S")

    def increment(self):
        self.current_trial += 1

    def export(self):
        data = {"current_trial":self.current_trial,"status":self.status,"start_time":self.start_time,"stop_time":self.stop_time,"nb_trials":self.nb_trials}
        return data

class Metric():

    def __init__(self):
        
        self.value_list = []

    def add_value(self,value):
        self.value_list.append(value)

    def export(self):
        data = {"y":self.value_list}
        return data

class Category_Metric():

    def __init__(self,name,metric_name_list,xlabel="x"):

        self.name = name 
        metric_list = {}
        for metric_name in metric_name_list:
            metric_list[metric_name] = Metric()

        self._metric_list = metric_list
        self._x = []
        self.xlabel = xlabel

    def default_layout(self):
        return {"xlabel":self.xlabel,"ylabel":self.name,"xtype":"linear","ytype":"linear"}

    def add_values(self,key,metric_name_list,value_list):

        self._x.append(key)
        for indice in range(len(metric_name_list)):
            metric_name = metric_name_list[indice]
            value = value_list[indice]
            self._metric_list[metric_name].add_value(value)

    def export(self):
        layout = self.default_layout()
        data = []
        for key in self._metric_list:
            metric = self._metric_list[key]
            data_temp = metric.export()
            data_temp["name"] = key
            data.append(data_temp)

        data = {"layout":layout,"name":self.name,"x":self._x,"data":data}
        return data



