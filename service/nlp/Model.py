import gensim
import os
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
import tensorflow.keras as keras
import nltk
import sklearn
import numpy
import collections
import pymorphy2
import pickle
import gensim.downloader
import os.path
import typing
import numpy as np
from tensorflow.keras.utils import to_categorical

__EMBED_SIZE = 300
__NUM_FILTERS = 512
__NUM_WORDS = 3
__BATCH_SIZE = 32
__NUM_EPOCHS = 15
__keras_model_path = '/app/service/nlp/keras_model.h5'
__tokenizer_path = '/app/service/nlp/tokenizer.pickle'
__maxlen_path = '/app/service/nlp/maxlen.bin'

def fit(requests, category_ids):
    save_ids(category_ids)

    category_ids = get_indices(category_ids)
    requests, category_ids = sklearn.utils.shuffle(requests, category_ids)

    sentences = numpy.array([tokenize(request) for request in requests])
    counter, maxlen = get_counter_and_maxlen(sentences)
    vocab_sz = len(counter) + 1
    embedding_weights = get_weights(counter, vocab_sz)
    X_train = get_X_train(sentences, maxlen)
    y_train = keras.utils.to_categorical(category_ids)
    keras_model = get_model(vocab_sz, maxlen, embedding_weights, classes_count=len(numpy.unique(category_ids)))

    history = keras_model.fit(X_train, y_train, batch_size=__BATCH_SIZE,
                              epochs=__NUM_EPOCHS,
                              callbacks=[keras.callbacks.ModelCheckpoint('keras_model.h5', save_best_only=True)],
                              validation_split=0.2, verbose=0)

    return history

def predict(request: str) -> int:
    #if os.path.isfile(__keras_model_path) and os.path.isfile(__tokenizer_path) and os.path.isfile(__maxlen_path):
    keras_model = keras.models.load_model(__keras_model_path)

    with open(__tokenizer_path, 'rb') as handle:
      tokenizer = pickle.load(handle)
    sentences = [tokenize(request)]
    X_predict = tokenizer.texts_to_sequences(sentences)
    X_predict = keras.preprocessing.sequence.pad_sequences(X_predict, maxlen=get_maxlen())

    prediction = np.argmax(keras_model.predict(X_predict), axis=-1)
    indices_unique = numpy.unique(get_ids())

    return indices_unique[prediction[0]]
    '''
    else:
        print('Error')

        return -1 '''

def get_indices(category_ids):
    consecutive_indices = []
    unique_id = numpy.unique(category_ids).tolist()

    for id in category_ids:
        consecutive_indices.append(unique_id.index(id))

    return consecutive_indices

def save_ids(category_ids):
    with open('/app/service/nlp/indices.pickle', 'wb') as f:
        pickle.dump(category_ids, f)

def get_ids():
    with open('/app/service/nlp/indices.pickle', 'rb') as f:
        indices = pickle.load(f)

    return indices

def get_weights(counter, vocab_sz):
    word2vec_model = gensim.downloader.load("word2vec-ruscorpora-300")

    embedding_weights = numpy.zeros(
        (vocab_sz, __EMBED_SIZE))
    index = 0
    sorted_counter = counter.most_common()
    for word in sorted_counter:
        try:
            embedding_weights[index, :] = word2vec_model[word[0]]
            index += 1
        except KeyError:
            index += 1
            pass

    return embedding_weights

def get_counter_and_maxlen(sentences):
    counter = collections.Counter()

    maxlen = 0
    for words in sentences:
        if len(words) > maxlen:
            maxlen = len(words)
        for word in words:
            counter[word] += 1

    save_maxlen(maxlen)

    return counter, maxlen

def save_maxlen(maxlen):
    f = open(__maxlen_path, 'w')
    f.write(str(maxlen))
    f.close()

def get_maxlen():
    f = open(__maxlen_path, 'r')
    maxlen = int(f.read())
    f.close()
    return maxlen

def get_X_train(sentences, maxlen):
    tokenizer = keras.preprocessing.text.Tokenizer()
    tokenizer.fit_on_texts(sentences)
    X_train = tokenizer.texts_to_sequences(sentences)
    X_train = keras.preprocessing.sequence.pad_sequences(X_train,
                                                         maxlen=maxlen)
    save_tokenizer(tokenizer)

    return X_train

def save_tokenizer(tokenizer):
    with open(__tokenizer_path, 'wb') as handle:
        pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)

def tokenize(request):
    morph = pymorphy2.MorphAnalyzer()
    regex_tokenizer = nltk.tokenize.RegexpTokenizer('[а-яА-ЯЁё]+')
    words = regex_tokenizer.tokenize(request.lower())
    stop_words = set(nltk.corpus.stopwords.words("russian"))
    without_stop_words = [(morph.parse(w)[0]).normal_form
    for w in words if w not in stop_words and len(w) > 1]
    output = [add_part_of_speech(morph, word) for word in without_stop_words]
    return output

def add_part_of_speech(morph, word):
    p = morph.parse(word)[0]
    word += '_' + str(p.tag.POS)
    return word

def get_model(vocab_sz, maxlen, embedding_weights, classes_count):
    model = keras.models.Sequential()
    model.add(keras.layers.Embedding(vocab_sz, __EMBED_SIZE, input_length=maxlen,
                                     weights=[embedding_weights],
                                     trainable=True))
    model.add(keras.layers.Dropout(0.2))
    model.add(keras.layers.Conv1D(50,
                                  3,
                                  padding='valid',
                                  activation='relu',
                                  strides=1))
    model.add(keras.layers.GlobalMaxPooling1D())
    model.add(keras.layers.Dense(250))
    model.add(keras.layers.Dropout(0.2))
    model.add(keras.layers.Activation('relu'))
    model.add(keras.layers.Dense(classes_count, activation='softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

    return model