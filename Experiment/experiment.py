# experiment.py
# source psychoEnv/bin/activate

from psychopy import core, monitors, visual, event, gui
from psychopy.hardware import keyboard
from random import uniform, shuffle, random
from functions import *
from datetime import datetime
import pandas as pd
import numpy as np
import time

fullTimer = time.time()

## Number of repetitions TO BE SET
repetitions = 20
repetitions_stop = 17

# Run instructions?
InstructionsParam = True
exp1, exp2, exp3 = True,True,True

## Showing GUI to ask for ID and Age (helper file)
ID, Age, dk = askForParticipantID()

## Storing exact time to use in .csv filename to avoid overwrite
now = datetime.now()
date = now.strftime("%d-%m-%Y-%H-%M-%S")

## Setting up psychopy hardware (keyboard, monitor and window)
MON_DISTANCE = 60
MON_WIDTH = 50
MON_SIZE = [2560, 1600]

kb = keyboard.Keyboard()

my_monitor = monitors.Monitor('testMonitor', width=MON_WIDTH, distance=MON_DISTANCE)  # Create monitor object from the variables above.
win = visual.Window(monitor=my_monitor, units='norm', fullscr=True, allowGUI=False, color='black',size = MON_SIZE)


text1 = "Hvis denne tekst står i midten, tryk på 'z'." if dk else "If this text is in the middle, press 'z'"
text2 = "Hvis denne tekst står i midten, tryk på 'x'." if dk else "If this text is in the middle, press 'x'"

visual.TextStim(win, text = text1, color = 'white', height = 0.1, pos = (0,0.65), wrapWidth=1.7).draw()
visual.TextStim(win, text = text2, color = 'white', height = 0.1, pos = (0.9,0.0), wrapWidth=1.7).draw()
win.flip()
keys = []
while keys == []:
    keys = kb.getKeys(['x','z'])
for k in keys:
    response = k.name
if response == 'z':
    xpos = 0
else:
    xpos = 0.9


#########################################################################################
################################ EXPERIMENT 1 - IMPLICIT ################################
#########################################################################################

## Running instructions for experiment one
def runInstructions(dk):
    instructions = setInstructions1(dk)

    for msg in instructions:
        showMSG(msg,win,xpos)
        event.waitKeys(keyList = 'space')
        if msg == instructions[2]:
            startingHand = visual.ImageStim(win = win, image = "hands/numberless.jpg")
            stimHand = visual.ImageStim(win = win, image = "hands/01index-1.jpg")
            startingHand.draw()
            win.flip()
            core.wait(2)
            stimHand.draw()
            win.flip()
            core.wait(2)
        if msg == instructions[5]:
            neutralImages = ["hands/numberless.jpg", "hands/numberless-mir.jpg"]
            stimImages = ["hands/01index-1.jpg", "hands/04index-2-mir.jpg"]
            correctResponses = ["x","z"]
            error = True
            while error:
                error = False
                for i in range(2):
                    startingHand = visual.ImageStim(win = win, image = neutralImages[i])
                    stimHand = visual.ImageStim(win = win, image = stimImages[i])
                    x, z, waited, shown, counter, keys = False, False, False, False, 0, []
                    while keys == []:
                        keys = kb.getKeys(['x', 'z'], waitRelease=True)
                        if shown:
                            counter += 1
                        else:
                            if not x and kb.getKeys(['x'], waitRelease=False, clear=False) != []:
                                x = True
                            if not z and kb.getKeys(['z'], waitRelease=False, clear=False) != []:
                                z = True
                            if not (x and z):
                                if dk:
                                    showMSG("Klik og hold både 'z' og 'x' knappen nede.", win, xpos)
                                else:
                                    showMSG("Press down and hold the ‘z’ and ‘x’ button.",win, xpos)
                            if x and z and not waited:
                                core.wait(0.5)
                                startingHand.draw()
                                win.flip()
                                waited = True
                                core.wait(2)
                            if not shown and waited:
                                stimHand.draw()
                                win.flip()
                                shown = True
                    bothButtonsError, liftBeforeStim, liftDuringWait, wrongFingerError = False, False, False, False,
                    for k in keys:
                        response = k.name
                    if not z or not x:
                        bothButtonsError = True
                        error = True
                    elif not waited:
                        liftBeforeStim = True
                        error = True
                    elif counter < 3:
                        liftDuringWait = True
                        error = True
                    elif response != correctResponses[i]:
                        wrongFingerError = True
                        error = True

                if bothButtonsError:
                    if dk:
                        showMSG("Ups, begge knapper blev ikke holdt nede. Prøv en gang til.\nKlik på mellemrum for at prøve igen.",win, xpos)
                    else:
                        showMSG("Oops, both keys were not on the keyboard. Try again.\nPress the space bar to try again",win, xpos)
                    event.waitKeys(keyList = 'space')
                if liftBeforeStim or liftDuringWait:
                    if dk:
                        showMSG("Ups, du løftede fingeren for tidligt.\nKlik på mellemrum for at prøve igen.",win, xpos)
                    else:
                        showMSG("Oops, you lifted your finger too early.\nPress the space bar to try again.",win, xpos)
                    event.waitKeys(keyList = 'space')
                if wrongFingerError:
                    if dk:
                        showMSG("Du kom til at løfte den forkerte finger.\nHusk 1-tal er pegefiner og 2-tal er langefinger.\nKlik på mellemrum for at prøve igen.",win, xpos)
                    else:
                        showMSG("You lifted the wrong finger.\nRemember to lift your index finger ‘1’ appears and your middle finger if ‘2’ appears.\nPress the space bar to try again.",win, xpos)
                    event.waitKeys(keyList = 'space')


