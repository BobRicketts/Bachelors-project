#functions.py

from psychopy import core, monitors, visual, event, gui
from random import uniform, shuffle


# Make list of possible stimuli for implicit experiment
def makeStimList():
    stims = []
    i = 0
    for finger in ["index", "middle"]:
        for number in [1,2]:
            for mirrored in [False, True]:
                i += 1
                index = str(i) if i >= 10 else str("0"+str(i))
                congruency = True if (finger == "index" and number == 1) or (finger == "middle" and number == 2) else False
                dicName = str(index+finger+"-"+str(number))
                dicName += "-mir" if mirrored else ""
                fileName = "hands/" + dicName + ".jpg"
                newDic = {
            		"finger"            : finger,
            		"number"            : number,
            		"correct response"  : "x" if finger == "index" else "z",
            		"finger congruency" : congruency,
            		"spatial congruency": congruency if mirrored else not congruency,
                    "mirrored"          : mirrored,
            		"img"               : fileName,
                    "neutralImg"        : "hands/numberless-mir.jpg" if mirrored else "hands/numberless.jpg",
                    "name"              : dicName
            	}
                stims.append(newDic)

    return stims

def makeStimListExplicit():
    stims = []
    i = 8
    for finger in ["index", "middle"]:
        for mirrored in [False, True]:
            i += 1
            index = str(i) if i >= 10 else str("0"+str(i))
            dicName = str(index+finger+"-"+"0")
            dicName += "-mir" if mirrored else ""
            fileName = "hands/" + dicName + ".jpg"
            newDic = {
        		"finger"            : finger,
        		"correct response"  : "x" if finger == "index" else "z",
        		"spatial congruency": mirrored,
                "mirrored"          : mirrored,
        		"img"               : fileName,
                "neutralImg"        : "hands/numberless-mir.jpg" if mirrored else "hands/numberless.jpg",
                "name"              : dicName
        	}
            stims.append(newDic)

    return stims


def makeStimListExecutive():
    stims = []
    # i is a counter for cycling through all possible stimuli. i = [0..23].
    # 0,1,2 left, stop
    # 3-11 left, go
    # 12-20 right, go
    # 21,22,23 right stop
    for i in range(24):
        stimDic = {
            'side' : 'left' if i < 12 else 'right',
            'stop' : True if i < 3 or i > 20 else False,
            'correct response' : 'z' if i < 12 else 'x'
        }
        stims.append(stimDic)
    return stims


def showMSG(text, win, xpos):
    msg = visual.TextStim(win, text = text, color = 'white', height = 0.1, pos = (xpos,0), wrapWidth = 1.7)
    msg.draw()
    win.flip()


def askForParticipantID():
    participant_id = gui.Dlg(title="Automatic Imitation Experiment")
    participant_id.addText('Info')
    participant_id.addField('ID:')
    participant_id.addField('Age/Alder:')
    participant_id.addField('Understand Danish/Forstår Dansk', choices = ['Yes/Ja', 'No/Nej'])
    participant_id.show()

    if participant_id.OK:
        ID = participant_id.data[0]
        Age = participant_id.data[1]
        dk = participant_id.data[2] == 'Yes/Ja'
    else:
        core.quite()
    return ID, Age, dk


msg1 ="""Velkommen til første del af dette eksperiment.\nVi starter med at gennemgå nogle instruktioner.\n
Gå videre igennem instruktionerne med mellemrumstasten."""

msg2 = """I denne del af eksperimentet skal du have fingrene på 'z' og 'x' tasterne med din venstre hånd.\n
Når vi går i gang, skal du holde de to taster nede med din pegefinger og din langefinger.\n"""

msg3 = """Du vil se en hånd på en blå baggrund. Mellem pegenfingeren og ringefingeren vil et tal dukke op.
Samtidig vil enten håndens pegefinger eller ringefinger løfte sig. \n
Her er et eksempel."""

