
Project Summary
 
TeamKill is an Artificial Intelligence Malmo-based project developed for a multiplayer Minecraft survival minigame “Falling Floor”. Our first goal is to create an intelligent agent that can survive the minigame as long as possible (Single player AI). Our second goal is to make the agent smart enough to win against multiple enemies in the same map (Multiplayer AI).
(display video)
 
Approach
 
Single Player Version
 
We implemented Breadth First Search algorithm to calculate number of contiguous tiles remaining once the agent moves to an adjacent tile (representing one movement direction), effectively detecting choke points on the map and preventing the agent from trapping itself, ensuring survival. BFS is run for 8 adjacent tiles from the agent’s location with 25 visited tiles cutoff, simulating a max tree of depth 1. We also applied pruning by skipping over adjacent tiles that have already been visited in the previous BFS. The resulting subset of adjacent tiles are then used as input for another algorithm that determines the most promising direction, one that has the most tiles in a straight line. In case of a tie, the algorithm will pick the last direction the agent was moving if it is within this subset of tiles, or the first direction in the subset otherwise.
 
Multiplayer Version
 
Our plan is to implement two algorithms for our agent: Breadth First Search to determine contiguous tiles, and Reinforcement Learning to set weight on each action the agent can take. Our algorithm takes the whole map and the position of individual players as input, and outputs the best possible movement direction our agent can make every second. Our algorithm considers (1) number of contiguous tiles (which makes up an ‘island’) in every possible direction originating from the player using BFS, (2) the number of enemy players in the island, and (3) the agent’s influence over the tiles in the island to calculate the score of the state.
A player’s influence is calculated as follows:
Influence = (# Tiles closer to the player than any other players)/(# Tiles in the island)
 
The input for our algorithm in single player mode:
	<# Contiguous tiles in our island>
The input for our algorithm in multiplayer mode:
<# Contiguous tiles in our island, # Players in our island, Agent’s influence>
The output:
The best possible direction our agent can move (including diagonals)
 
Each factor will contribute to the next direction our agent moves every second, with the weight of each action determined by Reinforcement Learning.
 
Evaluation
 
Our evaluation for the single player agent:
Able to survive as long as possible:
Prevent itself from being trapped in a small island
Approximate and move to the best direction based on tile length
 
Our evaluation plan for the multiplayer agent:
Able to choose the best course of actions in different scenarios:
Being able to trap other players in a small island
Being able to actively increase its influence over its island
Being able to revert back to survival mode in certain situations
 
So far, we have completed the implementation for the single player agent. Our evaluation for this part of the project include:
 
Ensuring that the agent leaves survives as long as possible in a 40x40 grid map with 3 seconds delay before the floor gets destroyed
Ensuring that the agent do not trap itself in a smaller island when it is on a choke point between two or more islands.
 
The result of our evaluation shows that the agent is successful in avoiding being trapped on a choke point (video).
Agent has been observed to be able to survive for 268 seconds in a 40x40 grid map with 3 seconds tile destroy delay.
Observation from 5 runs:
 
Run #
Survival Time (seconds)
1
268
2
276
3
282
4
 
5
 
 
 
Remaining Goal and Challenges:
 
The remaining goal is to finish the implementation of the multiplayer algorithm and to train our agent enough so that it displays intelligent behavior when playing the game against other AIs and possibly humans.
 
An algorithm design challenge arises as our algorithm has to take running time into account. Since this is a fast-paced minigame, our agent will not have time to calculate the best move possible using tree search. We tried running our agent using the Hypermax algorithm, a multiplayer version of minimax with pruning. While it was able to choose the correct result, it took ~3.5 seconds to choose the best move from looking 2 moves ahead in a 3-player game. We have decided not to use this algorithm for the multiplayer version of the game, but will still use its concept of looking ahead to prevent the agent from trapping itself and ensure its survival.
