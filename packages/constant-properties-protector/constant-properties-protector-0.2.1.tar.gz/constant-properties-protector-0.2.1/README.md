# Constant Properties Protector Package

With the help of this module, you can protect some of properties in a class. Protecting means avoiding to change them but keep them publicly available.

```python
from constant_properties_protector import CPP

class A:
    def __init__(self):
        CPP.protect(self, 'initialized_protected')
        CPP.protect(self, 'uninitialized_protected')
        self._initialized_protected = 12
        
a = A()
print(a.initialized_protected)
# >>> 12
a.t = 2
print(a.t)
# >>> 2
a.initialized_protected += 1
# Exception: Can not modify constant property: initialized_protected
a.uninitialized_protected = 10
# Exception: Can not modify constant property: uninitialized_protected

class B(A):
    def __init__(self):
        super().__init__()
        CPP.protect(self, 'new_protected_value')
        self._new_protected_value = 26

b = B()
print(b.new_protected_value)
# >>> 26
b.new_protected_value += 2
# Exception: Can not modify constant property: new_protected_value
```

NOTE: 

* There is no need to inherit from CPP.
* Use `_` first of the protected property name to get fully access to it.
* Use `protect` function to add to protected properties.
* CPP will defaine python properties for your class. So it affects on the class not the instance. DON'T use CPP to protect a property in runtime. Use it to define protected values for all instanses of a class.

## Installation
```pip install constant-properties-protector```