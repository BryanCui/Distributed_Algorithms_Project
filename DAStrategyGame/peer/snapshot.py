# coding=UTF-8
import logging
logging.getLogger().setLevel(logging.INFO)

# We assume there is only one snapshot taking place at any time.
class NodeSnapshot(object):
    def __init__(self, nodeList=None, jsonDict=None):
        if nodeList != None:
            self._localState = {}
            self._channelStates = {n[0]: {'msg': [], 'done': False} for n in nodeList}
            self._isDone = False
        elif jsonDict != None:
            self._localState = jsonDict.get('localState', {})
            self._channelStates = jsonDict.get('channelStates', []) 
            self._node = jsonDict.get('node', None)
            self._isDone = True
        else:
            raise ValueError

    @property
    def localState(self): # {'gold': ddd, 'wood': ddd, ...}
        return self._localState

    @property
    def channelStates(self): # {'node1_uuid': {'msg': [recorded messages], 'done': Boolean}, ...}
        return self._channelStates

    @property
    def node(self): # (uuid:int, ip:str, port:int, nickname:str)
        return self._node

    @property
    def isDone(self):
        return self._isDone
    
    @property
    def isDone(self): # True of False
        return self._isDone

    def isRecording(self, n):
        return self.channelStates[n[0]]['done']

    def finishRecord(self, n):
        self.channelStates[n[0]]['done'] = True
        for value in self.channelStates.values():
            if value['done'] == False:
                return
        self._isDone = True

    def recordMessage(self, n, msg):
        self.channelStates[n[0]]['msg'].append(msg)

    # we assume that node has implemented a method called localState, which returns a dict
    def recordLocalState(self, node):
        self._localState = node.localState()

# If we are to implement the function of gathering all NodeSnapshots, this is the class.
class SystemSnapshot(object):
    def __init__(self):
        self._nodeSnapshots = []

    @property
    def nodeSnapshots(self):
        return self._nodeSnapshots
    
    def addNodeSnapshot(self, nodeSnapshot):
        self.nodeSnapshots.append(nodeSnapshot)
