# -*- coding: utf-8 -*-
# sampleAgents.py
# parsons/07-oct-2017
#
# Version 1.1
#
# Some simple agents to work with the PacMan AI projects from:
#
# http://ai.berkeley.edu/
#
# These use a simple API that allow us to control Pacman's interaction with
# the environment adding a layer on top of the AI Berkeley code.
#
# As required by the licensing agreement for the PacMan AI we have:
#
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).

# The agents here are extensions written by Simon Parsons, based on the code in
# pacmanAgents.py

from time import sleep
from pacman import Directions
from game import Agent
import api
import random
import game
import util

# RandomAgent
#
# A very simple agent. Just makes a random pick every time that it is
# asked for an action.
class RandomAgent(Agent):

    def getAction(self, state):
        # Get the actions we can try, and remove "STOP" if that is one of them.
        legal = api.legalActions(state)
        if Directions.STOP in legal:
            legal.remove(Directions.STOP)
        # Random choice between the legal options.
        return api.makeMove(random.choice(legal), legal)

# RandomishAgent
#
# A tiny bit more sophisticated. Having picked a direction, keep going
# until that direction is no longer possible. Then make a random
# choice.
class RandomishAgent(Agent):

    # Constructor
    #
    # Create a variable to hold the last action
    def __init__(self):
         self.last = Directions.STOP
    
    def getAction(self, state):
        # Get the actions we can try, and remove "STOP" if that is one of them.
        legal = api.legalActions(state)
        if Directions.STOP in legal:
            legal.remove(Directions.STOP)
        # If we can repeat the last action, do it. Otherwise make a
        # random choice.
        if self.last in legal:
            return api.makeMove(self.last, legal)
        else:
            pick = random.choice(legal)
            # Since we changed action, record what we did
            self.last = pick
            return api.makeMove(pick, legal)

# SensingAgent
#
# Doesn't move, but reports sensory data available to Pacman
class SensingAgent(Agent):

    def getAction(self, state):

        # Demonstrates the information that Pacman can access about the state
        # of the game.

        # What are the current moves available
        legal = api.legalActions(state)
        print "Legal moves: ", legal

        # Where is Pacman?
        pacman = api.whereAmI(state)
        print "Pacman position: ", pacman

        # Where are the ghosts?
        print "Ghost positions:"
        theGhosts = api.ghosts(state)
        for i in range(len(theGhosts)):
            print theGhosts[i]

        # How far away are the ghosts?
        print "Distance to ghosts:"
        for i in range(len(theGhosts)):
            print util.manhattanDistance(pacman,theGhosts[i])

        # Where are the capsules?
        print "Capsule locations:"
        print api.capsules(state)
        
        # Where is the food?
        print "Food locations: "
        print api.food(state)

        # Where are the walls?
        print "Wall locations: "
        print api.walls(state)
        
        # getAction has to return a move. Here we pass "STOP" to the
        # API to ask Pacman to stay where they are.
        return api.makeMove(Directions.STOP, legal)

class GoWestAgent(Agent):
    def getAction(self, state):
        legal = api.legalActions(state)
        if Directions.WEST in legal:
            return api.makeMove(Directions.WEST,legal)
        elif Directions.NORTH in legal:
            return api.makeMove(Directions.NORTH,legal)
        elif Directions.SOUTH in legal:
            return api.makeMove(Directions.SOUTH,legal)
        else:
            return api.makeMove(Directions.STOP,legal)

class CornerSeekingAgent(Agent):
    def __init__(self):
        self.last = Directions.STOP
        self.corners = None
        self.visitedCorners = []
        self.nowCorner = None
        self.lastPosition = None

    def getAction(self, state):
        if len(self.visitedCorners) == 4:
            self.visitedCorners = []

        if self.corners is None:
            self.corners = [(18,1),(1,1),(1,9),(18,9)]

        if self.nowCorner is None:
            for corner in self.corners:
                if corner not in self.visitedCorners:
                    self.nowCorner = corner
                    # print nowCorner

        selfX, selfY = api.whereAmI(state)
        targetX, targetY = self.nowCorner
        legal = api.legalActions(state)
        walls = api.walls(state) 
        # print selfX

        if (selfX, selfY) == self.nowCorner:
            self.visitedCorners.append(self.nowCorner)
            self.nowCorner = None
            return api.makeMove(Directions.STOP,legal)

        bestDirection = None
        bestDistance = float('inf')

        for direction in legal:
            if direction == Directions.NORTH:
                nextX, nextY = selfX, selfY + 1
            elif direction == Directions.SOUTH:
                nextX, nextY = selfX, selfY - 1
            elif direction == Directions.EAST:
                nextX, nextY = selfX + 1, selfY
            elif direction == Directions.WEST:
                nextX, nextY = selfX - 1, selfY
            else:
                continue

            if (nextX, nextY) not in walls and (nextX, nextY) != self.lastPosition:
                distance = abs(nextX - targetX) + abs(nextY - targetY)
                if distance < bestDistance:
                    bestDistance = distance
                    bestDirection = direction

        if bestDirection:
            self.lastPosition = (selfX, selfY)
            return api.makeMove(bestDirection, legal)
        else:
            direction = random.choice(legal)
            self.lastPosition = (selfX, selfY)
            return api.makeMove(direction, legal)