## Setting up the data structure
cols = ['Participant', 'Age', 'Experiment','Spatial_Compatibility', 'Finger_Compatibility', 'Reaction_time',
        'Response', 'Correctness', 'Finger_Cue', 'Number_Cue', 'Waiting_Time', 'Error']
rows = np.arange(0)
data = pd.DataFrame(columns=cols, index = rows)

## Running the experiment
def runImplicit(dk, data = data, repetitions = repetitions):
    kb.getKeys(['x','z'], waitRelease=False, clear=True)
    stimuli = []
    for rep in range(repetitions):
        stims = makeStimList()
        shuffle(stims)
        stimuli.append(stims)
    stimuli = [stim for stimList in stimuli for stim in stimList]
    for stim in stimuli:
        startingHand = visual.ImageStim(win = win, image = stim['neutralImg'])
        stimHand = visual.ImageStim(win = win, image = stim['img'])
        x, z, waited, shown, error = False, False, False, False, False
        keys = []
        counter = 0
        while keys == []:
            keys = kb.getKeys(['x', 'z'], waitRelease=True)
            if shown:
                counter += 1
            else:
                if not x and kb.getKeys(['x'], waitRelease=False, clear=False) != []:
                    x = True
                if not z and kb.getKeys(['z'], waitRelease=False, clear=False) != []:
                    z = True
                if not (x and z):
                    if dk:
                        showMSG("Klik og hold både 'z' og 'x' knappen nede.",win, xpos)
                    else:
                        showMSG("Press down and hold the ‘z’ and ‘x’ button.",win, xpos)
                if x and z and not waited:
                    core.wait(uniform(0.2,0.5))
                    startingHand.draw()
                    win.flip()
                    waited = True
                    wait = round(uniform(0.8,2.4),1)
                    core.wait(wait)
                if not shown and waited:
                    stimHand.draw()
                    shown = True
                    c = core.MonotonicClock()
                    win.flip()


        RT = c.getTime()

        for k in keys:
            response = k.name

        if not z or not x:
            error = True
        elif not waited:
            error = True
        elif counter < 3:
            error = True

        if error:
            if dk:
                showMSG("Ups, der skete vist en fejl.\n\nLøft begge begge fingre fra tasterne og klik på mellemrumstasten for at fortsætte.",win, xpos)
            else:
                showMSG("Oops, a mistake happened.\n\nPlease lift both fingers from the buttons and press the spacebar to continue.",win, xpos)
            kb.getKeys(['x','z','space','escape'], waitRelease=False, clear=True)
            stimuli.append(stim)

            waitingKey = []
            while waitingKey == []:
                waitingKey = kb.getKeys(['space','escape'])

            for k in waitingKey:
                if k.name == 'escape':
                    core.quit()

            kb.getKeys(['x','z','escape','space'], waitRelease=False, clear=True)


        data = data.append({
            'Participant'           : ID,
            'Age'                   : Age,
            'Experiment'            : 'Implicit',
            'Spatial_Compatibility' : stim['spatial congruency'],
            'Finger_Compatibility'  : stim['finger congruency'],
            'Reaction_time'         : RT,
            'Response'              : response,
            'Correctness'           : response == stim['correct response'],
            'Finger_Cue'            : stim['finger'],
            'Number_Cue'            : stim['number'],
            'Waiting_Time'          : wait,
            'Error'                 : error
            }, ignore_index=True)

    return data
