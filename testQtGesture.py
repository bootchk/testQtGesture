#! /usr/bin/python

'''
Test Qt gestures.

Dumps/logs events.

Example custom gesture and recognizer.

QGestureManager is Qt internal class, see qgesturemanager.cpp

'''
from __future__ import print_function

from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsView, QGraphicsScene, QGraphicsTextItem
import sys

from gestureEventDumper import eventDumper
from gestureSetSubscriber import GestureSetSubscriber

ACCEPT_GESTURE_OVERRIDE = True



class DiagramScene(QGraphicsScene):
  def __init__(self, *args):
    QGraphicsScene.__init__(self, *args)
    
    # Add a graphic item, not responsive to gestures??
    text = QGraphicsTextItem("Test")
    text.setTextInteractionFlags(Qt.TextEditorInteraction)
    self.addItem(text)
    
  
  def event(self, event):
    eventDumper.dump(event, "Scene")
    return super(DiagramScene,self).event(event)
    
    
    
class DiagramView(QGraphicsView):
  '''
  A QGV whose viewport subscribes to custom gestures.
  '''
  def __init__(self, *args):
    super(DiagramView,self).__init__(*args)
    
    # Is this necessary?
    self.setAttribute(Qt.WA_AcceptTouchEvents)
    
    '''
    !!! Obscure: set the attribute on viewport(), the center of view, i.e. the scroll area.
    Which is a child of self, in addition to scrollbars (not used.)
    '''
    self.viewport().setAttribute(Qt.WA_AcceptTouchEvents)
        
    # !!! Viewport must subscribe to gestures
    GestureSetSubscriber.subscribeWidgetToGestures(widget=self.viewport())
    
    
  def viewportEvent(self, event):
    ''' Event in the scroll area child. '''
    eventDumper.dump(event, "View")
    return super(DiagramView, self).viewportEvent(event)



class EventDumpable(object):
  '''
  Mixin behaviour for QMainWindow: 
  dump all events received
  accept certain events (which enables future delivery of other events.)
  don't call super's handler (which cripples some normal Qt behaviour inside the window.)
  '''
  
  def event(self, event):
    '''
    Reimplement default event handler.
    '''
    eventDumper.dump(event, "MainWindow")
    """
    eventType = event.type() 
    if eventType in (QEvent.TouchBegin, QEvent.TouchUpdate, QEvent.TouchEnd, QEvent.TouchCancel):
      eventDumper.dump(event, "Window")
      event.accept()
    """
    if event.type() in (QEvent.GestureOverride,):
      # Conflicting gestures?
      # print dir(event)
      if ACCEPT_GESTURE_OVERRIDE:
        print("Accepting GestureOverride")
        event.accept()
      else:
        print("Not accepting GestureOverride")
        # by default is ignored ! (Does that mean the gesture, or the event.?)
      
    ## Not calling super's default handler
    ## return QMainWindow.event(self, event)
    
    return True # meaning: did process
  
  
class PlainMainWindow(GestureSetSubscriber, EventDumpable, QMainWindow):
    def __init__(self, *args):
        QMainWindow.__init__(self, *args)
        
        # Tell Qt to deliver touch events instead of translating friendly
        self.setAttribute(Qt.WA_AcceptTouchEvents)
    
        self.setWindowTitle("Test Qt gestures in plain main window");
        
        # For a plain window, self subscribes
        self.subscribeGestureSet()



class GraphicViewMainWindow(EventDumpable, QMainWindow):
    def __init__(self, *args):
        QMainWindow.__init__(self, *args)
        
        self.scene = DiagramScene()
        # Child is a view, in central area
        self.view = DiagramView(self.scene)
        # self.view.setRenderHint(QPainter.Antialiasing)
        self.setCentralWidget(self.view)
        
        # Tell Qt to deliver touch events instead of translating friendly
        self.setAttribute(Qt.WA_AcceptTouchEvents)
    
        self.setWindowTitle("Test Qt gestures in QGraphicsView");

        # Note main window is not subscribed to gestures

'''
Note a QMainWindow inherits QWidget, not QWindow (a different concept.)
QWindow has handler TouchEvent(), but QMainWindow does not.
'''    

def main(args):
    app = QApplication(args)
    
    # This is cruft for testing Linux/Ubuntu
    #app = QApplication(['testgesture', '-plugin evdevtouch:/dev/input/wacom-touch',])  # args in a list of strings
    #app = QApplication(['testgesture', '-plugin qevdevtouchplugin'])
    # -plugin evdevtouch:/dev/input/event[i
    
    # Choose one of these to demonstrate:
    
    # A QGV (the graphics framework)
    #mainWindow = GraphicViewMainWindow()
    
    # TODO a QGV with QGraphicsObjects that subscribe to gestures
    
    # A plain window (w/o graphics framework)
    mainWindow = PlainMainWindow()
    
    # TODO Nested widgets both subscribing
  
    
    mainWindow.setGeometry(100, 100, 500, 400)
    mainWindow.show()
    
    # Qt Main loop
    sys.exit(app.exec_())


"""
def loadEvdevPlugin():
  #plugin = QPluginLoader("libqevdevtouchplugin.so")
  #plugin = QPluginLoader("qevdevtouchplugin")
  plugin = QPluginLoader("evdevtouchplugin")
  result = plugin.load()
  if not result:
    print("PLUGIN LOAD FAIL")
"""

if __name__ == "__main__":
    main(sys.argv)