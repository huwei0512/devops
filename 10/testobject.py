#encoding:utf-8

class Animal(object):
    def __init__(self,name,age =10):
        self.name = name
        self.age = age

    def say(self):
        print self.name + " say"

    def run(self):
        print self.name + " run"

class Dog(Animal):
    def __init__(self,name,age,variety):
        super(Dog,self).__init__(name,age)  #重写方法并访问父类的属性
        self.variety = variety
      
    def say(self):
        super(Dog,self).say()  #调用父类的方法
        print self.name,self.variety +":"+ 'wangcai'


    def get_variety(self):
        return self.variety



