import threading
import time
from datetime import datetime

class Product:
    def __init__(self):
        pass

class Device:
    product: Product
    name: str
    time_a: int # cas ktory zariadenie potrebuje na pracu
    time_b: int # cas ktory zariadenie potrebuje po praci na navrat do pripraveneho stavu
    ready_to_work: bool
    ready_to_deliver: bool
    def __init__(self,name: str, time_a: int = 0, time_b: int = 0):
        self.name = name
        self.product = None
        self.time_a = time_a
        self.time_b = time_b
        self.ready_to_work = True
        self.ready_to_deliver = False

    def is_empty(self) -> bool:
        return self.product is None
    
    def log(self, msg: str):
        now = datetime.now()
        print(f"\n{now.strftime("%H:%M:%S")}--> {self.name}: {msg}",end="")
    
    def work(self, product: Product) -> bool:
        if product is None:
            self.log("Work Command Failed -> No Product Provided")
            return False
        if not self.ready_to_work:
            self.log("Work Command Failed -> Work In Progress")
            return False
        if not self.is_empty():
            self.log("Work Command Failed -> Already Has Product")
            return False
        
        self.product = product
        self.log("Work Command Success")
        def process():
            self.log("Work Started")
            self.ready_to_work = False
            time.sleep(self.time_a)
            self.ready_to_deliver = True
            self.log("Work Finished -> Ready To Deliver\n")

        thread = threading.Thread(target=process)
        thread.start()

        return True
    
    def deliver(self) -> Product:
        if self.is_empty():
            self.log("Delivery Command Failed -> No Product")
            return None
        if not self.ready_to_deliver:
            self.log("Delivery Command Failed -> Work In Progress")
            return None
        
        self.log("Delivery Command Success")
        def process():
            self.log("Default State Initiated")
            self.ready_to_deliver = False
            time.sleep(self.time_b)
            self.ready_to_work = True
            self.log("Default State Success\n")

        thread = threading.Thread(target=process)
        thread.start()
        
        product: Product = self.product
        self.product = None
        return product

class Workline:
    devices: list[Device]

    def __init__(self, devices: list[Device] = None):
        self.devices = devices if devices is not None else []

    def work_command(self, device_id: int):
        try:
            product: Product = None
            if device_id == 0:
                print(f'Command Detected: Load New Product')
                self.devices[0].work(Product())
            else:
                print(f'Command Detected: Work Device [{self.devices[device_id].name}]')
                product = self.devices[device_id - 1].deliver()
                if product is not None:
                    self.devices[device_id].work(product)

        except IndexError:
            # ak bol providnuty nespravny device_id vyhod chybu
            print(f"Work Failed : Device Identification Failed (Device ID = [{device_id}])")

    def receive_product(self):
        print('Command Detected: Deliver Product')
        if self.devices[-1].deliver() is not None:
            print(f"Delivery Success: {self.devices[-1].name} has delivered new product.")
