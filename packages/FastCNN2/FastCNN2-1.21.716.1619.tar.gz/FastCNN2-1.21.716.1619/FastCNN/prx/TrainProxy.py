from FastCNN.prx.DatasetProxy import DatasetProxy
from FastCNN.prx.PathProxy import PathProxy2 as PathProxy
from FastCNN.nn.neuralnets import getNeuralNet

from IutyLib.file.files import CsvFile
from IutyLib.commonutil.config import JConfig
import os

import numpy as np

import random
import shutil
import time
import json
import datetime

def get_train_batch(X_train, y_train, batch_size, img_w, img_h,img_f,endless = True):
    '''
    参数：
        X_train：所有图片路径列表
        y_train: 所有图片对应的标签列表
        batch_size:批次
        img_w:图片宽
        img_h:图片高
        color_type:图片类型
        is_argumentation:是否需要数据增强
    返回: 
        一个generator，x: 获取的批次图片 y: 获取的图片对应的标签
    '''
    queue_x = []
    queue_y = []
    
    
    
    seed = random.randint(1,30)
    random.seed(seed)
    random.shuffle(X_train)
    
    random.seed(seed)
    random.shuffle(y_train)
    
    queue_x += X_train
    queue_y += y_train
    
    while 1:
        
        while (len(queue_x) < batch_size):
            queue_x += X_train
            queue_y += y_train
            
        
        
        x = queue_x[0:batch_size]
        
        x = readBmp(x,img_w,img_h,img_f)
       # queue_x = queue_x[batch_size:]
        
        y = queue_y[0:batch_size]
        #queue_y = queue_y[batch_size:]
        
        queue_x = queue_x[batch_size:]
        queue_y = queue_y[batch_size:]
        
        #yield({'input': np.array(x)}, {'output': np.array(y)})
        yield(np.array(x), np.array(y))


class TrainProxy:
    projectid = ""
    modelid = ""
    config = None
    def getConfig(projectid,modelid):
        cfgpath = PathProxy.getConfigPath(projectid,modelid)
        jfile = JConfig(cfgpath)
        data = jfile.get()
        return data
    
    def getSuperParam(projectid,modelid):
        cfgpath = PathProxy.getSuperParamConfigPath(projectid,modelid)
        jfile = JConfig(cfgpath)
        data = jfile.get()
        return data
    
    def startTrainModel(self,projectid,modelid):
        self.projectid = projectid
        self.modelid = modelid
        self.config = TrainProxy.getConfig(projectid,modelid)
        trainset,validset,traintag,validtag = DatasetProxy.getData(projectid,modelid)
        
        superparam = TrainProxy.getSuperParam(projectid,modelid)
        batch = int(superparam["Batch"])
        width = int(self.config["Width"])
        height = int(self.config["Height"])
        formatter = self.config["Formatter"]
        
        train_batch = get_train_batch(trainset,traintag,batch,width,height,formatter)
        test_batch = get_train_batch(validset,validtag,1,width,height,formatter)
        
        self.model = getNeuralNet(self.config,superparam)
        return self.model
        pass

if __name__ == "__main__":
    pass