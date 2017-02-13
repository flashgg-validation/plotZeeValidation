#!/usr/bin/env python

from optparse import OptionParser
import sys, array

import transformationUtils

#----------------------------------------------------------------------

def evalChainedGraph(graphs, xval):
    
    assert len(graphs) > 0

    for gr in graphs:
        xval = gr.Eval(xval)

    return xval

#----------------------------------------------------------------------
# main
#----------------------------------------------------------------------

if (__name__ == "__main__"):
    parser = OptionParser(usage="Usage: %prog [options] transformationFile1.root transformationFile2.root [ transformationFile3.root ... ]")

    parser.add_option("-o", 
                      dest="outputFname", 
                      help="output file to write the chained transformations to", 
                      default = None,
                      metavar = "out.root")

    (options, ARGV) = parser.parse_args()

    if len(ARGV) < 2:
        print >> sys.stderr,"must specify at least two input files"
        sys.exit(1)

    if options.outputFname == None:
        print >> sys.stderr,"must specify an output file with -o"
        sys.exit(1)

    inputFnames = ARGV

    # open all input files and get a list of all graphs in them
    import ROOT

    # first index is input file number, second index is graph name, key is actual transformation graph
    inputGraphs = []
    
    commonNames = None

    for fname in inputFnames:
        fin = ROOT.TFile.Open(fname)
        
        if fin == None or not fin.IsOpen():
            print >> sys.stderr,"failed to open input file",fname
            sys.exit(1)

        graphs = transformationUtils.getTGraphs(fin)

        tmp = dict([ (graph.GetName(), graph) for graph in graphs])

        inputGraphs.append(tmp)
        
        if commonNames == None:
            commonNames = set(tmp.keys())
        else:
            commonNames = commonNames.intersection(tmp.keys())

    #----------
    # check for graph names not appearing 
    # in all input files
    #----------
    for fileData, fname in zip(inputGraphs, inputFnames):
        
        extraNames = set(fileData.keys()) - commonNames

        if extraNames:
            print >> sys.stderr,"warning: the following graphs in file",fname,"were not found in all files:", " ".join(extraNames)

    #----------
    # first calculate the result of the chained
    # graphs at any of the interpolation points
    # and only then create the graphs
    # in order to avoid creating graphs with the same
    # name in ROOT memory
    #----------    

    fout = ROOT.TFile(options.outputFname, "RECREATE")

    for graphName in commonNames:

        print "chaining",graphName

        thisInputGraphs = [ inputGraph[graphName] for inputGraph in inputGraphs ]

        graphPointsX = [ transformationUtils.getGraphPoints(graph)[0] for graph in thisInputGraphs ]

        # merge the lists
        import operator
        graphPointsX = reduce(operator.__add__, graphPointsX)

        # list of all graph points, avoid duplicates
        graphPointsX = sorted(set(graphPointsX))

        # evaluate the combined graph at these points
        graphPointsY = [ evalChainedGraph(thisInputGraphs, x) for x in graphPointsX ]

        # create the resulting TGraph object
        resultGraph = ROOT.TGraph(len(graphPointsX),
                                  array.array('f', graphPointsX),
                                  array.array('f', graphPointsY))

        resultGraph.SetName(graphName)


        fout.cd()
        resultGraph.Write()


    ROOT.gROOT.cd()
    fout.Close()
    print "wrote",options.outputFname
                                 
