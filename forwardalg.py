from graphviz import Digraph

class HMMGraph:
    
    def __init__(self, vertexNames, edgeProbs, emissionProbs):

        self.vertexNames = {}  # A dictionary storing the vertex name and its associated index 
        self.vertices = {}
        self.edgeProbs = None
        self.initProbs = None
        self.emissionProbs = None
        self.trellis = None
        
        self.__SetVertexNames(vertexNames)
        self.__SetEdgeProbs(edgeProbs)  # A nested list of edge probs. The columns must sum to 1.
        self.__CheckEmissionProbs(emissionProbs)
        self.SetInitialProbs()

        
        # If no exception was raised by __SetEdgeProbs, build the graph
        self.__BuildGraph()

       
    def __SetVertexNames(self, vertexNames):
        idx = 0
        for vertexName in vertexNames:
            self.vertexNames[vertexName] = idx
            idx += 1
            
        
    def __SetEdgeProbs(self, edgeProbs):
        # check health of supplied edgeProbs
        nVertices = len(self.vertexNames.keys())
        
        if len(edgeProbs) != nVertices or len(edgeProbs[0]) != nVertices:
            raise ValueError('supplied edge probs are not in the correct format.\nPlease supply a matrix as a nested list in row major format.')

        for vIdx in range(0,nVertices):
            if sum([edgeProbs[vIdx][i] for i in range(0,nVertices)]) != 1.0:
                raise ValueError("rows of supplied edge probs don't sum to 1")
            
        # Everything looks good
        self.edgeProbs = edgeProbs
        
    def __CheckEmissionProbs(self, emissionProbs):
        if len(emissionProbs) != len(self.vertexNames):
            raise ValueError('length of emission probs should be same dimension as number of vertices')
        self.emissionProbs = emissionProbs
        
    def __BuildGraph(self):
        # Set up each vertex
        for vertexName in self.vertexNames:
            self.vertices[vertexName] = Vertex(vertexName)  

        # For each vertex, set up connections
        nVertices = len(self.vertexNames.keys())
        for vertexName in self.vertexNames:
            # For each name, we have a list of probs. If prob is zero, you can go to that vertex
            # However, I need to associate the vertex name with which column of edgeProbs to look at
            # This is the value stored with the key in vertexNames
            vIdx = self.vertexNames[vertexName]

            # Get list of probabilities to this state, which is the column of edgeProbs
            predVertexEdgeProbs = [self.edgeProbs[i][vIdx] for i in range(0,nVertices)]
            # Now loop through and add to list of predecessors
            for predVertexName, pIdx in self.vertexNames.items():
                if predVertexEdgeProbs[pIdx] > 0:
                    # Add this to the list of predecessors
                    self.vertices[vertexName].predecessors[predVertexName] = predVertexEdgeProbs[pIdx]
                    
            # Now loop through and add to list of successors. These are rows of the edgeProbs matrix
            succVertexEdgeProbs = [self.edgeProbs[vIdx][i] for i in range(0,nVertices)]
            # Now loop through and add to list of successors
            for succVertexName, sIdx in self.vertexNames.items():
                if succVertexEdgeProbs[sIdx] > 0:
                    # Add this to the list of successors
                    self.vertices[vertexName].successors[succVertexName] = succVertexEdgeProbs[sIdx]

            # Set the emission probs
            self.vertices[vertexName].SetEmissionProbs(self.emissionProbs[vIdx])

    def SetInitialProbs(self, probs=None):
        nVertices = len(self.vertexNames)
        if not probs:
            # Just provide default initial probs
            self.initProbs = (1.0/nVertices)*nVertices
        else:
            if sum(probs) != 1:
                raise ValueError("Provided initial probs don't sum to 1")
            self.initProbs = probs

    def DrawGraph(self):
        dot = Digraph(comment='HMMGraph')

        # Build all the nodes
        for vertexName in self.vertexNames:
            dot.node(vertexName, vertexName)
            
        # Connect them up
        for vertexName in self.vertexNames:
            for successorName in self.vertices[vertexName].successors:
                # For each successor, draw a line to the successor
                dot.edge(vertexName, successorName, label = str(self.vertices[vertexName].successors[successorName]))            
        dot.render('outgraph')

    def PropagateTrellis(self, measurement):
        # The trellis for the forward prob stores
        # alpha_t(j) = P(O_1, O_2, ..., O_t, x_t=j)
        # Where t is the time, and j is a state index e.g 1 being hot, 2 being cold etc.
        # We store the trellis as a growing array
        if self.trellis is None:
            self.trellis = []
            # Initialize the trellis
            nVertices = len(self.vertexNames)
            temp = [0]*nVertices
            for vertexName in self.vertexNames:
                vCurrentIdx = self.vertexNames[vertexName]
                # For this state, check its predecessors.
                temp[vCurrentIdx] = self.vertices[vertexName].emissionProbs[measurement]
                tempSum = 0
                for predecessor, prob in self.vertices[vertexName].predecessors.items():
                    # Annoying mapping needed from dict to index of self.initProbs
                    initProbIdx = self.vertexNames[predecessor]
                    tempSum += prob*self.initProbs[initProbIdx]
                    
                temp[vCurrentIdx] *= tempSum
        else:
            # The trellis is already initialized
            nVertices = len(self.vertexNames)
            temp = [0]*nVertices

            for vertexName in self.vertexNames:
                # Let's populate the index of the trellis associated with "vertexName" state
                vCurrentIdx = self.vertexNames[vertexName] # idx associated with "vertexName"
                # For this state, check its predecessors.
                temp[vCurrentIdx] = self.vertices[vertexName].emissionProbs[measurement]
                
                tempSum = 0
                for predecessor, prob in self.vertices[vertexName].predecessors.items():
                    prevTrellisIdx = self.vertexNames[predecessor]
                    tempSum += prob*self.trellis[-1][prevTrellisIdx]

                temp[vCurrentIdx] *= tempSum
                    

                
        self.trellis.append(temp)
        
        
class Vertex:

    def __init__(self, vertexName):
        self.vertexName = vertexName
        self.predecessors = {}
        self.successors = {}
        self.emissionProbs = {} # Upgrade to a class that can handle different probs. Right now it's a discrete prob

    def SetEmissionProbs(self, probs):
        # Probs are associated with key value pairs
        # {1:0.3, 2:0.4, 3:0.3}
        idx=0
        for prob in probs:
            self.emissionProbs[idx] = prob
            idx+=1


