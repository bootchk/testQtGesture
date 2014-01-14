'''
'''
from __future__ import print_function

from PyQt5.QtWidgets import QGestureRecognizer

from gestureEventDumper import eventDumper


class EventDumpGestureRecognizer(QGestureRecognizer):
  '''
  A gesture recognizer that just dumps events sent to it.
  
  Never actually recognizes (Begin, Finish, or Cancel) any gesture.  Only returns "Maybe."
  TODO should it return Ignore?  What gesture type is create()'d?
  
  !!! Strange: Qt may send events of type QGestureEvent to a gesture recognizer.
  '''
  
  
  def __init__(self):
    print("Init ", self._name())
    super(EventDumpGestureRecognizer, self).__init__()
    
    
  def _name(self):
    ''' For dumping, name as receiver of events. '''
    return self.__class__.__name__
  
  
  # MUST be reimplemented
  def recognize(self, gesture, watched, event):
    '''
    Compute new state for gesture in watched widget based on event.
    
    Qt creates (as needed) and owns gesture.
    
    Not called for events outside watched widget.
    '''
    eventDumper.dumpRecognizeCall(gesture, event)
    
    '''
    A real recognizer would have decision logic on event.
    
    Here, we always let gesture remain 'alive'.
    Qt will pass the same gesture instance many times (maybe forever?)
    or Qt may create a new gesture instance if the pointer leaves watched widget?
    '''
    result = QGestureRecognizer.MayBeGesture
    '''
    result is a new state for gesture.
    But this doesn't work since enums in PyQt are fubar? assert isinstance(result, QGestureRecognizer.Result)
    '''
    return result
    
    
  '''
  create() and reset() methods are optional to reimplement.
  If not reimplemented, base class creates a generic QGesture having no type,
  and subsequently gesture manager creates and assigns a new gestureTypeID
  from the range that signifies a custom gesture.
  '''


  