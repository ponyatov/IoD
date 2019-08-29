# Internet of Data implementation /Python3/

import os,sys

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
    
    # dump

    def __repr__(self): return self.dump()
    def dump(self,depth=0,prefix=''):
        tree = self._pad(depth) + self.head(prefix)
        if not depth: Frame._dumped = []
        if self in Frame._dumped: return tree + ' _/'
        else: Frame._dumped.append(self)
        for i in self.slot:
            tree += self.slot[i].dump(depth+1,prefix='%s = '%i)
        for j in self.nest:
            tree += j.dump(depth+1)
        return tree
    def head(self,prefix=''):
        return '%s<%s:%s> @%.x' % (prefix,self.type,self._val(),id(self))
    def _pad(self,depth):
        return '\n' + '\t' * depth
    def _val(self):
        return str(self.val)

    # operators

    def __getitem__(self,key):
        return self.slot[key]
    def __setitem__(self,key,that):
        self.slot[key] = that ; return self
    def __lshift__(self,that):
        if callable(that): return self << Cmd(that) # wrap py fn
        self[that.val] = that ; return self
    def __floordiv__(self,that):
        self.nest.append(that) ; return self

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

class Cmd(Active):
    def __init__(self,F):
        Active.__init__(self,F.__name__)
        self.fn = F
    def eval(self,ctx):
        self.fn(ctx)

class Seq(Active,Vector): pass

class Doc(Frame): pass
class Color(Doc): pass
class Font(Doc): pass

class IO(Frame): pass
class Net(IO): pass
class Ip(Net): pass
class Port(Net): pass
class Web(Net):
    def __init__(self,V):
        Net.__init__(self,V)
        self['ip'] = Ip('127.0.0.1')
        self['port'] = Port(8888)
        self['back'] = Color('black')
        self['fore'] = Color('lightgreen')
        self['font'] = Font('monospace')
        self['font']['size'] = Symbol('3mm')
    def eval(self,ctx):
        flask = __import__('flask')
        app = flask.Flask(self.val)
        app.config['SECRET_KEY'] = os.urandom(32)

        wtf     = __import__('flask_wtf')
        wtforms = __import__('wtforms')
        class CLI(wtf.FlaskForm):
            pad = wtforms.TextAreaField('pad',default='# put your commands here')
            go  = wtforms.SubmitField('GO')

        @app.route('/',methods=['GET','POST'])
        def index():
            form = CLI()
            if form.validate_on_submit():
                ctx // String(str(form.pad.data))
            return flask.render_template('index.html',ctx=ctx,web=self,form=form)

        @app.route('/<path>.png')
        def png(path):
            return app.send_static_file('%s.png' % path)

        app.run(host=self['ip'].val,port=self['port'].val,debug=True)
