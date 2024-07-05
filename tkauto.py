import multiprocessing
import tkinter
import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext as st
from tkinter import messagebox
from typing import Callable, Any, Iterable, Mapping

from typing_extensions import Literal

from ttkthemes import ThemedTk

import customtkinter

import threading

# for deprecated anotation
import warnings
import functools


class NamedElement():
    name = None
    data = None

    def __init__(self, nombre: str):
        self.name = nombre

    def add_data(self, dato):
        self.data = dato

    def get_data(self):
        return self.data


class NamedList(NamedElement):

    def __init__(self, name):
        super().__init__(name)
        self.data = []

    def add_element(self, element):
        self.data.append(element)

    def get_element_by_name(self, nombre):
        for element in self.data:
            if element.name == nombre:
                return element

    def set_element_data_by_name(self):
        None

    def get_all(self):
        return self.data


class NamedPosElement(NamedElement):

    def __init__(self, nombre: str, raiz, x, y, width, height, isRelativePos: bool, isRelativeScl: bool):
        print(issubclass(self.__class__, NamedElement))
        try:
            super().__init__(nombre)
        except:
            try:
                super().__init__(nombre, raiz)
            except Exception as error:
                print(error)
        self.raiz = raiz
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.isRelativePos = isRelativePos
        self.isRelativeScl = isRelativeScl

    def place(self):
        if self.isRelativePos and self.isRelativeScl:
            self.data.place(relx=self.x, rely=self.y, relwidth=self.width, relheight=self.height)
        elif self.isRelativePos:
            self.data.place(relx=self.x, rely=self.y, width=self.width, height=self.height)
        elif self.isRelativeScl:
            self.data.place(x=self.x, y=self.y, relwidth=self.width, relheight=self.height)
        else:
            self.data.place(x=self.x, y=self.y, width=self.width, height=self.height)

    def addbgcolor(self, colorstring):
        self.data.configure(bg_color=colorstring)


class NamedLabel(NamedPosElement):
    text = None
    text_color = None

    def __init__(self, nombre, raiz, x, y, width, height, isRelativePos: bool, isRelativeScl: bool,
                 text: str, text_color: str):
        super().__init__(nombre, raiz, x, y, width, height, isRelativePos, isRelativeScl)
        self.text = text
        self.text_color = text_color
        self.data = customtkinter.CTkLabel(self.raiz, text=self.text,
                                           font=customtkinter.CTkFont(size=15, weight="bold"),
                                           text_color=self.text_color)

        self.data.configure(
            corner_radius=50,
            fg_color="transparent",
            padx="10"
        )

        self.addbgcolor("transparent")


class NamedTextBox(NamedPosElement):

    def __init__(self, nombre, raiz, x, y, width, height, isRelativePos, isRelativeScl, isReadOnly: bool):
        super().__init__(nombre, raiz, x, y, width, height, isRelativePos, isRelativeScl)
        self.data = customtkinter.CTkTextbox(self.raiz)
        self.data.configure(fg_color="#BB8888",
                            border_width=10,
                            border_color="#8888BB",
                            corner_radius=50)
        if isReadOnly:
            self.data.configure(state="disabled")


class NamedButton(NamedPosElement):
    text = None
    action = None

    def __init__(self, nombre, raiz, x, y, width, height, isRelativePos, isRelativeScl, text: str, action):
        super().__init__(nombre, raiz, x, y, width, height, isRelativePos, isRelativeScl)
        self.text = text
        self.action = action
        self.data = customtkinter.CTkButton(self.raiz)
        self.configure(self.text, self.action)

    def configure(self, text, action):
        self.data.configure(text=text, command=action)


class NamedCheckBox(NamedPosElement):
    text = None
    check_var = None

    def __init__(self, nombre, raiz, x, y, width, height, isRelativePos, isRelativeScl, text: str,
                 varValue: Literal["on", "off"]):
        super().__init__(nombre, raiz, x, y, width, height, isRelativePos, isRelativeScl)
        self.text = text
        self.check_var = customtkinter.StringVar(value=varValue)
        self.data = customtkinter.CTkCheckBox(self.raiz, text=self.text, command=self.checkbox_event,
                                              variable=self.check_var)

    def checkbox_event(self):
        print("checkbox toggled, current value:", self.check_var.get())


