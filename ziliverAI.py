import time
timeout = False
navigatingMemory = 10
t = [0]
delay = 0.25 # 0.25 for single // 0.2 for multi
directions = [(1,0),(-1,0),\
	(1,1),(1,-1),\
	(-1,-1),(-1,1),\
	(0,1),(0,-1)]
FirstDirections = None
surroundings = {}

def addDirection(grid,origin,direction,i):
	if origin[0]+direction[0]*i in range(len(grid)) and \
		origin[1]+direction[1]*i in range( len(grid[0])):
		return grid[origin[0]+direction[0]*i][origin[1]+direction[1]*i]
	else:
		return 0


def findSingleEight(grid,origin,LimitedDirection):
	l = 0
	# if grid[origin[0]][origin[0]] == 0 :
	# 	return (1,0),0
	# else:
	result = {}

	maxi = 0
	maxiDirection = None
	for direction in LimitedDirection:
		i = 1
		while addDirection(grid,origin,direction,i)!=0:
			i+=1
		result[direction] = i
		if i > maxi:
			maxi = i
			maxiDirection =  direction
	# print "directions:",result
	# print "use simpler",result

	return maxiDirection, maxi

def calculatePointValue(grid,point,blocking):
	result = 0
	margin = 1
	for direction in directions:

		if point[0]+direction[0] == blocking[0] and point[1]+direction[1] ==blocking[1]:
			continue
		i =0
		while addDirection(grid,point,direction,i)!=0:
			i+=1
		result += i
		if i == 0:
			margin *= 0.1

	return result * margin

def findAdvancedEight(grid,origin):
	LimitedDirection = []
	maxi = 0
	result = None
	resultDict = {}
	for direction in FirstDirections:
		x,y = (origin[0] + direction[0], origin[1]+direction[1])

		tmp = calculatePointValue(grid, (x,y) , origin)
		if saveCheckPoint(grid,x,y)==0:
			tmp =0
		resultDict[direction] = tmp
		if tmp > maxi:
			LimitedDirection = [direction]
			maxi = tmp
			result = direction
		elif tmp == maxi:
			LimitedDirection.append(direction)

	#if there are draws, use the simpler algorithms
	if len(LimitedDirection) >1:
		result, mm = findSingleEight(grid,origin,LimitedDirection)



	if result:
		return result
	else:
		return (1,0)


def updatePoint(grid,point):
	for i in (-1,0,1):
		for ii in (-1,0,1):
			x,y = point[0] + i, point[1]+ii
			if x in range(len(grid)) and y in range(len(grid)):
				grid[x][y] = 0

def updateGrid(grid,player,prev):
	for location in range(len(prev)-2):
		updatePoint(grid,prev[location])

def transformDirection(direction):
	return -direction[0],direction[1]

def checkSafety(grid,player):
	for i in (-1,0,1):
		for ii in (-1,0,1):
			x,y = player[0] + i, player[1]+ii
			if x in range(len(grid)) and y in range(len(grid)):
				if grid[x][y] == 1:
					return True
	return False

def initializeSurrounding(grid,player):

	for d in directions:
		if player[0] + d[0] in range(len(grid)) and player[1] + d[1] in range(len(grid)):
			surroundings[d] = grid[player[0] + d[0]][player[1] + d[1]]

def retrieveOriginalGrid(grid,player,prev):
	if  not checkSafety(grid,player) :

		for d in directions:
			if surroundings[d] == 1:
				if (player[0] + d[0], player[1] + d[1]) not in prev:
					if player[0] + d[0] in range(len(grid)) and player[1] + d[1] in range(len(grid)):

						grid[player[0] + d[0]][player[1] + d[1]] = 1

	if  not checkSafety(grid,player) :

		for d in directions:
			if surroundings[d] == 1:
				if player[0] + d[0] in range(len(grid)) and player[1] + d[1] in range(len(grid)):

					grid[player[0] + d[0]][player[1] + d[1]] = 1

def surroundValue(grid,x,y):
	if grid[x][y]==0:
		return 0
	result = 0
	for i in -1,1,0:
		for ii in -1,1,0:
			if x+i in range(len(grid)) and y + ii in range(len(grid[0])):
				result+= grid[x+i][y+ii]
	return result

def reValue(grid):
	newGrid = []
	for i in range(len(grid)):
		tmp = []
		for ii in range(len(grid[0])):
			tmp.append(surroundValue(grid,i,ii))
		newGrid.append(tmp)
	return newGrid

def createPowerGrid(grid):
	newGrid = grid
	for i in range(6):
		# print "regrid", i
		if time.time() - t[0] > delay:
			timeout = True
			return None
		newGrid = reValue(newGrid)
	return newGrid

