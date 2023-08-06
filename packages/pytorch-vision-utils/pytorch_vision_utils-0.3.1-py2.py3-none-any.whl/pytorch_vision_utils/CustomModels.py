"""Contains all of the available models for customization. Wrapper for another module I've been messing with.
"""

from torch import nn

from pretrainedmodels.models.xception import Xception, xception
from pretrainedmodels.models.mobilenetv2 import MobileNetV2, mobilenetv2

from torchvision.models import alexnet
from torchvision.models import densenet121, densenet161, densenet169, densenet201
from torchvision.models import inception_v3
from torchvision.models import resnet18, resnet34, resnet50, resnet101, resnet152
from torchvision.models import squeezenet1_0, squeezenet1_1
from torchvision.models import vgg11, vgg11_bn, vgg13, vgg13_bn, vgg16, vgg16_bn, vgg19, vgg19_bn



def get_avail_models() -> dict:
    """
    Gets all of the available pretrained models initialized.
    
    Returns
    -------
    `dict`\n
        Dictionary representation of model names (key) mapped with the actual model (value).
    """  
 
    
    model_names = [# ["alexnet"], 
    #                ['densenet121', 'densenet161', 'densenet169', 'densenet201'], 
    #                ["inceptionv3"], 
                   ["mobilenetv2"], 
                #    ['resnet18', 'resnet34', 'resnet50', 'resnet101', 'resnet152'], 
                #    ['squeezenet1_0', 'squeezenet1_1'], 
                #    ['vgg11', 'vgg11_bn', 'vgg13', 'vgg13_bn', 'vgg16', 'vgg16_bn', 'vgg19', 'vgg19_bn'], 
                   ["xception"]]
    
   

    model_wrappers = [# AlexNetWrapper, 
    #                 DenseNetWrapper,
    #                 InceptionV3Wrapper,
                    MobileNetV2Wrapper,
                    # ResNetWrapper,
                    # SqueezeNetWrapper,
                    # VGGWrapper,
                    XceptionWrapper]

    return (model_names, model_wrappers)



# class VGGWrapper():
#     _vgg_names = ['vgg11', 'vgg11_bn', 'vgg13', 'vgg13_bn', 'vgg16', 'vgg16_bn', 'vgg19', 'vgg19_bn']
#     _vgg_models = [vgg11, vgg11_bn, vgg13, vgg13_bn, vgg16, vgg16_bn, vgg19, vgg19_bn]
#     _vgg_dict = dict(zip(_vgg_names, _vgg_models))
    
#     def __init__(self, model_name, num_classes=2, debug=False):
#         """
#         Wrapper around the vgg function to change the classifier from 1000 to 2 and adds a debug functionality.

#         Attributes
#         ----------
#         `model_name`: `str`\n
#             String representation of the model name.
#         `num_classes` : `int`, `optional`\n
#             The number of classes being predicted on, by default 2.
#         `debug` : `bool`, `optional`\n
#             Boolean representing whether debug mode is on or off, by default False.
#         """  
        
#         self.num_classes = num_classes
#         self.model = _vgg_dict[model_name](pretrained=True, num_classes=self.num_classes)
        
#         if debug:
#             print(self.model)




# class SqueezeNetWrapper():
#     _squeeze_names = ['squeezenet1_0', 'squeezenet1_1']
#     _squeeze_models = [squeezenet1_0, squeezenet1_1]
#     _squeeze_dict = dict(zip(_squeeze_names, _squeeze_models))
    
#     def __init__(self, model_name, num_classes=2, debug=False):
#         """
#         Wrapper around the squeezenet function to change the classifier from 1000 to 2 and adds a debug functionality.

#         Attributes
#         ----------
#         `model_name`: `str`\n
#             String representation of the model name.
#         `num_classes` : `int`, `optional`\n
#             The number of classes being predicted on, by default 2.
#         `debug` : `bool`, `optional`\n
#             Boolean representing whether debug mode is on or off, by default False.
#         """  
        
#         self.num_classes = num_classes
#         self.model = _squeeze_dict[model_name](pretrained=True, num_classes=self.num_classes)
        
#         if debug:
#             print(self.model)



# class InceptionV3Wrapper():
    
#     def __init__(self, model_name, num_classes=2, debug=False):
#         """
#         Wrapper around the inceptionv3 function to change the classifier from 1000 to 2 and adds a debug functionality.

#         Attributes
#         ----------
#         `model_name`: `str`\n
#             String representation of the model name.
#         `num_classes` : `int`, `optional`\n
#             The number of classes being predicted on, by default 2.
#         `debug` : `bool`, `optional`\n
#             Boolean representing whether debug mode is on or off, by default False.
#         """  
        
#         self.num_classes = num_classes
#         self.model = inception_v3(num_classes=num_classes)
        
#         if debug:
#             print(self)


# class ResNetWrapper():
#     _resnet_names = ['resnet18', 'resnet34', 'resnet50', 'resnet101', 'resnet152']
#     _resnet_models = [resnet18, resnet34, resnet50, resnet101, resnet152]
#     _resnet_dict = dict(zip(_resnet_names, _resnet_models))
    
#     def __init__(self, model_name, num_classes=2, debug=False):
#         """
#         Wrapper around the resnet function to change the classifier from 1000 to 2 and adds a debug functionality.

