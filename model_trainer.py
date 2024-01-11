import json, pickle, random
import numpy as np

from nltk import WordNetLemmatizer
from nltk import word_tokenize as tokenizer

from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.optimizers import SGD

class ModelTrainer:
    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()
        self.intents = self.load_intents()
        self.words = []
        self.classes = []
        self.documents = []
        self.ignore_letters = ['?', '!', '.', ',']
        
        self.process_intents()

    def load_intents(self):
        with open(".\\resources\\intents.json") as file:
            intents = json.load(file)
        return intents

    def process_intents(self):
        for intent in self.intents['intents']:
            for pattern in intent['patterns']:
                word_list = tokenizer(pattern)
                self.words.extend(word_list)
                self.documents.append((word_list, intent['tag']))
                if intent['tag'] not in self.classes:
                    self.classes.append(intent['tag'])

        self.words = [self.lemmatizer.lemmatize(word) for word in self.words if word not in self.ignore_letters]
        self.words = sorted(set(self.words))
        self.classes = sorted(set(self.classes))
        self.save_data()

    def save_data(self):
        pickle.dump(self.words, open('.\\resources\\words.pkl', 'wb'))
        pickle.dump(self.classes, open('.\\resources\\classes.pkl', 'wb'))

    def create_training_data(self):
        training = []
        output_empty = [0] * len(self.classes)
        for document in self.documents:
            bag = []
            word_patterns = document[0]
            word_patterns = [self.lemmatizer.lemmatize(word.lower()) for word in word_patterns]
            for word in self.words:
                bag.append(1) if word in word_patterns else bag.append(0)
            output_row = list(output_empty)
            output_row[self.classes.index(document[1])] = 1
            training.append([bag, output_row])
        random.shuffle(training)
        return np.array(training)

    def train_model(self):
        training_data = self.create_training_data()
        training = np.array(training_data)

        train_x = list(training[:, 0])
        train_y = list(training[:, 1])

        model = Sequential()
        model.add(Dense(128, input_shape=(len(train_x[0]),), activation='relu'))
        model.add(Dropout(0.5))
        model.add(Dense(64, activation='relu'))
        model.add(Dropout(0.5))
        model.add(Dense(len(train_y[0]), activation='softmax'))

        sgd = SGD(lr=0.01, momentum=0.9, nesterov=True)
        model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])
        
        hist = model.fit(np.array(train_x), np.array(train_y), epochs=200, batch_size=5, verbose=1)

        model.save('.\\resources\\chatbot_model', hist)

if __name__ == "__main__":
    ModelTrainer().train_model()