if exp1:
    if InstructionsParam:
        runInstructions(dk)
        if dk:
            showMSG("Perfekt!\nHerfra begynder eksperimentet.\n\nReager så hurtigt som muligt uden at lave fejl.\n\nStart ved klikke på mellemrumstasten",win, xpos)
        else:
            showMSG("Perfect!\nNow the experiment begins.\n\nRespond as quickly as possible, without making mistakes.\n\nStart by pressing the space bar.",win, xpos)
        event.waitKeys(keyList = 'space')
    data = runImplicit(dk)
    # Storing a csv file

    # Proceding to 2nd experiment
    if dk:
        showMSG("Du er nu færdig med første del af eksperimentet.\n\nVi vil nu forklare anden del.\n\nKlik på mellemrumstasten for at gå videre.",win, xpos)
    else:
        showMSG("You finished the first part of the experiment.\n\nWe now move on to the second part.\n\nPress the space by to proceed.",win, xpos)
    event.waitKeys(keyList = 'space')

#########################################################################################
################################ EXPERIMENT 2 - EXPLICIT ################################
#########################################################################################

# Give introduction
showMSG(getInstructions2(dk),win, xpos)
event.waitKeys(keyList = 'space')

def runTestExplicit(dk):
    neutralImages = ["hands/numberless-mir.jpg", "hands/numberless.jpg"]
    stimImages = ["hands/10index-0-mir.jpg", "hands/11middle-0.jpg"]
    correctResponses = ["x","z"]
    error = True
    while error:
        error = False
        for i in range(2):
            startingHand = visual.ImageStim(win = win, image = neutralImages[i])
            stimHand = visual.ImageStim(win = win, image = stimImages[i])
            x, z, waited, shown, counter, keys = False, False, False, False, 0, []
            while keys == []:
                keys = kb.getKeys(['x', 'z'], waitRelease=True)
                if shown:
                    counter += 1
                else:
                    if not x and kb.getKeys(['x'], waitRelease=False, clear=False) != []:
                        x = True
                    if not z and kb.getKeys(['z'], waitRelease=False, clear=False) != []:
                        z = True
                    if not (x and z):
                        if dk:
                            showMSG("Klik og hold både 'z' og 'x' tasten nede.",win, xpos)
                        else:
                            showMSG("Press down and hold the ‘z’ and ‘x’ button.",win, xpos)
                    if x and z and not waited:
                        core.wait(0.5)
                        startingHand.draw()
                        win.flip()
                        waited = True
                        core.wait(2)
                    if not shown and waited:
                        stimHand.draw()
                        win.flip()
                        shown = True
            bothButtonsError, liftBeforeStim, liftDuringWait, wrongFingerError = False, False, False, False,
            for k in keys:
                response = k.name
            if not z or not x:
                bothButtonsError = True
                error = True
            elif not waited:
                liftBeforeStim = True
                error = True
            elif counter < 3:
                liftDuringWait = True
                error = True
            elif response != correctResponses[i]:
                wrongFingerError = True
                error = True

        if bothButtonsError:
            if dk:
                showMSG("Begge knapper blev ikke holdt nede. Prøv en gang til.\nKlik på mellemrum for at prøve igen.",win, xpos)
            else:
                showMSG("Both keys were not pressed down. Try again.\nPress the space by to try again.",win, xpos)
            event.waitKeys(keyList = 'space')
        if liftBeforeStim or liftDuringWait:
            if dk:
                showMSG("Ups, du løftede fingeren for tidligt.\nKlik på mellemrum for at prøve igen.",win, xpos)
            else:
                showMSG("Oops, you lifted your finger too du løftede fingeren for tidligt.\nPress the space bar to try again.",win, xpos)
            event.waitKeys(keyList = 'space')
        if wrongFingerError:
            if dk:
                showMSG("Du kom til at løfte den forkerte finger.\nHusk du skal kigge på om pegefingeren eller langefingeren blev løftet.\nKlik på mellemrum for at prøve igen.",win, xpos)
            else:
                showMSG("Oops, you lifted the wrong finger.\nRemember to lift your fingers according to which of the fingers on the screen moved.\nPress the space bar to try again.",win, xpos)
            event.waitKeys(keyList = 'space')
    if dk:
        showMSG("Perfekt!\nHerfra begynder eksperimentet.\n\nReager så hurtigt som muligt uden at lave fejl.\n\nStart ved klikke på mellemrumstasten.",win, xpos)
    else:
        showMSG("Perfect!\nNow the experiment begins.\n\nRespond as quickly as possible, without making mistakes.\n\nStart by pressing the space by.",win, xpos)

    event.waitKeys(keyList = 'space')