class NamedComboBox(NamedPosElement):

    def __init__(self, nombre: str, raiz, x, y, width, height, isRelativePos: bool, isRelativeScl: bool, values: list):
        super().__init__(nombre, raiz, x, y, width, height, isRelativePos, isRelativeScl)
        self.data = customtkinter.CTkComboBox(self.raiz, values=values,
                                              command=self.combobox_callback)
        self.data.set("opcion 1")

    def combobox_callback(self, choice):
        print("combobox dropdown clicked:", choice)


class NamedEntry(NamedPosElement):

    def __init__(self, nombre: str, raiz, x, y, width, height, isRelativePos: bool, isRelativeScl: bool, text):
        super().__init__(nombre, raiz, x, y, width, height, isRelativePos, isRelativeScl)
        self.data = customtkinter.CTkEntry(self.raiz, placeholder_text=text)


class NamedOptionMenu(NamedPosElement):
    option_var = None
    action = None

    def __init__(self, nombre: str, raiz, x, y, width, height, isRelativePos: bool, isRelativeScl: bool, values: list):
        super().__init__(nombre, raiz, x, y, width, height, isRelativePos, isRelativeScl)
        self.option_var = customtkinter.StringVar(value="option 1")
        self.data = customtkinter.CTkOptionMenu(self.raiz, values=values, command=self.optionmenu_callback,
                                                variable=self.option_var, dropdown_fg_color="black")

    def optionmenu_callback(self, choice):
        print("optionmenu dropdown clicked:", choice)


class NamedProgressBar(NamedPosElement):

    def __init__(self, nombre: str, raiz, x, y, width, height, isRelativePos: bool, isRelativeScl: bool,
                 orientation: Literal["horizontal", "vertical"]):
        super().__init__(nombre, raiz, x, y, width, height, isRelativePos, isRelativeScl)
        self.data = customtkinter.CTkProgressBar(self.raiz, orientation=orientation)
        self.set_progress_value(0)
        print(self.get_progress_value())

    def set_progress_value(self, value: float):
        self.data.set(value)

    def get_progress_value(self):
        return self.data.get()


class NamedRadioButton(NamedPosElement):
    radio_var = None

    def __init__(self, nombre: str, raiz, x, y, width, height, isRelativePos: bool, isRelativeScl: bool, text: str,
                 radio_var: int):
        super().__init__(nombre, raiz, x, y, width, height, isRelativePos, isRelativeScl)
        self.radio_var = tkinter.IntVar(value=radio_var)

        radiobutton_1 = customtkinter.CTkRadioButton(self.raiz, text="radiobutton_1", command=self.radiobutton_event,
                                                     variable=self.radio_var)

        radiobutton_2 = customtkinter.CTkRadioButton(self.raiz, text="radiobutton_2", command=self.radiobutton_event)

    def radiobutton_event(self):
        print("radiobutton toggled, current value:", self.radio_var.get())


class NamedScrollBar(NamedElement):
    target = None
    raiz = None

    def __init__(self, nombre: str, raiz, target):
        super().__init__(nombre)
        self.target = target
        self.raiz = raiz
        self.data = customtkinter.CTkScrollbar(raiz, command=self.target.yview)
        print(self.data)
        self.data.grid(row=0, column=1, sticky="ns")
        self.target.configure(yscrollcommand=self.data.set)


class NamedSegmentedButton(NamedPosElement):
    values = None

    def __init__(self, nombre: str, raiz, x, y, width, height, isRelativePos: bool, isRelativeScl: bool, values: list):
        super().__init__(nombre, raiz, x, y, width, height, isRelativePos, isRelativeScl)
        self.data = customtkinter.CTkSegmentedButton(raiz, values=["Value 1", "Value 2", "Value 3"],  # values
                                                     command=self.segmented_button_callback)

    def segmented_button_callback(self, value):
        print("segmented button clicked:", value)
        self.data.set("Value 1")


