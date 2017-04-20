---
layout: default
title: Proposal
---

## Summary of the Project


The first game of AI would be for a game about running in a collapsing map as shown in the video ( https://www.youtube.com/watch?v=E6yxgg0MMMM ) from 3:00 to 3:45. We will write an AI with the input of all the locations of the player and the enemy players. The output of our algorithm will be the direction the player should go in the next second.

The second phase of our AI would be for a game called “Capture the enemy flag” ( http://www.minecraftguides.org/capture-the-flag/ ). In this phase, we will write an AI with the input of player locations (both enemy players and ally players) and the flag location. The output will be the direction that our player should go in the next second and the weapon/abilities he will use. (His goal is to steal the flag from enemy base and bring it back to the ally base.)

Applications:

We can apply this AI to all the games with “Capture the flag mode map” including Overwatch.




## AI/ML Algorithms

For the first phase of our AI, we will get the locations of all the enemies in the map and the available map for players. The output will be the direction the player should go in the next second. Our logic:

1. Give positive values for the available road in one direction and negative values for enemy players in that direction.
2. Calculate the player’s next direction base on those values.
3. Calculate the directions of enemy players in the same way.
4. Adjust the player’s direction based on enemy’s direction by changing the values of enemy players in the values.
5. Repeat the step 2-4 until the result stabilized or reach the time limit.

In our algorithm, we will use min-max tree to stabilize the direction, reinforcement learning to determine the default impact of enemy according to its location and direction.



For the second game, capture the flag, we are going to implement two kinds of AI: global and individual.

\tThe global AI and individual AI have different visibility of the map:

\tThe global AI is the manager of the team and it will decide whether a teammate should go advancing or attack or defend.

The individual AI is the player itself. It will receive the basic command from global AI and all the information of other players and flags so that it can output the next behaviour of this individual player.

We are going to implement reinforcement learning with the difference of friendly team’s average distance to the enemy flag and enemy team’s average distance to the ally flag as a global heuristic. Individual behavior will be determined by a finite state machine of set behaviors (advancing, attacking, defending), with commands issued by the global AI. Individual AI decision will also be affected by their health (survival), the presence of enemies and teammates in their immediate surrounding (cooperation), and game-changing factors (ally/enemy has the flag, etc.).






## Evaluation Plan

The baseline of our AI is to expect reasonable behaviours from AI such as stopping/killing the player with the flag, running away from enemies, defending/stealing the flag. With reinforcement learning, we expect our AI with the capability to cooperate with its teammates, even more teamplay strategies.

To test our AI with the abilities we expect, we will have several sanity cases for each ability:

    A case in which the enemy with the flag is backing to its base, see if AI in the middle can stop/kill the enemy.
    A case in which AI with the flag is chased by many enemies, see if our AI can pass the flag to a healthier teammate or run toward to its base.
    A case in which our flag is well defended by our teammates, see if the AI can take enemies’ flag.



With the basic abilities, we try to apply AI to an actual game to see its behaviors.
To quantify the improvement, we can run games with old versions of AI and newer versions of AI. We can see improvement if newer versions of AI have a higher win ratio.


## Appointment with the Instructor

We reserved the appointment at 12:15pm, April 25, 2017.


