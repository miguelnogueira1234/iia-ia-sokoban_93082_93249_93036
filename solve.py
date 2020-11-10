import asyncio
import getpass
import json
import os
import collections
import copy
import websockets



## # -> parede
## - -> chao
## $ -> caixa
## @ -> player
## * -> caixa certa
## . -> local para por caixa
## + -> player em cima de local


## A variável lastMoves é um array que tem os movimentos testados pelo agente
## basta mandar o lastMoves (em cada iteraçao do ciclo while) para o server


for i in range(1, 156):

        board=[]
        maxLength=0

        boxAgent=[]
        walls=[]
        possibleMoves = {'U':[-1,0], 'R':[0,1],'D':[1,0],'L':[0,-1]}

        maxRowLength = 0	
        lines=0

        #File_map = input("Enter file name")
        print("Ficheiro "+str (i) + ".xsb")
        file_h = open('./levels/' + str (i) + ".xsb")


        for line in file_h:
                if line != "":
                        lines += 1
                        board.append(line)
                        if len(line)>maxRowLength:
                                maxRowLength=len(line)
                else:
                        break



        import time
        time_start = time.time()
        for i in range(0,lines):
                boxAgent.append([])
                walls.append([])
                for j in range(0,maxRowLength):
                        boxAgent[-1].append('-')
                        walls[-1].append('-')



        ## Making the board a rectangle even if the input is not one
        for i in range(0,len(board)):
                if len(board[i])<maxRowLength:
                        for j in range(len(board[i]),maxRowLength):
                                board[i]+='#'


        ## Storing walls&storage spaces in one 2d array , boxes and robot in another 2d array
        for i in range(0,len(board)):
                for j in range(0,maxRowLength):
                        if board[i][j]=='$' or board[i][j]=='@':
                                boxAgent[i][j]=board[i][j]
                                walls[i][j]=' '
                        elif board[i][j]=='.' or board[i][j]=='#':
                                walls[i][j] = board[i][j]
                                boxAgent[i][j] = ' '
                        elif board[i][j]=='-':
                                boxAgent[i][j] = ' '
                                walls[i][j]=' '
                        elif board[i][j] == '*':
                                boxAgent[i][j] = '$'
                                walls[i][j] = '.'
                        elif board[i][j] == '+':
                                boxAgent[i][j] = '@'
                                walls[i][j] = '.'

        ## Solving the problem with the BFS algorithm
        print ("Solving ...\n")

        movesList=[]
        passedMoves=[]

        ## Adding source to queue
        queue = collections.deque([])
        source = [boxAgent,movesList]
        if boxAgent not in passedMoves:
                passedMoves.append(boxAgent)
        queue.append(source)
        agent_x = -1
        agent_y = -1
        completed = 0
        while len(queue)!=0 and completed==0:


                ### Popping first item from the queue
                temp = queue.popleft()
                curPosition = temp[0]
                lastMoves = temp[1]

                for i in range(0,lines):
                        for j in range(0,maxRowLength):
                                if curPosition[i][j]=='@':
                                        agent_y = j
                                        agent_x = i
                                        break
                        else:
                                continue
                        break


                ## Getting agent position of the popped element.

                for key in possibleMoves:

                        ## Checking for all the four directions
                        agentNext_x = agent_x+possibleMoves[key][0]
                        agentNext_y = agent_y+possibleMoves[key][1] 
                        curPositionAux = copy.deepcopy(curPosition)

                        lastMovesAux = copy.deepcopy(lastMoves)
                        if curPositionAux[agentNext_x][agentNext_y] == '$':

                                ## If there is a box after agent makes a move
                                boxNext_x = agentNext_x + possibleMoves[key][0]
                                boxNext_y = agentNext_y + possibleMoves[key][1]
                                if curPositionAux[boxNext_x][boxNext_y]=='$' or walls[boxNext_x][boxNext_y]=='#':
                                        ## if the cell after agent pushes the box is another box or wall, avoid further steps.
                                        continue
                                else:
                                        ## if the agent can push the box
                                        curPositionAux[boxNext_x][boxNext_y]='$'
                                        curPositionAux[agentNext_x][agentNext_y] = '@'
                                        curPositionAux[agent_x][agent_y] = ' '
                                        if curPositionAux not in passedMoves:
                                                matches= 0
                                                for k in range(0,lines):
                                                        for l in range(0,maxRowLength):
                                                                if walls[k][l]=='.':
                                                                        if curPositionAux[k][l]!='$':
                                                                                matches=1
                                                lastMovesAux.append(key)
                                                if matches == 0:
                                                        completed = 1
                                                        print (lastMovesAux)
                                                else:
                                                        queue.append([curPositionAux,lastMovesAux])
                                                        passedMoves.append(curPositionAux)
                        else:

                                ## if the agent moves into a wall
                                if walls[agentNext_x][agentNext_y]=='#': 
                                        continue
                                else:
                                        ## if the agent moves into empty space
                                        curPositionAux[agentNext_x][agentNext_y]='@'
                                        curPositionAux[agent_x][agent_y]=' '
                                        if curPositionAux not in passedMoves:
                                                lastMovesAux.append(key)
                                                queue.append([curPositionAux,lastMovesAux])
                                                passedMoves.append(curPositionAux)
                
        if completed==0:
                print ("Can't make it")


        time_end = time.time()
        print ("Run time: "+str(time_end - time_start))

