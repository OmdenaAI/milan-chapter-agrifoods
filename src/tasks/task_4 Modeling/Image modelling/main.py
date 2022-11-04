import torch
from pathlib import Path

from src.models import ConvModel, RNNModel
from src.utils import read_config



class RunTask:

    def __init__(self,config):
        self.config= config
   

    def train_cnn(self):
        """
        Train an CNN model
        
        """

        histogram_path = Path(self.config["cnn_params"]["data_path"])

        model = ConvModel(self.config["cnn_params"],self.config["guassian"])
        
        model.run(self.config["cnn_params"])
        
    
    def train_rnn(self):
        
        """
        Train an RNN model
        
        """
        
        histogram_path = Path(self.config["rnn_params"]["data_path"])

        model = RNNModel(self.config["rnn_params"],self.config["guassian"])
        
        model.run(self.config["cnn_params"])
        


if __name__ == "__main__":
    config = read_config('./config/config.yaml')
    
    task = RunTask(config)
    #to run RNN model 
    print("Training RNN model")
    task.train_rnn()

    #to run CNN model 
    # print("Training CNN model")
    # task.train_cnn()
