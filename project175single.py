# ------------------------------------------------------------------------------------------------
# Copyright (c) 2016 Microsoft Corporation
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and
# associated documentation files (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge, publish, distribute,
# sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or
# substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT
# NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
# ------------------------------------------------------------------------------------------------

# Tutorial sample #2: Run simple mission using raw XML

import MalmoPython
import os
import sys
import time

#####
import math
import random
import json
import ziliverAI as ai
#####

sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)  # flush print output immediately

# More interesting generator string: "3;7,44*49,73,35:1,159:4,95:13,35:13,159:11,95:10,159:14,159:6,35:6,95:6;12;"

missionXML='''<?xml version="1.0" encoding="UTF-8" standalone="no" ?>
            <Mission xmlns="http://ProjectMalmo.microsoft.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">

              <About>
                <Summary>Hello world!</Summary>
              </About>

              <ServerSection>
                <ServerInitialConditions>
                  <Time>
                      <StartTime>1200</StartTime>
                      <AllowPassageOfTime>true</AllowPassageOfTime>
                  </Time>
                  <Weather>clear</Weather>
                </ServerInitialConditions>
                <ServerHandlers>
                  <FlatWorldGenerator forceReset="true" generatorString="3;57,2*10,1*198;12;village"/>
                  <DrawingDecorator>
                    <DrawCuboid x1="-100" y1="-16" z1="-100" x2="100" y2="16" z2="-20" type="diamond_block"/>
                    <DrawCuboid x1="-100" y1="-16" z1="21" x2="100" y2="16" z2="100" type="diamond_block"/>
                    <DrawCuboid x1="-100" y1="-16" z1="-100" x2="-20" y2="16" z2="100" type="diamond_block"/>
                    <DrawCuboid x1="21" y1="-16" z1="-100" x2="100" y2="16" z2="100" type="diamond_block"/>
                  </DrawingDecorator>
                  <ServerQuitFromTimeUp timeLimitMs="300000"/>
                  <ServerQuitWhenAnyAgentFinishes/>
                </ServerHandlers>
              </ServerSection>

              <AgentSection mode="Survival">
                <Name>MalmoTutorialBot</Name>
                <AgentStart>
                  <Placement x="18" y="4" z="18" yaw="90"/>
                </AgentStart>
                <AgentHandlers>
                  <ObservationFromFullStats/>
                  <AbsoluteMovementCommands/>
                  <ContinuousMovementCommands turnSpeedDegs="180"/>
                  <ObservationFromGrid>
                    <Grid name="floorAll">
                      <min x="-41" y="0" z="-41"/>
                      <max x="41" y="0" z="41"/>
                    </Grid>
                  </ObservationFromGrid>
                </AgentHandlers>
              </AgentSection>
            </Mission>'''

# Create default Malmo objects:

agent_host = MalmoPython.AgentHost()
try:
    agent_host.parse( sys.argv )
except RuntimeError as e:
    print 'ERROR:',e
    print agent_host.getUsage()
    exit(1)
if agent_host.receivedArgument("help"):
    print agent_host.getUsage()
    exit(0)

my_mission = MalmoPython.MissionSpec(missionXML, True)
my_mission_record = MalmoPython.MissionRecordSpec()

# Attempt to start a mission:
max_retries = 3
for retry in range(max_retries):
    try:
        agent_host.startMission( my_mission, my_mission_record )
        break
    except RuntimeError as e:
        if retry == max_retries - 1:
            print "Error starting mission:",e
            exit(1)
        else:
            time.sleep(2)

# Loop until mission starts:
print "Waiting for the mission to start ",
world_state = agent_host.getWorldState()
while not world_state.has_mission_begun:
    sys.stdout.write(".")
    time.sleep(0.1)
    world_state = agent_host.getWorldState()
    for error in world_state.errors:
        print "Error:",error.text

print
print "Mission running ",


