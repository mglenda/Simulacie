from evenlib import Device,Workline,threading,Product,time
import os

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

# Vytvorenie linky, naplnenie Device objektami, na poradi zalezi
# time_a = cas ktory zariadenie potrebuje na pracu (default = 0)
# time_b = cas ktory zariadenie potrebuje po praci na navrat do pripraveneho stavu (default = 0)
WORKLINE = Workline([
    Device(name="Dopravnik 1",time_a = 1.0)
    ,Device(name="Podavac 1",time_a = 1.0,time_b=1.0) 
    ,Device(name="Obrabanie 1",time_a = 5.0)
    ,Device(name="Podavac 2",time_a = 1.0,time_b=1.0)
    ,Device(name="Obrabanie 2",time_a = 5.0)
    ,Device(name="Podavac 3",time_a = 1.0,time_b=1.0)
    ,Device(name="Dopravnik 2",time_a = 1.0)
])

clear_console()
print("Workline created")

# naparovanie prikazov k spusteniu jednotlivych zariadeni
# vazba "prikaz" : "id_zariadenia"
# id zariadenia je vlastne array id, pridelene podla poradia v ktorom boli zariadenia pridane do WORKLINE na zaciatku
work_commands = {
    "i": 0
    ,"a": 1
    ,"b": 2
    ,"c": 3
    ,"d": 4
    ,"e": 5
    ,"f": 6
}


RUNNING = True
AUTO_MODE = False

def auto_process():
    while(AUTO_MODE):
        for i,d in enumerate(WORKLINE.devices):
            if d.ready_to_work:
                if i == 0:
                    # pre prve zariadenie na linke sa neodkazujeme na zariadenie predchadzajuce, vytvara sa novy produkt
                    d.work(product=Product())
                elif WORKLINE.devices[i-1].ready_to_deliver:
                    # pre ostatne zariadenia zistujem ci ma predchadzajuce zariadenie pripraveny produkt na odovzadnie
                    # ak ano produkt odovzdam a zacinam na nom pracovat s aktualnym zariadenim
                    p: Product = WORKLINE.devices[i-1].deliver()
                    d.work(p)
            time.sleep(0.1)
                

while(RUNNING):
    print("")
    command = input("")
    if not AUTO_MODE:
        if command in work_commands:
            WORKLINE.work_command(work_commands[command])
    if command == "t":
        WORKLINE.receive_product()
    if command == "exit":
        RUNNING = False
    if command == "auto" and not AUTO_MODE:
        AUTO_MODE = True
        threading.Thread(target=auto_process).start()
    if command == "manual" and AUTO_MODE:
        AUTO_MODE = False
