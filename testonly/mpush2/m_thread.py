#
# Copyright 2013 Y12Studio
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import threading,time

class BaseWorker():
    def __init__(self):
        self.stopFlag = False
        self.e = threading.Event()
        self.t = threading.Thread(target=self.worker)
        self.t.start()
        self.data = None
        
    def worker(self):
        e = self.e
        while not self.stopFlag:
            #print('wait_for_event_timeout starting')
            event_is_set = e.wait(1)
            # logging.debug('event set: %s', event_is_set)
            if event_is_set:
                self.handleEvent()
                e.clear()
            else:
                # logging.debug('doing other work')
                pass
                       
            if self.stopFlag:
                break
    
    def handleEvent(self):
        #logging.debug('processing event %d', self.count)
        print('processing event %d'% self.data)
        pass
         
    def stop(self):
        self.stopFlag = True
    
    def notify(self):
        self.e.set()
    
    def sendData(self, dvalue):
        self.data = dvalue
        self.notify()
        #logging.debug('Send Data: %d', self.count)
        # print('Send Data: %d'% self.count)
        

class MyBaseWorker(BaseWorker):
    
    def __init__(self):
        BaseWorker.__init__(self)
        self.data = 100
        
    def handleEvent(self):
        self.data += 2
        #logging.debug('MyBaseWorker processing event %d', self.data)
        print('MyBaseWorker processing event %d'% self.data)
         
    def sendData(self, d):
        self.data = d
        self.notify()
        #logging.debug('sendData event: %d', d)
        print('sendData event: %d'% d)

def test():
    wcls = MyBaseWorker()
    time.sleep(2)
    wcls.sendData(12)
    print('Event is Send 1')
    time.sleep(5)
    wcls.sendData(99)
    print('Event is Send 2')
    time.sleep(2)
    wcls.stop()