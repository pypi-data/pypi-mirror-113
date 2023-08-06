# -*- coding: utf-8 -*-
"""
Created on Thu Jan 31 00:17:06 2019

@author: LIM YUAN QING
"""
 
## Public libraries
import enum

@enum.unique
class ENUM_DATABASE_TYPE(enum.Enum):
    ACCESS  = 1
    POSTGRE = 2

@enum.unique
class ENUM_OPERATION_TYPE(enum.Enum):
    CREATE  = 1
    READ    = 2
    UPDATE  = 3
    DELETE  = 4    

@enum.unique
class ENUM_QUERY_TYPE(enum.Enum):
    SELECT          = 1
    INSERT          = 2
    CREATE_TABLE    = 3
    DROP_TABLE      = 4
    UPDATE          = 5

@enum.unique
class ENUM_OPERATOR_TYPE(enum.Enum):
    GREATER =       1
    LESSER =        2
    GREATER_EQUAL = 3
    LESSER_EQUAL =  4
    EQUAL =         5
    NOT_EQUAL =     6
    BETWEEN =       7
    
DIC_DATA_TYPES_MAPPING = {'text':{ENUM_DATABASE_TYPE.ACCESS:'MEMO',
                                  ENUM_DATABASE_TYPE.POSTGRE:'TEXT'},
                            'bool':{ENUM_DATABASE_TYPE.POSTGRE:'BOOLEAN'}}