def findMaximumPoints(powerGrid):

	maxi = 0
	maxiIndexes = []

	for i in range(len(powerGrid)):
		for ii in range(len(powerGrid[0])):
			if powerGrid[i][ii] > maxi:

				maxiIndexes = [(i,ii)]
				maxi = powerGrid[i][ii]
			elif powerGrid[i][ii] == maxi:
				maxiIndexes.append((i,ii))
	return maxiIndexes

def reduceMaximumPoints(grid, maxiIs):
	newGrid = [[ 0 for col in row]  for row in grid]
	newGrid2 = [[ 0 for col in row]  for row in grid]
	for x,y in maxiIs:
		newGrid[x][y] =1
	for x,y in maxiIs:
		if  time.time()-t[0] > delay:
			timeout = True
			return None
		newGrid2[x][y] = surroundValue(newGrid,x,y)

	maxi = 0
	maxiIndexes = []
	for x,y in maxiIs:
		if newGrid2[x][y] > maxi:
			maxiIndexes = [(x,y)]
			maxi = newGrid2[x][y]
		elif newGrid2[x][y] == maxi:
			maxiIndexes.append((x,y))
	return maxiIndexes

def powerfulDirection(grid,origin):

	powerGrid = createPowerGrid(grid)
	if powerGrid == None:
		return None
	maxiPoints = findMaximumPoints(powerGrid)
	# print "# of maxiPoints", len(maxiPoints)
	reducedP = reduceMaximumPoints(grid, maxiPoints)
	if reducedP == None:
		return None
	# print "# of reduced Points: ",len(reducedP)
	# for i in powerGrid:
	# 	print i
	# print  "power points",reducedP
	if reducedP!=[]:
		return reducedP[0]
	else:
		return None



# linked list
class node:
    def __init__(self,pre,d,dire):
        self.pre = pre
        self.data = d
        self.dire = dire

def suroundLava(grid,point):
	for i in 1,0,-1:
		for ii in 1,0,-1:
			x,y = point[0] + i, point[1]+ii
			if x in range(len(grid)) and y in range(len(grid)):
				if grid[x][y] == 0:
					return True
	return False

def suroundLavaNum(grid,point):
	x=0
	for i in 1,0,-1:
		for ii in 1,0,-1:
			x,y = point[0] + i, point[1]+ii
			if x in range(len(grid)) and y in range(len(grid)):
				if grid[x][y] == 0:
					x+=1
	return x

def findIsland(grid,player,depth):
	result = []
	visited = [player]
	queue = [player]
	loop = 0
	while queue != [] and loop < depth:
		if time.time() - t[0] > delay:
			return None
		p = queue.pop()
		for i in -1,0,1:
			for ii in -1,0,1:
				x,y = p[0]+i, p[1]+ii
				if (x,y) not in visited and x in range(len(grid)) and y in range(len(grid[0])) and grid[x][y]==1:
					queue.append((x,y))
					result.append((x,y))
					visited.append((x,y))
		loop +=1
	return result

#dikjstra
def navigateToPoint(grid,player,destination):
	visitedBlockNum = []
	currentBlocks = [node(None,player,None)]

	endNode = None
	# i = 0

	while endNode == None and len(currentBlocks) !=0:
		# i+=1
		# print "use navigation", i, len(currentBlocks)
		nextBlocksWithLava = []
		otherBlocks = []

		#get ride of dangerous directions
		if visitedBlockNum == []:
			dd = FirstDirections
		else:
			dd = directions

		for block in currentBlocks:

			for direction in dd:
				p = (block.data[0] + direction[0],block.data[1] + direction[1])


				if p == destination:
					endNode = node(block,destination,direction)
					break
				if p not in visitedBlockNum and p[0] in range(len(grid)) and p[1] in range(len(grid[1])) and grid[p[0]][p[1]] == 1:
					if suroundLava:
						nextBlocksWithLava.append(  node(block , p,direction)  )
					else:
						otherBlocks.append(node(block , p,direction))
					visitedBlockNum.append(p)

		currentBlocks = otherBlocks +nextBlocksWithLava

		if time.time() - t[0] > delay:
			return None

	if endNode:
	    res = []
	    resPoint = []
	    while endNode:
	        res.append(endNode.dire)
	        resPoint.append(endNode.data)
	        endNode = endNode.pre

	    resPoint.reverse()
	    if len(resPoint) > navigatingMemory:
	    	resPoint = resPoint[:navigatingMemory]
	    resPoint.pop(0)
	    # print "navigating:",res[:5], destination
	    return res[-2],resPoint
	else:
	    return None

def saveCheckPoint(grid,x,y):
	if x in range(len(grid)) and y in range(len(grid[0])):
		return grid[x][y] !=0

