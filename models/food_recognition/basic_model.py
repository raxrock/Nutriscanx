
import tensorflow as tf
from tensorflow.keras.applications import MobileNetV3Small
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.models import Model

def create_food_recognition_model(num_classes=101, img_size=224):
    """
    Create a basic food recognition model using transfer learning
    """
   
    base_model = MobileNetV3Small(
        weights='imagenet',
        include_top=False,
        input_shape=(img_size, img_size, 3)
    )
    

    for layer in base_model.layers:
        layer.trainable = False
    

    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    x = Dense(512, activation='relu')(x)
    x = Dropout(0.3)(x)
    predictions = Dense(num_classes, activation='softmax')(x)
    

    model = Model(inputs=base_model.input, outputs=predictions)

    model.compile(
        optimizer='adam',
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )
    
    return model