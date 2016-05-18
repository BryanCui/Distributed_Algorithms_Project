————————————————————————————————————————————————————————————
Distributed Algorithm Project

Xiangyu  Zhou 690709
Xiaoxuan Tang 692782
Da Zhang      665442
Tianying Cui  664885
—————————————————————————————————————————————————————————————————————————————————
To run the system, npyscreen should be installed. Then use python to execute the Tradercraft.py. Then the system will start. To start the game, users should choose their roles and input ip address and port of a known node, then press start. If not input ip address, the current node will be started as the first game node.

If you want to establish the bank (Central Server Based Algorithm), in the peer directory, run commonwealth.py with python. And the use the instruction below, you can also use the “a.csv ”file to batch import the cdkeys.

Game Commands:
Bank:
create: create cdkey as prize for both new uses and old users. Users can redeem the Cdkey to money.
	Example: create activateCode 1000
delete: delete the invalid cdkey.
	Example: delete activateCode
list: list all existing activate codes.
	Example: list
import: batch import activate codes from csv file.
	Example: import a.csv

Game Client:
Connect ip port: require the node list from a specific user
Example: connect 10.13.44.110 8000
nodelist: show current user list

snapshot: take snapshot of the system
buy ip port resource quantity: buy resources from others
Example: buy 10.13.44.110 8000 wood 20
trade resource quantity price: put resources into trading center
Example: trade wood 100 20
stock wood quantity: get resource back from trading center
Example: stock wood 20 
remote ip port: inspect the trading resources of the specific user
	Example: remote 10.13.44.110 8000
activate ip port activateCode: activate code from bank to get money
	Example: activate 10.13.44.110 3000 cdkey





Source code structure

DAStractegyGame: root folder
| ----- Tradercraft.py: App UI entry handling 

| ----- Singleton.py: to support singleton pattern

| ----- User
         |----- TradingCenter.py: users put their resources into it to sell
         |----- User.py: the user that playing the game
         |----- __init__.py: to support module import

| ----- Transactions
         |----- Transactions.py: transactions which support user to buy resources from others
         |----- __init__.py: to support module import

| ----- peer
         |----- bank.py: bank class provides functons maintaining the cdkeys
         |----- command.py: contains all command of the game
         |----- commonwealth.py: implementaion of central server based algorithm.
         |----- message.py: main all message types for whole system
         |----- node.py: main handler for the command
         |----- notificationCentre.py: send notification to UI if data changes
         |----- snapshot.py: snapshot algorithm
         |----- __init__.py: to support module import

| ----- GUI
         |----- LoginScreen.py: Login screen for entry connecton configuration and choose role
         |----- __init__.py: to support module import