def runExplicit(dk, data = data, repetitions = repetitions):
    kb.getKeys(['x','z'], waitRelease=False, clear=True)
    stimuli = []
    for rep in range(repetitions):
        stims = makeStimListExplicit()
        shuffle(stims)
        stimuli.append(stims)
    stimuli = [stim for stimList in stimuli for stim in stimList]
    for stim in stimuli:
        startingHand = visual.ImageStim(win = win, image = stim['neutralImg'])
        stimHand = visual.ImageStim(win = win, image = stim['img'])
        x, z, waited, shown, error = False, False, False, False, False
        keys = []
        counter = 0
        while keys == []:
            keys = kb.getKeys(['x', 'z'], waitRelease=True)
            if shown:
                counter += 1
            else:
                if not x and kb.getKeys(['x'], waitRelease=False, clear=False) != []:
                    x = True
                if not z and kb.getKeys(['z'], waitRelease=False, clear=False) != []:
                    z = True
                if not (x and z):
                    if dk:
                        showMSG("Klik og hold både 'z' og 'x' knappen nede.",win, xpos)
                    else:
                        showMSG("Press down and hold the ‘z’ and ‘x’ button.",win, xpos)
                if x and z and not waited:
                    core.wait(uniform(0.2,0.5))
                    startingHand.draw()
                    win.flip()
                    waited = True
                    wait = round(uniform(0.8,2.4),1)
                    core.wait(wait)
                if not shown and waited:
                    stimHand.draw()
                    c = core.MonotonicClock()
                    win.flip()
                    shown = True

        RT = c.getTime()

        for k in keys:
            response = k.name

        if not z or not x:
            error = True
        elif not waited:
            error = True
        elif counter < 3:
            error = True

        if error:
            if dk:
                showMSG("Ups, der skete vist en fejl.\n\nLøft begge begge fingre fra tasterne og klik på mellemrumstasten for at fortsætte.",win, xpos)
            else:
                showMSG("Oops, a mistake happened.\n\nPlease lift both fingers from the buttons and press the spacebar to continue.",win, xpos)
            kb.getKeys(['x','z','space','escape'], waitRelease=False, clear=True)
            stimuli.append(stim)

            waitingKey = []
            while waitingKey == []:
                waitingKey = kb.getKeys(['space','escape'])

            for k in waitingKey:
                if k.name == 'escape':
                    core.quit()

            kb.getKeys(['x','z','escape','space'], waitRelease=False, clear=True)

        data = data.append({
            'Participant'           : ID,
            'Age'                   : Age,
            'Experiment'            : 'Explicit',
            'Spatial_Compatibility' : stim['spatial congruency'],
            'Finger_Compatibility'  : None,
            'Reaction_time'         : RT,
            'Response'              : response,
            'Correctness'           : response == stim['correct response'],
            'Finger_Cue'            : stim['finger'],
            'Number_Cue'            : None,
            'Waiting_Time'          : wait,
            'Error'                 : error
            }, ignore_index=True)

    return data
