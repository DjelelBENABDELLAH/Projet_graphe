# This file allows separating the most CPU intensive routines from the
# main code.  This allows them to be optimized with Cython.  If you
# don't have Cython, this will run normally.  However, if you use
# Cython, you'll get speed boosts from 10-100x automatically.
#
# THE ONLY CATCH IS THAT IF YOU MODIFY THIS FILE, YOU MUST ALSO MODIFY
# fa2util.pxd TO REFLECT ANY CHANGES IN FUNCTION DEFINITIONS!
#
# Copyright (C) 2017 Bhargav Chippada <bhargavchippada19@gmail.com>
#
# Available under the GPLv3

from math import sqrt


# This will substitute for the nLayout object
class Node:
    def __init__(self):
        self.mass = 0.0
        self.old_dx = 0.0
        self.old_dy = 0.0
        self.old_dz = 0.0
        self.dx = 0.0
        self.dy = 0.0
        self.dz = 0.0
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0


# This is not in the original java code, but it makes it easier to deal with edges
class Edge:
    def __init__(self):
        self.node1 = -1
        self.node2 = -1
        self.weight = 0.0


# Here are some functions from ForceFactory.java
# =============================================

# Repulsion function.  `n1` and `n2` should be nodes.  This will
# adjust the dx and dy values of `n1`  `n2`
def linRepulsion(n1, n2, coefficient=0):
    xDist = n1.x - n2.x
    yDist = n1.y - n2.y
    zDist = n1.z - n2.z
    distance2 = xDist * xDist + yDist * yDist + zDist * zDist  # Distance squared

    if distance2 > 0:
        factor = coefficient * n1.mass * n2.mass / distance2
        n1.dx += xDist * factor
        n1.dy += yDist * factor
        n1.dz += zDist * factor
        n2.dx -= xDist * factor
        n2.dy -= yDist * factor
        n2.dz -= zDist * factor


# Repulsion function. 'n' is node and 'r' is region
def linRepulsion_region(n, r, coefficient=0):
    xDist = n.x - r.massCenterX
    yDist = n.y - r.massCenterY
    zDist = n.z - r.massCenterZ
    distance2 = xDist * xDist + yDist * yDist + zDist * zDist

    if distance2 > 0:
        factor = coefficient * n.mass * r.mass / distance2
        n.dx += xDist * factor
        n.dy += yDist * factor
        n.dz += zDist * factor


# Gravity repulsion function.  For some reason, gravity was included
# within the linRepulsion function in the original gephi java code,
# which doesn't make any sense (considering a. gravity is unrelated to
# nodes repelling each other, and b. gravity is actually an
# attraction)
def linGravity(n, g):
    xDist = n.x
    yDist = n.y
    zDist = n.z
    distance = sqrt(xDist * xDist + yDist * yDist + zDist * zDist)

    if distance > 0:
        factor = n.mass * g / distance
        n.dx -= xDist * factor
        n.dy -= yDist * factor
        n.dz -= zDist * factor


# Strong gravity force function. `n` should be a node, and `g`
# should be a constant by which to apply the force.
def strongGravity(n, g, coefficient=0):
    xDist = n.x
    yDist = n.y
    zDist = n.z

    if xDist != 0 and yDist != 0 and zDist != 0:
        factor = coefficient * n.mass * g
        n.dx -= xDist * factor
        n.dy -= yDist * factor
        n.dz -= zDist * factor


# Attraction function.  `n1` and `n2` should be nodes.  This will
# adjust the dx and dy values of `n1` and `n2`.  It does
# not return anything.
def linAttraction(n1, n2, e, distributedAttraction, coefficient=0):
    xDist = n1.x - n2.x
    yDist = n1.y - n2.y
    zDist = n1.z - n2.z
    if not distributedAttraction:
        factor = -coefficient * e
    else:
        factor = -coefficient * e / n1.mass
    n1.dx += xDist * factor
    n1.dy += yDist * factor
    n1.dz += zDist * factor
    n2.dx -= xDist * factor
    n2.dy -= yDist * factor
    n2.dz -= zDist * factor


# The following functions iterate through the nodes or edges and apply
# the forces directly to the node objects.  These iterations are here
# instead of the main file because Python is slow with loops.
def apply_repulsion(nodes, coefficient):
    i = 0
    for n1 in nodes:
        j = i
        for n2 in nodes:
            if j == 0:
                break
            linRepulsion(n1, n2, coefficient)
            j -= 1
        i += 1


def apply_gravity(nodes, gravity, scalingRatio, useStrongGravity=False):
    if not useStrongGravity:
        for n in nodes:
            linGravity(n, gravity)
    else:
        for n in nodes:
            strongGravity(n, gravity, scalingRatio)


