# MazeSolutionTCPDataTransfer
Program to convert solution to randomly generated maze into motor input for a robot. Uses TCP data packets to transmit the data from the server to the robot.


1. I first converted the maze solution to motor input, taking into consideration rotation and motor activity based on past and future values of the solution coordinates
1. The TCP Server is located in the MazeSolutionServer.py code and listens for client sockets to send the motor input to
1. The ClientSocket.py program creates a client socket that connects to the server and takes the data from the server

SAMPLE MAZE SOLUTION

![Project diagram](examplemazesolution.png)

DATA TRANSMITTED FROM SERVER TO CLIENT

![Project diagram](tcpdata.png)
