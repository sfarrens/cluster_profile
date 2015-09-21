## @file errors.py
#
#  ERROR FUNCTIONS 
#
#  Custom exceptions.
#  
#  @author Samuel Farrens
#  @version 1.0
#  @date 2015
#

import os.path

##
#  Function that checks if the input file
#  name is valid.
#
#  @param[in] file_name: Input file name.
#
#  @exception IOError for invalid file name.
#
def file_name_error(file_name):

   if file_name == '' or file_name[0][0] == '-':
      raise IOError('Input file name not specified.')
      
   elif os.path.isfile(file_name) == False:
      raise IOError('Input file name [%s] not found!' % file_name)