msg4 = """Din opgave er at reagere på tallet og IKKE på fingeren.\n
Hvis du ser et 1-tal skal du løfte din pegefinger.\n
Hvis du ser et 2-tal skal du løfte din langefinger.\n
Løft den korrekte finger så hurtigt som muligt, uden at lave fejl."""

msg5 = """Du vil blive vist en række af billeder. Når du holder begge taster nede, vil hånden dukke op.\n
Efter et kort øjeblik vil du se tallet. Løft den korrekte finger, men hold den anden nede. \n
For at gøre klar til næste omgang, lad bare den finger, du løftede, trykke på tasten igen."""

msg6 = """Vi starter med en prøverunde. \n
Her vises to billeder.\n
Følg instruktionerne så godt som du kan. Hvis du skulle have misforstået noget, kan du prøve igen. \n
Tryk på mellemrum for at starte."""

msg1_en ="""Welcome to the first part of this experiment.\nWe will start by going over some instructions.\n
Proceed through the instructions by pressing the space bar."""

msg2_en = """In this part of the experiment you will have to press down your fingers on the 'z' and 'x' keys with your left hand.\n
When we begin, you will have to hold down the two buttons with your index and middle fingers.\n"""

msg3_en = """You will see a hand on a blue background. A number will appear between the index and middle fingers.
Simultaniously, either the index finger or middle finger of the hand will move. \n
Here is an example."""

msg4_en = """Your task is to respond to the number and NOT the finger.\n
If you see '1', you should lift your index finger.\n
If you see '2', you should lift your middle finger.\n
Lift the correct finger as quickly as possible, without making mistakes."""

msg5_en = """You will be shown a series of images. When both your fingers are placed on the keys, the hand will appear.\n
After a short moment, the number will appear. Lift the correct finger, but keep the other finger rested on the keyboard. \n
In order to continue to the next trial, return the finger you lifted to the keyboard."""

msg6_en = """We begin with a trial round.\n
Shown here are two images.\n
Follow the instructions as well as you can. If you have misunderstood anything, you can try again. \n
Press the space bar to begin."""

def setInstructions1(dk=True):
    if dk:
        instructions = [msg1,msg2,msg3,msg4,msg5,msg6]
    else:
        instructions = [msg1_en,msg2_en,msg3_en,msg4_en,msg5_en,msg6_en]
    return instructions



msg7 = """Anden del af eksperimentet minder meget om første del.\n
Du vil se billeder af hænder ligesom sidst. Men denne gang er der ingen tal.
I stedet skal du løfte den samme finger, som hånden løfter. \n
Prøv engang."""
msg7_en = """The second part of the experiment is a lot like the first part.\n
As in the first part, you will see images of hands on the screen. But this time, numbers will not appear.
Instead you are supposed mimic the hand by lifting the same finger the hand lifts. \n
Have a try."""
def getInstructions2(dk=True):
    if dk:
        return msg7
    else:
        return msg7_en

