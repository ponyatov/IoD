# Internet of Data implementation /Python3/

class Frame:
    def __init__(self,V):
        # type/class tag (required for PLY parser library)
        self.type = self.__class__.__name__.lower()
        # scalar value
        self.val  = V
        # slots = attributes = string-keyed associative array
        self.slot = {}
        # nested elements = vector = stack = queue
        self.nest = []

class Primitive(Frame):
    def eval(self,ctx): ctx // self

class String(Primitive): pass
class Symbol(Primitive): pass
class Number(Primitive): pass

class Container(Frame): pass

class Vector(Container): pass
class Stack(Container): pass
class Dict(Container): pass
class Queue(Container): pass

class Active(Frame): pass
    
class VM(Active): pass
class Cmd(Active): pass
class Seq(Active,Vector): pass