def initializeDirections(differences,grid,player,preDir):
	x,y = differences
	global FirstDirections
	if x * y >=0:
		FirstDirections = [(1,0),(-1,0),(1,1),(-1,-1),(0,1),(0,-1)]
		if x >=0:

			if saveCheckPoint(grid, player[0] + 1,player[1] ):
				FirstDirections.append((1,-1))
			if saveCheckPoint(grid, player[0] , player[1] +1):
				FirstDirections.append((-1,1))
		else:
			if  saveCheckPoint(grid, player[0] - 1,player[1] ):
				FirstDirections.append((-1,1))
			if saveCheckPoint(grid, player[0] ,player[1] -1 ):
				FirstDirections.append((1,-1))
	else:
		FirstDirections = [(1,0),(-1,0),(1,-1),(-1,1),(0,1),(0,-1)]
		if x >=0:
			if  saveCheckPoint(grid, player[0] + 1,player[1] ):
				FirstDirections.append((1,1))
			if  saveCheckPoint(grid, player[0] ,player[1] -1):
				FirstDirections.append((-1,-1))
		else:
			if saveCheckPoint(grid, player[0] - 1,player[1] ):
				FirstDirections.append((-1,-1))
			if saveCheckPoint(grid, player[0] ,player[1] +1):
				FirstDirections.append((1,1))
	if len(preDir) >=1:
		if (-preDir[0][0],-preDir[0][1]) in FirstDirections:
			FirstDirections.remove((-preDir[0][0],-preDir[0][1]))
	if len(preDir) >=2:
		# print preDir
		(xx,yy) = (preDir[0][1]+preDir[0][0], preDir[1][1]+preDir[0][1])
		if (-xx,-yy) in FirstDirections:
			FirstDirections.remove((-xx,-yy))


def determineTarget(grid, player,previousTargets):
	limit = 500
	island = findIsland(grid,player,limit)
	if island == None:
		return None
	prelen = 0

	while len(island) > 1 and prelen != len(island):
		prelen = len(island)
		island = reduceMaximumPoints(grid,island)
		if island == None :
			return None
		if len(island) <= 3:
			for land in sorted(previousTargets):
				if land in island:
					return land

	if island == [] or island == None:
		return None
	return island[0]

def level3(grid, player,previousTargets):
	target = determineTarget(grid,player,previousTargets)
	print "target:", target
	if not target:
		return None

	tmp  =  navigateToPoint(grid,player,target)
	if tmp:
		d,navigatingRoute = tmp
	else:
		d = None
		navigatingRoute = []
	print "\n\nd:",d
	return (d,target,navigatingRoute)

def choose(grid,player,prev,differences,preDir,previousTargets,navigating):
	navigatingRoute = []
	info = ""
	t[0] = time.time()
	# grid[player[0]][player[1]] = 8
	target  = (1000000,10000000)
	initializeDirections(differences,grid,player,preDir)
	initializeSurrounding(grid,player)
	updateGrid(grid,player,prev)
	retrieveOriginalGrid(grid,player,prev)
	smartness = 1

	#smartness level 1
	direction, length = findSingleEight(grid,player,FirstDirections)

	#smartness level 2
	if time.time() - t[0] < delay:
		direction2 = findAdvancedEight(grid,player)
		if direction2 != None:
			direction = direction2
			smartness =2

	#smartness level 3

	if time.time() - t[0] < delay:
		done = False

		index = 0

		while navigating!= [] and index <len(navigating):
			point = navigating[index]
			index+=1
			if  point in prev or point ==player \
				or not saveCheckPoint(grid,point[0],point[1]) \
				or abs(point[0]-player[0])>1 or abs(point[1]-player[1])>1:

				continue
			done = True
			direction = point[0]-player[0],point[1]-player[1]
			smartness =3
			info= "using navigating memory",navigating


		if not done:
			tmp = level3(grid,player,previousTargets)
			if tmp and tmp[0]:
				direction = tmp[0]
				target =tmp[1]
				smartness =3
				navigatingRoute = tmp[2]
				info= "refresh navigating memory",navigatingRoute




	grid[player[0]][player[1]] = 8
	for i in grid:
                print i


	print "smartness level: ", smartness, "time usage:", time.time() -t[0],info
        returnValue = transformDirection(direction)
        print "inside ai direction:", returnValue, "result:", grid[returnValue[0]][returnValue[1]]
	return returnValue,target,navigatingRoute

	# for i in range(180):
	# for i in findMaximumPoints(grid):
	# 	print i
	# print "\n\n\n\n\n"

		# if not island:
		# 	powerDirectionChoice = powerfulDirection(grid,player)
		# if powerDirectionChoice == None:
		# 	if powerChoice != None:
		# 		nav = navigateToPoint(grid,origin,powerChoice)
		# 		if nav:
		# 			result = nav
		# 			print "use powerful"
		# 		else:
		# 			ps =
		# 			if not timeout:
		# 				pointsR = reduceMaximumPoints(grid,ps)
		# 				if not timeout:
		# 					retmp = navigateToPoint(grid,origin,pointsR[0])
		# 					if retmp:
		# 						result = retmp
		# 						print "use island"
		# 					else:
		# 						print "island not going, use advanced"
