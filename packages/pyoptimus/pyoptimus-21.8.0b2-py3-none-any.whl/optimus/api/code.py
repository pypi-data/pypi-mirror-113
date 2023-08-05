import re
import inspect
from inspect import signature
from pprint import pformat

from optimus.engines.base.basedataframe import BaseDataFrame as dataframe_class
from optimus.infer import is_list, is_str
from optimus.helpers.types import DataFrameType, ConnectionType, ClustersType, MaskDataFrameType, is_any_optimus_type
from optimus.helpers.core import val_to_list, one_list_to_val

from .prepare import prepare

from optimus.engines.base.engine import BaseEngine as engine_class
from optimus.engines.base.stringclustering import Clusters as clusters_class

from optimus.engines.base.create import BaseCreate as create_class
from optimus.engines.base.io.load import BaseLoad as load_class
from optimus.engines.base.io.save import BaseSave as save_class
from optimus.engines.base.io.connect import Connect as connect_class

from optimus.engines.base.columns import BaseColumns as cols_class
from optimus.engines.base.rows import BaseRows as rows_class
from optimus.engines.base.set import BaseSet as set_class
from optimus.engines.base.mask import Mask as mask_class
from optimus.engines.base.ml.models import ML as ml_class
from optimus.plots.plots import Plot as plots_class
from optimus.outliers.outliers import Outliers as outliers_class
from optimus.engines.base.profile import BaseProfile as profile_class

engine_accessors = {
    "create": create_class,
    "load": load_class,
    "save": save_class,
    "connect": connect_class
}

dataframe_accessors = {
    "cols": cols_class,
    "rows": rows_class,
    "set": set_class,
    "mask": mask_class,
    "ml": ml_class,
    "plot": plots_class,
    "outliers": outliers_class,
    "profile": profile_class
}

accessors = {**engine_accessors, **dataframe_accessors}

def _create_new_variable(base_name, names):
    while base_name in names:
        base_name = _increment_variable_name(base_name)
        
    return base_name
    
def _increment_variable_name(variable_name):
    match = re.search(r'\d+$', variable_name)
    if match:
        variable_name = variable_name[0:match.start()] + str(int(variable_name[match.start():match.endpos])+1)
    else:
        variable_name = variable_name + "2"
    return variable_name

def _arguments(args, args_properties=None):
    
    args_list = []
    
    # It doesn't find properties or allows kwargs
    if not args_properties or "kwargs" in args_properties:
        args_list = list(args.keys())
        for key in ["source", "target", "operation", "operation_options"]:
            if key in args_list:
                args_list.remove(key)
    
    # Properties from declaration
    else:
        args_list = args_properties.keys()

    # Formating
    for arg in args_list:
        # Variable names of list of variable names
        if arg in args:
            if arg in args_properties and is_any_optimus_type(args_properties[arg].get("type", None)):
                if is_list(args[arg]):
                    args[arg] = f"[{', '.join(args[arg])}]"
                else:
                    args[arg] = args[arg]
            # Native types
            elif is_str(arg) and args_properties[arg].get("type", None) == dict:
                pass
            else:
                args[arg] = pformat(args[arg])

        
    return ", ".join([f'{arg}={args[arg]}' for arg in args_list if arg in args])

def _generate_code_target(body, properties, target):

    arguments = _arguments(body, properties["arguments"])
    
    code = ''

    if target:
        code += f'{target} = '
    
    if body.get("source", None):
        code += f'{body["source"]}.'

    code += f'{body["operation"]}({arguments})'
    
    if target:
        return code, [target]
    else:
        return code, []

def _generate_code_dataframe_transformation(body, properties, variables):

    target = body.get("target")

    if target is None:
        target = body["source"]

    options = body.get("operation_options", None)
    if options:
      if options.get("creates_new", False):
        target = available_variable("df", variables)
    return _generate_code_target(body, properties, target)

def _generate_code_dataframe_mask(body, properties, variables):
    target = body.get("target", available_variable("mask", variables))
    return _generate_code_target(body, properties, target)

def _generate_code_dataframe_clusters(body, properties, variables):    
    target = body.get("target", available_variable("clusters", variables))
    return _generate_code_target(body, properties, target)

def _generate_code_output(body, properties, variables):    
    target = body.get("target", "result")
    return _generate_code_target(body, properties, target)

def _generate_code_engine_dataframe(body, properties, variables):    
    target = body.get("target", available_variable("df", variables))
    return _generate_code_target(body, properties, target)

def _generate_code_engine_connection(body, properties, variables):    
    target = body.get("target", available_variable("conn", variables))
    return _generate_code_target(body, properties, target)

def _generate_code_engine(body, properties, variables):    
    target = body.get("target", available_variable("op", variables))
    return _generate_code_target(body, properties, target)

