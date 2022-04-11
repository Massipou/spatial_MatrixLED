# import main Flask class and request object
from flask import Flask, request, render_template
import multiprocessing
from colorsender import *

# Initianize color sender thread 
rseuil = 15
gseuil = 14
bseuil = 15
zoom = 1
thread_colorsender = threadColorSender(1, "Thread-ColorSender", rseuil, gseuil, bseuil)

def template(number):
    thread_colorsender.data = "template"

    if number == 1:
        thread_colorsender.zoom = 3
        thread_colorsender.red = 255
        thread_colorsender.green = 0
        thread_colorsender.blue = 4

    elif number == 2:
        thread_colorsender.zoom = 1
        thread_colorsender.red = 255
        thread_colorsender.green = 0
        thread_colorsender.blue = 4

    elif number == 3:
        thread_colorsender.zoom = 5
        thread_colorsender.red = 255
        thread_colorsender.green = 0
        thread_colorsender.blue = 4

    elif number == 4:
        thread_colorsender.zoom = 3
        thread_colorsender.red = 200
        thread_colorsender.green = 0
        thread_colorsender.blue = 250

    elif number == 5:
        thread_colorsender.zoom = 1
        thread_colorsender.red = 200
        thread_colorsender.green = 0
        thread_colorsender.blue = 250

    elif number == 6:
        thread_colorsender.zoom = 5
        thread_colorsender.red = 200
        thread_colorsender.green = 0
        thread_colorsender.blue = 250

    elif number == 7:
        thread_colorsender.zoom = 3
        thread_colorsender.red = 0
        thread_colorsender.green = 0
        thread_colorsender.blue = 250

    elif number == 8:
        thread_colorsender.zoom = 1
        thread_colorsender.red = 0
        thread_colorsender.green = 0
        thread_colorsender.blue = 250

    elif number == 9:
        thread_colorsender.zoom = 5
        thread_colorsender.red = 0
        thread_colorsender.green = 0
        thread_colorsender.blue = 250

    elif number == 10:
        thread_colorsender.zoom = 4
        thread_colorsender.red = 255
        thread_colorsender.green = 0
        thread_colorsender.blue = 4

    elif number == 11:
        thread_colorsender.zoom = 2
        thread_colorsender.red = 255
        thread_colorsender.green = 0
        thread_colorsender.blue = 4

    elif number == 12:
        thread_colorsender.zoom = 11
        thread_colorsender.red = 255
        thread_colorsender.green = 0
        thread_colorsender.blue = 4

    elif number == 13:
        thread_colorsender.zoom = 4
        thread_colorsender.red = 200
        thread_colorsender.green = 0
        thread_colorsender.blue = 250

    elif number == 14:
        thread_colorsender.zoom = 2
        thread_colorsender.red = 200
        thread_colorsender.green = 0
        thread_colorsender.blue = 250

    elif number == 15:
        thread_colorsender.zoom = 11
        thread_colorsender.red = 200
        thread_colorsender.green = 0
        thread_colorsender.blue = 250

    elif number == 16:
        thread_colorsender.zoom = 4
        thread_colorsender.red = 0
        thread_colorsender.green = 0
        thread_colorsender.blue = 250

    elif number == 17:
        thread_colorsender.zoom = 2
        thread_colorsender.red = 0
        thread_colorsender.green = 0
        thread_colorsender.blue = 250

    elif number == 18:
        thread_colorsender.zoom = 11
        thread_colorsender.red = 0
        thread_colorsender.green = 0
        thread_colorsender.blue = 250





class globales:
    effect = "0"
    effect_option = "0"


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
        elif request.form.get("Template18"):
            template(18)


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

    return render_template('index.html', status=start_stop, R=thread_colorsender.r, G=thread_colorsender.g, B=thread_colorsender.b, RED=thread_colorsender.red, GREEN=thread_colorsender.green, BLUE=thread_colorsender.blue, EO=globales.effect_option, EFFECT=globales.effect)


if __name__ == '__main__':
    # run app in debug mode on port 5000
    app.run(debug=True, port=5000)
