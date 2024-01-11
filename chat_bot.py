import os, json, pickle
import numpy as np

from nltk import word_tokenize as tokenizer
from nltk.stem import WordNetLemmatizer
from keras.models import load_model

from module_manager import ModuleManager

manager = ModuleManager()

class ChatBot:
    def __init__(self):
        os.putenv('CUDA_VISIBLE_DEVICES', '')
        self.lemmatizer = WordNetLemmatizer()
        self.intents = json.loads(open('.\\resources\\intents.json').read())
        self.words = pickle.load(open('.\\resources\\words.pkl', 'rb'))
        self.classes = pickle.load(open('.\\resources\\classes.pkl', 'rb'))
        self.model = load_model('.\\resources\\chatbot_model')

    def clean_up_sentence(self, sentence):
        sentence_words = tokenizer(sentence) 
        sentence_words = [self.lemmatizer.lemmatize(word) for word in sentence_words] 
        return sentence_words

    def bag_of_words(self, sentence):
        sentence_words = self.clean_up_sentence(sentence)
        bag = [0] * len(self.words)
        for w in sentence_words:
            for i, word in enumerate(self.words):
                if word == w:
                    bag[i] = 1
        return np.array(bag)

    def predict_class(self, sentence):
        bow = self.bag_of_words(sentence)
        res = self.model.predict(np.array([bow]))[0]
        ERROR_THRESHOLD = 0.4
        results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
        results.sort(key=lambda x: x[1], reverse=True)
        return_list = []
        for r in results:
            return_list.append({'intent': self.classes[r[0]], 'probability': str(r[1])})
        return return_list

    def get_response(self, intents_list, intents_json):
        tag = intents_list[0]['intent']
        for i in intents_json['intents']:
            if i['tag'] == tag:
                return i['function']

    def get_response_function(self, message):
        ints = self.predict_class(message)
        task_class_name = self.get_response(ints, self.intents)
        return manager.run_from_module(task_class_name)