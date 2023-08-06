#===============================================
__all__ = ["DelegateUnary", "DelegateTuple", "DelegateList", "EventData", "EventBase", "Dispatcher"]
#===============================================
import functools
from typing import Callable, List, Tuple


class DelegateUnary(object):
    "Fastest delegate, contains just one function to call"
    def __init__(self, function: Callable = None):
        self.slot: Callable = function
    
    def invoke(self, *args, **kwargs):
        "Invokes function or method inside"
        return self.slot(*args, **kwargs) if callable(self.slot) else None
    
    def __call__(self, *args, **kwargs):
        return self.invoke(*args, **kwargs)
    
    def __len__(self):
        return 1
    
    def add(self, function: Callable):
        self.slot = function
    
    def clear(self):
        self.slot = None
    
    def remove(self, function:Callable):
        if self.slot == function:
            self.clear()
    
    def merge(self, other = None):
        raise TypeError("Unable to merge unary delegates")
    
    def __add__(self, other):
        return self.add(other)
    
    def __sub__(self, other):
        return self.remove(other)


class DelegateTuple(object):
    def __init__(self, *functions: Callable):
        self.slots: Tuple[Callable] = tuple(functions)

    def invoke(self, *args, **kwargs):
        "Invokes functions or methods inside, returns last result. Slow on add/remove, fast on call"
        res = None
        for f in self.slots:
            if (not callable(f)):
                continue
            res = f(*args, **kwargs)
        return res
    
    def __call__(self, *args, **kwargs):
        return self.invoke(*args, **kwargs)
    
    def __len__(self):
        return len(self.slots)
    
    def add(self, function: Callable):
        self.slots = tuple(self.slots + Tuple[Callable((function, ))])
    
    def clear(self):
        self.slots = tuple()
    
    def remove(self, function: Callable):
        lst = list(self.slots)
        try:
            lst.remove(function)
        except ValueError:
            return
        self.slots = tuple(lst)
    
    def merge(self, other):
        self.slots = self.slots + other.slots
    
    def __add__(self, other):
        return self.add(other)

    def __sub__(self, other):
        return self.remove(other)


class DelegateList(object):
    def __init__(self, *functions: Callable):
        self.slots: List[Callable] = list(functions)

    def invoke(self, *args, **kwargs):
        "Invokes functions or methods inside, returns last result. Slow on call, fast on add/remove"
        res = None
        for f in self.slots:
            if (not callable(f)):
                continue
            res = f(*args, **kwargs)
        return res
    
    def __call__(self, *args, **kwargs):
        return self.invoke(*args, **kwargs)

    def __len__(self):
        return len(self.slots)
    
    def add(self, function: Callable):
        self.slots.append(function)
    
    def clear(self):
        self.slots.clear()
    
    def remove(self, function: Callable):
        try:
            self.slots.remove(function)
        except ValueError:
            return
        
    
    def merge(self, other):
        self.slots = self.slots + other.slots
    
    def __add__(self, other):
        return self.add(other)

    def __sub__(self, other):
        return self.remove(other)


class EventData(dict):
    def __init__(self, name:str, *args , **kwargs):
        self.name = name
        self.args = args
        for key, value in kwargs.items():
            self[key] = value
    
    # !!! only for unknown attributes
    def __getattr__(self, name):
        if self.__contains__(name):
            return self[name]
        return None


class EventBase(object):
    def initEvents(self):
        "Initalizes variable to contain events, just call once for object."
        if not hasattr(self, "subscriptions") or self.subscriptions == None:
            self.subscriptions: dict = dict()
        return self
    
    def registerNewEvent(self, name:str, *, delegateObject = None):
        if delegateObject == None:
            delegateObject = DelegateList()
        self.subscriptions[name] = delegateObject
        return self
    
    def registerNewEvents(self, *names: str, delegateObjectType=None):
        if delegateObjectType == None:
            delegateObjectType = DelegateList
        for event in names:
            self.registerNewEvent(event, delegateObject=delegateObjectType())
        return self
    
    def subscribeToEvent(self, name: str, function: Callable):
        if name in self.subscriptions:
            self.subscriptions[name].add(function)
        else:
            raise NameError(f"Unregistered event <{name}>")
        return self
    
    def unsubscribeToEvent(self, name: str, function: Callable):
        if name in self.subscriptions:
            self.subscriptions[name].remove(function)
        else:
            raise NameError(f"Unregistered event <{name}>")
        return self
    
    def clearSubscribersAndRegistrations(self):
        self.subscriptions = dict()
        return self
    
    def clearSubscribers(self):
        for key, value in self.subscriptions.items():
            value.clear()
        return self
    
    def notifySubscribers(self, name: str, *args, **kwargs):
        if name in self.subscriptions:
            return self.subscriptions[name].invoke(*args, **kwargs)
        else:
            raise NameError(f"Unregistered event <{name}>")
    
    def notifySubscribersWithData(self, data: EventData):
        data["sender"] = self
        if data.name in self.subscriptions:
            return self.subscriptions[data.name].invoke(data)
        else:
            raise NameError(f"Unregistered event <{data.name}>")
        
    def notifySubscribersWithDataAuto(self, name: str, *args, **kwargs):
        data = EventData(name, *args, **kwargs)
        data["sender"] = self
        if data.name in self.subscriptions:
            return self.subscriptions[data.name].invoke(data)
        else:
            raise NameError(f"Unregistered event <{data.name}>")


def Dispatcher(delegateObject = None):
    if delegateObject == None:
        delegateObject = DelegateList()
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            wrapper.subscribers.invoke()
            return func(*args, **kwargs)
        wrapper.subscribers = delegateObject
        def subscribe(func: Callable):
            wrapper.subscribers.add(func)
            return func
        wrapper.subscribe = subscribe
        def unsubscribe(func: Callable):
            wrapper.subscribers.remove(func)
            return func
        wrapper.unsubscribe = unsubscribe
        return wrapper
    return decorator
    
