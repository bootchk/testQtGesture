'''
'''

from PyQt5.QtCore import Qt, QEvent

from dragGestureRecognizer import DragGestureRecognizer
from gesture.dragRMBGesture import DragRMBGesture


class DragRMBGestureRecognizer(DragGestureRecognizer):
  '''
  Specialized drag:
  - pointer is mouse 
  - press is mouse button down
  Compare to DragTouchGestureRecognizer
  '''
  gestureClass = DragRMBGesture
  
  
  def isBeginEvent(self, event):
    '''
    Does event signify start of drag?
    '''
    return event.type()==QEvent.MouseButtonPress \
        and event.button()==Qt.RightButton # TODO no other buttons are down

  def isFinishEvent(self, event):
    return event.type()==QEvent.MouseButtonRelease \
        and event.button()==Qt.RightButton
  
  def isContinueEvent(self, event):
    '''
    Does event signify continuation of drag?
    '''
    '''
    event.button() is button that caused event!!!
    buttons() is an OR of buttons down at time of event.
    We want only the one button to be down.
    '''
    return event.type()==QEvent.MouseMove \
        and event.buttons()==Qt.RightButton


  def isCancelEvent(self, event):
    ''' A drag RMB cannot be canceled by any event (only finished.) '''
    return False
  