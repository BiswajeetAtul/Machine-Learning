import logging, io, json, warnings
#logging.basicConfig(level="INFO")
#warnings.filterwarnings('ignore')
import rasa_nlu
import rasa_core
import spacy
from rasa_nlu.training_data import load_data
from rasa_nlu.config import RasaNLUModelConfig
from rasa_nlu.model import Trainer
from rasa_nlu import config

from rasa_core.actions import Action
from rasa_core.events import SlotSet
from rasa_core.policies import FallbackPolicy, KerasPolicy, MemoizationPolicy
from rasa_core.agent import Agent

print("Initializing the ChatBot:")
def initChatBot():
    print("STEP 1:Training the NLU Model")
    #Training the NLU MODEL:
    # loading the nlu training samples
    training_data = load_data("NLU_Train.json")
    # trainer to create the pipeline
    trainer = Trainer(config.load("NLU_model_Config.yml"))
    # training the model
    interpreter = trainer.train(training_data)
    # storeing it for future
    model_directory = trainer.persist("./models/nlu", fixed_model_name="current")
    print("Done")


    print("STEP 2: Training the CORE model")
    fallback = FallbackPolicy(fallback_action_name="utter_default",
                            core_threshold=0.2,
                            nlu_threshold=0.1)

    agent = Agent(domain='restaurant_domain.yml', policies=[MemoizationPolicy(), KerasPolicy(validation_split=0.0,epochs=200), fallback])
    training_data = agent.load_data('Core_Stories.md')
    agent.train(training_data)
    agent.persist('models/dialogue')
    print("Done")
    return model_directory

def startChatBot(model_directory):
    print("STEP 3: Starting the Bot")
    from rasa_core.agent import Agent
    agent = Agent.load('models/dialogue', interpreter=model_directory)
    print("Your bot is ready to talk! Type your messages here or send 'stop'")

    if(True):
        import rasa_core.run
        rasa_core.run.serve_application(agent,channel="cmdline")
    return agent    

if __name__ == "__main__":    
    model_directory=initChatBot()
    startChatBot(model_directory)