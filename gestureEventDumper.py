'''
'''
from __future__ import print_function

from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtWidgets import QGestureRecognizer
from PyQt5.QtGui import QTouchDevice


class EventDumper(object):
  '''
  Dumps objects related to gestures.
  
  Knows structures of objects.
  Knows to map enums to printable strings.
  '''
  def __init__(self):
    self.mapOfEventType = self._buildMap(QEvent, QEvent.Type)
    self.mapOfGestureType = self._buildMap(Qt, Qt.GestureType)
    self.mapOfGestureState = self._buildMap(Qt, Qt.GestureState)
    # Qt4 self.mapOfTouchDeviceType = self._buildMap(QTouchEvent, QTouchEvent.DeviceType)
    self.mapOfTouchDeviceType = self._buildMap(QTouchDevice, QTouchDevice.DeviceType)
    self.mapOfTouchPointState = self._buildMap(Qt, Qt.TouchPointState)
    self.mapOfRecognizerResult = self._buildMap(QGestureRecognizer, QGestureRecognizer.ResultFlag)
    
  '''
  Maps of enums.
  '''
  def _buildMap(self, className, EnumName):
      ''' Map from enum value to name of enum value. '''
      enumMap = {}
      print(className)
      for key, value in vars(className).items():  # Python2 iteritems():
          if isinstance(value, EnumName):
              print(key, value)
              enumMap[value] = key
      return enumMap

  def mapEventType(self, eventType):
    '''gesture
    !!! Strangely, map is not complete.  Errors in PyQt?
    '''
    try:
      result = self.mapOfEventType[eventType]
    except KeyError:
      # ??? usually 'not in client'
      result = str(eventType)
    return result
    
  def mapGestureType(self, gestureType):
    try:
      result = self.mapOfGestureType[gestureType]
    except KeyError:
      # Is custom gesture
      result = str(gestureType)
    return result

  def mapGestureState(self, state):
    try:
      result = self.mapOfGestureState[state]
    except KeyError:
      # Is an uninitialized gesture, 
      assert state == 0
      result = 'Uninitialized state'
    return result
  
  def mapRecognizerResult(self, result):
    return self.mapOfRecognizerResult[result]
  
  '''
  Main functions: dumping events
  '''

  def dump(self, event, receiverName):
    '''
    Log a single event received by some widget.
    '''
    # Announce briefly all events
    print(receiverName, "event", self.mapOfEventType[event.type()])
      
    # Announce in detail Gesture and Touch
    # !!! Obscure QEvent.GestureOverride: should be a subclass of QGestureEvent? but no method gestures()
    if event.type() in (QEvent.Gesture,):
      self.dumpGestureEvent(event)
    if event.type() in (QEvent.TouchUpdate, QEvent.TouchEnd, QEvent.TouchCancel, QEvent.TouchBegin):
      self.dumpTouchEvent(event)
  
  

  def dumpRecognizeCall(self, gesture, event):
    '''
    Log a call to a recognizer, in detail, without result.
    '''
    # log gesture being recognized
    print("recognize call for gesture", str(gesture), eventDumper.stringForGesture(gesture))
    # log event, which may be a gestureEvent having a second gesture !!
    eventDumper.dump(event, '  with ')
  
  
  def dumpRecognizeResult(self, gesture, event, result):
    '''
    Log return from a recognizer, short form, with result
    '''
    print("recognize", str(gesture), eventDumper.stringForGesture(gesture), 
          " event:", self.mapEventType(event.type()), 
          " result:", self.mapRecognizerResult(result))
    '''
    It is not useful to dump gesture events, since no gesture recognizer uses other gesture events?
    But it is useful to dump touch event detail
    '''
    # TODO dump touch events detail
    
    ## OLD
    ## log event, which may be a gestureEvent having a second gesture !!
    ## eventDumper.dump(event, '  with ')
    
    
  def dumpGestureEvent(self, event):
    gestures = event.gestures()
    # A gesture event has many gestures
    for gesture in gestures:
      self.dumpGesture(gesture)
      

  def dumpGesture(self, gesture):
    print("  ", self.stringForGesture(gesture))
    
  def stringForGesture(self, gesture):
    ''' 
    String representation for any gesture.
    Since str(gesture) returns insufficient info.
    '''
    return " ".join(( self.mapGestureType(gesture.gestureType()), 
                      self.mapGestureState(gesture.state()) ))
    
    
  def dumpTouchEvent(self, event):
    # name usually not set: print(event.device().name())
    print(self.mapOfTouchDeviceType[event.device().type()])
    touches = event.touchPoints()
    for touchPoint in touches:
        self.dumpTouchPoint(touchPoint)
        

  def dumpTouchPoint(self, touchPoint):
    print("  ", touchPoint.id(), self.mapOfTouchPointState[touchPoint.state()]) #self.mapOfGestureType[gesture.gestureType()], self.mapOfGestureState[gesture.state()]

  
  
# singleton
eventDumper = EventDumper()