class NamedSlider(NamedPosElement):

    def __init__(self, nombre: str, raiz, x, y, width, height, isRelativePos: bool, isRelativeScl: bool, from_: int,
                 to_: int):
        super().__init__(nombre, raiz, x, y, width, height, isRelativePos, isRelativeScl)
        self.data = customtkinter.CTkSlider(raiz, from_=from_, to_=to_, command=self.slider_event)

    def slider_event(self, value):
        print(value)


class NamedSwitch(NamedPosElement):
    switch_var = None

    def __init__(self, nombre: str, raiz, x, y, width, height, isRelativePos: bool, isRelativeScl: bool, text: str,
                 value: Literal["on", "off"]):
        super().__init__(nombre, raiz, x, y, width, height, isRelativePos, isRelativeScl)
        self.switch_var = customtkinter.StringVar(value="on")
        self.data = customtkinter.CTkSwitch(raiz, text=text, command=self.switch_event(), variable=self.switch_var,
                                            onvalue="on", offvalue="off")

    def switch_event(self):
        print("switch toggled, current value;", self.switch_var)


class ElementContainerType(NamedElement):
    list_container = NamedList("list_container")
    list_positionable = NamedList("list_positionable")
    list_names = ("frame_list", "label_list", "box_list", "button_list", "checkbox_list", "combobox_list", "entry_list",
                  "optionmenu_list", "progressbar_list", "radiobutton_list", "scrollableframe_list", "scrollbar_list",
                  "segmentedbutton_list", "slider_list", "switch_list", "tabview_list")

    def __init__(self, nombre: str, raiz):
        super().__init__(nombre)
        for elname in self.list_names:
            self.list_container.add_element(NamedList(elname))
        frame_list = self.list_container.get_element_by_name("frame_list")

    def create_frame(self, raiz, x, y, width, height, isRelativePos: bool, isRelativeScl: bool, name: str):
        try:
            self.list_container.get_element_by_name("frame_list").add_element(
                NamedFrame(nombre=name,
                           raiz=raiz,
                           x=x, y=y,
                           width=width, height=height,
                           isRelativePos=isRelativePos, isRelativeScl=isRelativeScl))
        except Exception as error:
            print("Error create frame ->", error)

    def create_label(self, raiz, x, y, width, height, isRelativePos: bool, isRelativeScl: bool, font: str, name: str,
                     text: str, text_color: str):

        try:
            self.list_container.get_element_by_name("label_list").add_element(
                NamedLabel(
                    nombre=name,
                    raiz=raiz,
                    x=x, y=y,
                    width=width, height=height,
                    isRelativePos=isRelativePos, isRelativeScl=isRelativeScl,
                    text=text, text_color=text_color))
        except Exception as error:
            print("Error create_label -> ", error)

    def create_textbox(self, raiz, name: str, x, y, width, height, isRelativePos: bool, isRelativeScl: bool,
                       isReadOnly: bool):
        try:
            self.list_container.get_element_by_name("box_list").add_element(NamedTextBox(
                nombre=name,
                raiz=raiz,
                x=x, y=y,
                width=width, height=height,
                isRelativePos=isRelativePos, isRelativeScl=isRelativeScl, isReadOnly=isReadOnly
            ))
        except Exception as error:
            print("Error create box -> ", error)

    def create_button(self, raiz, name: str, x, y, width, height, isRelativePos: bool, isRelativeScl: bool, text: str,
                      action):
        try:
            self.list_container.get_element_by_name("button_list").add_element(
                NamedButton(
                    nombre=name,
                    raiz=raiz,
                    x=x, y=y,
                    width=width, height=height,
                    isRelativePos=isRelativePos, isRelativeScl=isRelativeScl,
                    text=text,
                    action=action
                ))
        except Exception as error:
            print("Error create buttom -> ", error)

    def create_checkbox(self, raiz, name: str, x, y, width, height, isRelativePos: bool, isRelativeScl: bool, text: str,
                        varValue: Literal["on", "off"]):
        self.list_container.get_element_by_name("checkbox_list").add_element(
            NamedCheckBox(
                nombre=name,
                raiz=raiz,
                x=x, y=y,
                width=width, height=height,
                isRelativePos=isRelativePos, isRelativeScl=isRelativeScl,
                text=text, varValue=varValue))

    def create_combobox(self, raiz, name: str, x, y, width, height, isRelativePos: bool, isRelativeScl: bool, text: str,
                        varValue: Literal["on", "off"]):
        self.list_container.get_element_by_name("combobox_list").add_element(
            NamedComboBox(
                nombre=name,
                raiz=raiz,
                x=x, y=y,
                width=width, height=height,
                isRelativePos=isRelativePos, isRelativeScl=isRelativeScl,
                values=["option 1", "option 2"]
            ))

    def create_entry(self, raiz, name: str, x, y, width, height, isRelativePos: bool, isRelativeScl: bool, text: str,
                     varValue: Literal["on", "off"]):
        self.list_container.get_element_by_name("entry_list").add_element(
            NamedEntry(
                nombre=name,
                raiz=raiz,
                x=x, y=y,
                width=width, height=height,
                isRelativePos=isRelativePos, isRelativeScl=isRelativeScl,
                text="blabla"
            )
        )

    def create_optionmenu(self, raiz, name: str, x, y, width, height, isRelativePos: bool, isRelativeScl: bool,
                          values: list):
        self.list_container.get_element_by_name("optionmenu_list").add_element(
            NamedOptionMenu(
                nombre=name,
                raiz=raiz,
                x=x, y=y,
                width=width, height=height,
                isRelativePos=isRelativePos, isRelativeScl=isRelativeScl,
                values=values
            ))

    def create_progressbar(self, raiz, name: str, x, y, width, height, isRelativePos: bool, isRelativeScl: bool,
                           orientation: Literal["horizontal", "vertical"]):
        self.list_container.get_element_by_name("progressbar_list").add_element(
            NamedProgressBar(
                nombre=name,
                raiz=raiz,
                x=x, y=y,
                width=width, height=height,
                isRelativePos=isRelativePos, isRelativeScl=isRelativeScl,
                orientation=orientation
            ))

    def create_radiobutton(self, raiz, name: str, x, y, width, height, isRelativePos: bool, isRelativeScl: bool,
                           radio_var: int):
        self.list_container.get_element_by_name("radiobutton_list").add_element(
            NamedRadioButton(
                nombre=name,
                raiz=raiz,
                x=x, y=y,
                width=width, height=height,
                isRelativePos=isRelativePos, isRelativeScl=isRelativeScl,
            )
        )

    def create_scrollableframe(self, raiz, name: str, x, y, width, height, isRelativePos: bool, isRelativeScl: bool):
        self.list_container.get_element_by_name("scrollableframe_list").add_element(
            NamedScrollableFrame(
                nombre=name,
                raiz=raiz,
                x=x, y=y,
                width=width, height=height,
                isRelativePos=isRelativePos, isRelativeScl=isRelativeScl
            )
        )

    def create_scrollbar(self, raiz, name: str, target):
        self.list_container.get_element_by_name("scrollbar_list").add_element(
            NamedScrollBar(
                nombre=name,
                raiz=raiz,
                target=target
            )
        )

    def create_segmentedbutton(self, raiz, name: str, x, y, width, height, isRelativePos: bool, isRelativeScl: bool,
                               values: list):
        self.list_container.get_element_by_name("segmentedbutton_list").add_element(
            NamedSegmentedButton(
                nombre=name,
                raiz=raiz,
                x=x, y=y,
                width=width, height=height,
                isRelativePos=isRelativePos, isRelativeScl=isRelativeScl,
                values=values
            )
        )

    def create_slider(self, raiz, name: str, x, y, width, height, isRelativePos: bool, isRelativeScl: bool, from_: int,
                      to_: int):
        self.list_container.get_element_by_name("slider_list").add_element(
            NamedSlider(
                nombre=name,
                raiz=raiz,
                x=x, y=y,
                width=width, height=height,
                isRelativePos=isRelativePos, isRelativeScl=isRelativeScl,
                from_=from_, to_=to_
            )
        )

    def create_switch(self, raiz, name: str, x, y, width, height, isRelativePos: bool, isRelativeScl: bool, text: str,
                      value: Literal["on", "of"]):
        self.list_container.get_element_by_name("switch_list").add_element(
            NamedSwitch(
                nombre=name,
                raiz=raiz,
                x=x, y=y,
                width=width, height=height,
                isRelativePos=isRelativePos, isRelativeScl=isRelativeScl,
                text=text, value=value
            )
        )

    def create_tabview(self, raiz, name: str, x, y, width, height, isRelativePos: bool, isRelativeScl: bool,
                       tabListNames: list):
        self.list_container.get_element_by_name("tabview_list").add_element(
            NamedTabView(
                nombre=name,
                raiz=raiz,
                x=x, y=y,
                width=width, height=height,
                isRelativePos=isRelativePos, isRelativeScl=isRelativeScl,
                tablistNames=tabListNames
            )
        )


