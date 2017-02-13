#!/usr/bin/env python

from optparse import OptionParser
import sys, array

import transformationUtils

#----------------------------------------------------------------------
# main
#----------------------------------------------------------------------

if (__name__ == "__main__"):
    parser = OptionParser(usage="Usage: %prog [options] transformationFile.root")

    (options, ARGV) = parser.parse_args()

    if len(ARGV) != 1:
        print >> sys.stderr,"must specify exactly one input file"
        sys.exit(1)

    inputFname = ARGV.pop(0)


    #----------
    import ROOT ; gcs = []


    fin = ROOT.TFile.Open(inputFname)

    graphs = transformationUtils.getTGraphs(fin)

    yPadSplit = 0.5


    for graph in graphs:

        canvas = ROOT.TCanvas()

        gcs.append(canvas)

        canvas.Divide(1,2)


        #----------
        # draw the graph
        #----------

        canvas.cd(1)
        ROOT.gPad.SetPad(0, yPadSplit,
                         1, 1)

        graph.Draw()
        ROOT.gPad.SetGrid()
        graph.GetHistogram().SetTitle(graph.GetName())

        #----------
        # draw the difference of the graph w.r.t to one (the identity transformation)
        #----------

        # create a graph for the difference
        xval, yval = transformationUtils.getGraphPoints(graph)
        yval = [ y - x for x,y in zip(xval,yval) ]
        
        gr = ROOT.TGraph(len(xval),
                         array.array('f', xval),
                         array.array('f', yval))
        gcs.append(gr)

        canvas.cd(2)
        ROOT.gPad.SetPad(0, 0,
                         1, yPadSplit)

        gr.Draw()

        gr.GetHistogram().SetTitle("absolute shift")
        ROOT.gPad.SetGrid()

        #----------
        canvas.cd()