def _get_generator(func_properties, method_root_type):

    if method_root_type == "dataframe":
    
        # If the method returns a dataframe, it's a transformation
        if DataFrameType == func_properties["return_annotation"]:
            return _generate_code_dataframe_transformation
        # TO-DO: should mask functions be treated as transformations? (MaskDataFrameType)
        if MaskDataFrameType == func_properties["return_annotation"]:
            return _generate_code_dataframe_mask
        # If the method returns anything else, it's an output
        elif ClustersType == func_properties["return_annotation"]:
            return _generate_code_dataframe_clusters
        else:
            return _generate_code_output
    
    elif method_root_type == "engine":
    
        if DataFrameType == func_properties["return_annotation"]:
            return _generate_code_engine_dataframe
        elif ConnectionType == func_properties["return_annotation"]:
            return _generate_code_engine_connection
        else:
            return _generate_code_output
        
    elif method_root_type == "optimus":
        
        return _generate_code_engine
    
    elif method_root_type == "clusters":
    
        return _generate_code_output
        
def _get_method_root_type(accessor):
    if accessor in engine_accessors:
        return "engine"
    if accessor in dataframe_accessors:
        return "dataframe"

def _init_methods(engine):

    method = ""

    if engine == "pandas":
        from optimus.engines.pandas.engine import PandasEngine
        method = PandasEngine
    if engine == "vaex":
        from optimus.engines.vaex.engine import VaexEngine
        method = VaexEngine
    if engine == "spark":
        from optimus.engines.spark.engine import SparkEngine
        method = SparkEngine
    if engine == "dask":
        from optimus.engines.dask.engine import DaskEngine
        method = DaskEngine
    if engine == "ibis":
        from optimus.engines.ibis.engine import IbisEngine
        method = IbisEngine
    if engine == "cudf":
        from optimus.engines.cudf.engine import CUDFEngine
        method = CUDFEngine
    if engine == "dask_cudf":
        from optimus.engines.dask_cudf.engine import DaskCUDFEngine
        method = DaskCUDFEngine
        
    return method

def _generate_code(body=None, variables=[], **kwargs):
    
    if not body:
        body = kwargs

    operation = body["operation"].split(".")

    method = None
    method_root_type = None
    
    if operation[0] == "Optimus":
        method = _init_methods(body["engine"])
        method_root_type = "optimus"
        operation = []
    elif operation[0] in accessors:
        method = accessors[operation[0]]
        method_root_type = _get_method_root_type(operation[0])
        operation = operation[1:]
    elif getattr(dataframe_class, operation[0], None):
        method = dataframe_class
        method_root_type = "dataframe"
    elif getattr(engine_class, operation[0], None):
        method = engine_class
        method_root_type = "engine"
    elif getattr(clusters_class, operation[0], None):
        method = clusters_class
        method_root_type = "clusters"

    for item in operation:
        method = getattr(method, item)

    properties = method_properties(method, method_root_type)

    code, updated = properties["generator"](body, properties, variables)
    
    return code, updated

def optimus_variables():
    from optimus.helpers.functions import engines, dataframes, clusters, connections
    return [ *engines(), *dataframes(), *clusters(), *connections() ]

def available_variable(name, variables):
    return _create_new_variable(name, [*variables, *optimus_variables()])


def method_properties(func, method_root_type):
    
    try:
        fp = signature(func)
        func_properties = {"parameters": fp.parameters, "return_annotation": fp.return_annotation}
    except ValueError as e:
        if getattr(func, "funcs"):
            func_properties = {"parameters": {}, "return_annotation": None}
            for f in func.funcs.values():
                fp = signature(f)
                func_properties["parameters"].update(fp.parameters)
                if fp.return_annotation:
                    func_properties["return_annotation"] = fp.return_annotation
            print(func_properties)
        else:
            raise e

    if list(func_properties["parameters"].keys()) == ['root'] and getattr(func, "__call__"):
        fp = signature(func.__call__)
        func_properties = {"parameters": fp.parameters, "return_annotation": fp.return_annotation}

    arguments_list = list(func_properties["parameters"].items())
    arguments = {}
    for key, arg in arguments_list:
        
        if arg.name in ['self', 'cls']:
            continue
        
        arguments[arg.name] = {}
        
        if arg.annotation is not inspect._empty:
            arguments[arg.name].update({"type": arg.annotation})
            
        if arg.default is not inspect._empty:
            arguments[arg.name].update({"value": arg.default})
                        
    return {
        "arguments": arguments, 
        "returns": func_properties["return_annotation"],
        "generator": _get_generator(func_properties, method_root_type)
    }

def generate_code(body=None, variables=[], get_updated=False, **kwargs):

    if not body:
        body = kwargs

    body = val_to_list(body)

    updated = []

    code = []

    for operation in body:
        
        operation = prepare(operation)
        operation_code, operation_updated = _generate_code(operation, [*updated, *variables])
        updated.extend(operation_updated)
        code.append(operation_code)

    if get_updated:
        return "\n".join(code), one_list_to_val(updated)
    else:
        return "\n".join(code)
    
