import numpy as np
import cv2
from collections import deque
import copy
import random
from random import sample


COLOR_WATER = [255, 0, 0]
COLOR_GROUND = [37, 73, 141]
COLOR_TRAVEL = [0, 0, 255]
COLOR_BUOY = [0, 233, 255]
COLOR_PORT = [154, 152, 150]
COLOR_DESTINY_PORT = [0, 255, 0]
COLOR_STORM = [0, 0, 0]

ID_GROUND = 0
ID_WATER = 1
ID_PORT = 2
ID_DESTINY_PORT = 3
ID_BUOY = 4
ID_BOAT = 5
ID_STORM = 6
ID_TRAVEL = 7
ID_OLD_BUOY = 8

BUOY_POSITION = [[20, 75], [35, 40], [50, 62], [80, 21], [68, 36], [92, 60], [23, 54], [65, 65], [80, 60], [60, 40], [54, 50], [43, 45], [44, 62]]
MAX_PORTS = 10
PORT_POSITION = [[20,52], [41,40], [60, 22], [78,29], [89, 32], [25, 82], [37, 72], [49, 72], [62,72], [88,68]]

FPS = 25
SIZE_RENDER = (355, 533)
SIZE_GAME = (100, 100)
X_MIN = 100
X_MAX = 300
Y_MIN = 50
Y_MAX = 200

#MOVES
UP = 0
DOWN = 1
LEFT = 2
RIGTH = 3