def showExecInstruc(win, circle, lRect, rRect, kb, dk, xpos):
    kb.getKeys(['x','z'], waitRelease=False, clear=True)
    text1 = "I tredje del af eksperimentet præsenteres du for disse to figurer." if dk else "In this third part of the experiment you will be presented with these two shapes."
    visual.TextStim(win, text = text1, color = 'white', height = 0.1, pos = (xpos,0.65), wrapWidth=1.7).draw()
    showFigures(win, [lRect, rRect])
    event.waitKeys(keyList = 'space')

    text2 = "En af dem vil lyse op.\nHvis den højre firkant lyser op, skal du trykke på 'x' med din pegefinger.\nHvis den venstre lyser op skal du trykke på 'z' med din langefinger." if dk else "One of them will turn blue.\nIf the right square turns blue, press 'x' with your index finger.\nIf the left square turns blue, press 'z' with your middle finger."
    visual.TextStim(win, text = text2, color = 'white', height = 0.1, pos = (xpos,0.65), wrapWidth=1.7).draw()
    resetFigures([lRect,rRect])
    rRect.setColor((0, 128, 255), 'rgb255')
    showFigures(win, [lRect, rRect])
    event.waitKeys(keyList = 'space')

    text3 = "Du vil ikke have langt tid til at reagere!\nEfter et halvt sekund vil den holde op med at lyse.\nPlacer dine fingre over tasterne. Du skal ikke holde dem nede i denne del." if dk else "You will only have a short time in which to react!\nAfter half a second, the square will become uncoloured again.\nPlace your fingers above the keys. You are not supposed to hold down the keys for this part."
    visual.TextStim(win, text = text3, color = 'white', height = 0.1, pos = (xpos,0.65), wrapWidth=1.7).draw()
    showFigures(win, [lRect, rRect])
    event.waitKeys(keyList = 'space')

    text4 = "Vi indleder nu de første prøverunder. Reager så hurtigt som muligt uden at lave fejl." if dk else "We start off with a couple of trial rounds. Respond as quickly as possible without making mistakes."
    visual.TextStim(win, text = text4, color = 'white', height = 0.1, pos = (xpos,0.65), wrapWidth=1.7).draw()
    showFigures(win, [lRect, rRect])
    event.waitKeys(keyList = 'space')

    error = True
    while error:
        error = False
        stimuli = makeStimListExecutive()
        stimuli = stimuli[9:15]
        shuffle(stimuli)
        for stim in stimuli:
            resetFigures([lRect,rRect])
            showFigures(win, [lRect, rRect])
            core.wait(1)
            kb.getKeys(['x','z'], waitRelease=False, clear=True) # Clear keypresses.
            if stim['side'] == 'left':
                lRect.setColor((0, 128, 255), 'rgb255') ## TURN BLUE
            else:
                rRect.setColor((0, 128, 255), 'rgb255')

            showFigures(win, [lRect, rRect])

            key = []
            stopWatch = core.CountdownTimer(0.7)
            while stopWatch.getTime() > 0 and key == []:
                key = kb.getKeys(['x','z'])
            response = None
            for k in key:
                response = k.name

            if response == None:
                error = True
                print("none response")

            elif response != stim['correct response']:
                error = True
                print("wrong response")

        if error:
            errorText = "Du kom til at lave en fejl.\n\nHusk 'z' hvis den venstre lyser og 'x' hvis den højre lyser. Og du skal reagere inden den stopper med at lyse\n\nDu skal ikke holde knapperne nede, men bare trykke på dem.\n\nPrøv igen." if dk else "You made a mistake.\n\nRemember to press 'z' if the left square turns blue and 'x' if the right square turns blue. Respond within half a second.\n\nYou are not supposed to hold down the keys, only press them.\n\nTry again."
            visual.TextStim(win, text = errorText, color = 'white', height = 0.1, pos = (xpos,0), wrapWidth=1.7).draw()
            win.flip()
            event.waitKeys(keyList = 'space')

    text5 = "Vi introducerer nu også denne cirkel." if dk else "We now add a circle between the two squares."
    visual.TextStim(win, text = text5, color = 'white', height = 0.1, pos = (xpos,0.65), wrapWidth=1.7).draw()
    resetFigures([lRect,rRect])
    showFigures(win, [circle,lRect, rRect])
    event.waitKeys(keyList = 'space')

    text6 = "Nogen gange vil cirklen også lyse rød. I disse tilfælde skal du IKKE trykke på noget." if dk else "Sometimes the circle will turn red. In this case you are NOT supposed to press any key."
    visual.TextStim(win, text = text6, color = 'white', height = 0.1, pos = (xpos,0.65), wrapWidth=1.7).draw()
    circle.setColor((255, 0, 0), 'rgb255')
    lRect.setColor((0, 128, 255), 'rgb255')
    showFigures(win, [circle,lRect, rRect])
    event.waitKeys(keyList = 'space')


    text7 = "I starten vil cirklen lyse op samtidig med firkanterne.\n\nSenere vil der være en lille forsinkelse." if dk else "At the beginning the circle will light up simultaniously with the squares.\n\nSuebsequently, there will be a small delay."
    visual.TextStim(win, text = text7, color = 'white', height = 0.1, pos = (xpos,0.65), wrapWidth=1.7).draw()
    circle.setColor((255, 0, 0), 'rgb255')
    showFigures(win, [circle,lRect, rRect])
    event.waitKeys(keyList = 'space')

    text8 = "Vi starter med en prøverunde.\n\nHusk stadig at reagere så hurtigt som muligt, uden at lave fejl." if dk else "We start off with a trial round.\n\nRemember to still respond as quickly as possible without making mistakes."
    visual.TextStim(win, text = text8, color = 'white', height = 0.1, pos = (xpos,0.65), wrapWidth=1.7).draw()
    resetFigures([circle,lRect,rRect])
    showFigures(win, [circle, lRect, rRect])
    event.waitKeys(keyList = 'space')
    error = True
    while error:
        error = False
        stimuli = makeStimListExecutive()
        stimuli = [stimuli[1],stimuli[15],stimuli[5],stimuli[21],stimuli[2],stimuli[6],stimuli[16],stimuli[22]]
        for stim in stimuli:
            resetFigures([circle,lRect,rRect])
            showFigures(win, [circle, lRect, rRect])
            core.wait(0.5)
            kb.getKeys(['x','z'], waitRelease=False, clear=True) # Clear keypresses.
            if stim['side'] == 'left':
                lRect.setColor((0, 128, 255), 'rgb255') ## TURN BLUE
            else:
                rRect.setColor((0, 128, 255), 'rgb255')
            if stim['stop']:
                circle.setColor((255, 0, 0), 'rgb255')  ## TURN RED

            showFigures(win, [circle, lRect, rRect])

            key = []
            stopWatch = core.CountdownTimer(0.7)
            while stopWatch.getTime() > 0 and key == []:
                key = kb.getKeys(['x','z'])
            response = None
            for k in key:
                response = k.name

            if (response != stim['correct response'] and not stim['stop']) or (stim['stop'] and response != None):
                error = True

        if error:
            errorText = "Du kom til at lave en fejl.\n\nHusk 'z' hvis den venstre lyser og 'x' hvis den højre lyser. Og ikke tryk på noget, hvis cirklen også lyser.\n\nTryk mens firkanten lyser.\n\nPrøv igen." if dk else "You made a mistake.\n\nRemember to press 'z' if the left square turns blue and 'x' if the right square turns blue. Do NOT press anything if the circle turns red.\n\nPress the key when the square is blue, not afterwards.\n\nTry again."
            visual.TextStim(win, text = errorText, color = 'white', height = 0.1, pos = (xpos,0), wrapWidth=1.7).draw()
            win.flip()
            event.waitKeys(keyList = 'space')

    text8 = "Super godt!\n\nNu begynder vi eksperimentets sidste del.\n\nReager så hurtigt, du kan uden at lave fejl." if dk else "Great!\n\nWe now commence the last part of the experimemnt. \n\nRespond as quickly as possible without making mistakes."
    visual.TextStim(win, text = text8, color = 'white', height = 0.1, pos = (xpos,0), wrapWidth=1.7).draw()
    win.flip()
    event.waitKeys(keyList = 'space')


def showFigures(win, figures):
    for f in figures:
        f.draw()
    win.flip()

def resetFigures(figures):
    for f in figures:
        f.setColor((0, 0, 0), 'rgb255')
        f.setLineColor('white')


if __name__ == "__main__":
    stims = makeStimListExplicit()
    print(len(stims))
    #print(stims[0])