class NamedFrame(NamedPosElement, ElementContainerType):

    def __init__(self, nombre, raiz, x, y, width, height, isRelativePos, isRelativeScl):
        super().__init__(nombre, raiz, x, y, width, height, isRelativePos, isRelativeScl)
        self.data = customtkinter.CTkFrame(self.raiz)


class NamedScrollableFrame(NamedPosElement, ElementContainerType):

    def __init__(self, nombre: str, raiz, x, y, width, height, isRelativePos: bool, isRelativeScl: bool):
        super().__init__(nombre, raiz, x, y, width, height, isRelativePos, isRelativeScl)
        ElementContainerType.__init__(self, nombre=nombre, raiz=raiz)
        self.data = customtkinter.CTkScrollableFrame(master=raiz, fg_color="#000000", label_text="Frame")


class NamedTabView(NamedPosElement, ElementContainerType):
    tabListNames = None
    list_tab_elements_container = NamedList("list_tab_elements_container")

    def __init__(self, nombre: str, raiz, x, y, width, height, isRelativePos: bool, isRelativeScl: bool,
                 tablistNames: list):
        super().__init__(nombre, raiz, x, y, width, height, isRelativePos, isRelativeScl)
        self.data = customtkinter.CTkTabview(master=raiz)
        self.tabListNames = tablistNames
        self.addtablist()
        self.settabs()

    def addtablist(self):
        [self.data.add(str(tab)) for tab in self.tabListNames]

    def settabs(self):
        [self.data.set(str(tab)) for tab in self.tabListNames]

    def tabviewpack(self):
        self.data.pack(padx=1, pady=1)


