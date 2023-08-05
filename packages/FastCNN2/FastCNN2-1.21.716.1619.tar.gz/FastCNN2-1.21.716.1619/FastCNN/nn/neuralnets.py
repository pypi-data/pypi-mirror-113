from FastCNN.nn.alexnet import AlexNet
from FastCNN.nn.standard import Baseline
from FastCNN.nn.lenet import LeNet
from FastCNN.nn.vgg import VGG
#from FastCNN.nn.inspection import Inspection
#from FastCNN.nn.resnet import ResNet

nets = {
    "AlexNet":AlexNet,
    "Standard":Baseline,
    "LeNet":LeNet,
    "VGG":VGG,
}

def getNeuralNet(config,superparam):
    name = config["Type"]
    if name in nets:
        return nets[name](config,superparam)
    else:
        return BaseLine(config,superparam)