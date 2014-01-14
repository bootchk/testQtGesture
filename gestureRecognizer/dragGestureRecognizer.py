'''
'''
from __future__ import print_function

from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtWidgets import QGestureRecognizer

from gesture.dragRMBGesture import DragRMBGesture

from gestureEventDumper import eventDumper

class DragGestureRecognizer(QGestureRecognizer):
  '''
  A gesture recognizer recognizing a drag (pointer motion with pointer pressed.)
  
  !!! ABC for subclasses dragRMB and dragTouch.
  
  This illustrates that you recognize a gesture by logic on event.
  
  Similar to other gesture recognizer examples which recognize gestures in mouse motion.
  More generally, you can recognize gestures from many types of event.
  
  Specific logic for results:
  - TriggerGesture: on RMB pressed if no other buttons are down
  - CancelGesture: while RMB down, any other button down.
  - FinishGesture: on RMB release if triggered
  - Ignore: events unrelated to a RMB drag
  - MayBeGesture: mouseMove with RMB down (when gesture is started.)
  - ConsumeEventHint: ?
  '''
  
  # subclass must define class attribute gestureClass
  
  def __init__(self):
    print("Init DragGestureRecognizer")
    super(DragGestureRecognizer, self).__init__()
    
    '''
    A drag is a continuous gesture.
    It is useful to ensure that: it is not finished when it has not begun.
    E.G. that two touch end events in succession do not both finish the gesture,
    otherwise the second one engenders a Finish result, like a discrete gesture.
    
    This is ensured in recognize() below.
    Subclasses might be aware, depending on assumptions they make about events from lower levels (drivers).
    E.G. a mouse drag might assume that consecutive mouse releases do NOT occur,
    whereas a touch drag might assume that consecutive touch ends DO occur
    '''
    self.isBegun = False

  
  
  def recognize(self, gesture, watched, event):
    '''
    Compute new state for gesture in watched widget based on event.
    
    Qt creates (as needed) and owns gesture.
    
    Not called for events outside watched widget.
    
    Reimplemented from superclass (mandatory.)
    '''
    
    if self.isBeginEvent(event):
      print('>>> Trigger')
      result=QGestureRecognizer.TriggerGesture
      self.isBegun = True
      
    elif self.isFinishEvent(event):
      if not self.isBegun:
        # ignore a Finish that is out of order, else this gesture would act as if classified discrete
        result=QGestureRecognizer.Ignore
      else:
        result=QGestureRecognizer.FinishGesture
        self.isBegun = False
      print('>>> Finish')
      
    elif self.isContinueEvent(event):
      result=QGestureRecognizer.TriggerGesture
      '''
      !!! Usually this means subscribers will get a QGestureEvent ... update.
      But if it is the first such result, subscribers will get a QGE.Started.
      E.G. if for any reason, we missed a BeginEvent (missed button press but button is now down)
      This will start gesture, and now set our own state to match.
      '''
      self.isBegun = True
      
    elif self.isCancelEvent(event):
      # Generically, a drag can be cancelled.  Some subclasses are never cancelled.
      result = QGestureRecognizer.CancelGesture
      self.isBegun = False
    else:
      result = QGestureRecognizer.Ignore
    
    eventDumper.dumpRecognizeResult(gesture, event, result)
    #print("  result: ", eventDumper.mapRecognizerResult(result))
    return result
  
  
  
  def isBeginEvent(self, event):
    ''' Does event signify start of drag? '''
    raise NotImplementedError, 'Deferred'

  def isFinishEvent(self, event):
    raise NotImplementedError, 'Deferred'
  
  def isContinueEvent(self, event):
    ''' Does event signify continuation of drag? '''
    raise NotImplementedError, 'Deferred'

  def isCancelEvent(self, event):
    '''  '''
    raise NotImplementedError, 'Deferred'
  
  
  def create(self, targetWidgetOrQGraphicsObj):
    '''
    Called at registerRecognizer() time.
    
    reimplement since gesture type is  custom
    '''
    print("create", self.__class__.__name__)
    gesture = self.gestureClass(parent=targetWidgetOrQGraphicsObj) # MyGesture(parent=targetWidgetOrQGraphicsObj)
    eventDumper.dumpGesture(gesture)
    '''
    Not: assert gesture.state() == Qt.GestureStarted, "A new gesture is in the 'started' state."
    Apparently a new gesture is in an undefined state.
    '''
    return gesture
    
  
  def reset(self, gesture):
    print("reset" , self.__class__.__name__)
    # Do nothing extra since our custom gesture class has no extra state attributes
    # But do call super, which sets the gesture state.
    super(DragGestureRecognizer, self).reset(gesture)
    assert gesture.state() == 0, 'Base class resets gesture state to 0'
    
  