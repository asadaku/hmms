import forwardalg


def main():
    vertices = ("Hot","Cold")
    edgeProbs = [ [0.6,0.4], [0.5,0.5]]
    emissionProbs = [ [0.1, 0.9], [0.8, 0.2]]
    initProbs = [0.5,0.5]
    
    mygraph = forwardalg.HMMGraph(vertices, edgeProbs, emissionProbs)
    mygraph.SetInitialProbs(initProbs)

    
    
    # Draw the graph
    mygraph.DrawGraph()

    v = 0
    
    # meas is 0
    # mygraph.PropagateTrellis(0)
    # mygraph.PropagateTrellis(0)
    # v += sum(mygraph.trellis[-1])
    
    # mygraph.trellis = None
    # mygraph.PropagateTrellis(0)
    # mygraph.PropagateTrellis(1)
    # v += sum(mygraph.trellis[-1])

    # mygraph.trellis = None
    # mygraph.PropagateTrellis(1)
    # mygraph.PropagateTrellis(0)
    # v += sum(mygraph.trellis[-1])

    # mygraph.trellis = None
    # mygraph.PropagateTrellis(1)
    # mygraph.PropagateTrellis(1)
    # v += sum(mygraph.trellis[-1])
    # print(v)

    import time

    startTime = time.time()
    mygraph.trellis = None
    mygraph.PropagateTrellis(1)
    mygraph.PropagateTrellis(0)
    mygraph.PropagateTrellis(1)
    mygraph.PropagateTrellis(1)
    mygraph.PropagateTrellis(1)
    mygraph.PropagateTrellis(1)
    mygraph.PropagateTrellis(1)
    mygraph.PropagateTrellis(1)
    mygraph.PropagateTrellis(1)
    mygraph.PropagateTrellis(1)
    mygraph.PropagateTrellis(1)
    mygraph.PropagateTrellis(1)
    mygraph.PropagateTrellis(1)
    mygraph.PropagateTrellis(1)
    mygraph.PropagateTrellis(1)
    mygraph.PropagateTrellis(1)
    mygraph.PropagateTrellis(1)
    
    sumForwardAlg = sum(mygraph.trellis[-1])
    print('forward alg done in {} seconds'.format(time.time()-startTime))

    startTime = time.time()
    sumBrute = bruteForcePropTrellis(edgeProbs, emissionProbs, initProbs, [1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1])
    print('brute force alg done in {} seconds'.format(time.time()-startTime))

    



    # mygraph.trellis = None
    # mygraph.PropagateTrellis(0)
    # sumForwardAlg = sum(mygraph.trellis[-1])
    # sumBrute = bruteForcePropTrellis(edgeProbs, emissionProbs, initProbs, [0])

    print([sumBrute,sumForwardAlg])

    

def bruteForcePropTrellis(edgeProbs, emissionProbs, initProbs, measurements):
    # Go through all possible paths. In this case we only have two so it should be easy peasy
    nVertices = len(initProbs)

    # Get all permutations
    import itertools
    sequences = [p for p in itertools.product(range(0,nVertices), repeat=1+len(measurements))]

    sum = 0
    for sequence in sequences:
        Ps = 1
        Po = 1
        for idx,_ in enumerate(sequence):
            if idx==len(sequence)-1:
                Ps *= initProbs[sequence[-1]]
                break

            # NOTE THE FIRST IDX IN SEQUENCE IS THE START STATE
            Ps *= edgeProbs[ sequence[idx] ][ sequence[idx+1] ]
            Po *= emissionProbs[sequence[idx+1]][measurements[idx]]
        sum += Ps*Po
        
    return sum

    
if __name__=="__main__":
    main()