class ForgeSafelyAgent(Agent):
    def __init__(self):
        self.last = Directions.STOP
        self.corners = None
        self.visitedCorners = []
        self.nowCorner = None
        self.lastPosition = None
        self.state = 'foraging'
        self.ghostDistanceThreshold = 3
    
    def getAction(self, state):
        # if len(self.visitedCorners) == 4:
        #     pass

        if self.corners is None:
            self.corners = [(18,1), (1,1), (1,9), (18,9)]
        
        if self.nowCorner is None:
            for corner in self.corners:
                if corner not in self.visitedCorners:
                    self.nowCorner = corner
        
        selfX, selfY = api.whereAmI(state)
        legal = api.legalActions(state)
        walls = api.walls(state)
        ghostPositions = api.ghosts(state)
        food = api.food(state)
        distancesToGhosts = api.ghosts(state)
        # print food

        if any(dist <= self.ghostDistanceThreshold for dist in distancesToGhosts):
            self.state = 'surviving'
        else:
            self.state = 'foraging'

        if self.state == 'surviving':
            return self.survivalMode(legal, ghostPositions, walls)
        else:
            return self.foragingMode(legal, food, walls, selfX, selfY)
        
    def foragingMode(self, legal, food, walls, selfX, selfY):
        if (selfX, selfY) == self.nowCorner:
            self.visitedCorners.append(self.nowCorner)
            self.nowCorner = None
            return api.makeMove(Directions.STOP, legal)

        bestDirection = None
        bestDistance = float('inf')

        if len(self.visitedCorners) < 4:
            targetX, targetY = self.nowCorner
        else:
            if food == []:
                targetX, targetY = random.choice(self.corners)
            else:
                targetX, targetY = random.choice(food)

        for direction in legal:
            if direction == Directions.NORTH:
                nextX, nextY = selfX, selfY + 1
            elif direction == Directions.SOUTH:
                nextX, nextY = selfX, selfY - 1
            elif direction == Directions.EAST:
                nextX, nextY = selfX + 1, selfY
            elif direction == Directions.WEST:
                nextX, nextY = selfX - 1, selfY
            else:
                continue

            if (nextX, nextY) not in walls and (nextX, nextY) != self.lastPosition:
                distance = abs(nextX - targetX) + abs(nextY - targetY)
                if distance < bestDistance:
                    bestDistance = distance
                    bestDirection = direction

        if bestDirection:
            self.lastPosition = (selfX, selfY)
            return api.makeMove(bestDirection, legal)
        else:
            direction = random.choice(legal)
            self.lastPosition = (selfX, selfY)
            return api.makeMove(direction, legal)

    def survivalMode(self, legal, ghostPositions, walls):
        bestDirection = None
        maxDistance = -float('inf')
        selfX, selfY = api.whereAmI(self.state)

        for direction in legal:
            if direction == Directions.NORTH:
                nextX, nextY = selfX, selfY + 1
            elif direction == Directions.SOUTH:
                nextX, nextY = selfX, selfY - 1
            elif direction == Directions.EAST:
                nextX, nextY = selfX + 1, selfY
            elif direction == Directions.WEST:
                nextX, nextY = selfX - 1, selfY
            else:
                continue

            if (nextX, nextY) not in walls:
                distance = min([abs(nextX - gx) + abs(nextY - gy) for gx, gy in ghostPositions])
                if distance > maxDistance:
                    maxDistance = distance
                    bestDirection = direction

        if bestDirection:
            return api.makeMove(bestDirection, legal)
        else:
            direction = random.choice(legal)
            return api.makeMove(direction, legal)
