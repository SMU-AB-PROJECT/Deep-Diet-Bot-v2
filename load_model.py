import tensorflow as tf
#from tensorflow.keras.preprocessing.image import ImageDataGenerator
import cv2
import numpy as np
import os

img_size = 224
img_shape = (img_size,img_size,3)
batch_size = 32
epochs = 5
dropout_rate = 0.5
num_of_predict = 12
img_size = 224
img_shape = (img_size, img_size, 3)
batch_size = 32
epochs = 2
dropout_rate = 0.5
num_of_predict = 4
# # eff_model2 = tf.keras.models.load_model('./model/res')
# train_datagen = ImageDataGenerator(rescale=1. / 255,
#                                    shear_range=0.2,
#                                    zoom_range=0.2,
#                                    horizontal_flip=True)
# train_generator = train_datagen.flow_from_directory(
#     train_path,
#     target_size=(img_size, img_size),
#     batch_size=batch_size,
#     class_mode='categorical'
# )
#
# model = load_model()
#model.evaluate(train_generator)
def predict_output(model, in_path):
    img = cv2.imread(in_path)
    img = cv2.resize(img, (224, 224))  # resize image to match model's expected sizing
    img = np.reshape(img, [1, 224, 224, 3])
    img = img / 255.
    out = model.predict(img)
    return (np.argmax(out))
def load_model():
    model = tf.keras.models.load_model('models/eff_final.h5')
    return model
#
# def training_test():
#     img_size = 224
#     img_shape = (img_size,img_size,3)
#     batch_size = 32
#     epochs = 2
#     dropout_rate = 0.5
#     num_of_predict = 4
#     train_path = 'dataset/data'
#     # eff_model2 = tf.keras.models.load_model('./model/res')
#     train_datagen = ImageDataGenerator(rescale=1./255,
#                                       shear_range=0.2,
#                                       zoom_range=0.2,
#                                       horizontal_flip=True)
#     train_generator = train_datagen.flow_from_directory(
#         train_path,
#         target_size=(img_size,img_size),
#         batch_size=batch_size,
#         class_mode='categorical'
#     )
#     ResNet101 = ResNet50(
#         include_top=False, weights='imagenet',
#         input_shape=img_shape, classes=num_of_predict
#     )
#     efficientnet = EfficientNetB3(weights="model/efficientnetb3_notop.h5/efficientnetb3_notop.h5",
#                                   include_top=False,
#                                   input_shape=img_shape,
#                                   drop_connect_rate=dropout_rate)
#     inputs = Input(shape=img_shape)
#     efficientnet = efficientnet(inputs)
#     pooling = layers.GlobalAveragePooling2D()(efficientnet)
#     dropout = layers.Dropout(dropout_rate)(pooling)
#     outputs = Dense(num_of_predict, activation="softmax")(dropout)
#     eff_model = Model(inputs=inputs, outputs=outputs)
#     decay_steps = int(round(423/batch_size))*epochs
#     cosine_decay = CosineDecay(initial_learning_rate=1e-4, decay_steps=decay_steps, alpha=0.3)
#
#     #callbacks = [ModelCheckpoint(filepath='best_model.h5', monitor='val_loss', save_best_only=True)]
#     eff_model.compile(loss=tf.keras.losses.CategoricalCrossentropy(), optimizer=tf.keras.optimizers.Adam(cosine_decay), metrics=["accuracy"])
#     history = eff_model.fit(train_generator,
#                        epochs = epochs)
#     eff_model.save('model/testing_model/res.h5')
#     return eff_model, history
