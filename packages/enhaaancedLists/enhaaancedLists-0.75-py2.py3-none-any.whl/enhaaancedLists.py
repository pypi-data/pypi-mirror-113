#!/usr/bin/python
# -*- coding: utf-8 -*-

# EnhaaancedLists - Copyright & Contact Notice
##############################################
# Created by Dominik Niedenzu                #      
# Copyright (C) 2021 Dominik Niedenzu        #       
#     All Rights Reserved                    #
#                                            #
#           Contact:                         #
#      pyadaaah@blackward.de                 #         
#      www.blackward.de                      #         
##############################################

# EnhaaancedLists - Version & Modification Notice
#################################################
# Based on EnhaaancedLists Version 0.75         #
# Modified by --- (date: ---)                   #
#################################################

# EnhaaancedLists - License
#######################################################################################################################
# Use and redistribution in source and binary forms, without or with modification,                                    #
# are permitted (free of charge) provided that the following conditions are met (including the disclaimer):           #
#                                                                                                                     #
# 1. Redistributions of source code must retain the above copyright & contact notice and                              #
#    this license text (including the permission notice, this list of conditions and the following disclaimer).       #
#                                                                                                                     #
#    a) If said source code is redistributed unmodified, the belonging file name must be enhaaancedLists.py and       #
#       said file must retain the above version & modification notice too.                                            #
#                                                                                                                     #
#    b) Whereas if said source code is redistributed modified (this includes redistributions of                       #
#       substantial portions of the source code), the belonging file name(s) must be enhaaancedLists_modified*.py     #
#       (where the asterisk stands for an arbitrary intermediate string) and said files                               #
#       must contain the above version & modification notice too - updated with the name(s) of the change             #
#       maker(s) as well as the date(s) of the modification(s).                                                       #
#                                                                                                                     #
# 2. Redistributions in binary form must reproduce the above copyright & contact notice and                           #
#    this license text (including the permission notice, this list of conditions and the following disclaimer).       #
#    They must also reproduce a version & modification notice similar to the one above - in the                       #
#    sense of 1. a) resp. b).                                                                                         #
#                                                                                                                     #
# 3. Neither the name "Dominik Niedenzu", nor the name resp. trademark "Blackward", nor the names of authors resp.    #
#    contributors resp. change makers may be used to endorse or promote products derived from this software without   #
#    specific prior written permission.                                                                               #
#                                                                                                                     #
# THIS SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO   # 
# THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.                            #
#                                                                                                                     #
# IN NO EVENT SHALL DOMINIK NIEDENZU OR AUTHORS OR CONTRIBUTORS OR CHANGE MAKERS BE LIABLE FOR ANY CLAIM, ANY         # 
# (DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY OR CONSEQUENTIAL) DAMAGE OR ANY OTHER LIABILITY, WHETHER IN AN    #
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THIS SOFTWARE (OR PARTS OF THIS   #
# SOFTWARE) OR THE USE OR REDISTRIBUTION OR OTHER DEALINGS IN THIS SOFTWARE (OR PARTS OF THIS SOFTWARE).              #
#                                                                                                                     #
# THE USERS RESP. REDISTRIBUTORS OF THIS SOFTWARE (OR PARTS OF THIS SOFTWARE) ARE SOLELY RESPONSIBLE FOR ENSURING     #
# THAT AFOREMENTIONED CONDITIONS ALL ARE MET AND COMPLIANT WITH THE LAW IN THE RESPECTIVE JURISDICTION - BEFORE (!)   #
# THEY USE RESP. REDISTRIBUTE.                                                                                        #
#######################################################################################################################



#import (from) common libraries
from argparse         import ArgumentParser as Argparse_ArgumentParser
from sys              import version_info   as Sys_version_info
from functools        import partial        as Functools_partial
from operator         import attrgetter     as Operator_attrgetter
from operator         import itemgetter     as Operator_itemgetter
from sys              import stderr         as Sys_stderr
from os               import linesep        as Os_linesep
from threading        import Lock           as Threading_Lock
from threading        import Thread         as Threading_Thread
from multiprocessing  import Lock           as Multiprocessing_Lock
from random           import uniform        as Random_uniform
from random           import shuffle        as Random_shuffle
from time             import sleep          as Time_sleep
from pickle           import dumps          as Pickle_dumps
from pickle           import loads          as Pickle_loads
from math             import factorial      as Math_factorial

#python version 2 checker
def isPy2():
    """
         Returns True if Python version in use is < 3.0.
    """
    if    Sys_version_info.major < 3.0:
          return True
    else:
          return False
          
          
#python version 3 checker          
def isPy3():
    """
         Returns True if Python version in use is >= 3.0.
    """
    if    Sys_version_info.major >= 3.0:
          return True
    else:
          return False
          
          
### take differences between python2 and python3 into account ###        
if      isPy2() == True:
        ### python version < 3 ###
        #using the types library for checking for built-in types is (just) python 2(.7) style        
        from types            import FunctionType   as Types_FunctionType
        from types            import TupleType      as Types_TupleType
        from types            import NoneType       as Types_NoneType    
        from types            import StringTypes    as Types_StringTypes
        from types            import UnicodeType    as Types_UnicodeType
        
else:
        ### python version >= 3 ###
        def function(): 
            pass
        Types_FunctionType = (type(function), Functools_partial)
        Types_TupleType    = tuple
        Types_NoneType     = None
        Types_StringTypes  = str
        Types_UnicodeType  = str
        xrange = range


#############################
# supported operators tuple #
#############################
#TBD: add unary operators alike 'abs' too ???
operatorsT = ( 'lt', 'le', 'eq', 'ge', 'gt', 'ne', 'add', 'sub', 'mul', 'truediv', \
               'floordiv', 'mod', 'pow'                                            )
#'div' just exists in Python 2.*
if      isPy2() == True:
        operatorsT += ('div',)

for operatorS in operatorsT:
    exec("from operator import {0} as Operator_{0}".format(operatorS))   
del operatorS     
               
           
#####################
# exception handler #  
#####################      
try:
        #if the pyadaaah library is available, use its exceptions / exception handler
        from pyadaaah import *
        
except: 
        #if the pyadaaah library is not available, use a dummy exception handler 
        #(but the 'logExceptions' decorator has a real meaning!)
        #STR - accepting (and translating) unicode characters too
        class STR(str):
            """
                 String class accepting e.g. and in particular unicodes as well; 
                 the result is a pure ascii (0-127) string, which is achieved by 
                 replacing all non-ascii characters by '?'.
            """
            
            #return the pure ascii string
            def __new__(cls, text):
                """ """   
                
                try:
                       #make a str out of text - if not already one (resp. an unicode)
                       if    isinstance(text, Types_StringTypes):
                             textS = text
                       else:
                             textS = str(text)
                      
                       #make a unicode out of textS - if not already one
                       if not isinstance(textS, Types_UnicodeType):
                          textS = textS.decode("ascii", "replace")
                
                       #unicode is str in python 3 - but not in python 2
                       #in python 2: encode back to str
                       if isPy2() == True:
                          #replace non-ascii characters by '?'
                          textS = textS.encode("ascii", "replace")
                          
                       #return
                       return textS
                      
                except BaseException as ee:
                       return "Error in STR: %s!" % str(ee)
                       
               
               
        #dummy exception handler
        class ExceptionHandler(object):
              """ Dummy exception handler doing nothing. """
                             
              @classmethod
              def log(cls, exception):
                  """ Does nothing. """
                  
                  pass
                  
  
    
        #exception logger - decorator for methods (only !)
        def logExceptions(method, logger=ExceptionHandler):
            """ Method wrapper for exception logging (decorator). """
        
            def decorator(self, *params, **paramDict):
                try:   
                        return method(self, *params, **paramDict)              
                        
                except  BaseException as error: 
                        #get class-s name - in a safe manner
                        clsNameS = "no class"
                        if hasattr(self, "__class__"):
                           if hasattr(self.__class__, "__name__"):
                              clsNameS = self.__class__.__name__
                        
                        #get method name - in a safe manner
                        methodNameS = "no method"
                        if hasattr(method, "__name__"):
                           methodNameS = method.__name__
                        
                        #create message - in a safe manner
                        try:
                                errMsgS = "Error in %s.%s: %s" % (clsNameS, methodNameS, STR(error))
                        except:
                                errMsgS = "automatic exception message creation failed"
                                
                        #enhance readability / beauty
                        errMsgS = errMsgS.rstrip() + Os_linesep + Os_linesep
                        
                        #log error message
                        logger.log( type(error)(errMsgS) )
                        
                        #re-raise exception
                        raise type(error)(errMsgS)
                        
            #return new (decorator) method
            return decorator
            
            
        #as the dummy logger does nothing, muting means 'doing nothing' too
        def muteLogging(method, logger=ExceptionHandler):
            """ Decorator - adding nothing to each method decorated. """
            
            def decorator(self, *params, **paramDict):
                """ This wrapper does not add any functionality. """
                
                #call method
                retVal = method(self, *params, **paramDict)
                
                #return return value of method
                return retVal
                
            #return new (decorator) method
            return decorator    



#EnhaaancedLists version
__version__ = 0.75
def getVersion():
    global __version__
    return __version__
    


##################################################
# elem term - condition (partial) function class #
############# ####################################
class ConditionFunction(Functools_partial):
      """
          This is the basic unit of condition terms using the 'elem' term.
          
          It is a function, whose operator methods have been overloaded to
          return another ConditionFunction instance, which has been extended
          by the belonging operations / comparisons.
          
          In particular, the operator methods for getting an attribute ('.') and
          for getting an item ('[]') have been overloaded this way, as well as 
          the comparison operator methods. 
          
          Furthermore the bitwise 'or' and 'and' operator methods are abused 
          to provide a logical 'or' and 'and' too.
          
          Further operators taken into account can be found in operatorsT.
          
          In short: this condition resp. function can be 'extended' by 
          using said operators on it - which then leads to an(other) 
          (extended) condition resp. function resp. ConditionFunction.
          
          Example:
          ex = (elem['a'] > 5) & (elem['b'] < 5)
          #creates a ConditionFunction taking one parameter, namely an element
          
          ex( {'a':6, 'b':4} ) ==> True
          ex( {'a':4, 'b':6} ) ==> False
          
          Note, that the 'elem' term mechanism is very limited yet; it just is
          a short convenience notation, which can be used to enhance the 
          readability of SIMPLE conditions for element selection - TBD.
          
          Some methods of EnhList accept ConditionFunction-s as parameter. For
          those, you either can use the ConditionFunction resp. 'term'
          mechanism, or a function, alike a lambda, returning a truth value.
      """
      
      #generate comparison methods __lt__ ... __ne__, 
      #called if "<" ... "!=" are used on a ConditionFunction instance
      for operatorS in operatorsT:
          exec( """@logExceptions
def __{0}__(self, ohs):
    ' overloaded comparison method '
    if    isinstance(ohs, Functools_partial):
          return ConditionFunction( lambda x: Operator_{0}(self(x), ohs(x)) )
    else:
          return ConditionFunction( lambda x: Operator_{0}(self(x), ohs) )
                """.format(operatorS))   
      del operatorS
                
                
      #called if the 'bitwise and' operator '&' is used on a ConditionFunction instance
      @logExceptions
      def __and__(self, ohs):
          """ As there is no hook for the 'logical and' operator, 
              the 'bitwise and' is 'abused' instead.               """
      
          if    isinstance(ohs, Functools_partial):
                return ConditionFunction( lambda x: (self(x) and ohs(x)) )    
          else:
                return ConditionFunction( lambda x: (self(x) and ohs) )
          
          
      #called if the 'bitwise or' operator '|' is used on self
      @logExceptions
      def __or__(self, ohs):
          """ As there is no hook for the 'logical or' operator, 
              the 'bitwise or' is 'abused' instead.                """
       
          if    isinstance(ohs, Functools_partial):
                return ConditionFunction( lambda x: (self(x) or ohs(x)) ) 
          else:
                return ConditionFunction( lambda x: (self(x) or ohs) )
                
                
      #method called by ".nameS"
      @logExceptions
      def __getattribute__(self, nameS):
          """ overloaded get attribute method """
          
          #do not meddle with resp change the classes standard attributes (accesses)
          if    not nameS.startswith("__"): 
                return ConditionFunction( Operator_attrgetter(nameS) )
          else:
                return Functools_partial.__getattribute__(self, nameS)
          
          
      #method called by "[nameS]"
      @logExceptions
      def __getitem__(self, keyO):
          """ overloaded get item method """
          
          return ConditionFunction( Operator_itemgetter(keyO) )                
      
      
### short elem alias ###
elem = ConditionFunction(lambda x: x)


#self test method
def _testElem():
    """ Does some tests using the 'elem' notation. """
    
    print ( "Testing 'elem'..." )
    
    #lower than comparison operator
    fct = elem < 5
    assert fct(4) == True
    assert fct(6) == False  
    
    #lower or equal comparison operator
    fct = elem <= 5
    assert fct(5) == True
    assert fct(6) == False
    
    #equal comparison operator
    fct = elem == 5
    assert fct(5) == True
    assert fct(6) == False
    
    #greater or equal comparison operator
    fct = elem >= 5
    assert fct(6) == True
    assert fct(4) == False
    
    #greater comparison operator
    fct = elem > 5
    assert fct(6) == True
    assert fct(5) == False
    
    #not equal comparison operator
    fct = elem != 5
    assert fct(4) == True
    assert fct(5) == False
    
    #add operator
    fct = 1 < elem + 1
    assert fct(1) == True
    assert fct(0) == False
    
    #subtract operator
    fct = 1 < elem - 1
    assert fct(3) == True
    assert fct(2) == False
    
    #multiply operator
    fct = 1 < elem * 2
    assert fct(1) == True
    assert fct(0) == False
    
    #divide operator
    fct = 1 < elem / 2
    assert fct(4.0) == True
    assert fct(2.0) == False
    
    #int divide operator
    fct = elem // 2 >= 1
    assert fct(4) == True
    assert fct(1) == False
    
    #modulo operator
    fct = elem % 2 == elem % 4
    assert fct(4) == True
    assert fct(2) == False
    
    #power operator
    fct = elem ** 2 != 16
    assert fct(3) == True
    assert fct(4) == False

    print ("...'elem' tested successfully!")   



#single
class Single(object):
      """ 
          Just a helper class for EnhList.
          Some methods of EnhList accept that as a parameter.
      """
      pass
single = Single()

#several
class Several(object):
      """ 
          Just a helper class for EnhList.
          Some methods of EnhList accept that as a parameter.
      """
      pass
several = Several() 
      
      
    
#######################
# Enhanced List Class #
#######################
class EnhList(list):
      """ 
          List with extended / enhanced IN-PLACE capabilities.
          
          Together with the 'elem' term, some of its 
          methods (also) allow using a NEW OPERATOR NOTATION, closely 
          resembling mathematical conditions.
          
          Note that '&' and '|' are 'abused' as 'logical and / or' in this
          context (and NOT bitwise!).
          
          examples for said ADDITIONAL capabilities (standard list operations work too):
          
          
          #convert a parameter list to an enhanced list 
          eL = EnhList(1,3,5,7)                                       #eL: [1,3,5,7]
          
          #push single as well as multiple elements into the list
          eL.push(9)                                  ==> None        #eL: [1,3,5,7,9]
          eL.push(11,13,15)                           ==> None        #eL: [1,3,5,7,9,11,13,15]
          
          #pop - note that push/pop implements a FIFO - in contrast to the standard list
          eL.pop()                                    ==> 1           #eL: [3,5,7,9,11,13,15]
          eL.pop( (elem > 3) & (elem < 11), single )  ==> 5           #eL: [3,7,9,11,13,15]
          eL.pop( (elem > 3) & (elem < 11)         )  ==> [7,9]       #eL: [3,11,13,15]      
          
          #get items from list
          eL[ elem >= 10         ]                    ==> [11,13,15]  #eL: unchanged
          eL[ elem >= 10, single ]                    ==> 11          #eL: unchanged
          eL[ elem <  3,  single ]                    ==> None        #eL: unchanged
          
          #check whether list contains items
          ( elem <  3 ) in eL                         ==> False       #eL: unchanged
          ( elem >= 3 ) in eL                         ==> True        #eL: unchanged
          
          #delete items from list
          del eL[ elem < 12, single ]                 ==> ---         #eL: [11,13,15]
          del eL[ elem > 12         ]                 ==> ---         #eL: [11]
          
          eL = EnhList(1,3,5,7)                                       #eL: [1,3,5,7]
          #check whether all element meet a condition
          eL.areAll( elem % 2 == 1 )                  ==> True
          eL.areAll( elem     >= 3 )                  ==> False
          
          #map function on elements / work with items of elements
          eL.mapIf( lambda x: dict(a=x) )                          
                                                      ==> None        #eL: [{'a':1},{'a':3},{'a':5},{'a':7}]
          eL.mapIf( lambda x: x['a'] + 1, elem['a'] > 3)           
                                                      ==> None        #eL: [{'a':1},{'a':3},6,8]
          
          #work with attributes of elements
          class Attr(object):
                def __init__(self, value):
                    self.a = value
                def __repr__(self):
                    return ".a=%s" % self.a
          eL.mapIf( lambda x: Attr(x), lambda x: type(x) ==  int ) 
                                                      ==> None        #eL: [{'a':1},{'a':3},.a=6,.a=8]
                
          More examples can be found in the source code of the selftest function
          of the module and the methods called from there.
          
          Please also take the doc/help-texts of each revised method into account too.
          
          Also note, that 'elem' just is an alias defined as follows:
          
          elem = ConditionFunction(lambda x: x)
          
          So that more informations about 'elem' also can be found in the doc/help-text
          belonging to the class 'ConditionFunction', which, by the way, is inherited from
          functools.partial.
      """
      
      
      #initialisation
      @logExceptions
      def __init__(self, *params):
          """
               If several parameters 'params' are given, they are taken 
               as the initial elements of the (enhanced) list.
               
               Otherwise, 'params' (just) is forwarded to the __init__ method
               of the parent 'list' class as is.
          """

          #handle parameters and call the __init__ of the parent 'list' class accordingly
          if    len(params) <= 1:
                #no or one parameter ==> use it as parameter for __init__ of the parent class
                list.__init__(self, *params)
                
          else:
                #several parameters ==> use it as initial elements of the (enhanced) list
                list.__init__(self,  params)
                
                
      #method testing __init__
      @classmethod
      @muteLogging
      def _initSelftest(cls):
          """ """
          
          print ( "Testing EnhList.__init__..." )
          
          #no parameter
          assert EnhList() == []

          #one -non iterable- parameter  
          try:        
                  assert EnhList(1)
                  assert False
          except:
                  pass
                
          #one -iterable- parameter
          assert EnhList([1,3,5,7]) == [1,3,5,7]
          assert EnhList((1,3,5,7)) == [1,3,5,7]
          
          
          #several parameters
          assert EnhList(1,3,5,7) == [1,3,5,7]
          
          print ( "...EnhList.__init__ tested sucessfully!" )
                
                
      #push element to the end
      @logExceptions
      def push(self, *params):
          """
              The methods 'push' and 'pop' implement a FIFO.
              
              'Push' hereby appends to the end of the (enhanced) list.
              
              It accepts no, one or several parameters (elements) to be appended.
              Returns None.
          """
          
          #accept no, one or several parameters
          if    len(params) == 1:
                #one parameter
                return list.append( self, *params )
                
          else:
                #no or several parameters
                return list.extend( self, params ) 
                
                
      #method testing push
      @classmethod
      def _pushSelftest(cls):
          """ """
          
          print ( "Testing EnhList.push..." )
          
          testL = EnhList(1,3,5,7)
          
          #no parameter
          testL.push()
          assert testL == [1,3,5,7]
          
          #one parameter
          testL.push(9)
          assert testL == [1,3,5,7,9]
          
          #several parameters
          testL.push(11,13,15)
          assert testL == [1,3,5,7,9,11,13,15]
          
          print ( "...EnhList.push tested sucessfully!" )                

                                
      #pop element(s) meeting a condition
      @logExceptions
      def pop(self, selector=0, multitude=several):
          """
              The methods 'push' and 'pop' implement a FIFO.
              
              By default (with no parameter given), 'pop' hereby pops from the 
              beginning of the (enhanced) list.
              
              If the parameter 'selector' is a (condition) function resp. partial, taking
              one parameter, namely an element, (just) the elements, for which said
              function resp. partial returns True, are popped.
              
              If, in this situation, the parameter 'multitude' is 'single', just the first
              element meeting said condition is popped (if there is none, None is returned), 
              whereas if it is 'several', all elements meeting said condition are popped.
              
              If on the other hand the 'selector' parameter neither is of type function 
              nor of type partial, it is (just) forwarded to the list.pop method, leading
              to the behaviour of the standard list type.
          """
             
          if  isinstance(selector, (Types_FunctionType, Functools_partial)):
                #selector is a function, returning True (just) for the elements to be popped
                selectionFunction = selector
          
                if    multitude is single:
                      #just pop the (very) first element meeting the condition
                      for indexI in xrange(list.__len__(self)):
                          if selectionFunction( list.__getitem__(self, indexI) ) == True:
                             return list.pop( self, indexI )
                          
                      #if no element meets the condition, return None
                      return None
          
                elif  multitude is several:
                      #pop all elements meeting the condition
          
                      popL              = EnhList()
                      indexI            = list.__len__(self) - 1
                               
                      #process list starting from the end using indices - as the list might be 
                      #modified during processing (by the pops)
                      while indexI >= 0:
                          
                            #just pop elements, for which selectionFunction(element) returns True 
                            if selectionFunction( list.__getitem__(self, indexI) ) == True:
                               popL.insert(0, list.pop( self, indexI ))
                         
                            #next element
                            indexI -= 1
                          
                          
                      #return the (enhanced) list containing the popped elements
                      #if no element met the condition, said list is empty
                      return popL
                     
                else:
                      raise Exception("The parameter 'multitude' must either be 'single' or 'several'!")
                      
          else:    
                #standard list behaviour 
                #selector should be an index to the element to be popped
                return list.pop(self, selector)  


      #method testing pop
      @classmethod
      def _popSelftest(cls):
          """ """
          
          print ( "Testing EnhList.pop..." )
          
          #no parameter
          testL = EnhList(1,3,5,7,9,11,13,15)
          assert testL.pop() == 1
          assert testL == [3,5,7,9,11,13,15]
          
          #index parameter
          testL = EnhList(1,3,5,7,9,11,13,15)
          assert testL.pop(4) == 9
          assert testL == [1,3,5,7,11,13,15]
          
          #(lambda) function parameter - logical 'and'
          testL = EnhList(1,3,5,7,9,11,13,15)
          poppedL = testL.pop( lambda x: (x > 6) and (x < 10) )
          assert poppedL == [7,9]
          assert isinstance(poppedL, EnhList)
          assert testL == [1,3,5,11,13,15]
          
          #(lambda) function parameter - logical 'or'
          testL = EnhList(1,3,5,7,9,11,13,15)
          poppedL = testL.pop( lambda x: (x < 6) or (x > 10) ) 
          assert poppedL == [1,3,5,11,13,15]
          assert isinstance(poppedL, EnhList)
          assert testL == [7,9]   
          
          #(lambda) function parameter - just the first
          testL = EnhList(1,3,5,7,9,11,13,15)
          assert testL.pop( lambda x: (x > 6), single ) == 7
          assert testL == [1,3,5,9,11,13,15]
          
          #(lambda) function parameter - none
          testL = EnhList(1,3,5,7,9,11,13,15)
          assert testL.pop( lambda x: (x > 15), single ) == None
          assert testL == [1,3,5,7,9,11,13,15]         
                      
          #'partial' parameter - logical 'and'
          testL = EnhList(1,3,5,7,9,11,13,15)
          poppedL = testL.pop( (elem > 6) & (elem < 10) )
          assert poppedL == [7,9]
          assert isinstance(poppedL, EnhList)
          assert testL == [1,3,5,11,13,15]
          
          #'partial' function parameter - logical 'or'
          testL = EnhList(1,3,5,7,9,11,13,15)
          poppedL = testL.pop( (elem < 6) | (elem > 10) ) 
          assert poppedL == [1,3,5,11,13,15]
          assert isinstance(poppedL, EnhList)
          assert testL == [7,9]
          
          #'partial' function parameter - just the first
          testL = EnhList(1,3,5,7,9,11,13,15)
          assert testL.pop( (elem > 6), single ) == 7
          assert testL == [1,3,5,9,11,13,15]
          
          #'partial' function parameter - none
          testL = EnhList(1,3,5,7,9,11,13,15)
          assert testL.pop( (elem > 15), single ) == None
          assert testL == [1,3,5,7,9,11,13,15]          
          
          print ( "...EnhList.pop tested sucessfully!" )                                          
                
                
      #get element(s) meeting a condition
      @logExceptions
      def __getitem__(self, *params):
          """
              If the first positional parameter is a (condition) function resp. partial, 
              taking one parameter, namely an element, (just) the elements, for which said
              function resp. partial returns True, are returned.
              
              If, in this situation, the second parameter is 'single', 
              just the first element meeting said condition is returned 
              (if there is none, None is returned), whereas if it is 'several', 
              all elements meeting said condition are returned. Default is 'several'.
              
              If on the other hand the first positional parameter neither is of type 
              function nor of type partial, the parameters (just) are forwarded to 
              the list.__getitem__ method, leading to the behaviour of the standard 
              list type.
          """

          #getitem just takes exactly one parameter, this is why, if several
          #are given, e.g. self[a,b], this leads to params == ((a,b),),
          #which is not the common way of passing parameters to methods
          #the following changes this back to the common way
          paramsT = tuple()
          if (len(params) > 0):
             if     isinstance( params[0], Types_TupleType ):
                    #if params is a tuple containing a tuple (at the first position)
                    paramsT = params[0]
                
             else:
                    #if params is a tuple containing a non-tuple (at the first position)
                    paramsT = params
          
          #one or two 'real' parameters are accepted
          if    len(paramsT) == 1:
                #exactly one positional parameter ==> use it as the selector
                selector  = paramsT[0]
                multitude = several           #use a default for multitude
                
          elif  (len(paramsT) == 2) and (paramsT[1] in (single, several)):
                #two positional parameters and the second either is 'single' or 'several'
                selector  = paramsT[0]
                multitude = paramsT[1]
                
          else:
                raise Exception( "Either one parameter or two parameters - with the "  \
                                 "second being 'single' or 'several' - is allowed!"    )
          
          #check, whether the selector is a function or a 'partial' or something else
          if  isinstance(selector, (Types_FunctionType, Functools_partial)):
                #selector is a function, returning True (just) for the elements to be returned
                selectionFunction = selector
          
                if    multitude is single:
                      #just return the (very) first element meeting the condition
                      for indexI in xrange(list.__len__(self)):
                          if selectionFunction( list.__getitem__(self, indexI) ) == True:
                             return list.__getitem__( self, indexI )
                          
                      #if no element meets the condition, return None
                      return None
          
                elif  multitude is several:
                      #return all elements meeting the condition                
                      return EnhList([ element for element in self if selectionFunction(element) == True ])
                     
                else:
                      raise Exception("The parameter 'multitude' must either be 'single' or 'several'!")
                      
          else:    
                #forward to standard list behaviour 
                retVal = list.__getitem__( self, selector )
                if isinstance(retVal, list):
                   retVal = EnhList(retVal)
                return retVal
                
                
      #method testing __getitem__
      @classmethod
      def _getitemSelftest(cls):
          """ """
          
          print ( "Testing EnhList.__getitem__..." )
          
          #index parameter
          testL = EnhList(1,3,5,7,9,11,13,15)
          assert testL[4] == 9
          assert testL == [1,3,5,7,9,11,13,15]
          
          #cross check slicing
          testL = EnhList(1,3,5,7,9,11,13,15)
          gotL = testL[4:6] 
          assert gotL == [9,11]
          assert isinstance(gotL, EnhList)
          assert testL == [1,3,5,7,9,11,13,15]
          
          #cross check slicing with step with 2
          testL = EnhList(1,3,5,7,9,11,13,15)
          gotL = testL[2:7:2]
          assert gotL == [5,9,13]
          assert isinstance(gotL, EnhList) 
          assert testL == [1,3,5,7,9,11,13,15]          
          
          #(lambda) function parameter - logical 'and'
          testL = EnhList(1,3,5,7,9,11,13,15)
          gotL = testL[ lambda x: (x > 6) and (x < 10) ] 
          assert gotL == [7,9]
          assert isinstance(gotL, EnhList)
          assert testL == [1,3,5,7,9,11,13,15]
          
          #(lambda) function parameter - logical 'or'
          testL = EnhList(1,3,5,7,9,11,13,15)
          gotL = testL[ lambda x: (x < 6) or (x > 10) ] 
          assert gotL == [1,3,5,11,13,15]
          assert isinstance(gotL, EnhList)
          assert testL == [1,3,5,7,9,11,13,15]
          
          #(lambda) function parameter - just the first
          testL = EnhList(1,3,5,7,9,11,13,15)
          assert testL[ lambda x: (x > 6), single ] == 7
          assert testL == [1,3,5,7,9,11,13,15]
          
          #(lambda) function parameter - none
          testL = EnhList(1,3,5,7,9,11,13,15)
          assert testL[ lambda x: (x > 15), single ] == None
          assert testL == [1,3,5,7,9,11,13,15]        
                      
          #'partial' parameter - logical 'and'
          testL = EnhList(1,3,5,7,9,11,13,15)
          gotL = testL[ (elem > 6) & (elem < 10) ]
          assert gotL == [7,9]
          assert isinstance(gotL, EnhList)
          assert testL == [1,3,5,7,9,11,13,15]
          
          #'partial' function parameter - logical 'or'
          testL = EnhList(1,3,5,7,9,11,13,15)
          gotL = testL[ (elem < 6) | (elem > 10) ]
          assert gotL == [1,3,5,11,13,15]
          assert isinstance(gotL, EnhList)
          assert testL == [1,3,5,7,9,11,13,15]
          
          #'partial' function parameter - just the first
          testL = EnhList(1,3,5,7,9,11,13,15)
          assert testL[ (elem > 6), single ] == 7
          assert testL == [1,3,5,7,9,11,13,15]
          
          #'partial' function parameter - none
          testL = EnhList(1,3,5,7,9,11,13,15)
          assert testL[ (elem > 15), single ] == None
          assert testL == [1,3,5,7,9,11,13,15]     
          
          print ( "...EnhList.__getitem__ tested sucessfully!" )                 
        
                      
      ##delete element(s) meeting a condition
      @logExceptions
      def __delitem__(self, *params):
          """ 
              If the first positional parameter is a (condition) function resp. partial, 
              taking one parameter, namely an element, (just) the elements, for which said
              function resp. partial returns True, are deleted.
              
              If, in this situation, the second parameter is 'single', 
              just the first element meeting said condition is deleted 
              (if there is none, None is returned), whereas if it is 'several', 
              all elements meeting said condition are deleted. Default is 'several'.
              
              If on the other hand the first positional parameter neither is of type 
              function nor of type partial, the parameter (just) is forwarded to 
              the list.__delitem__ method, leading to the behaviour of the standard 
              list type.
          """

          #delitem just takes exactly one parameter, this is why, if several
          #are given, e.g. self[a,b], this leads to params == ((a,b),),
          #which is not the common way of passing parameters to methods
          #the following changes this back to the common way
          paramsT = tuple()
          if (len(params) > 0):
             if     isinstance( params[0], Types_TupleType ):
                    #if params is a tuple containing a tuple (at the first position)
                    paramsT = params[0]
                
             else:
                    #if params is a tuple containing a non-tuple (at the first position)
                    paramsT = params
          
          #one or two 'real' parameters are accepted
          if    len(paramsT) == 1:
                #exactly one positional parameter ==> use it as the selector
                selector  = paramsT[0]
                multitude = several
                
          elif  (len(paramsT) == 2) and (paramsT[1] in (single, several)):
                #two positional parameters and the second either is 'single' or 'several'
                selector  = paramsT[0]
                multitude = paramsT[1]
                
          else:
                raise Exception( "Either one parameter or two parameters - with the "  \
                                 "second being 'single' or 'several' - is allowed!"    )
          
          #check, whether the selector is a function or a 'partial' or something else
          if  isinstance(selector, (Types_FunctionType, Functools_partial)):
                #selector is a function, returning True (just) for the elements to be returned
                selectionFunction = selector
          
                if    multitude is single:
                      #just delete the (very) first element meeting the condition
                      for indexI in xrange(list.__len__(self)):
                          if selectionFunction( list.__getitem__(self, indexI) ) == True:
                             return list.__delitem__( self, indexI )
                          
                      #if no element meets the condition, do nothing and return None
                      return None
          
                elif  multitude is several:
                      #delete all elements meeting the condition
          
                      indexI            = list.__len__(self) - 1
                               
                      #process list starting from the end using indices - as the list might be 
                      #modified during processing (by the deletions)
                      while indexI >= 0:
                          
                            #just delete elements, for which selectionFunction(element) returns True 
                            if selectionFunction( list.__getitem__(self, indexI) ) == True:
                               list.__delitem__(self, indexI )
                         
                            #next element
                            indexI -= 1
                          
                      #return the None
                      return None
                     
                else:
                      raise Exception("The parameter 'multitude' must either be 'single' or 'several'!")
                      
          else:    
                #forward to standard list behaviour 
                return list.__delitem__( self, selector )
                
                
      #method testing __getitem__
      @classmethod
      def _delitemSelftest(cls):
          """ """
          
          print ( "Testing EnhList.__delitem__..." )
          
          #index parameter
          testL = EnhList(1,3,5,7,9,11,13,15)
          del testL[4]
          assert testL == [1,3,5,7,11,13,15]
          
          #cross check slicing
          testL = EnhList(1,3,5,7,9,11,13,15)
          del testL[4:6]
          assert testL == [1,3,5,7,13,15]
          
          #cross check slicing with step with 2
          testL = EnhList(1,3,5,7,9,11,13,15)
          del testL[2:7:2]
          assert testL == [1,3,7,11,15]          
          
          #(lambda) function parameter - logical 'and'
          testL = EnhList(1,3,5,7,9,11,13,15)
          del testL[ lambda x: (x > 6) and (x < 10) ]
          assert testL == [1,3,5,11,13,15]
          
          #(lambda) function parameter - logical 'or'
          testL = EnhList(1,3,5,7,9,11,13,15)
          del testL[ lambda x: (x < 6) or (x > 10) ]
          assert testL == [7,9]
          
          #(lambda) function parameter - just the first
          testL = EnhList(1,3,5,7,9,11,13,15)
          del testL[ lambda x: (x > 6), single ]
          assert testL == [1,3,5,9,11,13,15]
          
          #(lambda) function parameter - none
          testL = EnhList(1,3,5,7,9,11,13,15)
          del testL[ lambda x: (x > 15), single ]
          assert testL == [1,3,5,7,9,11,13,15]        
                      
          #'partial' parameter - logical 'and'
          testL = EnhList(1,3,5,7,9,11,13,15)
          del testL[ (elem > 6) & (elem < 10) ]
          assert testL == [1,3,5,11,13,15]
          
          #'partial' function parameter - logical 'or'
          testL = EnhList(1,3,5,7,9,11,13,15)
          del testL[ (elem < 6) | (elem > 10) ]
          assert testL == [7,9]
          
          #'partial' function parameter - just the first
          testL = EnhList(1,3,5,7,9,11,13,15)
          del testL[ (elem > 6), single ]
          assert testL == [1,3,5,9,11,13,15]
          
          #'partial' function parameter - none
          testL = EnhList(1,3,5,7,9,11,13,15)
          del testL[ (elem > 15), single ]
          assert testL == [1,3,5,7,9,11,13,15]     
          
          print ( "...EnhList.__delitem__ tested sucessfully!" )               
          
        
      #check whether element(s) meeting a condition is/are in list
      @logExceptions
      def __contains__(self, selector):
          """
              If the (positional) parameter is a (condition) function resp. partial, 
              taking one parameter, namely an element, __contains__ returns True, if
              the list contains an element, for which said condition function returns 
              True - False otherwise.
              
              If on the other hand the (positional) parameter neither is of type 
              function nor of type partial, the parameter (just) is forwarded to 
              the list.__contains__ method, leading to the behaviour of the standard 
              list type.
          """
          
          if  isinstance(selector, (Types_FunctionType, Functools_partial)):
                #selector is a function, returning True (just) for elements checked for
                selectionFunction = selector
          
                #just search until one element meeting the condition has been found
                for indexI in xrange(list.__len__(self)):
                    if selectionFunction( list.__getitem__(self, indexI) ) == True:
                       #one element meeting the condition found
                       return True
                          
                #if no element met the condition, return False
                return False
          
          else:    
                #standard list behaviour 
                #selector should be an index to the element to be deleted
                return list.__contains__(self, selector)  
                
                
      #method testing __contains__
      @classmethod
      def _containsSelftest(cls):
          """ """
          
          print ( "Testing EnhList.__contains__..." )
          
          #object
          testL = EnhList(1,3,5,7,9,11,13,15)
          assert 7 in testL
              
          #(lambda) function parameter - logical 'and'
          testL = EnhList(1,3,5,7,9,11,13,15)
          assert (lambda x: (x > 5) and (x < 9)) in testL
          
          #(lambda) function parameter - logical 'or'
          testL = EnhList(1,3,5,7,9,11,13,15)
          assert (lambda x: (x < 1) or (x > 15)) not in testL
          
          #'partial' parameter - logical 'or' and 'and'
          testL = EnhList(1,3,5,7,9,11,13,15)
          assert (((elem == 3) | (elem == 7)) & ((elem > 4) | (elem < 4))) in testL
          
          print ( "...EnhList.__contains__ tested sucessfully!" )                 
        
   
      #check whether all elements of the list meet an condition
      @logExceptions
      def areAll(self, conditionFct):
          """ 
              Checks whether all elements of the list meet the condition
              described by the parameter conditionFct - which either can be a
              function or a 'partial' (inheritors are fine too).
              
              If conditionFct is True for all elements, True is returned - 
              False otherwise.
          """
          
          #ensure, that conditionFct is a function or a 'partial'
          assert isinstance(conditionFct, (Types_FunctionType, Functools_partial)),                           \
                 "The parameter 'conditionFct' must either be of type function or of type 'partial'!"
                 
          #just search until one element does not meet the condition has been found
          for indexI in xrange(list.__len__(self)):
              if conditionFct( list.__getitem__(self, indexI) ) == False:
                 #(at least) one element does not meet the condition
                 return False
                    
          #all elements met the condition
          return True
          
                                        
      #method testing areAll
      @classmethod
      def _areAllSelftest(cls):
          """ """
          
          print ( "Testing EnhList.areAll..." )
          
          #(lambda) function parameter - logical 'and'
          testL = EnhList(1,3,5,7,9,11,13,15)
          assert testL.areAll( lambda x: (x >= 1) and (x <= 15) )
          
          #(lambda) function parameter - logical 'or'
          testL = EnhList(1,3,5,7,9,11,13,15)
          assert testL.areAll( lambda x: (x >= 9) or (x <= 10) )
          
          #'partial' parameter - logical 'and'
          testL = EnhList(1,3,5,7,9,11,13,15)
          assert testL.areAll( (elem >= 1) & (elem <= 15) )
          
          #'partial' parameter - logical 'or'
          testL = EnhList(1,3,5,7,9,11,13,15)
          assert testL.areAll( (elem >= 9) | (elem <= 10) )

          #'partial' parameter - logical 'or'
          testL = EnhList(1,3,5,7,9,11,13,15)
          assert not testL.areAll( (elem >= 11) | (elem <= 8) )          
          
          print ( "...EnhList.areAll tested sucessfully!" ) 


      #map function to all elements meeting condition
      @logExceptions
      def mapIf(self, *params):
          """ 
               The first positional parameter 'mapO' is the 
               function / 'partial' / object to be  
               mapped to the list elements (inheritors are fine too). 
               
               The second positional parameter 'conditionFct' is the 
               condition function / 'partial'
               - the mapping just is done for list elements, which meet said 
               condition (means: for which the condition function returns True).
               
               If the (second positional) parameter 'conditionFct' is omitted, 
               it defaults to: 'lambda x: True' (means: True in any case).
          """
             
          #method accepts one or two parameters          
          if    len(params) == 1:
                #map all elements
                mapO = params[0]
                
                #ensure the correct type for mapO
                assert isinstance(mapO, (Types_FunctionType, Functools_partial, object)), \
                       "First positional parameter 'mapO' has the wrong type!"
                
                #map mapO to all elements - in-place
                for indexI in xrange(list.__len__(self)):
                   list.__setitem__( self, indexI, mapO(list.__getitem__(self, indexI)) )
                 
          elif  len(params) == 2:
                #just map elements, meeting the condition
                mapO         = params[0]
                conditionFct = params[1] 
                
                #ensure the correct type for mapO and conditionFct
                assert isinstance(mapO,         (Types_FunctionType, Functools_partial, object))          and \
                       isinstance(conditionFct, (Types_FunctionType, Functools_partial, Types_NoneType)),     \
                       "Parameter types do not fit!"                
                
                #map mapO to all elements, for which conditionFct returns True - in place
                for indexI in xrange(list.__len__(self)):
                    if conditionFct( list.__getitem__(self, indexI) ) == True:
                       list.__setitem__( self, indexI, mapO(list.__getitem__(self, indexI)) )
                       
          else:
                raise Exception("Method expects one or two parameters!")
                
          #just to be clear
          return None
              
              
      #method testing mapAll
      @classmethod
      def _mapIfSelftest(cls):
          """ """
          
          print ( "Testing EnhList.mapIf..." )
          
          #(lambda) function parameter
          testL = EnhList(1,3,5,7,9)
          testL.mapIf( lambda x: x*2 )
          assert testL == [2,6,10,14,18]
          
          #object parameter
          testL = EnhList(1,3,5,7,9)
          class testO(object):
                def __init__(self, value):
                    self.abc = value
          testL.mapIf( testO )
          assert [element.abc for element in testL] == [1,3,5,7,9]    
          
          ### with condition ###
          #(lambda) function parameter
          testL = EnhList(range(1,10))
          testL.mapIf( lambda x: x*2, lambda x: x % 2 == 0)
          assert testL == [1,4,3,8,5,12,7,16,9]
          
          #object parameter
          testL = EnhList(range(1,10))
          class testO(object):
                def __init__(self, value):
                    self.abc = value
                def __repr__(self):
                    return "abc=%s" % self.abc
                def __eq__(self, ohs):
                    return (True if self.abc == ohs else False)
          testL.mapIf( testO, elem > 5 )
          assert testL == [1,2,3,4,5,testO(6),testO(7),testO(8),testO(9)]

          print ( "...EnhList.mapIf tested sucessfully!" )    


      #create wrapper methods, which ensure, that all lists returned are of type EnhList
      for methodNameS in ( "__getslice__", "__add__", "__mul__", "__rmul__" ):
          #create methods using exec
          exec("""@logExceptions
def {0}(self, *params, **paramDict):
    ' A wrapper, which ensure that lists returned are of type EnhList. '
    
    #keep standard behaviour of standard list
    retVal = list.{0}(self, *params, **paramDict)
    
    #ensure that return value is a EnhList
    if isinstance(retVal, list):
       retVal = EnhList( retVal )
       
    #return value
    return retVal
               """.format(methodNameS))       


      #method testing self
      @classmethod
      def _selftest(cls):            
          """
              If no exception is raised during the execution of this method 
              the EnhList class behaves as expected.
              
              It e.g. can be used to check the integrity after modifications
              or to check the compatibility with specific python versions.
              
              Have a look into the methods called in this method for examples,
              how EnhList can be used.
          """
          
          print ( "Testing EnhList..." )
          
          cls._initSelftest()
          cls._pushSelftest()
          cls._popSelftest()
          cls._getitemSelftest()
          cls._delitemSelftest()
          cls._containsSelftest()
          cls._areAllSelftest()
          cls._mapIfSelftest()
          
          #test, whether all returned lists are EnhList-s
          eL = EnhList(1,3,5,7,9,11,13)
          assert isinstance( eL,               EnhList )
          assert isinstance( eL[2:4],          EnhList )
          assert isinstance( eL[2::2],         EnhList )
          assert isinstance( eL + [15,17],     EnhList )
          assert isinstance( eL * 3,           EnhList )
          assert isinstance( 3 * eL,           EnhList )
          assert isinstance( eL[elem > 3],     EnhList )
          assert isinstance( eL.pop(elem > 3), EnhList)
          
          print ( "...EnhList tested sucessfully!" )
          
          
          
class SemiBlockingMutex(object):
      """ 
          Locks normally either are blocking or non-blocking.
          
          Whereas this mutex is a lock, which is neither nor - it (just) is temporarily
          blocking. It blocks (just) until the internal lock either has been acquired 
          successfully or until a maximal total timeout (parameter 'timeoutMsF') 
          has expired.
          
          Until that, the 'acquire' method of the internal lock is polled. The time 
          interval/duration between two such polls is random - but it is in the range 
          given by the polling interval range tuple (parameter 'pollIntervalRangeMsT').
          
          Note, that the minimum of said range always is taken as the very first
          polling resp. sleep interval/duration. Just the following polling resp.
          sleep intervals/durations are random then - if any further (necessary at all).
          
          This mutex comes with the known 'acquire' and 'release' methods as well as 
          with context manager methods.

          Example:
          mutex = SemiBlockingMutex('threading')     #alternative: 'multiprocessing'
          with mutex: 
               print 'Mutex locked before this and unlocked after this - both automatically.' 
      """
      
      _lock                 = None      #either a threading.Lock or a multiprocessing.Lock
      _timeoutBucketMsF     = None      #contains the time left for acquiring successfully
      
      _timeoutMsF           = None      #max total timeout in ms - initial time bucket value
      _pollIntervalRangeMsT = None      #(min,max) single timeout time in ms
      
      _enterCntI             = None      #just used for the selfttests
      _exitCntI              = None      #just used for the selfttests


      #constructor
      @logExceptions
      def __init__( self, lockTypeS="threading",                       \
                    timeoutMsF=250.0, pollIntervalRangeMsT=(0.05, 5.0) ):
          """ 
               The positional parameter 'lockTypeS' either must be 'threading' or 'multiprocessing'
               - first leads to using a threading.Lock internally, second to multiprocessing.Lock.
               
               The 'acquire' method just blocks temporarily, the belonging total timeout is given               
               by the parameter 'timeoutMsF'.
               
               The parameter 'pollIntervalRangeMsT' determines the mean polling frequency during
               said temporary blocking phases.                              
          """
                    
          #init lock - either threading.Lock or multiprocessing.Lock
          if    lockTypeS  == "threading":
                self._lock  = Threading_Lock()
                
          elif  lockTypeS  == "multiprocessing":
                self._lock  = Multiprocessing_Lock()
                
          else:
                raise Exception("The positional parameter 'lockTypeS' either must be 'threading' or 'multiprocessing'!")
                
          #init total timeout and polling interval
          self._timeoutMsF           = timeoutMsF
          self._pollIntervalRangeMsT = pollIntervalRangeMsT
          
          #init variables for selftest
          self._enterCntI = 0
          self._exitCntI  = 0


      #blocks until SemiBlockingMutex is unlocked or a timeout has expired
      @logExceptions
      def acquire(self):
          """ 
              Polls 'acquire' until the internal lock has been acquired successfully - or
              until the self._timeoutBucketMsF has become empty.
              
              If SemiBlockingMutex is resp. becomes unlocked in time, the return value 
              is True (False otherwise). 
          """
          
          #reset timeout bucket
          self._timeoutBucketMsF = self._timeoutMsF
          
          #first poll 
          if self._lock.acquire(False) == True:
             return True
          
          #sleep minimal time
          minTimeMsF = min(self._pollIntervalRangeMsT)
          Time_sleep( minTimeMsF / 1000.0 )
          self._timeoutBucketMsF -= minTimeMsF
          
          #prepare random 'iterator' for the loop
          maxTimeMsF = max(self._pollIntervalRangeMsT)
          nextPollIntervalMsFct = Functools_partial( Random_uniform, minTimeMsF, maxTimeMsF )
          
          #retry acquiring until successful or timeout expired
          while self._lock.acquire(False) == False:
                
                #block this thread temporarily
                currTimeMsF = nextPollIntervalMsFct()
                Time_sleep( currTimeMsF / 1000.0 )
                
                #check for timeout
                self._timeoutBucketMsF -= currTimeMsF
                if self._timeoutBucketMsF <= 0:
                   #acquiring failed
                   return False

          #acquiring successful
          return True
          
          
      @logExceptions
      def release(self):
          """ Releases the lock. Just a forward to self._lock.release(). """

          self._lock.release()           


      #enter context
      @logExceptions
      def __enter__(self):
          """ Context is just entered if SemiBlockingMutex is resp. has successfully been unlocked.
              An exception is raised otherwise. """

          #increment counter for selftests
          self._enterCntI += 1    
          
          #acquire lock
          if self.acquire() == False:
             raise Exception('SemiBlockingMutex blocked too long (and is still locked)!')
             
          #return mutex itself for 'as' - if any
          return self


      #exit context
      @logExceptions
      def __exit__(self, *exception):
          """ When context is left, unlock SemiBlockingMutex in any case (as it has been acquired by
              entering said context before). """

          #increment counter for selftests
          self._exitCntI += 1
          
          #release lock
          self._lock.release() 
          
          #return None
          return None
          
          
          
#list with automatic locking mechanism
class LockedList(object):
      """ 
          Intelligent wrapper class. Wraps all methods named in the
          tuple 'lockedMethodsT' with a 'self._lock.acquire()' (before) 
          and a 'self._lock.release()' (after) -- by entering an 
          according 'with' context -- to make (in particular in-place) 
          access to classes inheriting from 'LockedList' thread-safe.
         
          Such locked methods wrap the belonging methods of the first 
          class in the inheritance order list, which is to the right to 
          the first entry being a subclass of 'LockedList' (likely this 
          class) and which furthermore is a subclass of 'TypedList' or 
          'list'.
          
          In other words: a 'locked' method of this class calls the 
          method of the same name of the class '_fwdToCls'.
          
          Example:
          class Ex(AAA,LockedList,BBB,EnhList):
                ...
                
          ex = Ex()
          ex[2]
          
          Assuming that isinstance(BBB, list) ist False, the last line  
          resp. command  leads to calling 'LockedList.__getitem__',
          which, after entering said 'lock'-'with' context, calls 
          'EnhList.__getitem__'.
          
          Parameters are: 
          ---------------
              
          'lockTypeS','timeoutMsF' and 'pollIntervalRangeMsT'
              
           - which are forwarded to the constructor of SemiBlockingMutex; 
           other parameters are just ignored! 
           
           Have a look at the doc/help-text for SemiBlockingMutex for
           details.
      """

      _fwdToCls      = None       #the methods of LockedList just wrap the methods of the same name of Cls  
      _lock          = None
      
      lockedMethodsT = ( "__add__", "__contains__", "__delitem__", "__delslice__", "__eq__",  \
                         "__ge__", "__getitem__", "__getslice__", "__gt__",                   \
                         "__iadd__", "__imul__", "__le__", "__len__", "__lt__", "__mul__",    \
                         "__ne__", "__repr__", "__reversed__",                                \
                         "__rmul__", "__setitem__", "__setslice__", "__sizeof__",             \
                         "append", "areAll", "count", "extend", "index", "insert", "mapIf",   \
                         "pop", "push", "remove", "reverse", "sort"                           ) 
      
      
      #init
      @logExceptions
      def __init__(self, **paramDict):
          """ 
              Accepted parameters are: 
              
              'lockTypeS','timeoutMsF' and 'pollIntervalRangeMsT'
              
              - which are forwarded to the constructor of 
              SemiBlockingMutex; other parameters are just ignored!
          """
          
          #ignore keys from paramDict, which aren't valid keys for keyword parameters for 
          #self resp. its internal lock
          selfParamDict = dict()
          for key in ('lockTypeS','timeoutMsF','pollIntervalRangeMsT'):
              #Python 2, Python 3 compatibility 
              if    isPy2() == True:
                    #'has_key' is Python 2.* only
                    hasKeyB = paramDict.has_key(key)
              else:
                    #this usage of 'in' is Python 3.* only
                    hasKeyB = key in paramDict
                    
              #copy values just for keys of tuple if found in dict
              if hasKeyB == True:
                 selfParamDict[key] = paramDict[key]
                 
          #create the internal lock
          self._lock = SemiBlockingMutex( **selfParamDict )

          #inheritance order list belonging to super class          
          basesL              = EnhList(self.__class__.__bases__)   
          
          #get index of first element of inheritance order list, which is a subclass of
          #LockedList (this class)
          lockedListIndexI    = [issubclass(element, LockedList) for element in basesL].index(True)
          
          #just take classes into account, which are 'to the right' in the inheritance order list
          #from POV of the first element, which is a subclass of LockedList
          basesL              = basesL[lockedListIndexI+1:]
          
          #get first class, being a subclass of list, to the right to this class
          self._fwdToCls = basesL.pop( lambda e: issubclass(e, (TypedList, list)), single )
          if self._fwdToCls == None:
             raise Exception( "There at least must be one 'list' or 'TypedList' type,  " \
                              "with lower precedence ('to the right, POV LockedList'), " \
                              "in the inheritance (order) list!"                         )
                              
             
      #create wrapper methods
      for methodNameS in lockedMethodsT:
          exec( """def {0}(self, *params, **paramDict):
    " Wraps '{0}' of self._fwdToCls with a lock-acquire/lock-release (using 'with self._lock:...'). "
          
    with self._lock:
         return getattr( self._fwdToCls, "{0}" )(self, *params, **paramDict)
                  """.format(methodNameS) )
      del methodNameS
                           

          
#list with an automatic type check / enforcement    
class TypedList(object):
      """ TBD. Just a dummy yet. Parameters: 'elemTypesT', others are ignored. """
      
      _fwdToCls    = None
      _elemTypesT  = None
          
         
      #init
      @logExceptions
      def __init__(self, **paramDict):
          """ TBD. """
          
          
          #Python 2, Python 3 compatibility 
          if    isPy2() == True:
                #'has_key' is Python 2.* only
                hasKeyB = paramDict.has_key('elemTypesT')
                
          else:
                hasKeyB = 'elemTypesT' in paramDict
                   
          ###ignore keys from paramDict - but the parameter 'elemTypesT' ###
          if    hasKeyB == True:
                #init
                self._elemTypesT = paramDict['elemTypesT']
                
                #check elem types
                if not isinstance(self._elemTypesT, tuple)                   or \
                   not all( map(lambda x: type(x) == type, self._elemTypesT)    ):
                   raise Exception("Parameter 'elemTypesT' must be a tuple of types!")
                
          else:
                self._elemTypesT = None
             
             
      #TBD: if self._elemTypesT is a tuple of types, the elements of the list will only
      #be allowed to be of said types. If, on the other hand, self._elemTypesT == None
      #there will be no such restriction for the elements of the list (as it is now). 
    

    
#secured EnhList list providing thread-safe access 
class SecList(TypedList, LockedList, EnhList):
      """ 
          A 'SecList' is a wrapped 'EnhList' whereby the wrapper ensures,
          that access to the content of the list automatically is secured 
          by an internal threading or multiprocessing lock; this is achieved  
          by wrapping the access methods in a 'with' context using said 
          internal lock.
          
          The belonging '__enter__' method 'acquires' said lock, the 
          belonging '__exit__' method releases said lock. Said lock is a 
          'SemiBlockingMutex' which blocks - but just temporarily (timeout).
          See the doc texts of 'SemiBlockingMutex' and 'LockedList' for 
          further informations.
          
          Simple example for an automatically secured (thread-safe) access:
          -----------------------------------------------------------------
          
          sL = SecList(1,3,5,7)
          nL = sL[ (elem > 1) & (elem < 7) ]      #nL ==> [3,5]   
          
          A more extensive example for safe multi threaded access can be found
          in self._testThreadSafety().


          The iterator protocol is not (automatically) wrapped / secured; 
          if thread safety is not necessary, but performance is, then
          iterator access can be used on 'SecList'-s. But you of course also 
          can secure it manually by using the 'with' statement.
          
          Simple example for a manually secured (thread-safe) access:
          -----------------------------------------------------------
          
          sL = SecList(1,3,5,7)
          with sL:           
               nL = [element+1 for element in sL]  #nL ==> [2,4,6,8]
               
          Further examples can be found in self._selftest().

          
          Using (external) functions alike the built-ins 'map', 'reduce', 
          'sum' or the 'pickle.dumps/loads' on a 'SecList' should not be 
          done at all or should at least be done with care - they might
          not behave like intuitively expected.
          
          They e.g.:
          - might not be secured by a 'SecList'-'with' context 
            (might not be thread safe without further means)
          - might not work in a 'SecList'-'with' context 
            (might not be usable in a thread safe manner)
          - might not return a 'SecList' but e.g. a 'list' instead
            (might return an unexpected type)
          - might not work on a 'SecList' at all (e.g. pickle)
          
          You might want to convert the 'SecList' to a 'list', before you 
          use said functions on it.
          
          Parameters are: 
          ---------------
              
          'elemTypesT', 'lockTypeS', 'timeoutMsF' and 'pollIntervalRangeMsT'
          
          whereby is fed into the constructor of the parent class 'TypedList'
          and
          
          'lockTypeS', 'timeoutMsF' and 'pollIntervalRangeMsT'
          
          are fed into the constructor of the parent class 'LockedList'. 
          
          Positional parameters are fed into the constructor of 'EnhList'.
          
          Have a look at doc/help-texts of 'TypedList', 'LockedList' and 
          'EnhList' for further details.
      """
       
       
      #initialisation
      @logExceptions
      def __init__(self, *params, **paramDict):
          """ See source code and belonging comments! """
           
          TypedList.__init__(  self, **paramDict )  #ignores all parameters but with key 'elemTypesT'
          LockedList.__init__( self, **paramDict )  #ignores all parameters but with keys 'lockTypeS',
                                                    #'timeoutMsF' and 'pollIntervalRangeMsT'
          EnhList.__init__(    self, *params     )  #just takes positional parameters into account
          
          
      #method called when entering a 'with' block
      @logExceptions
      def __enter__(self):
          """ With the 'with' statement a lock context is enetered. """
          
          return self._lock.__enter__()
          
          
      #method called when exiting a 'with' block
      @logExceptions
      def __exit__(self, *exception):
          """ Leave the lock context. """
          
          return self._lock.__exit__(*exception)          
          
          
      #create wrapper method, which ensure, that all lists returned are of type SecList
      for methodNameS in ( "__getitem__", "__getslice__",          \
                           "pop", "__add__", "__mul__", "__rmul__" ):
          #create methods using exec
          exec("""@logExceptions
def {0}(self, *params, **paramDict):
    ' A wrapper, which ensure that lists returned are of type SecList. '
    
    #keep standard behaviour of LockedList / EnhList
    retVal = LockedList.{0}(self, *params, **paramDict)
    
    #ensure that return value is a SecList
    if isinstance(retVal, list):
       retVal = SecList( retVal )
       
    #return value
    return retVal
               """.format(methodNameS))
                      
            
            
      #test thread-safety
      @classmethod
      @muteLogging
      def _testThreadSafety(self):
          """ Test whether SecList can be used thread-safe. """
          
          print ( "Testing Thread-Safety (needs a little time) ..." )
   
          def lockTest(threadIndexI, sL, numberOfElemsI=1000):
              """ Thread function - run by several threads in parallel. """    
              global elem
              
              #a 'define'
              numberOfElemsI = 1000
              
              #create a list of indices with random order
              baseL          = list(range(1,numberOfElemsI))
              Random_shuffle(baseL)
              
              #list for comparison
              cmpL = EnhList()
              
              #push elements into sL
              for element in baseL:
                  #identity function with high CPU effort
                  currO = TestO( threadIndexI, Math_factorial(element) / Math_factorial(element-1) )
                  
                  #this is a first secured (thread-safe) operation
                  sL.push( currO )
                       
              #pop elements from sL
              for indexI in range(1,numberOfElemsI):
                  #pop elements in order - this is a second secured (thread-safe) operation
                  popped = sL.pop((elem.a == threadIndexI) & (elem.b <= indexI))
                  
                  #check whether popped element is OK
                  if (len(popped) != 1) or (not hasattr(popped[0], "b")) or (popped[0].b != indexI):
                     raise Exception("Popped wrong element!") 
                     
                  #append to compare list
                  cmpL.push( popped[0] )
                     
              #check result
              cmpL.mapIf( lambda x: x.b )
              assert cmpL == list(range(1,numberOfElemsI))
              
             
          #the 'global' list for all threads
          sL     = SecList()
                       
          #create threads
          print("Test thread number 0 created")
          thread0        = Threading_Thread(target=lockTest, args=(0, sL))
          thread0.daemon = True
          print("Test thread number 1 created")
          thread1        = Threading_Thread(target=lockTest, args=(1, sL))
          thread1.daemon = True          
          print("Test thread number 2 created")
          thread2        = Threading_Thread(target=lockTest, args=(2, sL))
          thread2.daemon = True         
             
          #start threads
          thread0.start()
          thread1.start()
          thread2.start()
            
          #wait until threads finished
          thread0.join()
          thread1.join()
          thread2.join()
          
          print("All test threads finished.")
               
          print ( "Thread-Safety tested successfully!" )
            
            
      #selftest
      @classmethod
      @muteLogging
      def _selftest(self):
          """ 
              Tests whether this class works as expected. It seems to, 
              if no exceptions are raised during the test.
          """
          
          print ( "Testing SecList..." )
          
          #create list using several parameters
          sL = SecList(1,3,5,7,9,11,13,15,17)
          assert isinstance(sL, SecList)
          assert sL == [1,3,5,7,9,11,13,15,17]
          assert sL._lock._enterCntI == 1
          assert sL._lock._exitCntI  == 1
          
          #create list using another list
          sL = SecList([1,3,5,7,9,11,13,15,17])
          assert isinstance(sL, SecList)
          assert sL == [1,3,5,7,9,11,13,15,17]
          assert sL._lock._enterCntI == 1
          assert sL._lock._exitCntI  == 1            
          
          #get item using an index
          item = sL[2]
          assert item == 5
          assert sL == [1,3,5,7,9,11,13,15,17]
          assert sL._lock._enterCntI == 3
          assert sL._lock._exitCntI  == 3
          
          #get single item using a condition
          item = sL[(elem > 5) & (elem < 11), single]
          assert sL == [1,3,5,7,9,11,13,15,17]
          assert item == 7
          assert sL._lock._enterCntI == 5
          assert sL._lock._exitCntI  == 5
          
          #get several items using a condition
          items = sL[(elem > 5) & (elem < 11), several]
          assert sL == [1,3,5,7,9,11,13,15,17]
          assert items == [7,9]
          assert isinstance(items, SecList)
          assert sL._lock._enterCntI == 7
          assert sL._lock._exitCntI  == 7           
          
          #get slice
          slicee = sL[3:5]
          assert slicee == [7,9]
          assert isinstance(slicee, SecList)
          assert sL == [1,3,5,7,9,11,13,15,17]
          assert sL._lock._enterCntI == 9
          assert sL._lock._exitCntI  == 9           

          #pop first
          popped = sL.pop()
          assert popped == 1
          assert sL == [3,5,7,9,11,13,15,17]
          assert sL._lock._enterCntI == 11
          assert sL._lock._exitCntI  == 11
          
          #pop first meeting a condition
          popped = sL.pop( (elem > 5) & (elem < 11), single )
          assert popped == 7
          assert sL == [3,5,9,11,13,15,17]
          assert sL._lock._enterCntI == 13
          assert sL._lock._exitCntI  == 13     
          
          #pop all meeting a condition
          popped = sL.pop( (elem > 11) & (elem < 17), several )
          assert popped == [13,15]
          assert isinstance(popped, SecList)
          assert sL == [3,5,9,11,17]
          assert sL._lock._enterCntI == 15
          assert sL._lock._exitCntI  == 15                   

          #push single
          pushed = sL.push(19)
          assert pushed == None
          assert sL == [3,5,9,11,17,19]
          assert sL._lock._enterCntI == 17
          assert sL._lock._exitCntI  == 17 
          
          #push several
          pushed = sL.push(21,23,25)
          assert pushed == None
          assert sL == [3,5,9,11,17,19,21,23,25]
          assert sL._lock._enterCntI == 19
          assert sL._lock._exitCntI  == 19            
          
          #set slice
          sL[2:4] = [111,222]
          assert sL == [3,5,111,222,17,19,21,23,25]
          assert sL._lock._enterCntI == 21
          assert sL._lock._exitCntI  == 21            
          
          #append
          assert sL.append( 27 ) == None
          assert sL == [3,5,111,222,17,19,21,23,25,27]
          assert sL._lock._enterCntI == 23
          assert sL._lock._exitCntI  == 23          
          
          #are all test
          assert sL.areAll( elem > 2 ) == True
          assert sL == [3,5,111,222,17,19,21,23,25,27]
          assert sL._lock._enterCntI == 25
          assert sL._lock._exitCntI  == 25            
          
          #count number of occurences
          assert sL.count( 19 ) == 1
          assert sL == [3,5,111,222,17,19,21,23,25,27]
          assert sL._lock._enterCntI == 27
          assert sL._lock._exitCntI  == 27

          #extend list
          assert sL.extend([29,31]) == None
          assert sL == [3,5,111,222,17,19,21,23,25,27,29,31]
          assert sL._lock._enterCntI == 29
          assert sL._lock._exitCntI  == 29

          #get index of an element
          assert sL.index(19) == 5
          assert sL == [3,5,111,222,17,19,21,23,25,27,29,31]
          assert sL._lock._enterCntI == 31
          assert sL._lock._exitCntI  == 31

          #insert in list
          assert sL.insert(3, 333) == None
          assert sL == [3,5,111,333,222,17,19,21,23,25,27,29,31]
          assert sL._lock._enterCntI == 33
          assert sL._lock._exitCntI  == 33  

          #map function on elements 
          assert sL.mapIf( lambda x: x * 2 ) == None
          assert sL == [6,10,222,666,444,34,38,42,46,50,54,58,62]
          assert sL._lock._enterCntI == 35
          assert sL._lock._exitCntI  == 35   
          
          #map function on elements if codition is met
          assert sL.mapIf( lambda x: x / 3, elem % 3 == 0 ) == None
          assert sL == [2,10,74,222,148,34,38,14,46,50,18,58,62]
          assert sL._lock._enterCntI == 37
          assert sL._lock._exitCntI  == 37            
          
          #remove value
          assert sL.remove( 222 ) == None
          assert sL == [2,10,74,148,34,38,14,46,50,18,58,62]
          assert sL._lock._enterCntI == 39
          assert sL._lock._exitCntI  == 39   

          #reverse element order
          assert sL.reverse() == None
          assert sL == [62,58,18,50,46,14,38,34,148,74,10,2]
          assert sL._lock._enterCntI == 41
          assert sL._lock._exitCntI  == 41   
          
          #sort list
          assert sL.sort() == None
          assert sL == [2,10,14,18,34,38,46,50,58,62,74,148]
          assert sL._lock._enterCntI == 43
          assert sL._lock._exitCntI  == 43 
          
          #add list
          nL = sL + [150,151]
          assert nL == [2,10,14,18,34,38,46,50,58,62,74,148,150,151]
          assert isinstance(nL, SecList) == True
          assert sL._lock._enterCntI == 44
          assert sL._lock._exitCntI  == 44           
          
          #check whether list contains a value
          assert (50 in sL) == True
          assert (51 in sL) == False
          assert ((elem > 46) in sL) == True
          assert (((elem > 46) & (elem < 50)) in sL) == False
          assert sL == [2,10,14,18,34,38,46,50,58,62,74,148]
          assert sL._lock._enterCntI == 49
          assert sL._lock._exitCntI  == 49  
          
          #delete item(s)
          del sL[2]
          assert sL == [2,10,18,34,38,46,50,58,62,74,148]
          
          del sL[elem > 50, single]
          assert sL == [2,10,18,34,38,46,50,62,74,148]
          
          del sL[elem < 34]
          assert sL == [34,38,46,50,62,74,148]
          
          assert sL._lock._enterCntI == 55
          assert sL._lock._exitCntI  == 55          
          
          #delete slice
          del sL[::2]
          assert sL == [38,50,74]
          assert sL._lock._enterCntI == 57
          assert sL._lock._exitCntI  == 57 

          #string/display conversion
          out1S = "test: {0}".format(sL)
          out2S = "test: %s" % sL
          out3S = "test: " + repr(sL)
          out4S = "test: " + str(sL)
          assert (out1S == out2S == out3S == out4S) == True
          assert sL._lock._enterCntI == 61
          assert sL._lock._exitCntI  == 61 
          
          #concatenate
          sL += [101,102]
          assert sL == [38,50,74,101,102]
          assert isinstance(sL, SecList)
          assert sL._lock._enterCntI == 63
          assert sL._lock._exitCntI  == 63      
          
          #in-place multiply
          sL *= 2
          assert sL == [38,50,74,101,102,38,50,74,101,102]
          assert isinstance(sL, SecList)
          assert sL._lock._enterCntI == 65
          assert sL._lock._exitCntI  == 65   
          
          #get number of elements
          noes = len(sL)
          assert noes == 10
          assert sL._lock._enterCntI == 66
          assert sL._lock._exitCntI  == 66
          
          #multiply
          nL = sL * 2
          assert nL == [38,50,74,101,102,38,50,74,101,102,38,50,74,101,102,38,50,74,101,102]
          assert isinstance(nL, SecList)
          assert sL._lock._enterCntI == 67
          assert sL._lock._exitCntI  == 67  
          
          #set item
          sL[2]  = 75
          sL[2] += 1
          assert sL == [38,50,76,101,102,38,50,74,101,102]
          assert isinstance(sL, SecList)
          assert sL._lock._enterCntI == 71
          assert sL._lock._exitCntI  == 71   
          
          #right multiply
          nL = 2 * sL
          assert nL == [38,50,76,101,102,38,50,74,101,102,38,50,76,101,102,38,50,74,101,102]
          assert isinstance(nL, SecList)
          assert sL._lock._enterCntI == 72
          assert sL._lock._exitCntI  == 72  
          
          #get size in memory
          assert isinstance(sL.__sizeof__(), int) == True
          assert sL._lock._enterCntI == 73
          assert sL._lock._exitCntI  == 73 

          #external functions do not trigger a lock context
          #that's why a 'with' is necessary here
          with sL:
               if isPy2() == True:
                  reduced = reduce(lambda x,y: x+y, sL)
                  sumed   = sum(sL)
                  assert reduced == sumed
          assert sL._lock._enterCntI == 74
          assert sL._lock._exitCntI  == 74
          
          #pop indexed
          assert sL.pop(3) == 101
          assert sL == [38,50,76,102,38,50,74,101,102]
          assert sL._lock._enterCntI == 76
          assert sL._lock._exitCntI  == 76          
          
          #comparison - not equal
          assert (sL != []) == True
          assert (sL != [38,50,76,102,38,50,74,101,102]) == False
          assert sL._lock._enterCntI == 78
          assert sL._lock._exitCntI  == 78
          
          #iterator protocol - list comprehension
          with sL:
               nL = [element for element in sL if element > 50]
          assert nL == [76,102,74,101,102]
          assert sL._lock._enterCntI == 79
          assert sL._lock._exitCntI  == 79 
          
          #iterator protocol - tuple comprehension
          with sL:
               nL = SecList((element for element in sL if element > 50))
          assert nL == [76,102,74,101,102]
          assert sL._lock._enterCntI == 80
          assert sL._lock._exitCntI  == 80   
          
          #iterator protocol - next
          nL = SecList()
          iterator = iter(sL)
          try:
                 with sL:
                      while True:
                            if    isPy2() == True:
                                  nL.push( iterator.next() )
                            else:
                                  nL.push( iterator.__next__() )
                        
          except StopIteration:
                 pass
          assert sL == nL
          assert sL._lock._enterCntI == 82
          assert sL._lock._exitCntI  == 82 
          
          #min, max
          assert min(sL) == 38
          assert max(sL) == 102
          assert sL._lock._enterCntI == 82
          assert sL._lock._exitCntI  == 82 

          #for ... in ...
          summed = 0
          with sL:
               for element in sL:
                   summed += element
          assert summed == sum(sL)
          assert sL._lock._enterCntI == 83
          assert sL._lock._exitCntI  == 83           
          
          #pickle
          pickled   = Pickle_dumps(list(sL))
          unpickled = Pickle_loads(pickled)
          assert unpickled == sL
          assert sL._lock._enterCntI == 85
          assert sL._lock._exitCntI  == 85            
          
          #map
          mapped    = map(int, list(sL))
          assert list(mapped) == sL
          assert sL._lock._enterCntI == 87
          assert sL._lock._exitCntI  == 87  

          #test thread safety
          self._testThreadSafety()    
          
          #test, whether all returned lists are SecList-s
          sL = SecList(1,3,5,7,9,11,13)
          assert isinstance( sL,               SecList )
          assert isinstance( sL[2:4],          SecList )
          assert isinstance( sL[2::2],         SecList )
          assert isinstance( sL + [15,17],     SecList )
          assert isinstance( sL * 3,           SecList )
          assert isinstance( 3 * sL,           SecList )
          assert isinstance( sL[elem > 3],     SecList )
          assert isinstance( sL.pop(elem > 3), SecList)          
        
          print ( "...SecList tested successfully!" )
          
 

                             
##################
### Test Means ###
##################
class TestO(object):
      """ """
      
      def __init__(self, vala, valb=None):
          """ """
          
          self.a = vala   
          self.b = vala if valb == None else valb
          
      def __eq__(self, ohs):
          return (self.a==ohs.a) and (self.b==ohs.b)
 
      def __repr__(self):
          return "(a=%s, b=%s)" % (self.a, self.b)  
          
class TestL(list):
      """ """

      def __init__(self, val):
          """ """
          
          list.__init__(self, (val, val, val))
 
class TestD(dict):
      """ """
      
      def __init__(self, val):
          """ """
          
          dict.__init__(self, a=val, b=val)
          
      def __eq__(self, ohs):
          return (self['a']==ohs['a']) and (self['b']==ohs['b'])
          
      
#############################
# module selfttest function #
#############################
def selftest():
    """
        Calls all test functions contained in this module.
        If there is no exception resp. assertion error, module seems to do what it
        is expected to.
    """
    
    print ( "Testing Module..." )
    
    _testElem()
    EnhList._selftest()
    
    ### test attribute and item access using 'elem' ###
    #list of objects with attributes 
    print ( "Testing attribute and item access..." )
    
    enhList = EnhList( range(1,17) )
    poppedL = enhList.pop( ((elem > 3) & (elem < 9)) | ((elem > 9) & (elem < 15)) )
    assert poppedL  == [4,5,6,7,8,10,11,12,13,14]
    assert enhList  == [1,2,3,9,15,16]
    
    #list of objects with attributes 
    enhList = EnhList( map(TestO, range(1,17)) )
    poppedL = enhList.pop( ((elem.a > 3) & (elem.a < 9)) | ((elem.b > 9) & (elem.b < 15)) )
    assert poppedL  == list(map(TestO, [4,5,6,7,8,10,11,12,13,14]))
    assert enhList  == list(map(TestO, [1,2,3,9,15,16]))

    #list of lists 
    enhList = EnhList( map(TestL, range(1,17)) )
    poppedL = enhList.pop( ((elem[0] > 3) & (elem[2] < 9)) | ((elem[0] > 9) & (elem[2] < 15)) )
    assert poppedL  == list(map(TestL, [4,5,6,7,8,10,11,12,13,14]))
    assert enhList  == list(map(TestL, [1,2,3,9,15,16]))  
   
    #list of dictionaries 
    enhList = EnhList( map(TestD, range(1,17)) )
    poppedL = enhList.pop( ((elem['a'] > 3) & (elem['b'] < 9)) | ((elem['a'] > 9) & (elem['b'] < 15)) )
    assert poppedL  == list(map(TestD, [4,5,6,7,8,10,11,12,13,14]))
    assert enhList  == list(map(TestD, [1,2,3,9,15,16]))
    
    SecList._selftest()
    
    print ( "...attribute and item access tested successfully!" )
    
    print ( "...Module tested successfully!" )        
          

       
       
if __name__ == "__main__":
  
   #parse command line arguments
   argParser = Argparse_ArgumentParser()
   argParser.add_argument("--test", action="store_true", help="run code testing this library for errors using test cases.")
   argParser.add_argument("--intro", action="store_true", help="print introduction to this library.")
   args      = argParser.parse_args()
   

   #run tests if '--test' is given in command line
   if    args.test == True:          
         selftest()
       
       
   if    args.intro == True:
         introS=\
"""
############
# EnhList: #
############

""" + EnhList.__doc__ + \
"""


############
# SecList: #
############
""" + SecList.__doc__

         print (introS)
         
         
         
             
#TBD: implement/finish TypedList
#TBD: ponder about whether to also implement a conditional __setitem__ 
#(alike eL[elem > 3] = lambda x: x**2 or at least alike eL[elem > 3] = None)
#TBD: check cythonized



