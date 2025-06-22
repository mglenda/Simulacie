from random import randint
from typing import Callable, Any

class Routine():
    def __init__(self, func: Callable[..., Any], *params: tuple, **kwargs: dict[str, Any]):
        self.func = func
        self.params = params
        self.kwargs = kwargs

    def run(self):
        return self.func(*self.params,**self.kwargs)

class Action():
    routines: list[Routine]
    order_min: int #minimum amount of delay
    order_max: int #maximum amount of delay
    current_order: int
    initial_order: int
    def __init__(self,current_order: int = None,order_min: int = 1, order_max: int = 1, routines: list[Routine] = None):
        self.order_min = order_min
        self.order_max = order_max
        self.current_order = randint(order_min,order_max) if current_order is None else current_order
        self.routines = [] if routines is None else routines

        self.initial_order = self.current_order

    def change_order(self, order: int = None):
        self.current_order += randint(self.order_min,self.order_max) if order is None else order

    def add_routine(self, routine: Routine):
        self.routines.append(routine)

    def run(self):
        for r in self.routines:
            r.run()

    def reset(self):
        self.current_order = self.initial_order

class Queue():
    actions: list[Action]
    def __init__(self, actions: list[Action] = []):
        self.actions = actions

    def add(self, action: Action):
        self.actions.append(action)

    def remove(self, action: Action):
        self.actions.remove(action)

    def run_next(self):
        self.actions[0].run()
        self.actions[0].change_order()
        self.actions.sort(key=lambda action: action.current_order)

    def reset(self):
        for a in self.actions:
            a.reset()
        self.actions.sort(key=lambda action: action.current_order)
