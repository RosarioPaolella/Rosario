from guizero import *
from gpiozero import LEDBoard

leds = LEDBoard(17,18,27,23,22,24,25,2,3,16,active_high=False)

def ConvertiIntero(s):
    try:
        return int(s)
    except ValueError:
        return 0

def ConvertiNumero():
    binary = []
    for i in range(10):
        binary.append(0)

    print ("Init bit array:" + str(binary))

    #convert number in binary string
    number=ConvertiIntero(text_box.value)
    i=len(binary)-1

    while number>0 :
        bit=number%2
        binary[i]=bit
        number=number//2
        i=i-1

    print ("Decimal is "+ text_box.value + " Binary is :" + str(binary))


    for i in range (len(binary)-1,-1,-1):
        if binary[i]==1  :
            leds.on(i)
        else : 
            leds.off (i)




#GUI WINDOW ###########################################
app = App(title="Binary Converter")



title_box = Box(app, width="fill", align="top",height=100)
main_box = Box(app, width="fill", align="top",height="fill")
command_box = Box(app, width="fill", align="bottom")

title=Text(title_box, text="\n\nConvertirore Binario con LedBoard\n",size=16,width="fill", bg="#0affa0")
text = Text(main_box, text="\n\n\nInserire il numero da convertire",size=12)
text_box = TextBox(main_box, text="",width=50)
button = PushButton(command_box, text="Converti Numero",command=ConvertiNumero)
Text(command_box, text="\n")

app.display()