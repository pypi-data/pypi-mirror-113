# -*- coding: utf-8 -*-
"""
Created on Fri Apr 26 07:49:31 2019

@author: ROMDHANA
"""
import re
from functools import reduce
# =============================================================================
# =================== encode, decode (flow, flow_property) ====================
def encode(keys):
    return reduce(lambda x,y:x+chr(10)+y,keys)
def decode(key):
    return key.split(chr(10))
# =============================================================================
from prettytable import PrettyTable
class table(PrettyTable):
    def __init__(self,*cnames):
        PrettyTable.__init__(self,field_names=cnames)
        for cname in cnames:
            self.align[cname]='l'
    def disp(self,title=None):
        print #self.get_string(title)
        
class key_struct_class(dict):
    def __init__(self,*fields):
        self.inner_fields=fields
    def put(self,*keys,**defaults):
        class inner_class:
            def __init__(self,fields,**defaults):
                for field in fields:
                    if field in defaults.keys():
                        setattr(self,field,defaults[field])
                    else:
                        setattr(self,field,None)
        key=encode(list(keys))
        if not key in self.keys():self[key]=inner_class(self.inner_fields,**defaults)
    def get(self,*keys):
        return self[encode(keys)]
class list_to_dict(dict):
    def __init__(self,list_,struct_class,progress=None):
        for el in list_:
            self[el['key']]=struct_class(el)
            if progress: progress.update()
    def iterate_over_values(self,function,*args):
        for val in self.values():
            if args:function(val,args)
            else:function(val)
class dict_struct_class:
    def __init__(self,json,**args):
        self.keys=json.keys()
        self.user_object={}
        for key in self.keys:
            if isinstance(json[key],list):
                if json[key] and isinstance(json[key][0],dict):
                    if 'list_struct_class' in args:
                        list_struct_class=args['list_struct_class']
                        setattr(self,key,map(lambda x:list_struct_class(x),json[key]))
                    else:
                        setattr(self,key,map(lambda x:dict_struct_class(x),json[key]))
            else:
                setattr(self,key,json[key])
# data_base field classes =====================================================
class category_class(dict_struct_class):
    def __init__(self,json):
        dict_struct_class.__init__(self,json)
        self.parents=[]
        self.path=''
    def get_parents(self,data_base):
        parent=self.category
        while parent:
            self.parents.append(parent)
            parent_=data_base.get_category(parent)
            parent=parent_.category
            if self.path:
                self.path=parent_.name+' / '+self.path
            else: self.path=parent_.name
class unit_class(dict_struct_class):
        def __init__(self,json):
            dict_struct_class.__init__(self,json)
class flow_class(dict_struct_class):
        def __init__(self,json):
            dict_struct_class.__init__(self,json)
            self.providers=set()
            self.treatment_processes=set()
class unit_group_class(dict_struct_class):
        def __init__(self,json):
            dict_struct_class.__init__(self,json)           
class flow_property_class(dict_struct_class):
        def __init__(self,json):
            dict_struct_class.__init__(self,json)
#------------------------------------------------------------------------------
class group_class:
    def __init__(self):
        self.products=key_struct_class('default_provider','value')
        self.wastes=key_struct_class('value')
        self.elementaries=key_struct_class('value')
class grouping_class:
    def __init__(self):
        self.inputs=group_class()
        self.outputs=group_class()
        self.uf=[]# flow, flow_property
class exchange_class(dict_struct_class):
    def __init__(self,json):
        dict_struct_class.__init__(self,json)
class process_class(dict_struct_class):
    def __init__(self,json):
        dict_struct_class.__init__(self,json,list_struct_class=exchange_class)
        self.grouping=grouping_class()
    def disp(self,data_base,inputs=True,group='products'):
        def get_prop(keys):
            # flow_key 0
            # flow_property_key 1
            flow=data_base.get_flow(keys[0])
            flow_property=data_base.get_flow_property(keys[1])
            category=data_base.get_category(flow.category)
            unit_group=data_base.get_unit_group(flow_property.unitGroup)
            unit=data_base.get_unit(unit_group.unit)
            return flow,unit,category
        def get_table(data):
            t=table('flow','category','amount','unit')                
            for k,v in data.items():
                flow,unit,category=get_prop(decode(k))
                t.add_row([flow.name,category.path+'\\'+category.name,str(v.value),unit.name])
            return t
        flow,unit,category=get_prop(self.grouping.uf)
        list_=getattr({True:self.grouping.inputs,False:self.grouping.outputs}[inputs],group)
        get_table(list_).disp(title={True:'input',False:'output'}[inputs]+' ('+len(list_)+")\n"+flow.name+' [1 '+unit.name+']')
                    
        
def grouping(data_base,progress=None):
        for process in data_base.processes.values():
            if progress: progress.update()
            fu=next((e for e in process.exchanges if e.quantitativeReference),None)
            # set fu
            process.grouping.fu=[fu.flow,fu.flowProperty]
            # set flow provider
            data_base.get_flow(fu.flow).providers.add(process.key)
            # to SI, amount = 1
            fu_unit = data_base.get_unit(fu.unit)
            val = 1.0 / (fu.amount * fu_unit.conversionFactor)
            for e in process.exchanges:
                if not e.quantitativeReference:
                    flow=data_base.get_flow(e.flow)
                    unit=data_base.get_unit(e.unit)
                    group={True:process.grouping.inputs,False:process.grouping.outputs}[e.input]
                    amount=val*unit.conversionFactor*e.amount
                    if flow.flowType=="ELEMENTARY_FLOW":
                        group.elementaries.put(e.flow,e.flowProperty,value=amount)
                    if flow.flowType=="PRODUCT_FLOW":
                        group.products.put(e.flow,e.flowProperty,default_provider=e.defaultProvider,value=amount)
                    if flow.flowType=="WASTE_FLOW":
                        group.wastes.put(e.flow,e.flowProperty,value=amount)
                        # set waste treatment process
                        if e.input:
                            flow.treatment_processes.add(process.key)
            
#==============================================================================
class data_base_class:
    def __init__(self,file_name):
        import json
        from tqdm import tqdm
        field_classes={"categories":category_class,'processes':process_class,'units':unit_class,'flows':flow_class,'unit_groups':unit_group_class,'flow_properties':flow_property_class}
        def map_(field,class_):
            list_=json_data_base[field]
            with tqdm(total=len(list_),desc='map '+field) as pbar:
                setattr(self,field,list_to_dict(list_,class_,pbar))
        with open(file_name, "r") as read_file:
            json_data_base= json.load(read_file)
            for field, class_ in field_classes.items():
                map_(field,class_)
        
#------------------------------------------------------------------------------
    def get_category(self,key):
        return self.categories[key]
    def get_process(self,key):
        return self.processes[key]
    def get_flow(self,key):
        return self.flows[key]
    def get_flow_property(self,key):
        return self.flow_properties[key]
    def get_unit(self,key):
        return self.units[key]
    def get_unit_group(self,key):
        return self.unit_groups[key]
# def test():
#     from tqdm import tqdm
#     db= data_base_class('elcd.json')
#     db.categories.iterate_over_values(lambda v:v.get_parents(db))
#     with tqdm(total=len(db.processes),desc='grouping ') as pbar:
#         grouping(db,pbar)
#     return db
# db=test()

                        
                        