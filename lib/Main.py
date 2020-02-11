import os
import sys
from random import randint
from threading import Thread
from time import time, sleep
from tkinter import PhotoImage, Button, Canvas, TRUE, FLAT, NW, TclError, HIDDEN

# from lib import control
from lib.maintance import Maintance
from lib.registry import get_register
from lib.startup import start
from lib.stats import get_stats, set_stat, set_stats, get_stat
from lib.utils import get_coords
from .init import Init
from .utils.config import Convert, Reader


# noinspection PyPep8Naming
from .utils.get_set import set_root
from .window import RootWindow


def control(event):
    pass


# noinspection PyUnusedLocal
class Game(object):
    def __init__(self, launcher_cfg):
        self.move_fps = 1
        print(launcher_cfg)
        print(os.listdir("."))
        print(os.getcwd())

        self.returnmain: bool = False
        self.ship = dict()

        self.window = RootWindow(launcher_cfg, self.start_game)

    def _movent(self):
        from lib.stats import get_stats
        if (not get_stats("Modes")["teleport"]) and (not get_stats("Modes")["store"]) and (
                not get_stats("Modes")["window"]):
            if not get_stats("Modes")["pause"]:
                if not get_stats("Stats")["paralis"]:
                    x, y = get_coords(self.canvas, self.ship["id"])
                    if get_stats("Stats")["speedboost"]:
                        a = 6
                    else:
                        a = 1
                    if get_stats("Temp")["Pressed"]['Up']:
                        if y > 72 + get_register("Config")["game"]["ship-radius"]:
                            self.canvas.move(self.ship["id"], 0,
                                             (-get_stats("Stats")["shipspeed"] / (self.move_fps / 4) - a))
                            self._root.update()
                    elif get_stats("Temp")["Pressed"]['Down']:
                        if y < get_register("Config")["height"] - get_register("Config")["game"]["ship-radius"]:
                            self.canvas.move(self.ship["id"], 0,
                                             (get_stats("Stats")["shipspeed"] / (self.move_fps / 4) + a))
                            self._root.update()
                    elif get_stats("Temp")["Pressed"]['Left']:
                        if x > 0 + get_register("Config")["game"]["ship-radius"]:
                            self.canvas.move(self.ship["id"],
                                             (-get_stats("Stats")["shipspeed"] / (self.move_fps / 4) - a), 0)
                            self._root.update()
                    elif get_stats("Temp")["Pressed"]['Right']:
                        if x < get_register("Config")["width"] - get_register("Config")["game"]["ship-radius"]:
                            self.canvas.move(self.ship["id"],
                                             (get_stats("Stats")["shipspeed"] / (self.move_fps / 4) + a), 0)
                            self._root.update()
                    get_stats("Stats")["ship-position"] = get_coords(self.canvas, self.ship["id"])

    def pause_states(self):
        get_stats("Temp")["scorestate-save"] = get_stats("Stats")["scorestate-time"] - time()
        get_stats("Temp")["secure-save"] = get_stats("Stats")["secure-time"] - time()
        get_stats("Temp")["timebreak-save"] = get_stats("Stats")["timebreak-time"] - time()
        get_stats("Temp")["confusion-save"] = get_stats("Stats")["confusion-time"] - time()
        get_stats("Temp")["slowmotion-save"] = get_stats("Stats")["slowmotion-time"] - time()
        get_stats("Temp")["paralis-save"] = get_stats("Stats")["paralis-time"] - time()
        get_stats("Temp")["shotspeed-save"] = get_stats("Stats")["shotspeed-time"] - time()
        get_stats("Temp")["notouch-save"] = get_stats("Stats")["notouch-time"] - time()
        get_stats("Temp")["special-level-save"] = get_stats("Stats")["special-level-time"] - time()

    def unpause_states(self):
        get_stats("Stats")["scorestate-time"] = get_stats("Temp")["scorestate-save"] + time()
        get_stats("Stats")["secure-time"] = get_stats("Temp")["secure-save"] + time()
        get_stats("Stats")["timebreak-time"] = get_stats("Temp")["timebreak-save"] + time()
        get_stats("Stats")["confusion-time"] = get_stats("Temp")["confusion-save"] + time()
        get_stats("Stats")["slowmotion-time"] = get_stats("Temp")["slowmotion-save"] + time()
        get_stats("Stats")["paralis-time"] = get_stats("Temp")["paralis-save"] + time()
        get_stats("Stats")["shotspeed-time"] = get_stats("Temp")["shotspeed-save"] + time()
        get_stats("Stats")["notouch-time"] = get_stats("Temp")["notouch-save"] + time()

    # noinspection PyTypeChecker,PyUnresolvedReferences
    def xboxControlDeamon(self):
        while not self.returnmain:
            if self.returnmain:
                threading.Event()
            if get_stats("Modes")["store"] and get_stats("Commands")["store"] is not None:
                if self.xControl["UpDPad"]:
                    get_stats("Commands")["store"].set_selected(self.canvas, -1)
                if self.xControl["DownDPad"]:
                    get_stats("Commands")["store"].set_selected(self.canvas, 1)
                if self.xControl["LeftDPad"]:
                    get_stats("Commands")["store"].set_selected(self.canvas, -get_stats("Commands")["store"].f - 1)
                if self.xControl["RightDPad"]:
                    get_stats("Commands")["store"].set_selected(self.canvas, get_stats("Commands")["store"].f - 1)
                if self.xControl["A"]:
                    get_stats("Commands")["store"].buy_selected(get_register("Config"), get_stats("Modes"), self.log,
                                                                self._root,
                                                                self.canvas,
                                                                get_stats("Stats"), get_stats("Bubbles"),
                                                                get_register("Background"),
                                                                get_register("Texts"), get_stats("Commands"),
                                                                get_stats("Temp"), get_register("Panels"))
                if self.xControl["B"]:
                    get_stats("Commands")["store"].exit(self.canvas, self.log, get_stats("Modes"), get_stats("Stats"),
                                                        get_stats("Temp"),
                                                        get_stats("Commands"))
                    get_stats("Commands")["store"] = None
                if self.xControl["Back"]:
                    sleep(1)
                    get_stats("Commands")["store"].exit(self.canvas, self.log, get_stats("Modes"), get_stats("Stats"),
                                                        get_stats("Temp"),
                                                        get_stats("Commands"))
                    get_stats("Commands")["store"] = None
            if get_stats("Modes")["present"]:
                if self.xControl["A"]:
                    if False != get_stats("Commands")["present"] != True:
                        get_stats("Commands")["present"].exit(self.canvas)
                        get_stats("Modes")["pause"] = False
                        get_stats("Modes")["present"] = False
                        self.unpause_states()
            if get_stats("Modes")["teleport"]:
                x, y = get_coords(self.canvas, get_stats("TP")["id1"])
                if self.xControl['UpDPad']:
                    if y > 72 + 5:
                        self.canvas.move(get_stats("TP")["id1"], 0, -5)
                        self.canvas.move(get_stats("TP")["id2"], 0, -5)
                        self.canvas.move(get_stats("TP")["id3"], 0, -5)
                        self.canvas.move(get_stats("TP")["id4"], 0, -5)
                if self.xControl["DownDPad"]:
                    if y < get_register("Config")["height"] - 105 - 5:
                        self.canvas.move(get_stats("TP")["id1"], 0, 5)
                        self.canvas.move(get_stats("TP")["id2"], 0, 5)
                        self.canvas.move(get_stats("TP")["id3"], 0, 5)
                        self.canvas.move(get_stats("TP")["id4"], 0, 5)
                if self.xControl["LeftDPad"]:
                    if x > 0 + 5:
                        self.canvas.move(get_stats("TP")["id1"], -5, 0)
                        self.canvas.move(get_stats("TP")["id2"], -5, 0)
                        self.canvas.move(get_stats("TP")["id3"], -5, 0)
                        self.canvas.move(get_stats("TP")["id4"], -5, 0)
                if self.xControl["RightDPad"]:
                    if x < get_register("Config")["width"] - 5:
                        self.canvas.move(get_stats("TP")["id1"], 5, 0)
                        self.canvas.move(get_stats("TP")["id2"], 5, 0)
                        self.canvas.move(get_stats("TP")["id3"], 5, 0)
                        self.canvas.move(get_stats("TP")["id4"], 5, 0)
                if self.xControl["B"]:
                    get_stats("Modes")["pause"] = False
                    self.unpause_states()
                if self.xControl["Back"]:
                    get_stats("Modes")["pause"] = False
                    self.unpause_states()
                    sleep(1)
                if self.xControl["A"]:
                    get_stats("Modes")["pause"] = False
                    self.unpause_states()
                    get_stats("Stats")["teleports"] -= 1
                    teleport(self.canvas, self._root, get_stats("Stats"), get_stats("Modes"), self.ship, get_stats("TP"),
                             get_stats("TP")["id1"])
            if self.xControl["Back"] and (not get_stats("Modes")["pause"]) and (not get_stats("Modes")["store"]) and (
                    not get_stats("Modes")["teleport"]) and \
                    (not get_stats("Modes")["window"]) and (not get_stats("Modes")["present"]) and (
                    not get_stats("Modes")["cheater"]):
                get_stats("Modes")["pause"] = True

                self.canvas.delete(get_registrer("Icons")["pause"])
                if get_stats("Stats")["special-level"]:
                    get_stats("Temp")['pause/bg'] = self.canvas.create_rectangle(0, 69,
                                                                                 get_register("Config")["width"],
                                                                                 get_register("Config")[
                                                                                    "height"],
                                                                                 fill="#3f3f3f",
                                                                                 outline="#3f3f3f")
                    get_stats("Temp")['pause/toline'] = self.canvas.create_line(0, 69, get_register("Config")["width"],
                                                                                69,
                                                                                fill="#afafaf")
                    get_stats("Temp")['pause/menu_frame'] = Frame(self._root, bg="#3f3f3f")
                    get_stats("Temp")['pause/menu'] = self.canvas.create_window(get_register("Config")["middle-x"],
                                                                                get_register("Config")[
                                                                                   "middle-y"] / 2 + 130,
                                                                                window=get_stats("Temp")[
                                                                                   'pause/menu_frame'],
                                                                                anchor='n',
                                                                                height=20, width=300)

                    get_stats("Temp")["pause/back-to-menu"] = Button(get_stats("Temp")["pause/menu_frame"],
                                                                     text=self.lang["pause.back-to-home"],
                                                                     command=lambda: self.return_main(),
                                                                     relief=FLAT, bg="#1f1f1f", fg="#afafaf",
                                                                     font=self.font)
                    back = "#1f1f1f"
                    fore = "yellow"
                else:
                    get_stats("Temp")['pause/bg'] = self.canvas.create_rectangle(0, 69,
                                                                                 get_register("Config")["width"],
                                                                                 get_register("Config")[
                                                                                    "height"],
                                                                                 fill="darkcyan",
                                                                                 outline="darkcyan")
                    get_stats("Temp")['pause/toline'] = self.canvas.create_line(0, 69, get_register("Config")["width"],
                                                                                69,
                                                                                fill="#7fffff")
                    # get_stats("Temp")['pause/bottom.line'] = self.canvas.create_line(0, get_register("Config")[
                    # "height"] - 102, get_register("Config")["width"], get_register("Config")["height"] - 102,
                    # fill="#7fffff")

                    get_stats("Temp")['pause/menu_frame'] = Frame(self._root, bg="darkcyan")
                    get_stats("Temp")['pause/menu'] = self.canvas.create_window(get_register("Config")["middle-x"],
                                                                                get_register("Config")[
                                                                                   "middle-y"] / 2 + 130,
                                                                                window=get_stats("Temp")[
                                                                                   'pause/menu_frame'],
                                                                                anchor='n',
                                                                                height=500, width=300)

                    get_stats("Temp")["pause/back-to-menu"] = Button(get_stats("Temp")["pause/menu_frame"],
                                                                     text=self.lang["pause.back-to-home"],
                                                                     command=lambda: self.return_main(),
                                                                     relief=FLAT, bg="#005f5f", fg="#7fffff",
                                                                     font=[self.font])

                    back = "#005f5f"
                    fore = "#7fffff"

                get_stats("Temp")["s_frame"] = Frame(self._root, bg=back)
                get_stats("Temp")["s_frame"].place(x=get_register("Config")["middle-x"],
                                                   y=get_register("Config")["middle-y"] / 2 + 250, anchor='n',
                                                   width=1000)

                get_stats("Temp")["sw"] = ScrolledWindow(get_stats("Temp")["s_frame"], 1020, 321, height=321, width=1000)

                get_stats("Temp")["canv"] = get_stats("Temp")["sw"].canv
                get_stats("Temp")["canv"].config(bg=back)
                get_stats("Temp")["sw"].scrollwindow.config(bg=back)

                get_stats("Temp")["frame"] = get_stats("Temp")["sw"].scrollwindow

                a = ("Normal", "Double", "Kill", "Triple", "SpeedUp", "SpeedDown", "Up", "Ultimate", "DoubleState",
                     "Protect", "SlowMotion", "TimeBreak", "Confusion", "HyperMode", "Teleporter",
                     "Coin", "NoTouch", "Paralis", "Diamond", "StoneBub", "Present", "SpecialKey", "LevelKey")

                c = (
                    "bubble.normal", "bubble.double", "bubble.kill", "bubble.triple", "bubble.speedup",
                    "bubble.speeddown",
                    "bubble.up", "bubble.state.ultimate", "bubble.state.double", "bubble.state.protect",
                    "bubble.state.slowmotion",
                    "bubble.state.timebreak", "bubble.state.confusion", "bubble.state.hypermode", "bubble.teleporter",
                    "bubble.coin", "bubble.state.notouch", "bubble.state.paralis", "bubble.diamond",
                    "bubble.stonebubble",
                    "bubble.present", "bubble.state.specialkey", "bubble.levelkey")

                # noinspection PyAttributeOutsideInit
                self.canvass = Canvas(get_stats("Temp")["frame"], bg=back, highlightthickness=0)
                x = 50
                y = 50
                get_stats("Temp")["pause/bubble.iconss"] = []
                for i in range(len(a)):
                    # print(a[i], b[i])
                    place_bubble(self.canvass, self.bub, x, y, 25, a[i])
                    self.canvass.create_text(x, y + 40, text=self.lang[c[i]], fill=fore, font=[self.font, 10])
                    if x > 900:
                        x = 50
                        y += 100
                    else:
                        x += 100

                self.canvass.config(height=y + 70, width=1000)
                self.canvass.pack(fill=Y)

                get_stats("Temp")["pause/back-to-menu"].pack(fill=X)

                get_register("Icons")["pause"] = self.canvas.create_image(get_register("Config")["middle-x"],
                                                                          get_register("Config")["middle-y"] / 2,
                                                                          image=get_register("Icons")["pause-id"])
                self.pause_states()

                self.canvas.itemconfig(texts["pause"], text="")
                self._root.update()
            elif self.xControl["Back"] and get_stats("Modes")["pause"] and (not get_stats("Modes")["store"]) and (
                    not get_stats("Modes")["teleport"]) and \
                    (not get_stats("Modes")["window"]) and (not get_stats("Modes")["present"]) and (
                    not get_stats("Modes")["cheater"]):
                get_stats("Modes")["pause"] = False

                self.canvas.itemconfig("Config")(get_register("Icons")["pause"], state=HIDDEN)
                self.canvas.itemconfig("Config")(texts["pause"], text="")

                get_stats("Temp")["pause/back-to-menu"].destroy()
                get_stats("Temp")['pause/menu_frame'].destroy()
                get_stats("Temp")["s_frame"].destroy()

                self.canvas.delete(get_stats("Temp")['pause/toline'])
                # self.canvas.delete(get_stats("Temp")['pause/bottom.line'])
                self.canvas.delete(get_stats("Temp")['pause/menu'])
                self.canvas.delete(get_stats("Temp")['pause/bg'])

                self._root.update()
            if self.xControl["Y"] and get_stats("Stats")["teleports"] > 0 and (not get_stats("Modes")["teleport"]):
                get_stats("Modes")["pause"] = True
                self.pause_states()

                get_stats("Modes")["teleport"] = True

                get_stats("Modes")["tp"](self.canvas, get_register("Config"), get_stats("Stats"), get_stats("Modes"),
                                         get_stats("TP"))
            if self.xControl["X"] and (not get_stats("Modes")["store"]):
                get_stats("Modes")["pause"] = True
                self.pause_states()
                get_stats("Modes")["store"] = True
                self.log.debug("bub_move", "Creating Store() to variable \"store\"")
                self.log.debug("bub_move", "storemode=" + str(get_stats("Modes")["store"]))
                get_stats("Commands")["store"] = Store(self.canvas, self.log, get_register("Config"), get_stats("Modes"),
                                                       get_stats("Stats"), get_register("Icons"),
                                                       get_register("Foreground"),
                                                       self.font, self.launcherCfg)
            # if event.char == "/": CheatEngine().event_handler(self.canvas, get_stats("Modes"), get_stats("Stats"),
            # get_register("Config"), get_stats("Temp"), self.log, get_register("Background"), bubble, event,
            # self.bub) if get_stats("Modes")[ "cheater"]: CheatEngine().input_event_handler(self.canvas, self.log,
            # get_stats("Stats"), get_register("Background"), bubble, event, get_register("Config"), self.bub,
            # get_stats("Temp"), get_stats("Modes"))

            if self.xControl["Back"]:
                s.save()
            self._root.update()

            sleep(0.01)

    def movementChangeDaemon(self):
        time2 = time()
        while not self.returnmain:
            time1 = time()

            try:
                # print(time1 - time2)
                # print(1/(time1 - time2))
                self.move_fps = 1 / (time1 - time2)
            except ZeroDivisionError:
                pass
            time2 = time()
            Thread(None, lambda: self._movent()).start()
            sleep(0.01)

    def _xboxInput(self):
        time2 = time()
        while not self.returnmain:
            self.xbox.update()
            a = [int(self.xbox.leftJoystickX * 7), int(self.xbox.leftJoystickY * 7)]
            b = [int(self.xbox.rightJoystickX * 7), int(self.xbox.rightJoystickY * 7)]
            self.xControl["LeftJoystick"] = a
            self.xControl["RightJoystick"] = b
            self.xControl["A"] = bool(self.xbox.a)
            self.xControl["B"] = bool(self.xbox.b)
            self.xControl["X"] = bool(self.xbox.x)
            self.xControl["Y"] = bool(self.xbox.y)
            self.xControl["Back"] = bool(self.xbox.back)
            self.xControl["Start"] = bool(self.xbox.start)
            self.xControl["LeftBumper"] = bool(self.xbox.leftBumper)
            self.xControl["RightBumper"] = bool(self.xbox.rightBumper)
            self.xControl["LeftTrigger"] = int((self.xbox.leftBumper + 1) / 2 * 7)
            self.xControl["RightTrigger"] = int((self.xbox.rightBumper + 1) / 2 * 7)
            self.xControl["UpDPad"] = bool(self.xbox.upDPad)
            self.xControl["DownDPad"] = bool(self.xbox.downDPad)
            self.xControl["LeftDPad"] = bool(self.xbox.leftDPad)
            self.xControl["RightDPad"] = bool(self.xbox.rightDPad)

    def xboxDeamon(self):
        time2 = time()
        while not self.returnmain:
            time1 = time()

            try:
                # print(time1 - time2)
                # print(1/(time1 - time2))
                self.xmove_fps = 1 / (time1 - time2)
            except ZeroDivisionError:
                self.xmove_fps = 1
            time2 = time()
            Thread(None, lambda: self.xMovement()).start()
            sleep(0.01)

    def xMovement(self):
        if get_stats("Modes")["present"]:
            if self.xControl["A"]:
                if False != get_stats("Commands")["present"] != True:
                    # noinspection PyUnresolvedReferences
                    get_stats("Commands")["present"].exit(self.canvas)
                    get_stats("Modes")["pause"] = False
                    get_stats("Modes")["present"] = False
                    get_stats("Stats")["scorestate-time"] = get_stats("Temp")["scorestate-save"] + time()
                    get_stats("Stats")["secure-time"] = get_stats("Temp")["secure-save"] + time()
                    get_stats("Stats")["timebreak-time"] = get_stats("Temp")["timebreak-save"] + time()
                    get_stats("Stats")["confusion-time"] = get_stats("Temp")["confusion-save"] + time()
                    get_stats("Stats")["slowmotion-time"] = get_stats("Temp")["slowmotion-save"] + time()
                    get_stats("Stats")["paralis-time"] = get_stats("Temp")["paralis-save"] + time()
                    get_stats("Stats")["shotspeed-time"] = get_stats("Temp")["shotspeed-save"] + time()
                    get_stats("Stats")["notouch-time"] = get_stats("Temp")["notouch-save"] + time()

        if (not get_stats("Modes")["teleport"]) and (not get_stats("Modes")["store"]) and (
                not get_stats("Modes")["window"]):
            if not get_stats("Modes")["pause"]:
                if not get_stats("Stats")["paralis"]:
                    x, y = get_coords(self.canvas, self.ship["id"])
                    if get_stats("Stats")["speedboost"]:
                        a = 6
                    else:
                        a = 1

                    self.canvas.move(self.ship["id"],
                                     (get_stats("Stats")["shipspeed"] / (self.xmove_fps / 4) + a) * self.xControl[
                                         "LeftJoystick"][0] / 7,
                                     -((get_stats("Stats")["shipspeed"] / (self.xmove_fps / 4) + a) * self.xControl[
                                         "LeftJoystick"][1] / 7))
                    self.canvas.update()

                    # if self.xControl['Up']:
                    #     if y > 72 + get_register("Config")["game"]["ship-radius"]:
                    #         self.canvas.move(self.ship["id"], 0, (-get_stats("Stats")["shipspeed"] / (self.move_fps / 4) - a))
                    #         self._root.update()
                    # elif self.xControl['Down']:
                    #     if y < get_register("Config")["height"] - get_register("Config")["game"]["ship-radius"]:
                    #         self.canvas.move(self.ship["id"], 0, (get_stats("Stats")["shipspeed"] / (self.move_fps / 4) + a))
                    #         self._root.update()
                    # elif self.xControl['Left']:
                    #     if x > 0 + get_register("Config")["game"]["ship-radius"]:
                    #         self.canvas.move(self.ship["id"], (-get_stats("Stats")["shipspeed"] / (self.move_fps / 4) - a), 0)
                    #         self._root.update()
                    # elif self.xControl['Right']:
                    #     if x < get_register("Config")["width"] - get_register("Config")["game"]["ship-radius"]:
                    #         self.canvas.move(self.ship["id"], (get_stats("Stats")["shipspeed"] / (self.move_fps / 4) + a), 0)
                    #         self._root.update()
                    # get_stats("Stats")["ship-position"] = get_coords(self.canvas, self.ship["id"])

    @staticmethod
    def _press(e):
        if e.keysym == "Up":
            get_stats("Pressed")["Up"] = True
        if e.keysym == "Down":
            get_stats("Pressed")["Down"] = True
        if e.keysym == "Left":
            get_stats("Pressed")["Left"] = True
        if e.keysym == "Right":
            get_stats("Pressed")["Right"] = True

    @staticmethod
    def _release(e):
        if e.keysym == "Up":
            get_stats("Pressed")["Up"] = False
        if e.keysym == "Down":
            get_stats("Pressed")["Down"] = False
        if e.keysym == "Left":
            get_stats("Pressed")["Left"] = False
        if e.keysym == "Right":
            get_stats("Pressed")["Right"] = False

    @staticmethod
    def up_press(event):
        get_stats("Pressed")["Up"] = True

    @staticmethod
    def down_press(event):
        get_stats("Pressed")["Down"] = True

    @staticmethod
    def left_press(event):
        get_stats("Pressed")["Left"] = True

    @staticmethod
    def right_press(event):
        get_stats("Pressed")["Right"] = True

    def up_release(self, event):
        get_stats("Pressed")["Up"] = False
        if get_stats("Modes")["teleport"]:
            x, y = get_coords(self.canvas, get_stats("TP")["id1"])
            if y > 72 + 5:
                self.canvas.move(get_stats("TP")["id1"], 0, -5)
                self.canvas.move(get_stats("TP")["id2"], 0, -5)
                self.canvas.move(get_stats("TP")["id3"], 0, -5)
                self.canvas.move(get_stats("TP")["id4"], 0, -5)
        if get_stats("Modes")["store"]:
            if event.keysym == "Up":
                get_stats("Commands")["store"].set_selected(self.canvas, -1)
            if event.keysym == "Right":
                get_stats("Commands")["store"].set_selected(self.canvas,
                                                            int((get_register("Config")["height"] - 215) / 140 + 1))

    def down_release(self, event):
        get_stats("Pressed")["Down"] = False
        if get_stats("Modes")["teleport"]:
            x, y = get_coords(self.canvas, get_stats("TP")["id1"])
            if y < get_register("Config")["height"] - 105 - 5:
                self.canvas.move(get_stats("TP")["id1"], 0, 5)
                self.canvas.move(get_stats("TP")["id2"], 0, 5)
                self.canvas.move(get_stats("TP")["id3"], 0, 5)
                self.canvas.move(get_stats("TP")["id4"], 0, 5)
        if get_stats("Modes")["store"]:
            get_stats("Commands")["store"].set_selected(self.canvas, 1)

    def left_release(self, event):
        get_stats("Pressed")["Left"] = False
        if get_stats("Modes")["teleport"]:
            x, y = get_coords(self.canvas, get_stats("TP")["id1"])
            if x > 0 + 5:
                self.canvas.move(get_stats("TP")["id1"], -5, 0)
                self.canvas.move(get_stats("TP")["id2"], -5, 0)
                self.canvas.move(get_stats("TP")["id3"], -5, 0)
                self.canvas.move(get_stats("TP")["id4"], -5, 0)
        if get_stats("Modes")["store"]:
            get_stats("Commands")["store"].set_selected(self.canvas,
                                                        int(-((get_register("Config")["height"] - 215) / 140 + 1)))

    def right_release(self, event):
        get_stats("Pressed")["Right"] = False
        if get_stats("Modes")["teleport"]:
            x, y = get_coords(self.canvas, get_stats("TP")["id1"])
            if x < get_register("Config")["width"] - 5:
                self.canvas.move(get_stats("TP")["id1"], 5, 0)
                self.canvas.move(get_stats("TP")["id2"], 5, 0)
                self.canvas.move(get_stats("TP")["id3"], 5, 0)
                self.canvas.move(get_stats("TP")["id4"], 5, 0)
        if get_stats("Modes")["store"]:
            get_stats("Commands")["store"].set_selected(self.canvas,
                                                        int((get_register("Config")["height"] - 215) / 140 + 1))

    # noinspection PyMethodMayBeStatic,PyMethodMayBeStatic
    def shot(self, event):
        print("WARNING: Using shot event. This not been used anymore, because of incompatibility.", file=sys.stderr)

    # def shot(self, event):
    #     if (not get_stats("Modes")["teleport"]) and (not get_stats("Modes")["store"]) and (not get_stats("Modes")["window"]):
    #         if not get_stats("Modes")["pause"]:
    #             if not get_stats("Stats")["paralis"]:
    #                 if event.keysym == "space":
    #                     # noinspection PyTypeChecker
    #                     create_shot(self.canvas, self.ammo, get_register("Config"), self.ship, get_stats("Stats"))

    def auto_save(self):
        while not self.returnmain:
            Maintance.auto_save(self.saveName, get_stats("Stats"), get_stats("Bubbles"))
            print(self.returnmain)
            sleep(2)

    def moveSingleBubble(self, index):
        try:
            for j in range(len(get_stats("Bubbles")["bub-id"][index]) - 1, -1, -1):
                if not get_stats("Bubbles")["bub-action"][index] == "Null":
                    if get_stats("Stats")["slowmotion"]:
                        self.canvas.move(get_stats("Bubbles")["bub-id"][index][j],
                                         -get_stats("Bubbles")["bub-speed"][index] / 10 / (self.xmove_fps / 4), 0)
                    else:
                        self.canvas.move(get_stats("Bubbles")["bub-id"][index][j],
                                         -get_stats("Bubbles")["bub-speed"][index] / (self.xmove_fps / 4), 0)
                    self._root.update()
                x, y, = get_coords(self.canvas, get_stats("Bubbles")["bub-id"][index][j])
                get_stats("Bubbles")["bub-position"][index] = [x, y]
                self.canvas.update()
        except IndexError:
            pass
        except TclError:
            exit(0)
        except AttributeError:
            exit(0)

    def move_bubbles(self):
        """
        The base of motion for the bubbles
        """
        try:
            for bub_index in range(len(get_stats("Bubbles")["bub-id"])):
                Thread(None, lambda: self.moveSingleBubble(bub_index)).start()
        except IndexError:
            pass
        except TclError:
            exit(0)

    def moveBubblesDaemon(self):
        time2 = time()
        while not self.returnmain:
            time1 = time()

            try:
                # print(time1 - time2)
                # print(1/(time1 - time2))
                self.bub_fps = 1 / (time1 - time2)
            except ZeroDivisionError:
                self.bub_fps = 1
            time2 = time()
            Thread(None, lambda: self.move_bubbles()).start()

    def checkLangItem(self, item, alt) -> str:
        return get_register("Language")[item] if item in get_register("Language").keys() else alt

    # noinspection PyAttributeOutsideInit
    def start_game(self, save_name, save_build):
        """
        Starts the game.
        """
        self.saveName = save_name
        self.saveBuild = save_build
        from .utils import xbox
        from .utils.get_set import get_canvas, set_canvas
        from .stats import get_stats
        from .registry import get_register, add_register, set_register, get_value, register

        # Create canvas.
        self.canvas = Canvas(self._root, height=get_register("Config")["height"], width=get_register("Config")["width"],
                             highlightthickness=0)
        self.canvas.place(x=0, y=0)
        self.canvas.update()
        self.canvas.update_idletasks()
        self._root.update()
        self._root.update_idletasks()
        set_canvas(self.canvas)
        t0 = self.canvas.create_rectangle(0, 0, get_register("Config")["width"], get_register("Config")["height"],
                                          fill="#3f3f3f", outline="#3f3f3f")
        t1 = self.canvas.create_text(get_register("Config")["middle-x"], get_register("Config")["middle-y"] - 30,
                                     text="Loading...", font=(
                get_register("Config")["font"]["family"], 50 + get_register("Config")["font"]["size"]), fill="#afafaf")
        t2 = self.canvas.create_text(get_register("Config")["middle-x"], get_register("Config")["middle-y"] + 20,
                                     text="Check Version compatibility", font=(
                get_register("Config")["font"]["family"], 15 + get_register("Config")["font"]["size"]), fill="#afafaf")
        self.canvas.update()
        self.canvas.update_idletasks()

        print("[SaveLoading]: Loading Save %s" % save_name)
        print("[SaveLoading]: Build of Save is %s" % save_build)

        self.saveBuild = int(self.saveBuild)

        if type(self.saveBuild) != int:
            self.canvas.itemconfig(t1, text="Game can't load!")
            self.canvas.itemconfig(t2, text="Build version isn't an integer.")
            Button(self._root, relief=FLAT, text=self.checkLangItem("general.back-to-title", "Back to title"),
                   bg="#7f7f7f", fg="white",
                   font=[get_register("Config")["font"]["family"], 20 + get_register("Config")["font"]["size"]],
                   command=lambda: self.__init__(self.launcher_cfg))
            self.canvas.mainloop()
            exit(0)

        # Convert Save if needed.
        if self.saveBuild == -1:
            self.canvas.itemconfig(t1, text="Version information not read!")
            self.canvas.itemconfig(t2, text="Check if you have a info.data file. So not, please go back to title.")
        elif self.saveBuild < 7:
            self.canvas.itemconfig(t1, text="Version incompatible")
            self.canvas.itemconfig(t2, text="The build {version} is not compatible with this game.".format(
                version=self.saveBuild))

            text = "Return to Title"
            try:
                text = get_register("Language")["error.return"]
            except KeyError:
                text = "Return to Title"
            self.incompBtn = Button(self.canvas, relief=FLAT, text=text, bg="#afafaf", width=7,
                                    font=[get_register("Config")["font"]["family"],
                                          15 + get_register("Config")["font"]["size"]])

            self.canvas.mainloop()
        if self.saveBuild < 16:
            print("converting")
            Convert("slots/" + self.saveName + "/info.json").convert()
            Convert("slots/" + self.saveName + "/game.json").convert()
            Convert("slots/" + self.saveName + "/bubble.json").convert()
        if 7 >= self.saveBuild < 16:
            get_stats("")["seed"] = 0

        # Reload Save Data
        set_stats("Stats", Reader("slots/" + self.saveName + "/game.data").get_decoded())
        try:
            self.saveInfo = Reader("slots/" + self.saveName + "/info.data").get_decoded()
        except FileNotFoundError:
            self.saveBuild = -1

        self.t0 = t0
        self.t1 = t1
        self.t2 = t2

        print("Game Stating")
        print("[Game]:", "Starting XboxController")
        self.xbox = xbox.XboxController()
        print("[Game]:", "Started XboxController")

        self.xControl = dict()

        self.canvas = get_canvas()
        if self.canvas is None:
            raise TypeError("Canvas is None. Can't start the game. Report this on Qboi123's Github")

        a = [int(self.xbox.leftJoystickX * 7), int(self.xbox.leftJoystickY * 7)]
        b = [int(self.xbox.rightJoystickX * 7), int(self.xbox.rightJoystickY * 7)]
        self.xControl["LeftJoystick"] = a
        self.xControl["RightJoystick"] = b
        self.xControl["A"] = bool(self.xbox.a)
        self.xControl["B"] = bool(self.xbox.b)
        self.xControl["X"] = bool(self.xbox.x)
        self.xControl["Y"] = bool(self.xbox.y)
        self.xControl["Start"] = bool(self.xbox.start)
        self.xControl["Back"] = bool(self.xbox.back)
        self.xControl["LeftBumper"] = bool(self.xbox.leftBumper)
        self.xControl["RightBumper"] = bool(self.xbox.rightBumper)
        self.xControl["LeftTrigger"] = int((self.xbox.leftBumper + 1) / 2 * 7)
        self.xControl["RightTrigger"] = int((self.xbox.rightBumper + 1) / 2 * 7)
        t0 = self.t0
        t1 = self.t1
        t2 = self.t2
        self.canvas.update()

        # Pre-Initialize
        # self.modLoader.pre_initialize(self)

        self.canvas.itemconfig(t1, text="Loading...")
        self.canvas.itemconfig(t2, text="Loading Config")
        self.canvas.update()

        # Reload config resolution.
        get_register("Config")["height"] = self.canvas.winfo_height()
        get_register("Config")["width"] = self.canvas.winfo_width()

        # Copy self.canvas into c.
        c = self.canvas

        # Reload middle positions.
        mid_x = get_register("Config")["width"] / 2
        mid_y = get_register("Config")["height"] / 2

        self.canvas.itemconfig(t1, text="Loading Bubbles")
        self.canvas.itemconfig(t2, text="Creating Dicts")
        self.canvas.update()

        # Adding the dictionaries for the bubbles. With different res.
        # get_register("Bub")["Normal"] = dict()
        # get_register("Bub")["Triple"] = dict()
        # get_register("Bub")["Double"] = dict()
        # get_register("Bub")["Kill"] = dict()
        # get_register("Bub")["SpeedUp"] = dict()
        # get_register("Bub")["SpeedDown"] = dict()
        # get_register("Bub")["Ultimate"] = dict()
        # get_register("Bub")["Up"] = dict()
        # get_register("Bub")["Teleporter"] = dict()
        # get_register("Bub")["SlowMotion"] = dict()
        # get_register("Bub")["DoubleState"] = dict()
        # get_register("Bub")["Protect"] = dict()
        # get_register("Bub")["ShotSpdStat"] = dict()
        # get_register("Bub")["HyperMode"] = dict()
        # get_register("Bub")["TimeBreak"] = dict()
        # get_register("Bub")["Confusion"] = dict()
        # get_register("Bub")["Paralis"] = dict()
        # get_register("Bub")["StoneBub"] = dict()
        # get_register("Bub")["NoTouch"] = dict()
        # get_register("Bub")["Key"] = dict()
        # get_register("Bub")["Diamond"] = dict()
        # get_register("Bub")["Present"] = dict()
        # get_register("Bub")["SpecialKey"] = dict()

        # _min = 21
        # _max = 80
        # 
        # # Adding the different resolutions to the bubbles.
        # for i in range(_min, _max + 1):
        #     get_register("Bub")["Normal"][i] = __init__.createbubble_image((i, i), None, "white")
        #     get_register("Bub")["Double"][i] = __init__.createbubble_image((i, i), None, "gold")
        #     get_register("Bub")["Triple"][i] = __init__.createbubble_image((i, i), None, "blue", "#007fff", "#00ffff", "white")
        #     get_register("Bub")["SpeedDown"][i] = __init__.createbubble_image((i, i), None, "#ffffff", "#a7a7a7", "#7f7f7f",
        #                                                            "#373737")
        #     get_register("Bub")["SpeedUp"][i] = __init__.createbubble_image((i, i), None, "#ffffff", "#7fff7f", "#00ff00",
        #                                                          "#007f00")
        #     get_register("Bub")["Up"][i] = __init__.createbubble_image((i, i), None, "#00ff00", "#00ff00", "#00000000", "#00ff00")
        #     get_register("Bub")["Ultimate"][i] = __init__.createbubble_image((i, i), None, "gold", "gold", "orange", "gold")
        #     get_register("Bub")["Kill"][i] = __init__.createbubble_image((i, i), None, "#7f0000", "#7f007f", "#7f0000", )
        #     get_register("Bub")["Teleporter"][i] = __init__.createbubble_image((i, i), None, "#7f7f7f", "#7f7f7f", "#ff1020",
        #                                                             "#373737")
        #     get_register("Bub")["SlowMotion"][i] = __init__.createbubble_image((i, i), None, "#ffffffff", "#00000000", "#000000ff")
        #     get_register("Bub")["DoubleState"][i] = __init__.createbubble_image((i, i), None, "gold", "#00000000", "gold", "gold")
        #     get_register("Bub")["Protect"][i] = __init__.createbubble_image((i, i), None, "#00ff00", "#3fff3f", "#7fff7f",
        #                                                          "#9fff9f")
        #     get_register("Bub")["ShotSpdStat"][i] = __init__.createbubble_image((i, i), None, "#ff7f00", "#ff7f00", "gold")
        #     get_register("Bub")["HyperMode"][i] = __init__.createbubble_image((i, i), None, "black", "black", "white", "black")
        #     get_register("Bub")["TimeBreak"][i] = __init__.createbubble_image((i, i), None, "red", "orange", "yellow", "white")
        #     get_register("Bub")["Confusion"][i] = __init__.createbubble_image((i, i), None, "black", "purple", "magenta", "white")
        #     get_register("Bub")["Paralis"][i] = __init__.createbubble_image((i, i), None, "#ffff00", "#ffff00", "#ffff7f",
        #                                                          "#ffffff")
        #     get_register("Bub")["StoneBub"][i] = __init__.createbubble_image((i, i), None, "black", "orange", "yellow")
        #     get_register("Bub")["NoTouch"][i] = __init__.createbubble_image((i, i), None, "#7f7f7f", "#7f7f7f", "#7f7f7f",
        #                                                          "#373737")
        # 
        #     self.canvas.itemconfig(t1, text="Loading Bubbles Sizes")
        #     self.canvas.itemconfig(t2, text="Loading %s of %s" % (i - _min, _max - 1 - _min))
        #     self.canvas.update()
        # 
        # # Adding the static-resolution-bubbles.
        # get_register("Bub")["Key"][60] = PhotoImage(file="" + self.gameversion_dir + "/data/bubbles/Key.png")
        # get_register("Bub")["Diamond"][36] = PhotoImage(
        #     file="" + self.gameversion_dir + "/data/bubbles/Diamond.png")
        # get_register("Bub")["Present"][40] = PhotoImage(
        #     file="" + self.gameversion_dir + "/data/bubbles/Present.png")
        # # noinspection PyTypeChecker
        # get_register("Bub")["Coin"] = PhotoImage(file="" + self.gameversion_dir + "/data/CoinBub.png")
        # get_register("Bub")["SpecialKey"][48] = PhotoImage(
        #     file="" + self.gameversion_dir + "/data/bubbles/SpecialMode.png")
        # 
        # for i in self.bub.keys():
        #     print("%s: %s" % (i, get_register("Bub")[i]))

        # Adding ship image.
        self.ship["image"] = PhotoImage(file="" + self.gameversion_dir + "/data/Ship.png")

        # Reload stats with auto-restore.
        set_stats("Stats", Maintance.auto_restore_stats(self.saveName))

        self.canvas.itemconfig(t1, text="Loading Background")
        self.canvas.itemconfig(t2, text="Normal")
        self.canvas.update()

        # Getting the normal background.
        add_register("Background", {})
        register("Background", "normal", PhotoImage(file="" + self.gameversion_dir + "/data/BackGround.png"))

        self.canvas.itemconfig(t1, text="Loading Icons")
        self.canvas.itemconfig(t2, text="")
        self.canvas.update()

        # Getting the store-icons.
        add_register("Icons", {})
        register("Icons", "store-pack", list())
        get_value("Icons", "store-pack").append(
            PhotoImage(file="" + self.gameversion_dir + "/data/Images/StoreItems/Key.png"))
        self.canvas.itemconfig(t2, text="Store Item: Key")
        self.canvas.update()
        get_value("Icons", "store-pack").append(
            PhotoImage(file="" + self.gameversion_dir + "/data/Images/StoreItems/Teleport.png"))
        self.canvas.itemconfig(t2, text="Store Item: Teleport")
        self.canvas.update()
        get_value("Icons", "store-pack").append(
            PhotoImage(file="" + self.gameversion_dir + "/data/Images/StoreItems/Shield.png"))
        self.canvas.itemconfig(t2, text="Store Item: Shield")
        self.canvas.update()
        get_value("Icons", "store-pack").append(
            PhotoImage(file="" + self.gameversion_dir + "/data/Images/StoreItems/DiamondBuy.png"))
        self.canvas.itemconfig(t2, text="Store Item: Diamond")
        self.canvas.update()
        get_value("Icons", "store-pack").append(
            PhotoImage(file="" + self.gameversion_dir + "/data/Images/StoreItems/BuyACake.png"))
        self.canvas.itemconfig(t2, text="Store Item: Buy A Cake")
        self.canvas.update()
        get_value("Icons", "store-pack").append(
            PhotoImage(file="" + self.gameversion_dir + "/data/Images/StoreItems/Pop_3_bubs.png"))
        self.canvas.itemconfig(t2, text="Store Item: Pop 3 Bubbles")
        self.canvas.update()
        get_value("Icons", "store-pack").append(
            PhotoImage(file="" + self.gameversion_dir + "/data/Images/StoreItems/PlusLife.png"))
        self.canvas.itemconfig(t2, text="Store Item: PlusLife")
        self.canvas.update()
        get_value("Icons", "store-pack").append(
            PhotoImage(file="" + self.gameversion_dir + "/data/Images/StoreItems/SpeedBoost.png"))
        self.canvas.itemconfig(t2, text="Store Item: Speedboost")
        self.canvas.update()
        get_value("Icons", "store-pack").append(
            PhotoImage(file="" + self.gameversion_dir + "/data/Images/StoreItems/SpecialMode.png"))
        self.canvas.itemconfig(t2, text="Store Item: Special Mode")
        self.canvas.update()
        get_value("Icons", "store-pack").append(
            PhotoImage(file="" + self.gameversion_dir + "/data/Images/StoreItems/DoubleScore.png"))
        self.canvas.itemconfig(t2, text="Double Score")
        self.canvas.update()
        get_value("Icons", "store-pack").append(None)
        get_value("Icons", "store-pack").append(None)
        get_value("Icons", "store-pack").append(None)
        get_value("Icons", "store-pack").append(None)

        self.canvas.itemconfig(t1, text="Loading Background")
        self.canvas.itemconfig(t2, text="Line")
        self.canvas.update()
        # Unknown
        register("Background", "line", PhotoImage(file="" + self.gameversion_dir + "/data/LineIcon.png"))

        self.canvas.itemconfig(t1, text="Loading Foreground")
        self.canvas.itemconfig(t2, text="For Bubble Gift")
        self.canvas.update()

        add_register("Foreground", {})
        # Setting present foreground
        register("Foreground", "present-fg", PhotoImage(
            file="" + self.gameversion_dir + "/data/EventBackground.png"))

        self.canvas.itemconfig(t1, text="Loading Icons")
        self.canvas.itemconfig(t2, text="Circle")
        self.canvas.update()

        # Setting present icons.
        register("Icons", "circle", PhotoImage(file="" + self.gameversion_dir + "/data/Circle.png"))

        self.canvas.itemconfig(t1, text="Loading Icons")
        self.canvas.itemconfig(t2, text="Present")
        self.canvas.update()

        register("Icons", "present", PhotoImage(file="" + self.gameversion_dir + "/data/Present.png"))

        self.canvas.itemconfig(t1, text="Loading Foreground")
        self.canvas.itemconfig(t2, text="Store FG")
        self.canvas.update()

        # Setting store foreground
        register("Foreground", "store-fg", PhotoImage(file="" + self.gameversion_dir + "/data/FG2.png"))

        self.canvas.itemconfig(t1, text="Loading Icons")
        self.canvas.itemconfig(t2, text="Store: Diamond & Coin")
        self.canvas.update()

        # Setting standard store icons.
        register("Icons", "store-diamond", PhotoImage(
            file="" + self.gameversion_dir + "/data/Diamond.png"))
        register("Icons", "store-coin", PhotoImage(file="" + self.gameversion_dir + "/data/Coin.png"))

        self.canvas.itemconfig(t1, text="Loading Icons")
        self.canvas.itemconfig(t2, text="Pause")
        self.canvas.update()

        # Setting pause-icon.
        register("Icons", "pause-id", PhotoImage(file="" + self.gameversion_dir + "/data/Pause.png"))

        self.canvas.itemconfig(t1, text="Loading Icons")
        self.canvas.itemconfig(t2, text="SlowMotion")
        self.canvas.update()

        # Setting slowmotion-icon.
        register("Icons", "slowmotion", PhotoImage(
            file="" + self.gameversion_dir + "/data/SlowMotionIcon.png"))

        self.canvas.itemconfig(t1, text="Loading Background")
        self.canvas.itemconfig(t2, text="Special")
        self.canvas.update()

        # Setting special background.
        register("Background", "special", PhotoImage(
            file="" + self.gameversion_dir + "/data/Images/Backgrounds/GameBG Special2.png"))

        # Setting normal background.
        register("Background", "normal", PhotoImage(
            file="" + self.gameversion_dir + "/data/Images/Backgrounds/GameBG2.png"))
        self.canvas.itemconfig(t2, text="Normal")
        self.canvas.update()

        # Setting background from nothing to normal.
        register("Background", "id", self.canvas.create_image(0, 0, anchor=NW,
                                                              image=get_register("Background")["normal"]))

        # Creating shi
        self.ship["id"] = self.canvas.create_image(7.5, 7.5, image=self.ship["image"])
        print(self.ship["id"])

        # Moving ship to position
        c.move(self.ship["id"], get_stats("Stats")["ship-position"][0], get_stats("Stats")["ship-position"][1])

        self.canvas.itemconfig(t1, text="Creating Stats objects")
        self.canvas.itemconfig(t2, text="")

        add_register("Panels", {})

        # Initializing the panels for the game.
        register("Panels", "game/top", self.canvas.create_rectangle(
            -1, -1, get_register("Config")["width"], 69, fill="darkcyan"
        ))

        # Create seperating lines.
        self.canvas.create_line(0, 70, get_register("Config")["width"], 70, fill="lightblue")
        self.canvas.create_line(0, 69, get_register("Config")["width"], 69, fill="white")

        self.canvas.create_text(55, 30, text=get_register("Language")["info.score"], fill='orange',
                                font=[get_register("Config")["font"]["family"],
                                      15 + get_register("Config")["font"]["size"]])
        self.canvas.itemconfig(t2, text="Score")
        self.canvas.create_text(110, 30, text=get_register("Language")["info.level"], fill='orange',
                                font=[get_register("Config")["font"]["family"],
                                      15 + get_register("Config")["font"]["size"]])
        self.canvas.itemconfig(t2, text="Level")
        self.canvas.create_text(165, 30, text=get_register("Language")["info.speed"], fill='orange',
                                font=[get_register("Config")["font"]["family"],
                                      15 + get_register("Config")["font"]["size"]])
        self.canvas.itemconfig(t2, text="Speed")
        self.canvas.create_text(220, 30, text=get_register("Language")["info.lives"], fill='orange',
                                font=[get_register("Config")["font"]["family"],
                                      15 + get_register("Config")["font"]["size"]])
        self.canvas.itemconfig(t2, text="Lives")
        self.canvas.create_text(330, 30, text=get_register("Language")["info.state.score"],
                                fill="gold",
                                font=[get_register("Config")["font"]["family"],
                                      15 + get_register("Config")["font"]["size"]])
        self.canvas.itemconfig(t2, text="Score State")
        self.canvas.create_text(400, 30, text=get_register("Language")["info.state.protect"],
                                fill="gold",
                                font=[get_register("Config")["font"]["family"],
                                      15 + get_register("Config")["font"]["size"]])
        self.canvas.itemconfig(t2, text="State Protect")
        self.canvas.create_text(490, 30, text=get_register("Language")["info.state.slowmotion"],
                                fill="gold",
                                font=[get_register("Config")["font"]["family"],
                                      15 + get_register("Config")["font"]["size"]])
        self.canvas.itemconfig(t2, text="State Slow Motion")
        self.canvas.create_text(580, 30, text=get_register("Language")["info.state.confusion"],
                                fill="gold",
                                font=[get_register("Config")["font"]["family"],
                                      15 + get_register("Config")["font"]["size"]])
        self.canvas.itemconfig(t2, text="State Confusion")
        self.canvas.create_text(670, 30, text=get_register("Language")["info.state.timebreak"],
                                fill="gold",
                                font=[get_register("Config")["font"]["family"],
                                      15 + get_register("Config")["font"]["size"]])
        self.canvas.itemconfig(t2, text="State Time Break")
        self.canvas.create_text(760, 30, text=get_register("Language")["info.state.spdboost"],
                                fill="gold",
                                font=[get_register("Config")["font"]["family"],
                                      15 + get_register("Config")["font"]["size"]])
        self.canvas.itemconfig(t2, text="State SpeedBoost")
        self.canvas.create_text(850, 30, text=get_register("Language")["info.state.paralis"],
                                fill="gold",
                                font=[get_register("Config")["font"]["family"],
                                      15 + get_register("Config")["font"]["size"]])
        self.canvas.itemconfig(t2, text="State Paralize")
        self.canvas.create_text(940, 30, text=get_register("Language")["info.state.shotspeed"],
                                fill="gold",
                                font=[get_register("Config")["font"]["family"],
                                      15 + get_register("Config")["font"]["size"]])
        self.canvas.itemconfig(t2, text="State Ammo Speed")
        self.canvas.create_text(1030, 30, text=get_register("Language")["info.state.notouch"],
                                fill="gold",
                                font=[get_register("Config")["font"]["family"],
                                      15 + get_register("Config")["font"]["size"]])
        self.canvas.itemconfig(t2, text="State Ghost Mode")
        self.canvas.create_text(1120, 30, text=get_register("Language")["info.tps"], fill='gold',
                                font=[get_register("Config")["font"]["family"],
                                      15 + get_register("Config")["font"]["size"]])
        self.canvas.itemconfig(t2, text="Teleports")
        c.create_image(1185, 30, image=get_register("Icons")["store-diamond"])
        self.canvas.itemconfig(t2, text="Diamonds")
        c.create_image(1185, 50, image=get_register("Icons")["store-coin"])
        self.canvas.itemconfig(t2, text="Coins")

        self.canvas.itemconfig(t1, text="Creating Stats Data")
        self.canvas.itemconfig(t2, text="")

        add_register("Texts", {})

        # Game information values.
        register("Texts", "score", self.canvas.create_text(55, 50, fill='cyan'))
        self.canvas.itemconfig(t2, text="Score")
        register("Texts", "level", self.canvas.create_text(110, 50, fill='cyan'))
        self.canvas.itemconfig(t2, text="Level")
        register("Texts", "speed", self.canvas.create_text(165, 50, fill='cyan'))
        self.canvas.itemconfig(t2, text="Speed")
        register("Texts", "lives", self.canvas.create_text(220, 50, fill='cyan'))
        self.canvas.itemconfig(t2, text="Lives")
        register("Texts", "scorestate", self.canvas.create_text(330, 50, fill='cyan'))
        self.canvas.itemconfig(t2, text="State Score")
        register("Texts", "secure", self.canvas.create_text(400, 50, fill='cyan'))
        self.canvas.itemconfig(t2, text="State Protection")
        register("Texts", "slowmotion", self.canvas.create_text(490, 50, fill='cyan'))
        self.canvas.itemconfig(t2, text="State Slowmotion")
        register("Texts", "confusion", self.canvas.create_text(580, 50, fill='cyan'))
        self.canvas.itemconfig(t2, text="State Confusion")
        register("Texts", "timebreak", self.canvas.create_text(670, 50, fill='cyan'))
        self.canvas.itemconfig(t2, text="State Time Break")
        register("Texts", "speedboost", self.canvas.create_text(760, 50, fill='cyan'))
        self.canvas.itemconfig(t2, text="State SpeedBoost")
        register("Texts", "paralis", self.canvas.create_text(850, 50, fill='cyan'))
        self.canvas.itemconfig(t2, text="State Paralis")
        register("Texts", "shotspeed", self.canvas.create_text(940, 50, fill='cyan'))
        self.canvas.itemconfig(t2, text="State Ammo Speed")
        register("Texts", "notouch", self.canvas.create_text(1030, 50, fill='cyan'))
        self.canvas.itemconfig(t2, text="State Ghost Mode")
        register("Texts", "shiptp", self.canvas.create_text(1120, 50, fill='cyan'))
        self.canvas.itemconfig(t2, text="Teleports")
        register("Texts", "diamond", self.canvas.create_text(1210, 30, fill='cyan'))
        self.canvas.itemconfig(t2, text="Diamonds")
        register("Texts", "coin", self.canvas.create_text(1210, 50, fill='cyan'))
        self.canvas.itemconfig(t2, text="Coins")
        register("Texts", "level-view", self.canvas.create_text(mid_x, mid_y, fill='Orange', font=(
            get_register("Config")["font"]["family"], 50 + get_register("Config")["font"]["size"])))
        self.canvas.itemconfig(t2, text="Level View")

        register("Texts", "pause", self.canvas.create_text(mid_x, mid_y, fill='Orange', font=(
            get_value("Config", "font")["family"], 60 + get_value("Config", "font")["size"], "bold")))
        self.canvas.itemconfig(t2, text="Pauze")
        register("Icons", "pause", self.canvas.create_image(mid_x, mid_y, image=get_register("Icons")["pause-id"],
                                                            state=HIDDEN))
        self.canvas.itemconfig(t2, text="Pauze")

        # Threaded Automatic Save (TAS)
        # self.t_auto_save = StoppableThread(None, lambda: self.auto_save(), name="AutoSaveThread").start()

        kw = {}

        # for i in Ammo.requires:
        #     if i in self.__dict__.keys():
        #         kw[i] = self.__dict__[i]
        #     else:
        #         raise ClassRequirementInvalid("Requirement \"%s\" of class Ammo is invalid." % i)

        # self.c_ammo = Ammo()

        # Binding key-events for control
        self.canvas.itemconfig(t1, text="Binding Objects")
        self.canvas.itemconfig(t2, text="Main Binding")
        c.bind_all('<Key>',
                   lambda event: control(event))
        # get_stats("Modes"), get_register("Config"), self._root, self.canvas,
        # get_stats("Stats"),
        # get_stats("Bubbles"),
        # get_register("Background"), get_register("Texts"), get_stats("Commands"),
        # get_stats("Temp"), get_register("Panels"), get_register("Foreground"),
        # self.ship, get_stats("TP"), get_register("Language"),
        # self.return_main,
        # get_register("Icons"),
        # self.bub, get_register("Config")["font"]["family"], event, self.c_ammo,
        # self.launcherConfig))

        self.canvas.itemconfig(t2, text="Player Motion")
        c.bind_all("<KeyPress-Up>", lambda event: self.up_press(event))
        c.bind_all("<KeyPress-Down>", lambda event: self.down_press(event))
        c.bind_all("<KeyPress-Left>", lambda event: self.left_press(event))
        c.bind_all("<KeyPress-Right>", lambda event: self.right_press(event))

        c.bind_all("<KeyRelease-Up>", lambda event: self.up_release(event))
        c.bind_all("<KeyRelease-Down>", lambda event: self.down_release(event))
        c.bind_all("<KeyRelease-Left>", lambda event: self.left_release(event))
        c.bind_all("<KeyRelease-Right>", lambda event: self.right_release(event))
        c.bind_all("<Key-Z>", lambda event: self.r_update())

        # # Binding other key-events.
        # c.bind_all('Configure', lambda event: self.resize)

        print("Key-bindings binded to 'move_ship'")
        if len(get_stats("Bubbles")["bub-id"]) == 0:
            print("Bubbel-ID lijst is gelijk aan lengte nul.", file=sys.stderr)

        if len(get_stats("Bubbles")["bub-action"]) == 0:
            print("Bubble-actie lijst is gelijk aan lengte nul.", file=sys.stderr)

        if len(get_stats("Bubbles")["bub-speed"]) == 0:
            print("Bubbel-snelheid lijst is gelijk aan lengte nul.", file=sys.stderr)

        set_stats("Ammo", retime=time())

        stats = get_stats("Stats")

        self.canvas.itemconfig(t1, text="Fixing Saved States")
        self.canvas.itemconfig(t2, text="")

        if stats["scorestate-time"] <= time():
            stats["scorestate"] = 1
            stats["scorestate-time"] = time()
        if stats["secure-time"] <= time():
            stats["secure"] = False
            stats["secure-time"] = time()
        if stats["slowmotion-time"] <= time():
            stats["slowmotion"] = False
            stats["slowmotion-time"] = time()
        if stats["timebreak-time"] <= time():
            stats["timebreak"] = False
            stats["timebreak-time"] = time()
        if stats["confusion-time"] <= time():
            stats["confusion"] = False
            stats["confusion-time"] = time()
        if stats["speedboost-time"] <= time():
            stats["speedboost"] = False
            stats["speedboost-time"] = time()
        if stats["paralis-time"] <= time():
            stats["paralis"] = False
            stats["paralis-time"] = time()
        if stats["shotspeed-time"] <= time():
            stats["shotspeed"] = 0.1
            stats["shotspeed-time"] = time()
        if stats["special-level-time"] <= time():
            stats["special-level"] = False
            stats["special-level-time"] = time()
        else:
            self.canvas.itemconfig(get_register("Background")["id"], image=get_register("Background")["special"])
            self.canvas.itemconfig(get_register("Panels")["game/top"], fill="#3f3f3f")
        if stats["score"] < 0:
            print("The 'Score' variable under zero.", file=sys.stderr)
            stats["score"] = 0
        if stats["score"] > stats["hiscore"]:
            stats["hiscore"] = stats["score"]
        if stats["confusion"] and not stats["secure"]:
            pass
            # shuffling(get_stats("Bubbles"))

        set_stats("Bubbles", Maintance.auto_restore_bubbles(self.saveName))

        set_stat("Bubbles", active2=[])
        set_stat("Bubbles", active=0)

        set_stats("Stats", Maintance.auto_restore_stats(self.saveName))

        print("{DEBUG}: Stats after Restore at line(s) 1412 - 1415:")
        print("{DEBUG}: BUBBLES | %s" % get_stats("Bubbles"))

        start(get_stats("Bubbles"), self.saveName, get_stats("Stats"), get_register("Config"), get_register("Bubbles"),
              get_stats("Modes"),
              self.canvas)

        print("{DEBUG}: Stats after Start Bubble Generation at line(s) 1417 - 1412:")
        print("{DEBUG}: BUBBLES | %s" % get_stats("Bubbles"))

        Maintance.auto_save(self.saveName, get_stats("Stats"), get_stats("Bubbles"))

        global Mainloop
        Mainloop = False

        set_stats("Stats", stats)

        # Post Initalize mods

        self.canvas.itemconfig(t1, text="Post Initialize Mods")
        self.canvas.itemconfig(t2, text="")
        # self.modLoader.post_initialize(self)

        height = get_register("Config")["height"]
        width = get_register("Config")["width"]

        a = randint(0, width)
        b = randint(0, width)
        c = randint(0, width)

        d = stats["ship-position"][0]

        e = 40

        if a + e < d or d > a - e:
            a = d - e
        if b + e < d or d > b - e:
            b = d - e - 20
        if c + e < d or d > c - e:
            c = d - e - 40

        # bariers = [BaseBarier(self), BaseBarier(self), BaseBarier(self)]
        # bariers[0].create(a, height / 2 + 72 / 2)
        # bariers[1].create(b, height / 2 + 72 / 2)
        # bariers[2].create(c, height / 2 + 72 / 2)

        c = self.canvas

        print("[XboxController]:", "Starting Daemons")

        Thread(None, lambda: self._xboxInput(), daemon=True).start()
        Thread(None, lambda: self.xboxDeamon(), daemon=True).start()
        Thread(None, lambda: self.xboxControlDeamon(), daemon=True).start()
        Thread(None, lambda: self.movementChangeDaemon(), "MotionThread").start()
        Thread(None, lambda: self.moveBubblesDaemon(), "BubbleMove").start()

        self.canvas.delete(t0)
        self.canvas.delete(t1)
        self.canvas.delete(t2)

    def mainloop(self):
        """
        Mainloop method. This is the Mainloop of the game.
        For more information go to https://www.google.com and search for "what is a mainloop?"
        """
        # for i in get_stats("States"):
        #     pass
        while not self.returnmain:
            self.update()
        pass

    def t_update(self):
        # print(self.mod_loader.events)
        # for events in self.modLoader.events.values():
        #     for event in events:
        #         Thread(None, lambda: event.on_t_update(self)).start()
        pass  # /kill @e

    def update(self):
        # self.get_bubbles()

        from .stats import get_stats
        from .data import GetBubbleClassByID
        for i in get_stats("Bubbles")["bub-id"]:
            GetBubbleClassByID(i).update()

    def r_update(self):
        self.update()
        Thread(None, lambda: self.t_update(), "UpdateThread")

    # noinspection PyTypeChecker,PyShadowingNames
    def main(self):
        from threading import Thread
        from lib.utils import xbox

        try:
            # MAIN GAME LOOP
            while True:
                # self.stats = self.cfg.auto_restore_stats(self.save_name)
                # while self.bubbles["active"] <= len(self.bubbles["bub-index"]) - 1:
                #     self.canvas.itemconfig(t2, text="Created " + str(self.bubbles["active"]) + " of " + str(
                #         len(self.bubbles["bub-index"]) - 1) + " active...")
                #     self.canvas.update()
                #     self.root.update()
                #     sleep(0.1)

                print("[MAIN]: starting mainloop")

                self.mainLoop()

                self._root.update()

                # for barier in bariers:
                #     barier.destroy()
                g1 = self.canvas.create_text(mid_x, mid_y, text='GAME OVER', fill='Red', font=('Helvetica', 60, "bold"))
                g2 = self.canvas.create_text(mid_x, mid_y + 60, text='Score: ' + str(get_stat("Stats", "score")), fill='white',
                                             font=('Helvetica', 30))
                g3 = self.canvas.create_text(mid_x, mid_y + 90, text='Level: ' + str(get_stat("Stats", "level")), fill='white',
                                             font=('Helvetica', 30))
                log.info("Game.main", "Game Over!")
                self._root.update()
                sleep(4)
                self.canvas.delete(g1)
                self.canvas.delete(g2)
                self.canvas.delete(g3)
                del g1, g2, g3
                Maintance().reset(self.saveName)
                self.return_main()
        except TclError as e:
            if self.returnmain:
                pass
            else:
                if e.args[0] == 'can\'t invoke "update" command: application has been destroyed':
                    log.info('<root>', "Exit...")
                    exit(0)
                elif e.args[0] == 'can\'t invoke "update_idletasks" command: application has been destroyed':
                    log.info('<root>', "Exit...")
                    exit(0)
                elif e.args[0] == 'invalid command name ".!canvas"':
                    log.info('<root>', "Exit...")
                    exit(0)
                elif e.args[0] == 'invalid command name ".!canvas"':
                    log.info('<root>', "Exit...")
                    exit(0)
                else:
                    print('TclError: ' + e.args[0] + "Line: " + str(e.__traceback__.tb_next.tb_lineno))
                    exit(1)
        except AttributeError as e:
            if self.returnmain:
                pass
            else:
                if e.args[0] == "self.tk_widget is None. Not hooked into a Tk instance.":
                    exit(0)
                else:
                    raise AttributeError(e.args[0])

    def mainLoop(self):
        time2 = time()
        while self.stats["lives"] > 0 and not self.returnmain:
            time1 = time()

            try:
                # print(time1 - time2)
                # print(1/(time1 - time2))
                self.upd_fps = 1 / (time1 - time2)
            except ZeroDivisionError:
                self.upd_fps = 0

            time2 = time()

            if not self.modes["pause"]:
                Thread(None, lambda: self.update()).start()
                Thread(None, lambda: self.t_update()).start()

            self.root.update()
            self.root.update_idletasks()

    def r_update(self):
        pass

    def return_main(self):
        pass