def apply_attraction(nodes, edges, distributedAttraction, coefficient, edgeWeightInfluence):
    # Optimization, since usually edgeWeightInfluence is 0 or 1, and pow is slow
    if edgeWeightInfluence == 0:
        for edge in edges:
            linAttraction(nodes[edge.node1], nodes[edge.node2], 1, distributedAttraction, coefficient)
    elif edgeWeightInfluence == 1:
        for edge in edges:
            linAttraction(nodes[edge.node1], nodes[edge.node2], edge.weight, distributedAttraction, coefficient)
    else:
        for edge in edges:
            linAttraction(nodes[edge.node1], nodes[edge.node2], pow(edge.weight, edgeWeightInfluence),
                          distributedAttraction, coefficient)


# For Barnes Hut Optimization
class Region:
    def __init__(self, nodes):
        self.mass = 0.0
        self.massCenterX = 0.0
        self.massCenterY = 0.0
        self.massCenterZ = 0.0
        self.size = 0.0
        self.nodes = nodes
        self.subregions = []
        self.updateMassAndGeometry()

    def updateMassAndGeometry(self):
        if len(self.nodes) > 1:
            self.mass = 0
            massSumX = 0
            massSumY = 0
            massSumZ = 0
            for n in self.nodes:
                self.mass += n.mass
                massSumX += n.x * n.mass
                massSumY += n.y * n.mass
                massSumZ += n.z * n.mass
            self.massCenterX = massSumX / self.mass
            self.massCenterY = massSumY / self.mass
            self.massCenterZ = massSumZ / self.mass

            self.size = 0.0
            for n in self.nodes:
                distance = sqrt((n.x - self.massCenterX) ** 2 + (n.y - self.massCenterY) ** 2 + (n.z - self.massCenterZ) ** 2)
                self.size = max(self.size, 2 * distance)

    def buildSubRegions(self):
        if len(self.nodes) > 1:
            topleftfrontNodes = []
            topleftbackNodes = []
            bottomleftfrontNodes = []
            bottomleftbackNodes = []
            toprightfrontNodes = []
            toprightbackNodes = []
            bottomrightfrontNodes = []
            bottomrightbackNodes = []
            # Optimization: The distribution of self.nodes into 
            # subregions now requires only one for loop. Removed 
            # topNodes and bottomNodes arrays: memory space saving.
            for n in self.nodes:
                if n.x < self.massCenterX:
                    if n.y < self.massCenterY:
                        if n.z <self.massCenterZ:
                            bottomleftbackNodes.append(n)
                        else:
                            bottomleftfrontNodes.append(n)
                    else:
                        if n.z < self.massCenterZ:
                            topleftbackNodes.append(n)
                        else:
                            topleftfrontNodes.append(n) 
                else:
                    if n.y < self.massCenterY:
                        if n.z < self.massCenterZ:
                            bottomrightbackNodes.append(n)
                        else:
                            bottomrightfrontNodes.append(n)
                    else:
                        if n.z < self.massCenterZ:
                            toprightbackNodes.append(n)
                        else:
                            toprightfrontNodes.append(n)      

            if len(topleftbackNodes) > 0:
                if len(topleftbackNodes) < len(self.nodes):
                    subregion = Region(topleftbackNodes)
                    self.subregions.append(subregion)
                else:
                    for n in topleftbackNodes:
                        subregion = Region([n])
                        self.subregions.append(subregion)
            
            if len(topleftfrontNodes) > 0:
                if len(topleftfrontNodes) < len(self.nodes):
                    subregion = Region(topleftfrontNodes)
                    self.subregions.append(subregion)
                else:
                    for n in topleftfrontNodes:
                        subregion = Region([n])
                        self.subregions.append(subregion)

            if len(bottomleftbackNodes) > 0:
                if len(bottomleftbackNodes) < len(self.nodes):
                    subregion = Region(bottomleftbackNodes)
                    self.subregions.append(subregion)
                else:
                    for n in bottomleftbackNodes:
                        subregion = Region([n])
                        self.subregions.append(subregion)
            
            if len(bottomleftfrontNodes) > 0:
                if len(bottomleftfrontNodes) < len(self.nodes):
                    subregion = Region(bottomleftfrontNodes)
                    self.subregions.append(subregion)
                else:
                    for n in bottomleftfrontNodes:
                        subregion = Region([n])
                        self.subregions.append(subregion)

            if len(toprightbackNodes) > 0:
                if len(toprightbackNodes) < len(self.nodes):
                    subregion = Region(toprightbackNodes)
                    self.subregions.append(subregion)
                else:
                    for n in toprightbackNodes:
                        subregion = Region([n])
                        self.subregions.append(subregion)
            
            if len(toprightfrontNodes) > 0:
                if len(toprightfrontNodes) < len(self.nodes):
                    subregion = Region(toprightfrontNodes)
                    self.subregions.append(subregion)
                else:
                    for n in toprightfrontNodes:
                        subregion = Region([n])
                        self.subregions.append(subregion)

            if len(bottomrightbackNodes) > 0:
                if len(bottomrightbackNodes) < len(self.nodes):
                    subregion = Region(bottomrightbackNodes)
                    self.subregions.append(subregion)
                else:
                    for n in bottomrightbackNodes:
                        subregion = Region([n])
                        self.subregions.append(subregion)
            
            if len(bottomrightfrontNodes) > 0:
                if len(bottomrightfrontNodes) < len(self.nodes):
                    subregion = Region(bottomrightfrontNodes)
                    self.subregions.append(subregion)
                else:
                    for n in bottomrightfrontNodes:
                        subregion = Region([n])
                        self.subregions.append(subregion)

            for subregion in self.subregions:
                subregion.buildSubRegions()

    def applyForce(self, n, theta, coefficient=0):
        if len(self.nodes) < 2:
            linRepulsion(n, self.nodes[0], coefficient)
        else:
            distance = sqrt((n.x - self.massCenterX) ** 2 + (n.y - self.massCenterY) ** 2 + (n.z - self.massCenterZ) ** 2)
            if distance * theta > self.size:
                linRepulsion_region(n, self, coefficient)
            else:
                for subregion in self.subregions:
                    subregion.applyForce(n, theta, coefficient)

    def applyForceOnNodes(self, nodes, theta, coefficient=0):
        for n in nodes:
            self.applyForce(n, theta, coefficient)


