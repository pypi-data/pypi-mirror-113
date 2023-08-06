# -*- coding: utf-8 -*-
"""
Created on Tue Oct 22 14:07:34 2019

@author: yuanq
"""

def find_path(dic_graph, start, end, lst_path=[]):
    lst_path = lst_path + [start]
    if start == end:
        return lst_path
    if not start in dic_graph:
        return None
    for node in graph[start]:
        if node not in lst_path:
            lst_newpath = find_path(dic_graph, node, end, lst_path)
            if lst_newpath: return lst_newpath
    return None

def find_all_paths(graph, start, end, path=[]):
    path = path + [start]
    if start == end:
        return [path]
    if not graph.has_key(start):
        return []
    paths = []
    for node in graph[start]:
        if node not in path:
            newpaths = find_all_paths(graph, node, end, path)
            for newpath in newpaths:
                paths.append(newpath)
    return paths

def find_shortest_path(graph, start, end, path=[]):
    path = path + [start]
    if start == end:
        return path
    if not graph.has_key(start):
        return None
    shortest = None
    for node in graph[start]:
        if node not in path:
            newpath = find_shortest_path(graph, node, end, path)
            if newpath:
                if not shortest or len(newpath) < len(shortest):
                    shortest = newpath
    return shortest