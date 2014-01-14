'''
'''
from PyQt5.QtWidgets import QGesture  # , QPanGesture

class DragRMBGesture(QGesture): 
  '''
  Custom gesture.
  
  All methods below are reimplementation of base class.
  
  
  '''
  
  def __init__(self, parent):
    print("initting DragRMBGesture", parent)
    super(DragRMBGesture, self).__init__()  # parent?
    #print self.gestureType()
    #print "returning init"

  def gestureCancelPolicy(self):
    #print "cancelPolicy"
    return QGesture.CancelNone
  
  """
  def gestureType(self):
    ''' This property is constant: no setter.  But you must implement this getter. '''
    print "gestureType"
    return Qt.CustomGesture
  """
  
  def hasHotSpot(self):
    ''' This property is constant: no setter.  But you must implement this getter. '''
    #print "hasHotSpot"
    return False
  
  def hotSpot(self):
    ''' '''
    #print "hotSpot"
    return False
  
  def setHotSpot(self, value):
    #print "sethotSpot"
    pass
    
  def unsetHotSpot(self, value):
    #print "unsethotSpot"
    pass
    
  def state(self):
    #print "state"
    return super(DragRMBGesture, self).state()