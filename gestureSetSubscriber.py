'''
'''
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGestureRecognizer

from gestureRecognizer.eventDumpGestureRecognizer import EventDumpGestureRecognizer
from gestureRecognizer.dragRMBGestureRecognizer import DragRMBGestureRecognizer
from gestureRecognizer.dragTouchGestureRecognizer import DragTouchGestureRecognizer

from gestureEventDumper import eventDumper



class GestureSetSubscriber(object):
  '''
  Mixin behaviour for QWidget based classes:  subscribe to gestures.
  
  grabGesture() IS a 'grab' in the traditional sense of getting events not contained in self's bounding rect.
  But there are many aspects of grab:
  - events contained outside app's windows (which are grabbed if a gesture starts in an app's widget)
  - events contained in child widgets and other top-level widgets of the app
  The docs also say it is a 'subscribe.'
  
  A widget can control propagation of gestures to parents by not accepting the Begin.
  If a parent does not accept the begin of a gesture that a child has accepted??
  Then the parent gets no further gesture events,
  and the child continues to receive events even if the gesture leaves the child widget?
  '''
  
  @classmethod
  def generateCustomGestureClasses(cls):
    # You can modify this to affect which custom gestures are recognized
    
    ##for recognizerClass in (EventDumpGestureRecognizer):  # dump all events in detail
    for recognizerClass in (DragRMBGestureRecognizer, DragTouchGestureRecognizer):  # two toy gesture recognizers that dump short version of events
      yield recognizerClass
  
  @classmethod
  def generateQtGestureTypeIDs(cls):
    # You can modify this to affect which Qt gestures are grabbed
    
    for gestureTypeID in (Qt.PanGesture, Qt.PinchGesture, Qt.TapGesture, Qt.TapAndHoldGesture, Qt.SwipeGesture):
      yield gestureTypeID
  
  @classmethod
  def createRecognizer(cls, recognizerClass):
    '''
    create QGestureRecognizer of recognizerClass
    '''
    '''
    Invoke class (a factory) to create gesture recognizer instance.
    
    Each subscriber has separate recognizer instance (two nested widgets may both be recognizing gestures.)
    '''
    myRecognizer = recognizerClass()
    
    # Call class method to let app take control of recognizer
    #print "registering custom gesture"
    gestureTypeID = QGestureRecognizer.registerRecognizer(myRecognizer)
    '''
    ID is Qt::CustomGesture 0x100 plus 1, i.e. 257
    '''
    print("created gesture type id: ", gestureTypeID, " recognizer ", recognizerClass.__name__)
    return gestureTypeID
  
  
  @classmethod
  def subscribeWidgetToGestures(cls, widget):
    '''
    Subscribe widget (not self) to gestures.
    '''
    # Custom
    for recognizerClass in cls.generateCustomGestureClasses():
      gestureTypeID = cls.createRecognizer(recognizerClass=recognizerClass)
      widget.grabGesture(gestureTypeID)
    # Qt
    for gestureTypeID in cls.generateQtGestureTypeIDs():
      widget.grabGesture(gestureTypeID)
  
  
  def subscribeGestureSet(self):
    '''
    Subscribe self to a defined set of gestures.
    
    You can modify to grab relevant gestures.
    '''
    print("grabGestureSet")
    self._subscribeQtGestures()
    self.grabCustomGestureSet()
    
  
  def _subscribeQtGestures(self):
    '''
    Subscribe self to all gestures recognized by Qt.
    '''
    for gestureType in GestureSetSubscriber.generateQtGestureTypeIDs():
      self.myGrabGesture(gestureType)
    
    
  def myGrabGesture(self, gestureType):
    ''' Wrap with print. '''
    print('grab', eventDumper.mapGestureType(gestureType))
    self.grabGesture(gestureType)
    
    
    
  def grabCustomGestureSet(self):
    '''
    Grab set of custom gestures.
    '''
    for recognizerClass in GestureSetSubscriber.generateCustomGestureClasses():
      gestureTypeID = GestureSetSubscriber.createRecognizer(recognizerClass=recognizerClass)
      self.grabGesture(gestureTypeID)
    
    
  
  
  
    