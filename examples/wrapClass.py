from inspect import getmembers, ismethod
from string import capitalize
import sys
from simpleargs import argv

def decorateClass(cls):
    '''
    This method wraps around a class and extracts properties from it.
    These properties are then set if they are found in the arguments passed it.
    It also generates a help doc from the docstring of each function.
    '''
    #Use dictionary comprehension to make names lowercase
    argDic = {name.lower():value for name, value in argv.__dict__['_options'].items()}

    #another dictionary comprehension that finds all set methods
    setMethods = {name[3:].lower():func for name, func in getmembers(cls, ismethod)
                  if name.startswith("set")}
    #each method object has a docstring, this can be used to make a man page.
    helpDoc = cls.__doc__ + "\nArguments:\n\t" + "\n\t".join(method.__doc__ for method in setMethods.values())
    if "help" in argDic.keys():
        print helpDoc
        sys.exit(0)
    try:
        for arg, value in argDic.items():
            #setmethod = "set"+capitalize(key)
            if arg in setMethods:
                setMethods[arg](value)
            else:
                print "Argument {} not defined".format(arg)
                sys.exit(-1)
    except SystemExit:
        print "Try: "+cls.__name__ +" --help"
        sys.exit(-1)
    except:
        print "Try: "+cls.__name__ +" --help"
        print   "Unexpected error:", sys.exc_info()[0]
        sys.exit(-1)
    return cls

@decorateClass
class Foo(object):
    '''This is the Foo doc'''
    name = "Willem"
    age = 2
    height = 5

    def __init__(self):
        print "name: ", Foo.name
        print "age: ", Foo.age

    @classmethod
    def setName(cls, name):
        '''--name name'''
        cls.name = name

    @classmethod
    def setAge(cls, age):
        '''--age age'''
        cls.age = age

    @classmethod
    def setHeight(cls, height):
        '''--height height'''
        cls.height = height

F = Foo()
