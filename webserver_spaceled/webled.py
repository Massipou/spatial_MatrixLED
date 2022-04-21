# import main Flask class and request object
from flask import Flask, request, render_template
import multiprocessing
import threading
import time
from colorsender import *
                                   
# Create and initialize automatic thread
class threadAutomatic (threading.Thread):
    def __init__(self, threadID, name, mode, step_time):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.mode = mode
        self.step_time = step_time
        self.start_time = time.time()
   
    def run(self):
        step = 0
        steps_number = 0
        while True:
            if self.mode == 1:
                steps_number = 15
            
            now = time.time() - self.start_time
            
            if now >= self.step_time:
                self.start_time = time.time()
                step = step + 1
                
                if step > steps_number:
                    step = 1
                
                if self.mode == 1:
                    
                    if step == 1:
                        color(1) # RED
                        template(1)
                    elif step == 2:
                        template(6) # L
                    elif step == 3:
                        template(10) # M-SMOUTH
                    elif step == 4:
                        color(4)    # PURPLE
                        template(15) # BR SMOUTH
                    elif step == 5:
                        #color(3)    # ULTRA SPEED
                        template(17) #BB
                    elif step == 6:
                        template(2) # 2 - SPEED
                    elif step == 7:
                        template(11) # 6 - M-SMOUTH
                    elif step == 8:
                        template(4)# 6 - ACID
                    elif step == 9:
                        color(5)    #ORANGE
                        template(8) #LG
                    elif step == 10:
                        template(11) #MR
                    elif step == 11:
                        template(15) #BR
                    elif step == 12:
                        color(6)    #Cyan
                        template(16) #BG
                    elif step == 13:
                        template(15)  #BB
                    elif step == 14:
                        template(17) #BB
                        thread_colorsender.data = "skip"
                    elif step == 15:
                        template(5) #NO EFFECT
                        
            
        
        
                
                
mode = 0
step_time = 5 # second
thread_automatic = threadAutomatic(2, "thread-automatic", mode, step_time)

# Initianize color sender thread 
rseuil = 15
gseuil = 14
bseuil = 15
zoom = 1
thread_colorsender = threadColorSender(1, "Thread-ColorSender", rseuil, gseuil, bseuil)



def template(number):
    thread_colorsender.data = "template"

    if number <= 17:
        thread_colorsender.zoom = number
        
def color(number):
    if number == 1:
        thread_colorsender.red = 255
        thread_colorsender.green = 0
        thread_colorsender.blue = 0
    elif number == 2:
        thread_colorsender.red = 0
        thread_colorsender.green = 255
        thread_colorsender.blue = 0
    elif number == 3:
        thread_colorsender.red = 0
        thread_colorsender.green = 0
        thread_colorsender.blue = 255
    elif number == 4:
        thread_colorsender.red = 200
        thread_colorsender.green = 0
        thread_colorsender.blue = 250
    elif number == 5:
        thread_colorsender.red = 200
        thread_colorsender.green = 70
        thread_colorsender.blue = 0    
    elif number == 6:
        thread_colorsender.red = 0
        thread_colorsender.green = 90
        thread_colorsender.blue = 200    



class globales:
    effect = "0"
    effect_option = "0"
    auto = "0"


# create the Flask app
app = Flask(__name__)
start_stop = False

@app.route('/', methods=['GET', 'POST'])
def start_stop():
    global start_stop
    global effect_option
    # global rseuil
    # global gseuil
    # global bseuil

    # handle the POST request
    if request.method == 'POST':
        g = globales
        start_stop = request.form.get('start_stop')
        zoom = request.form.get("Zoom")
        
        
        g.auto = request.form.get('Automatic')
        if not g.auto is None:
            print (g.auto)
            if g.auto == "1":
                thread_automatic.start()
                thread_automatic.mode = 1
            elif g.auto == 0:
                thread_automatic.stop()

        if not request.form.get("Effect") is None: g.effect = request.form.get("Effect")
        if not request.form.get("EO") is None: g.effect_option = request.form.get("EO")
        print (g.effect)

        #if g.effect_option is None: g.effect_option = globales.effect_option

        rseuil = request.form.get('R')
        gseuil = request.form.get('G')
        bseuil = request.form.get('B')

        if rseuil is None: rseuil = thread_colorsender.r
        if gseuil is None: gseuil = thread_colorsender.g
        if bseuil is None: bseuil = thread_colorsender.b

        thread_colorsender.r = float(rseuil)
        thread_colorsender.g = float(gseuil)
        thread_colorsender.b = float(bseuil)

        red = request.form.get('RED')
        green = request.form.get('GREEN')
        blue = request.form.get('BLUE')

        if red is None: red = thread_colorsender.red
        if green is None: green = thread_colorsender.green
        if blue is None: blue = thread_colorsender.blue

        thread_colorsender.red = int(red)
        thread_colorsender.green = int(green)
        thread_colorsender.blue = int(blue)

        if request.form.get("Skip"):
            thread_colorsender.data = "skip"


        if request.form.get("Template1"):
            template(1)
        elif request.form.get("Template2"):
            template(2)
        elif request.form.get("Template3"):
            template(3)
        elif request.form.get("Template4"):
            template(4)
        elif request.form.get("Template5"):
            template(5)
        elif request.form.get("Template6"):
            template(6)
        elif request.form.get("Template7"):
            template(7)
        elif request.form.get("Template8"):
            template(8)
        elif request.form.get("Template9"):
            template(9)
        elif request.form.get("Template10"):
            template(10)
        elif request.form.get("Template11"):
            template(11)
        elif request.form.get("Template12"):
            template(12)
        elif request.form.get("Template13"):
            template(13)
        elif request.form.get("Template14"):
            template(14)
        elif request.form.get("Template15"):
            template(15)
        elif request.form.get("Template16"):
            template(16)
        elif request.form.get("Template17"):
            template(17)

        if request.form.get("Color1"):
            color(1)
        elif request.form.get("Color2"):
            color(2)
        elif request.form.get("Color3"):
            color(3)
        elif request.form.get("Color4"):
            color(4)
        elif request.form.get("Color5"):
            color(5)


        if zoom:
            print ("zoom")
            thread_colorsender.zoom = int(zoom)
            thread_colorsender.data = "zoom"

        if g.effect == "acid":
            print ("acid")
            thread_colorsender.data = "acid"
        elif int(g.effect) >= 1:
            thread_colorsender.zoom = float(g.effect_option)
            thread_colorsender.data = g.effect


        if start_stop == "start": thread_colorsender.start()
        elif start_stop == "stop": thread_colorsender.stop()
        

    return render_template('index.html', status=start_stop, R=thread_colorsender.r, G=thread_colorsender.g, B=thread_colorsender.b, RED=thread_colorsender.red, GREEN=thread_colorsender.green, BLUE=thread_colorsender.blue, EO=globales.effect_option, EFFECT=globales.effect)


if __name__ == '__main__':
    # run app in debug mode on port 5000
    app.run(debug=True, port=5000)
