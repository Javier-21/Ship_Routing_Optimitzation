# Ship Routing Optimitzation

## Table of content

* [Introduction](#introduction)
* [Context](#context)
* [Description](#description)
* [Enviroment](#enviroment)
    * [Creation](#creation)
    * [Inputs and Outputs](#inputs-and-outputs)
* [Solutions](#solutions)
   * [First solution. No heuristics](first-solution.-no-heuristics)
   * [Second solution. Heuristic 1: No return](second-solution.-heuristic-1:-no-return)
   * [Third solution. Heuristic 2: Direction of destination](third-solution.-heuristic-2:-direction-of-destination)
* [Conclusions](#conclusions)
* [Final video](#final-video)
* [Author](#author)

## Introduction
This project is the Computer Engineering Final Project. The main motivation was to do a project where I could apply reinforcement learning to solve an IT problem.

## Context
In the sea there are buoys that are specialized in obtaining information from the environment and transfer this information to the ships. In these situations, the problem is that there is no infrastructure to establish communication and it is necessary to use opportunistic protocols to spread the data. In this context, the boats are mobile agents whose location we do not know and the buoys are static elements and we know their location. With opportunistic protocols, communication is available when the mobile agents that want to receive information are close to the static elements that broadcast the data.

## Description
The project wants to solve the previous problem by modifying the route of the boats to cross the maximum number of buoys, but without deviating too much from the destination. To carry out a solution, we first need an environment that simulates the navigation of the boats and their interaction with the buoys and the rest of the elements of the sea and the land.

## Enviroment
The environment is like a game. We have an image of the Atlantic Ocean and we can manage the movement of a ship and we receive a response and a new image with the updated information.

### Creation
<img src="https://github.com/Javier-21/Ship_Routing_Optimitzation/blob/master/rsc/map_enviroment.png" align="right" width="350" alt="Enviroment map"/>

To create the simulator, I used python to code. I took an image of the world and resized the image to have just the Atlantic Ocean as a 100x100 matrix. On the screen there are seven different elements:
* Water: In these cells the ship can move without problems.
* Land: The ship cannot move in these cells.
* Ship: Is the agent that we want to manage.
* Buoys: Are the elements that we want to cross before reaching the destination.
* Storm: They are water cells, but in this case the ship moves slower.
* Ports: There are 5 cells indicating the ports, but only one is the destination port.
* Route line: It is a red line that indicates where the ship was.

### Inputs and Outputs
To simplify the simulator, the ship can only move in 4 directions (north, south, east, west), and this is the only input we need to specify.

The environment output is the updated matrix and a reward. The value of the reward depends on the interaction of the ship with other elements of the map. Possible answers are:
* Interaction with land, without destination port or outside image border: The ship does not move and the environment expects another movement.
* Interaction with water: The reward is -1.
* Interaction with buoy: The reward is 20. If the same buoy is repeated on the same route, the reward is -1.5.
* Interaction with buoy: The reward is -2.
* Interaction with destination port: The reward is 200.
* Interaction with route line: The reward is -1.5.

## Solutions
Now we have the environment to simulate the navigation of the ship. The next step is to implement an algorithm to solve the problem. I have applied a reinforcement learning algorithm. The field is based on learning by trial and error. In order to implement this, we need an environment where we can enter an action, and it returns a reward and a state. This environment is the simulator that I created earlier. The agent that performs the actions and receives the output of the environment is the ship in this project.

<p align="center">
<img src="https://github.com/Javier-21/Ship_Routing_Optimitzation/blob/master/rsc/rl_image.png" width="400" alt="Reinforcement learning"/>
</p>

The specific algorithm I used was Q-learning. To implement this we need to build a matrix with all possible states and for each state all possible moves. For this project we need a 100x100x4 shape matrix. Each cell contains a reward value for performing an action in a specific state. The value is updated using the following formula:

$$ Q^{new}(s_t, a_t) = (1-α) * Q(s_t, a_t)+α(r+γ * max_{a_{t+1}}Q(s_{t+1}, a_{t+1})) $$

$ Q^{new}(s_t, a_t) $ is the current value for a state and an action. α is the weighting factor between the current value and the new value based on the reward of the current move. r is the reward. γ is the discount factor.

One matrix is useful for one destination port, for this reason we need to build five matrix, one for each port. When we have the matrix we must begin to learn, for this we begin to move the ship randomly. During iterations, we started mixing random actions and matrix-based actions. In the end, actions will be taken mostly based on the matrix. To control for chance we need to use a variable ε. This variable will decrease exponentially with the step of the iteration until reaching the minimum.

I created three solutions based on this algorithm and applying some heuristic technique on some solutions. For all solutions, I initialize the matrix to the value minus infinity.

### First solution. No heuristics
In this first solution I applied the original algorithm, without variation. The result was very good, only one route is unsuccessful. In the following image we can see the heat map of the Q matrix at the end of the training to study this error case.

<p align="center">
<img src="https://github.com/Javier-21/Ship_Routing_Optimitzation/blob/master/rsc/sh_heatmap.png" width="400" alt="Error solution 1"/>
</p>

The green dot is the destination and the rest of the red dots are the different origin ports. The error appears when we start at port 3. The drawback of the algorithm is that when the port is very far from the destination and there are no intermediate ports on the routes, you will likely have trouble reaching the destination. If there is a port in the middle, it probably fixes this error, because learning from each port is used for the others.

### Second solution. Heuristic 1: No return
<img src="https://github.com/Javier-21/Ship_Routing_Optimitzation/blob/master/rsc/h1.png" align="right" width="400" alt="Heuristic 1: No return"/>

In the second solution we apply a heuristic. We need to find the vector that joins the ship to the destination port and calculate the perpendicular that divides the map into two areas. In case of making a movement in the area where the destination port is not located, the negative rewards are doubled.

The result with this solution is perfect, all the trips end successfully. In this section we are only talking about the success rate of boat routes, but in later sections we will talk about crossed buoys and distances.

### Third solution. Heuristic 2: Direction of destination
<img src="https://github.com/Javier-21/Ship_Routing_Optimitzation/blob/master/rsc/h2.png" align="right" width="400" alt="Heuristic 1: No return"/>
In this solution we apply other heuristic. In this case we need to find the vector that joins the ship with the destination port too. The difference is that now we calculate the angle with this vector and each movement. Depends of the grade we modify the reward multiplying for a factor between 1 and 2. The reward is calculated with the next formula:

$$ r = r * (1 + |β|/180) $$

<p align="center">
<img src="https://github.com/Javier-21/Ship_Routing_Optimitzation/blob/master/rsc/h2_heatmap.png" width="400" alt="Error solution 1"/>
</p>

## Conclusions

## Final video
[![Ship learning](https://img.youtube.com/vi/wj3ZSi1u1rY/0.jpg)](https://www.youtube.com/watch?v=wj3ZSi1u1rY)
<br/>
Click on the image to view the video on YouTube.

## Author
- [Javier Alegre Revuelta](https://github.com/Javier-21)
