import importlib.util
import sys
from auxml.parser import el_location_info

class PatchupModule():    
    def __init__(self, module_path):
        self.mod_path = module_path
        self.mod = self.load_module(module_path)

    def run(self, tree, el):
        func_name = el.get("func")
        if func_name is None:
            msg = f'''
            patchup element at {el_location_info(el)}
            
            patchup element must have a `func` attribute that
            specifies patch function, something like:

            <patchup func="my_function"/>
            
            for more information see docs 
            '''
            raise Exception(msg)

        if hasattr(self.mod, func_name):
            f = getattr(self.mod, func_name)
            # log this instead of stdout.
            print(f"processing patchup element with function: {func_name}" + el_location_info(el))
            return f(tree, el)
        else:
            msg = f'''
            patchup element at {el_location_info(el)}
            patchup function with name : `{func_name}` not found in
            patchup module located at  : `{self.mod_path}'

            Please check your paths and that the function `{func_name}` actually exists.
            '''
            raise Exception(msg)
        
    def load_module(self, module_path):
        print(f"loading python module {module_path}")
        module_name = "patchup_module"
        spec = importlib.util.spec_from_file_location(module_name, module_path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)
        return module