#####
def moveByDirection(x, y):
    r = math.hypot(x, y)
    speed = 0.35
    vertical = - speed * y / r
    horizontal = speed * x / r
    agent_host.sendCommand("move " + str(vertical))
    agent_host.sendCommand("strafe " + str(horizontal))
    return

def load_grid():
    grid = None
    if len(world_state.errors) > 0:
        raise AssertionError('Could not load grid.')
    if world_state.number_of_observations_since_last_state > 0:
        msg = world_state.observations[-1].text
        observations = json.loads(msg)

        playerLoc = observations.get("ZPos") + 19, observations.get("XPos")+ 19
        grid = observations.get(u'floorAll', 0)

    if grid:
        start = None
        for i in range(len(grid)):
            if grid[i] != 'diamond_block':
                start = i
                break

        twoDGrid = []
        playerIndex = 41-start//83, 41-start%83

        for i in range(40):
            temp = []
            for j in range(40):
                if grid[start+83*i+j] == 'air':
                    temp.append(0)
                elif grid[start+83*i+j] == 'test_block':
                    temp.append(1)
                else:
                    temp.append(2)
            twoDGrid.append(temp)

        return twoDGrid, playerIndex, playerLoc
    else:
        return None, None, None

def handleGrid(twoDGrid, playerIndex, prev_tiles, difference, preDir, previousTargets,navigating):
    direction, target,navigatingR = ai.choose(twoDGrid, playerIndex, prev_tiles, difference, preDir, previousTargets,navigating)

    resultIndex = playerIndex[0]-direction[0], playerIndex[1]+direction[1]
    if resultIndex[0] in range(len(twoDGrid)) and resultIndex[1] in range(len(twoDGrid[0])):
        print "from", playerIndex, "current value:", twoDGrid[playerIndex[0]][playerIndex[1]], "going", direction, "result:", resultIndex, "value:", twoDGrid[resultIndex[0]][resultIndex[1]]

    moveByDirection(direction[0],direction[1])
    return direction, target,navigatingR
#####
tile_track_limit = 10
delay = 0.35
prev_tiles = []
moving = (0,0)
preDir = [(0,0),(0,0)]
previousTargets = [None]*10
#####

navigating = []
counter = 0


t0 = time.time()
# Loop until mission ends:
while world_state.is_mission_running:
    tn = time.time()

    time.sleep(0.1)
    world_state = agent_host.getWorldState()
    counter += 1
    #####
    twoDGrid, playerIndex, playerLoc = load_grid()
    difference = playerLoc[0] -float(playerIndex[0]) ,  playerLoc[1] - float(playerIndex[1])
    playerIndex = int(playerLoc[0]), int(playerLoc[1])

    if twoDGrid[playerIndex[0]][playerIndex[1]] == 2:
        print "agent is dead, mission ends, time:", time.time() - t0
        print "average time usage:", (time.time() - t0) / counter
        print "last location:", playerLoc
        exit(0)

    twoDGrid[playerIndex[0]][playerIndex[1]] = 8
##    for i in twoDGrid:
##        print i
    twoDGrid[playerIndex[0]][playerIndex[1]] = 1

    if twoDGrid and playerIndex:
        predir,target,navigating = handleGrid(twoDGrid, playerIndex, prev_tiles, difference, preDir, previousTargets,navigating)
        preDir.pop(0)
        preDir.append(predir)
        if target:
            previousTargets.pop(0)
            previousTargets.append(target)

    if len(prev_tiles) >= tile_track_limit:
        prev_tiles.pop(0)
    if playerIndex not in prev_tiles:
        prev_tiles.append(playerIndex)
    print "playerIndex:", playerIndex, "playerLoc:", playerLoc
    print "difference:", difference
    print "moving:", (moving[0] - playerIndex[0], moving[1] - playerIndex[1])
    moving = playerIndex
    while time.time() - t0 < 0.33:
        continue
    print "using time:", time.time() - tn
    #####

    for error in world_state.errors:
        print "Error:",error.text

print
print "Mission ended"
# Mission has ended.