# Adjust speed and apply forces step
def adjustSpeedAndApplyForces(nodes, speed, speedEfficiency, jitterTolerance):
    # Auto adjust speed.
    totalSwinging = 0.0  # How much irregular movement
    totalEffectiveTraction = 0.0  # How much useful movement
    for n in nodes:
        swinging = sqrt((n.old_dx - n.dx) * (n.old_dx - n.dx) + (n.old_dy - n.dy) * (n.old_dy - n.dy) + (n.old_dz - n.dz) * (n.old_dz - n.dz))
        totalSwinging += n.mass * swinging
        totalEffectiveTraction += .5 * n.mass * sqrt(
            (n.old_dx + n.dx) * (n.old_dx + n.dx) + (n.old_dy + n.dy) * (n.old_dy + n.dy) + (n.old_dz - n.dz) * (n.old_dz - n.dz))

    # Optimize jitter tolerance.  The 'right' jitter tolerance for
    # this network. Bigger networks need more tolerance. Denser
    # networks need less tolerance. Totally empiric.
    estimatedOptimalJitterTolerance = .05 * sqrt(len(nodes))
    minJT = sqrt(estimatedOptimalJitterTolerance)
    maxJT = 10
    jt = jitterTolerance * max(minJT,
                               min(maxJT, estimatedOptimalJitterTolerance * totalEffectiveTraction / (
                                   len(nodes) * len(nodes))))

    minSpeedEfficiency = 0.05

    # Protective against erratic behavior
    if totalEffectiveTraction and totalSwinging / totalEffectiveTraction > 2.0:
        if speedEfficiency > minSpeedEfficiency:
            speedEfficiency *= .5
        jt = max(jt, jitterTolerance)

    if totalSwinging == 0:
        targetSpeed = float('inf')
    else:
        targetSpeed = jt * speedEfficiency * totalEffectiveTraction / totalSwinging

    if totalSwinging > jt * totalEffectiveTraction:
        if speedEfficiency > minSpeedEfficiency:
            speedEfficiency *= .7
    elif speed < 1000:
        speedEfficiency *= 1.3

    # But the speed shoudn't rise too much too quickly, since it would
    # make the convergence drop dramatically.
    maxRise = .5
    speed = speed + min(targetSpeed - speed, maxRise * speed)

    # Apply forces.
    #
    # Need to add a case if adjustSizes ("prevent overlap") is
    # implemented.
    for n in nodes:
        swinging = n.mass * sqrt((n.old_dx - n.dx) * (n.old_dx - n.dx) + (n.old_dy - n.dy) * (n.old_dy - n.dy) + + (n.old_dz - n.dz) * (n.old_dz - n.dz))
        factor = speed / (1.0 + sqrt(speed * swinging))
        n.x = n.x + (n.dx * factor)
        n.y = n.y + (n.dy * factor)
        n.z = n.z + (n.dz * factor)

    values = {}
    values['speed'] = speed
    values['speedEfficiency'] = speedEfficiency

    return values


try:
    import cython

    if not cython.compiled:
        print("Warning: uncompiled fa2util module.  Compile with cython for a 10-100x speed boost.")
except:
    print("No cython detected.  Install cython and compile the fa2util module for a 10-100x speed boost.")