class ElementTunning(multiprocessing.Process):
    targ = None

    def __init__(self, targ):
        super().__init__()
        self.targ = targ

    def run(self):
        while True:
            try:
                self.modifyparameter(self.targ)
            except Exception as error:
                None

    def modifyparameter(self, ui):
        print(ui.list_container.get_element_by_name("progressbar_list").get_element_by_name("progressbar1"))
        i = 0
        while i <= 1:
            ui.list_container.get_element_by_name("progressbar_list").get_element_by_name(
                "progressbar1").get_data().set(i)
            i += 0.01
            if i == 1:
                i = 0


class UI(multiprocessing.Process, ElementContainerType):
    uiname = "principal"
    root = None

    def __init__(self):
        super().__init__()
        self.root = customtkinter.CTk()
        ElementContainerType.__init__(self, nombre=self.uiname, raiz=self.root)

    def run(self):
        for lelemento in self.list_container.get_data():
            for telemento in lelemento.data:
                if issubclass(telemento.__class__, NamedPosElement):
                    self.list_positionable.add_element(lelemento)

        [[element.place() for element in lista.get_data()] for lista in self.list_positionable.get_data()]

        threading.Thread(target=self.programlop()).start()

    def programlop(self):
        try:
            while True:
                self.root.update()
        except Exception as error:
            print("Update break ->", error)

    def messagebox_ok_cancel(self, text: str, title: str):
        return messagebox.askokcancel(message=str(text), title=str(title))

    def messagebox_warning(self, text: str, title: str):
        messagebox.showwarning(message=str(text), title=str(title))

    def error_box(self, text: str, title: str):
        messagebox.showerror(message=text, title=title)

    def list_searcher(self, list_name: str):
        return self.list_container.get_element_by_name(list_name).data

    def element_searcher(self, list_name: str, element_name: str):
        return self.list_container.get_element_by_name(list_name).get_element_by_name(element_name)

    def get_frame_by_name(self, name):
        return self.frame_list.get_element_by_name(str(name))