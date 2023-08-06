"""File knapsack.py

:author: Michel Bierlaire
:date: Fri Feb 19 15:19:14 2021

This illustrates how to use the multi-objective VNS algorithm using a
simple knapsack problem.  There are two objectives: maximize utility
and minimize weight. The wegiht cannot go beyong capacity.

"""
import numpy as np
import biogeme.vns as vns
import biogeme.exceptions as excep
import biogeme.messaging as msg
logger = msg.bioMessage()
logger.setDetailed()



class oneSack(vns.solutionClass):
    def __init__(self, solution):
        super().__init__()
        self.x = solution
        self.totalWeight = None
        self.totalUtility = None


    def isDefined(self):
        if self.x is None:
            return False
        if self.totalWeight is None:
            return False
        if self.totalUtility is None:
            return False
        return True

    def __repr__(self):
        return str(self.x)

    def __str__(self):
        return str(self.x)

    def dominates(self, anotherSolution):
        """Checks if the current solution dominates another one.
        """
        if not self.isDefined():
            raise excep.biogemeError('Solution has not been defined.')

        my_f = (-self.totalUtility, self.totalWeight)
        her_f = (-anotherSolution.totalWeight, anotherSolution.totalWeight)

        if my_f > her_f:
            return False

        return my_f != her_f

class knapsack(vns.problemClass):
    """Class defining the knapsack problem. Note the inheritance from the
    abstract class used by the VNS algorithm. It guarantees the
    compliance with the requirements of the algorithm.

    """
    def __init__(self, aUtility, aWeight, aCapacity):
        """ Ctor
        """
        super().__init__()
        self.utility = aUtility
        self.weight = aWeight
        self.capacity = aCapacity
        self.operators = {'Add items': self.addItems,
                          'Remove items': self.removeItems,
                          'Change decision for items': self.changeDecisions}
        self.operatorsManagement = vns.operatorsManagement(self.operators.keys())
        self.currentSolution = None
        self.lastOperator = None


    def emptySack(self):
        z = np.zeros_like(self.utility)
        return oneSack(z)

    def addItems(self, aSolution, size=1):
        absent = np.where(aSolution.x == 0)
        n = min(len(absent), size)
        absent = absent[:n]
        xplus = aSolution.x
        xplus[absent] = 1
        return oneSack(xplus), n

    def removeItems(self, aSolution, size=1):
        present = np.where(aSolution.x == 1)
        n = min(len(present), size)
        present = present[:n]
        xplus = aSolution.x
        xplus[present] = 0
        return oneSack(xplus), n

    def changeDecisions(self, aSolution, size=1):
        n = min(len(aSolution.x), size)
        order = np.random.permutation(n)
        xplus = aSolution.x
        for i in range(n):
            xplus[order[i]] = 1 - xplus[order[i]]
        return oneSack(xplus), n

    def isValid(self, solution):
        self.evaluate(solution)
        return solution.totalWeight <= self.capacity, 'Infeasible sack'

    def evaluate(self, solution):
        solution.totalWeight = np.inner(solution.x, self.weight)
        solution.totalUtility = np.inner(solution.x, self.utility)

    def describe(self, solution):
        return str(solution)

    def generateNeighbor(self, solution, neighborhoodSize):
        # Select one operator.
        self.lastOperator = self.operatorsManagement.selectOperator()
        return self.applyOperator(solution, self.lastOperator, neighborhoodSize)

    def neighborRejected(self, solution, aNeighbor):
        if self.lastOperator is None:
            raise excep.biogemeError('No operator has been used yet.')
        self.operatorsManagement.decreaseScore(self.lastOperator)

    def neighborAccepted(self, solution, aNeighbor):
        if self.lastOperator is None:
            raise excep.biogemeError('No operator has been used yet.')
        self.operatorsManagement.increaseScore(self.lastOperator)

    def applyOperator(self, solution, name, size=1):
        op = self.operators.get(name)
        if op is None:
            raise excep.biogemeError(f'Unknown operator: {name}')
        return op(solution, size)

### Run one instance

utility = np.array([ 80, 31, 48, 17, 27, 84, 34, 39, 46, 58, 23, 67])
weight =  np.array([ 84, 27, 47, 22, 21, 96, 42, 46, 54, 53, 32, 78])
capacity = 300

theKnapsack = knapsack(utility, weight, capacity)
emptySack = theKnapsack.emptySack()

vns.vns(theKnapsack,
        [emptySack],
        maxNeighborhood=12,
        numberOfNeighbors=10,
        archiveInputFile='knapsackPareto.pickle',
        pickleOutputFile='knapsackPareto.pickle')