if exp2:
    if InstructionsParam:
        runTestExplicit(dk)

    data = runExplicit(dk)
    # Storing a csv file
    data.to_csv('data/imitation/'+ID+'-'+date+'.csv', index = None)
    if dk:
        showMSG('Vi er nu færdige med andet del af eksperimentet.\n\nKlik på mellemrum for at gå videre til tredje del.',win, xpos)
    else:
        showMSG('You completed the second part of the experiment.\n\nPress the space bar to proceed to the third part',win, xpos)
    event.waitKeys(keyList = 'space')


#########################################################################################
############################ EXPERIMENT 3 - Stop Signal Task ############################
#########################################################################################


execCols = ['Participant', 'Age', 'Experiment', 'Reaction_Time', 'Response',
            'Correctness','Side', 'Stop_Signal', 'Stop_Mistake']
execRows = np.arange(0)
execData = pd.DataFrame(columns=execCols, index = execRows)


circle = visual.Circle(win, radius = 0.25, edges = 1024)
lRect = visual.Rect(win, width=0.3, height=0.6, pos = (-0.7,0))
rRect = visual.Rect(win, width=0.3, height=0.6, pos = (0.7,0))


def runExec(execData=execData, repetitions = repetitions_stop):
    timeToReact = 0.7
    kb.getKeys(['x','z'], waitRelease=False, clear=True)
    SSD = 0
    stimuli = []
    for rep in range(repetitions):
        stims = makeStimListExecutive()
        shuffle(stims)
        stimuli.append(stims)
    stimuli = [stim for stimList in stimuli for stim in stimList]
    for stim in stimuli:
        resetFigures([circle,lRect,rRect])
        showFigures(win, [circle, lRect, rRect])
        core.wait(uniform(0.3,0.8))
        kb.getKeys(['x','z'], waitRelease=False, clear=True) # Clear keypresses.
        if stim['side'] == 'left':
            lRect.setColor((0, 128, 255), 'rgb255') # Change Color to Blue
        else:
            rRect.setColor((0, 128, 255), 'rgb255')

        key = []
        changed = False
        showFigures(win, [circle, lRect, rRect])

        stopWatch = core.CountdownTimer(timeToReact)
        while stopWatch.getTime() > 0 and key == []:
            if stim['stop'] and (timeToReact-stopWatch.getTime()) > SSD and not changed:
                circle.setColor((255, 0, 0), 'rgb255')
                showFigures(win, [circle, lRect, rRect])
                changed = True
            RT = timeToReact-stopWatch.getTime()
            key = kb.getKeys(['x','z'])
        response = None
        for k in key:
            response = k.name

        execData = execData.append({
            'Participant'   : ID,
            'Age'           : Age,
            'Experiment'    : 'Executive',
            'Reaction_Time' : RT,
            'Response'      : response,
            'Correctness'   : True if response == stim['correct response'] or (stim['stop'] and response == None) else False,
            'Side'          : stim['side'],
            'Stop_Signal'   : stim['stop'],
            'SSD'           : SSD,
            'Stop_Mistake'  : True if stim['stop'] and response != None else False
            }, ignore_index=True)


        if stim['stop']:
            if response == None:
                SSD += 0.015
            else:
                SSD -= 0.015


    return execData
if exp3:
    if InstructionsParam:
        showExecInstruc(win, circle, lRect, rRect, kb, dk, xpos)
        execData = runExec()
        execData.to_csv('data/executive/'+ID+'-exec-'+date+'.csv', index = None)

    if dk:
        showMSG('Vi er nu færdige med tredje og sidste del af eksperimentet.\n\nTusinde tak for din deltagelse!\n\nKlik på mellemrum for at aflsutte.',win, xpos)
    else:
        showMSG('You finished the third and last part of the experiment.\n\nThank you very much for your participation!\n\nPress the space bar to quit the experiment.',win, xpos)
    event.waitKeys(keyList = 'space')