class Enviroment:
    def __init__(self):
        #Init variables and load the map
        self.list_frames = []
        self.state = []
        self.info = []
        self.done = False
        self.reward = 0
        self.old_buoy = False
        _, self.np_game = cv2.threshold(cv2.imread('img/mapa_mundi_binario.jpg',cv2.IMREAD_GRAYSCALE), 0, 1, cv2.THRESH_OTSU)
        self.__increment_duration(50)

        #Zoom the map
        self.__zoom()
        self.np_game = cv2.resize(self.np_game, SIZE_GAME, interpolation = cv2.INTER_AREA)
        self.__increment_duration(25)

        #Init static elements (buoys and ports)
        for x, y in BUOY_POSITION:
            self.np_game[x, y] = ID_BUOY
        for x, y in PORT_POSITION:
            self.np_game[x, y] = ID_PORT

    #Function to add frames at video
    def __increment_duration(self, n_frames):
        for i in range(n_frames):
            self.list_frames.append(copy.copy(self.np_game))

    #Function to zoom the map
    def __zoom(self):
        step = 10
        x_min = 0
        x_max = self.np_game.shape[0]
        y_min = 0
        y_max = self.np_game.shape[1]
        static_frame = copy.copy(self.np_game)
        while x_min != X_MIN or x_max != X_MAX or y_min != Y_MIN or y_max != Y_MAX:
            x_min = min(X_MIN, x_min + step)
            x_max = max(X_MAX, x_max - step)
            y_min = min(Y_MIN, y_min + step)
            y_max = max(Y_MAX, y_max - step)
            self.np_game = static_frame[y_min:y_max, x_min:x_max]
            self.__increment_duration(10)

    #Function to create a video
    def render(self):
        out = cv2.VideoWriter('output.mp4', cv2.VideoWriter_fourcc(*'mp4v'), FPS, SIZE_RENDER)
        for single_frame in self.list_frames:
            np_render = np.zeros((single_frame.shape[0], single_frame.shape[1], 3), dtype='uint8')

            np_render[single_frame==ID_WATER,:] = COLOR_WATER
            np_render[single_frame==ID_GROUND,:] = COLOR_GROUND
            np_render[single_frame==ID_STORM,:] = COLOR_STORM
            np_render[single_frame==ID_PORT,:] = COLOR_PORT
            np_render[single_frame==ID_BUOY,:] = COLOR_BUOY
            np_render[single_frame==ID_OLD_BUOY,:] = COLOR_BUOY
            np_render[single_frame==ID_DESTINY_PORT,:] = COLOR_DESTINY_PORT
            np_render[single_frame==ID_TRAVEL,:] = COLOR_TRAVEL

            x, y = np.where(single_frame == ID_BOAT)
            if (x and y):
                x, y = x[0], y[0]
                np_render[x, y-3:y+3, :] = [65, 138, 222]
                np_render[x+1, y-2:y+2, :] = [65, 138, 222]
                np_render[x-4:x, y, :] = [0, 0, 0]
                np_render[x-4:x-1, y+1, :] = [255, 255, 255]
                np_render[x-3, y+2, :] = [255, 255, 255]


            data1 = cv2.resize(np_render, SIZE_RENDER, interpolation = cv2.INTER_AREA)
            out.write(data1)
        out.release()

    #Init variables of a game
    def reset(self):
        self.state.clear()
        self.info.clear()
        self.done = False

        self.np_game[((self.np_game==ID_BOAT) + (self.np_game==ID_TRAVEL))] = ID_WATER
        #Init static elements (buoys and ports)
        for x, y in BUOY_POSITION:
            self.np_game[x, y] = ID_BUOY
        for x, y in PORT_POSITION:
            self.np_game[x, y] = ID_PORT

        source, destiny = sample(range(0, MAX_PORTS-1), 2)
        self.np_game[PORT_POSITION[source][0], PORT_POSITION[source][1]] = ID_BOAT
        self.np_game[PORT_POSITION[destiny][0], PORT_POSITION[destiny][1]] = ID_DESTINY_PORT
        self.__increment_duration(25)
        x, y = np.where(self.np_game == ID_BOAT)
        self.state.append(x[0])
        self.state.append(y[0])
        x, y = np.where(self.np_game == ID_DESTINY_PORT)
        self.info.append(x[0])
        self.info.append(y[0])
        self.info.append(False)

        return self.state, self.info

    #Execute and action
    def step(self, action):
        self.info[2] = False

        if action == UP:
            self.info[2] = self.__move(self.state[0]-1, self.state[1])
        elif action == DOWN:
            self.info[2] = self.__move(self.state[0]+1, self.state[1])
        elif action == RIGTH:
            self.info[2] = self.__move(self.state[0], self.state[1]+1)
        elif action == LEFT:
            self.info[2] = self.__move(self.state[0], self.state[1]-1)

        if self.info[2]:
            self.__increment_duration(10)

        

        return self.state, self.reward, self.done, self.info

    def __move(self, x, y):
        if self.np_game[x, y] == ID_GROUND or self.np_game[x, y] == ID_PORT:
            self.reward = 0
            return False
        else:
            if self.old_buoy:
                self.np_game[self.state[0], self.state[1]] = ID_OLD_BUOY
                self.old_buoy = False
            else:
                self.np_game[self.state[0], self.state[1]] = ID_TRAVEL

            if self.np_game[x, y] == ID_WATER or self.np_game[x, y] == ID_TRAVEL:
                self.reward = -1
            elif self.np_game[x, y] == ID_BUOY:
                self.reward = 10
                self.old_buoy = True
            elif self.np_game[x, y] == ID_DESTINY_PORT:
                self.reward = 100
                self.done = True
            elif self.np_game[x,y] == ID_OLD_BUOY:
                self.reward = -1
                self.old_buoy = True
            else:
                print('Uknow: ', self.np_game[x,y])

            self.np_game[x,y] = ID_BOAT
            self.state[0] = x
            self.state[1] = y
            return True




N_EPISODES = 20
MAX_ITER = 100

env = Enviroment()

for episode in range (N_EPISODES):
    state, info = env.reset()
    done = False
    iteration = 0
    episode_reward = 0

    while not done and iteration < MAX_ITER:
        action = random.randint(0,3)
        state, reward, done, info = env.step(action)
        episode_reward += reward
        iteration += 1
    print (done, episode_reward)
#env.render()
