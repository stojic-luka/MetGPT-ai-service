import os, importlib

class ModuleManager():
    def __init__(self):
        self.path_prefix = "modules"
        self.modules = {}

        for filename in os.listdir(self.path_prefix):
            if filename.endswith('.py'):
                module_name = f"{self.path_prefix}.{filename[:-3]}"
                module = importlib.import_module(module_name)
                if not hasattr(module, "setup"):
                    raise AttributeError(f"Setup function not present in module {module_name}")

                self.modules[filename[:-3]] = getattr(module, "setup")()

    def run_from_module(self, module_name):
        if module_name not in self.modules:
            raise ValueError(f"Module {module_name} not available.")

        return self.modules[module_name].run()