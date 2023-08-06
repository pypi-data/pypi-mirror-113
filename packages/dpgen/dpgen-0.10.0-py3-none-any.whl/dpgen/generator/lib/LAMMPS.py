from abc import ABC,abstractmethod
from Task import Task

# it is an abstract class
class LAMMPS(Task):
    @abstractmethod
    def __init__ (self, 
                  paramters, 
                  path_to_poscar) :
        pass

    @abstractmethod
    def make_potential_files(self, 
                             output_dir):
        pass

    @abstractmethod
    def make_input_file(self,
                        output_dir, 
                        task_type, 
                        task_param):
        pass

    @abstractmethod
    def post (self):
        pass
