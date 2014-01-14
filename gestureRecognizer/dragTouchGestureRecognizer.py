'''
'''

from PyQt5.QtCore import QEvent

from dragGestureRecognizer import DragGestureRecognizer
from gesture.dragTouchGesture import DragTouchGesture



class DragTouchGestureRecognizer(DragGestureRecognizer):
  '''
  Specialized drag:
  - pointer is mouse 
  - press is mouse button down
  Compare to DragTouchGestureRecognizer
  '''
  gestureClass = DragTouchGesture
  
  
  def isBeginEvent(self, event):
    '''
    Does event signify start of drag?
    '''
    return event.type()==QEvent.TouchBegin 
    # TODO singletouch?

  def isFinishEvent(self, event):
    return event.type()==QEvent.TouchEnd
    # TODO
  
  def isContinueEvent(self, event):
    '''
    Does event signify continuation of drag?
    '''
    return event.type()==QEvent.TouchUpdate

  def isCancelEvent(self, event):
    ''' 
    A drag touch CAN be canceled if the touch is canceled!!! 
    Why is a touch canceled, more so than a RMB?
    '''
    return event.type()==QEvent.TouchCancel
  