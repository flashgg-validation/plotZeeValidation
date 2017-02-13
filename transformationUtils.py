#!/usr/bin/env python

#----------------------------------------------------------------------

def getTGraphs(rootDir):
    
    import ROOT

    retval = []

    for key in rootDir.GetListOfKeys():

        obj = rootDir.Get(key.GetName())

        if isinstance(obj, ROOT.TGraph):
            retval.append(obj)

    return retval


#----------------------------------------------------------------------

def getGraphPoints(graph):

    n = graph.GetN();

    xarray = graph.GetX()
    yarray = graph.GetY()

    return [ xarray[i] for i in range(n)], [ yarray[i] for i in range(n) ]


#----------------------------------------------------------------------
