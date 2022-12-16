import RPi.GPIO as gpio

import serial

import time

import random

from flask import Flask, render_template, request, jsonify


import smtplib


RS =18

EN =23

D4 =24

D5 =25

D6 =8

D7 =7


DT =27

SCK=17

led=22

buz=5


m1=19

m2=26


HIGH=1

LOW=0


sample=0

val=0


flag=0


gpio.setwarnings(False)

gpio.setmode(gpio.BCM)

gpio.setup(RS, gpio.OUT)

gpio.setup(EN, gpio.OUT)

gpio.setup(D4, gpio.OUT)

gpio.setup(D5, gpio.OUT)

gpio.setup(D6, gpio.OUT)

gpio.setup(D7, gpio.OUT)

gpio.setup(led, gpio.OUT)

gpio.setup(buz, gpio.OUT)

gpio.setup(m1, gpio.OUT)

gpio.setup(m2, gpio.OUT)

gpio.setup(SCK, gpio.OUT)

gpio.output(led , 0)

gpio.output(buz , 0)

gpio.output(m1 , 0)

gpio.output(m2 , 0)



app = Flask(__name__)

a=1

@app.route("/")

def index():

 return render_template('web.html')

  

@app.route('/show_weight')

def show_weight():

    count= readCount()

    w=0

    w=(count-sample)/106

    print w,"g"

    setCursor(0,0)

    data=str(w);

    lcdprint(data)

    lcdprint("g   ")

    global flag

    if w>300:

      if flag == 0:

        lcdclear()

        lcdprint("Container Is Full")

        setCursor(0,1);

        lcdprint("Sending Email")

        server = smtplib.SMTP('smtp.gmail.com', 587)

        server.starttls()

        server.login("saddam4201@gmail.com", "password")

        msg = "Smart Container Alert.... Container Full"

        server.sendmail("robo.satp@gmail.com", "satish.pawale687@gmail.com", msg)

        server.quit()

        lcdclear()

        lcdprint("Email Sent")

        flag=1;

        lcdclear()

    elif w<300:

      if flag==1:

        lcdclear()

        lcdprint("Container Empty")

        setCursor(0,1);

        lcdprint("Sending Email")

        server = smtplib.SMTP('smtp.gmail.com', 587)

        server.starttls()

        server.login("robo.satp@gmail.com", "Jaibalaji12#")

        msg = "Smart Container Alert.... Container is Empty"

        server.sendmail("robo.satp@gmail.com", "satish.pawale687@gmail.com", msg)

        server.quit()

        lcdclear()

        lcdprint("Email Sent")

        flag=0;

        lcdclear()


    return jsonify(result=w)


def begin():

  lcdcmd(0x33) 

  lcdcmd(0x32) 

  lcdcmd(0x06)

  lcdcmd(0x0C) 

  lcdcmd(0x28) 

  lcdcmd(0x01) 

  time.sleep(0.0005)

 

def lcdcmd(ch): 

  gpio.output(RS, 0)

  gpio.output(D4, 0)

  gpio.output(D5, 0)

  gpio.output(D6, 0)

  gpio.output(D7, 0)

  if ch&0x10==0x10:

    gpio.output(D4, 1)

  if ch&0x20==0x20:

    gpio.output(D5, 1)

  if ch&0x40==0x40:

    gpio.output(D6, 1)

  if ch&0x80==0x80:

    gpio.output(D7, 1)

  gpio.output(EN, 1)

  time.sleep(0.005)

  gpio.output(EN, 0)


  # Low bits

  gpio.output(D4, 0)

  gpio.output(D5, 0)

  gpio.output(D6, 0)

  gpio.output(D7, 0)

  if ch&0x01==0x01:

    gpio.output(D4, 1)

  if ch&0x02==0x02:

    gpio.output(D5, 1)

  if ch&0x04==0x04:

    gpio.output(D6, 1)

  if ch&0x08==0x08:

    gpio.output(D7, 1)

  gpio.output(EN, 1)

  time.sleep(0.005)

  gpio.output(EN, 0)

  

def lcdwrite(ch): 

  gpio.output(RS, 1)

  gpio.output(D4, 0)

  gpio.output(D5, 0)

  gpio.output(D6, 0)

  gpio.output(D7, 0)

  if ch&0x10==0x10:

    gpio.output(D4, 1)

  if ch&0x20==0x20:

    gpio.output(D5, 1)

  if ch&0x40==0x40:

    gpio.output(D6, 1)

  if ch&0x80==0x80:

    gpio.output(D7, 1)

  gpio.output(EN, 1)

  time.sleep(0.005)

  gpio.output(EN, 0)


  # Low bits

  gpio.output(D4, 0)

  gpio.output(D5, 0)

  gpio.output(D6, 0)

  gpio.output(D7, 0)

  if ch&0x01==0x01:

    gpio.output(D4, 1)

  if ch&0x02==0x02:

    gpio.output(D5, 1)

  if ch&0x04==0x04:

    gpio.output(D6, 1)

  if ch&0x08==0x08:

    gpio.output(D7, 1)

  gpio.output(EN, 1)

  time.sleep(0.005)

  gpio.output(EN, 0)


def lcdclear():

  lcdcmd(0x01)

 

def lcdprint(Str):

  l=0;

  l=len(Str)

  for i in range(l):

    lcdwrite(ord(Str[i]))

    

def setCursor(x,y):

    if y == 0:

        n=128+x

    elif y == 1:

        n=192+x

    lcdcmd(n)


def readCount():

  i=0

  Count=0

 # print Count

 # time.sleep(0.001)

  gpio.setup(DT, gpio.OUT)

  gpio.output(DT,1)

  gpio.output(SCK,0)

  gpio.setup(DT, gpio.IN)


  while gpio.input(DT) == 1:

      i=0

  for i in range(24):

        gpio.output(SCK,1)

        Count=Count<<1


        gpio.output(SCK,0)

        #time.sleep(0.001)

        if gpio.input(DT) == 0: 

            Count=Count+1

            #print Count

        

  gpio.output(SCK,1)

  Count=Count^0x800000

  #time.sleep(0.001)

  gpio.output(SCK,0)

  return Count 


print "Hello"

begin()

lcdcmd(0x01)

lcdprint("Smart Container   ")

lcdcmd(0xc0)

lcdprint("    Using RPI     ")

time.sleep(3)

lcdcmd(0x01)

lcdprint("Circuit Digest")

lcdcmd(0xc0)

lcdprint("Welcomes You")

time.sleep(3)

sample= readCount()

lcdclear()

while 1:

  print "Start"  

  if __name__ == "__main__":

   app.run(host='0.0.0.0',port=5010)