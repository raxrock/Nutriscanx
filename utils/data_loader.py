
import os
import tensorflow as tf
import requests
import zipfile
import io

def download_food101():
    """Download Food-101 dataset (smaller subset for testing)"""

    os.makedirs("data/images/food101", exist_ok=True)
    
    print("Downloading Food-101 dataset (smaller test subset)...")
    
    import tensorflow_datasets as tfds
    
    
    dataset, info = tfds.load(
        'food101', 
        split=['train[:100%]', 'validation[:100%]'],
        with_info=True,
        as_supervised=True,
        shuffle_files=True
    )
    
    train_dataset, val_dataset = dataset
    
    print(f"Dataset loaded with {info.splits['train'].num_examples} training examples")
    print(f"and {info.splits['validation'].num_examples} validation examples")
    
    return train_dataset, val_dataset

def preprocess_data(dataset, img_size=224, batch_size=32):
    """Preprocess dataset for training"""
   
    def preprocess(image, label):
        image = tf.image.resize(image, [img_size, img_size])
        image = image / 255.0  # Normalize to [0,1]
        return image, label
    
    #  preprocessing
    dataset = dataset.map(preprocess, num_parallel_calls=tf.data.AUTOTUNE)
    
    # Batch and prefetch
    dataset = dataset.batch(batch_size).prefetch(tf.data.AUTOTUNE)
    
    return dataset