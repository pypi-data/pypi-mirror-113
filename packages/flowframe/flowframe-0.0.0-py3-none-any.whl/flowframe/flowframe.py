#
# Gary Davenport
# dovedweller@gmail.com
# 7/14/2021
#
# This Object, FlowFrame inherets from Frame.
# I added methods:
#           'addWidget'
#           'destroyWidgets'
# 
# Make sure the instance of the frame is made to expand
# into parent container for the FlowFrame to work correctly.
#       
from tkinter import Frame

class FlowFrame(Frame):
    def __init__(self, *args, **kwargs):
        super(FlowFrame, self).__init__(*args, **kwargs)
        self.widgets=[]
        self.bind("<Configure>", lambda event:self._reorganizeWidgets())

    def addWidget(self, widget, **kwargs):
        #get the names of all widgets and place in list
        self.widgetChildList=[]
        for child in self.children:
            self.widgetChildList.append(child)

        #add the new widget to the list
        self.widgetChildList.append(widget)

        #grid the widget with its keyword arguments
        widget.grid(kwargs)

    def destroyWidgets(self):

        #get the names of all widgets in the frame and place in list
        self.widgetChildList=[]
        for child in self.children:
            self.widgetChildList.append(child)

        #destroy the widgets    
        for  i in range(len(self.children)):
            self.children[self.widgetChildList[i]].destroy()

        #reset list to empty
        self.widgetChildList=[]
            
    def _reorganizeWidgets(self):
        #set list to empty
        self.widgetChildList=[]

        #make new list based on current children of frame/self
        for child in self.children:
            self.widgetChildList.append(child)

        #algorithm for flow/gridding children based on window width and widgets widths
        rowNumber=0
        columnNumber=0
        width=0
        i=0
        while i<len(self.children):
            width+=self.children[self.widgetChildList[i]].winfo_width()
            if i==0:
                self.children[self.widgetChildList[i]].grid(row=rowNumber, column=columnNumber)
            elif width > self.winfo_width():
                rowNumber=rowNumber+1             
                columnNumber = 0               
                width=self.children[self.widgetChildList[i]].winfo_width()
            else:
                columnNumber=columnNumber+1
            self.children[self.widgetChildList[i]].grid(row=rowNumber, column=columnNumber)
            i+=1

