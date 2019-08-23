# import os
import sys
import time 
import signal
import threading
import curses # key

from PCA9685 import PCA9685

def Turning():
    print("Turning x and y")
    # servo = PCA9685()
    # servo.setPWMFreq(50)
    
    
    # Servo.setRotationAngle(0, 20)
    
# def Turn_y():
    # pwm.exit_PCA9685()
    # GPIO.cleanup()
    # print("Turn_y")
    # Servo.setRotationAngle(1, 20)
    
def Get_Light():
    # pwm.exit_PCA9685()
    # GPIO.cleanup()
    print("\nProgram end")
    # sys.exit()
    
# def timerfunc():  
    # global t        #Notice: use global variable!
    # t = threading.Timer(0.02, timerfunc)
    # t.start()

try:
    # signal.signal(signal.SIGINT, exit)
    # signal.signal(signal.SIGTERM, f)
    # t = threading.Timer(0.02, timerfunc)
    # t.setDaemon(True)
    # t.start()

    # print 'server is running....'  
    # server = SocketServer.ThreadingTCPServer(addr,Servers)
    # time.sleep(0.1) 
    # tx = threading.Thread(target = Turning) 
    # tx.setDaemon(True)
    # tx.start()
    
    screen=curses.initscr()
    curses.noecho()
    curses.cbreak()
    screen.keypad(1)
    screen.nodelay(0)  
    # istr = input('please Enter: ')
    
    while(True):
        char=screen.getch()
        print("\r\nget str = \r\n", char)
    # while True:


except:
    # pwm.exit_PCA9685()
    #GPIO.cleanup()
    print("\nProgram end")
    curses.nocbreak()
    screen.keypad(0)
    curses.echo()
    curses.endwin()
    exit()