#         Attributes
#         ----------
#         `model_name`: `str`\n
#             String representation of the model name.
#         `num_classes` : `int`, `optional`\n
#             The number of classes being predicted on, by default 2.
#         `debug` : `bool`, `optional`\n
#             Boolean representing whether debug mode is on or off, by default False.
#         """  
        
#         self.num_classes = num_classes
#         self.model = _resnet_dict[model_name](pretrained=True, num_classes=self.num_classes)
        
#         if debug:
#             print(self.model)



# class DenseNetWrapper():
#     _densenet_names = ['densenet121', 'densenet161', 'densenet169', 'densenet201']
#     _densenet_models = [densenet121, densenet161, densenet169, densenet201]
#     _densenet_dict = dict(zip(_densenet_names, _densenet_models))
    
#     def __init__(self, model_name, num_classes=2, debug=False):
#         """
#         Wrapper around the densenet function to change the classifier from 1000 to 2 and adds a debug functionality.

#         Attributes
#         ----------
#         `model_name`: `str`\n
#             String representation of the model name.
#         `num_classes` : `int`, `optional`\n
#             The number of classes being predicted on, by default 2.
#         `debug` : `bool`, `optional`\n
#             Boolean representing whether debug mode is on or off, by default False.
#         """    
        
#         self.num_classes = num_classes
#         self.model = _densenet_dict[model_name](pretrained=True, num_classes=self.num_classes)
        
#         if debug:
#             print(self.model)

            
                    
# class AlexNetWrapper():
    
#     def __init__(self, model_name, num_classes=2, debug=False):
#         """
#         Wrapper around the alexnet function to change the classifier from 1000 to 2 and adds a debug functionality.

#         Attributes
#         ----------
#         `model_name`: `str`\n
#             String representation of the model name.
#         `num_classes` : `int`, `optional`\n
#             The number of classes being predicted on, by default 2.
#         `debug` : `bool`, `optional`\n
#             Boolean representing whether debug mode is on or off, by default False.
#         """  
       
#         self.num_classes = num_classes
#         self.model = alexnet(pretrained=True, num_classes=self.num_classes)
        
#         if debug:
#             print(self.model)
      
      
   
class XceptionWrapper(Xception):
    def __init__(self, model_name, num_classes=2, debug=False):
        """ Constructor
        Args:
            num_classes: number of classes
        """
        Xception.__init__(self, num_classes=num_classes)
        
        self.model_name = model_name
        self.num_classes = num_classes
        
        self.last_linear = self.fc
        del self.fc
        
        if debug:
            print(self)
            
        
    # def __init__(self, num_classes=1000):
    #     """
    #     Wrapper around the xception class to change the classifier from 1000 to 2 and adds a debug functionality.

    #     Attributes
    #     ----------
    #     `model_name`: `str`\n
    #         String representation of the model name.
    #     `num_classes` : `int`, `optional`\n
    #         The number of classes being predicted on, by default 2.
    #     `debug` : `bool`, `optional`\n
    #         Boolean representing whether debug mode is on or off, by default False.
    #     """      
        
    #     # self.num_classes = num_classes
    #     # self.model = xception()  
    #     # dim_feats = self.model.last_linear.in_features
    #     # self.model.last_linear = nn.Linear(dim_feats, self.num_classes)    
        
    #     # if debug:
    #     #     print(self.model)  
        
    #     super(Xception, self).__init__()

        
        
    #     def forward(self, x):
    #         x = self.features(input)
    #         x = self.logits(x)
    #         return x


class MobileNetV2Wrapper(MobileNetV2):
    def __init__(self, model_name, n_class=2, debug=False, input_size=224, width_mult=1.):
     #     """
    #     Wrapper around the mobilenetv2 class to change the classifier from 1000 to 2 and adds a debug functionality.

    #     Attributes
    #     ----------
    #     `model_name`: `str`\n
    #         String representation of the model name.
    #     `num_classes` : `int`, `optional`\n
    #         The number of classes being predicted on, by default 2.
    #     `debug` : `bool`, `optional`\n
    #         Boolean representing whether debug mode is on or off, by default False.
    #     """  
        MobileNetV2.__init__(self, num_classes=n_class)
        
        self.model_name = model_name
        self.num_classes = n_class
        if debug:
            print(self)
            
        
    # def __init__(self, num_classes=2):
    #     """
    #     Wrapper around the mobilenetv2 class to change the classifier from 1000 to 2 and adds a debug functionality.

    #     Attributes
    #     ----------
    #     `model_name`: `str`\n
    #         String representation of the model name.
    #     `num_classes` : `int`, `optional`\n
    #         The number of classes being predicted on, by default 2.
    #     `debug` : `bool`, `optional`\n
    #         Boolean representing whether debug mode is on or off, by default False.
    #     """  
           
    #     # self.num_classes = num_classes   
    #     # self.model = mobilenetv2() 
    #     # dim_feats = self.model.classifier.in_features
    #     # # self.model.classifier = nn.Linear(dim_feats, self.num_classes)
        
    #     # if debug:
    #     #     print(self.model)
        
    #     super(MobileNetV2, self).__init__()
    #     self.model_name = model_name
    #     self.num_classes = num_classes
        # if debug:
        #     print(self)

        
        # def forward(self, x):
        #     super()
        #     x = self.features(x)
        #     x = x.mean(3).mean(2)
        #     x = self.classifier(x)
        #     return x
            
        