import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms
import numpy as np
import cv2
from PIL import Image
import os
import json
from typing import Dict, List, Tuple
from api.utils.logger import logger
from api.simulations.components.event_context import ContextCNN

class HandballDataset(Dataset):
    """Dataset for handball context analysis"""
    
    def __init__(self, 
                 data_dir: str,
                 transform: transforms.Compose,
                 split: str = 'train'):
        """
        Initialize dataset
        
        Args:
            data_dir: Directory containing training data
            transform: Image transforms
            split: 'train' or 'val'
        """
        self.data_dir = data_dir
        self.transform = transform
        self.split = split
        
        # Load annotations
        with open(os.path.join(data_dir, f'{split}_annotations.json'), 'r') as f:
            self.annotations = json.load(f)
            
        # Define class mappings
        self.game_situation_map = {
            "defensive_block": 0,
            "attacking_play": 1,
            "set_piece": 2,
            "open_play": 3,
            "counter_attack": 4
        }
        
        self.intent_map = {
            "deliberate": 0,
            "accidental": 1,
            "natural_position": 2,
            "unnatural_position": 3
        }

    def __len__(self) -> int:
        return len(self.annotations)

    def __getitem__(self, idx: int) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        """
        Get a training sample
        
        Returns:
            Tuple of (image, game_situation_label, intent_label)
        """
        annotation = self.annotations[idx]
        
        # Load and transform image
        image_path = os.path.join(self.data_dir, annotation['image_path'])
        image = Image.open(image_path).convert('RGB')
        image = self.transform(image)
        
        # Get labels
        game_situation = self.game_situation_map[annotation['game_situation']]
        intent = self.intent_map[annotation['player_intent']]
        
        return image, torch.tensor(game_situation), torch.tensor(intent)

def train_model(
    data_dir: str,
    model_save_path: str,
    num_epochs: int = 50,
    batch_size: int = 32,
    learning_rate: float = 0.001
) -> None:
    """
    Train the context analysis model
    
    Args:
        data_dir: Directory containing training data
        model_save_path: Path to save trained model
        num_epochs: Number of training epochs
        batch_size: Batch size for training
        learning_rate: Learning rate for optimizer
    """
    # Define transforms
    transform = transforms.Compose([
        transforms.Resize((64, 64)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406],
                           std=[0.229, 0.224, 0.225])
    ])
    
    # Create datasets
    train_dataset = HandballDataset(data_dir, transform, 'train')
    val_dataset = HandballDataset(data_dir, transform, 'val')
    
    # Create data loaders
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False)
    
    # Initialize model
    model = ContextCNN()
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = model.to(device)
    
    # Define loss functions and optimizer
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)
    
    # Training loop
    best_val_loss = float('inf')
    for epoch in range(num_epochs):
        # Training phase
        model.train()
        train_loss = 0.0
        for images, game_situations, intents in train_loader:
            images = images.to(device)
            game_situations = game_situations.to(device)
            intents = intents.to(device)
            
            # Forward pass
            game_situation_logits, intent_logits = model(images)
            
            # Calculate losses
            game_situation_loss = criterion(game_situation_logits, game_situations)
            intent_loss = criterion(intent_logits, intents)
            loss = game_situation_loss + intent_loss
            
            # Backward pass
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            
            train_loss += loss.item()
        
        # Validation phase
        model.eval()
        val_loss = 0.0
        with torch.no_grad():
            for images, game_situations, intents in val_loader:
                images = images.to(device)
                game_situations = game_situations.to(device)
                intents = intents.to(device)
                
                # Forward pass
                game_situation_logits, intent_logits = model(images)
                
                # Calculate losses
                game_situation_loss = criterion(game_situation_logits, game_situations)
                intent_loss = criterion(intent_logits, intents)
                loss = game_situation_loss + intent_loss
                
                val_loss += loss.item()
        
        # Calculate average losses
        train_loss /= len(train_loader)
        val_loss /= len(val_loader)
        
        # Log progress
        logger.info(f'Epoch {epoch+1}/{num_epochs}:')
        logger.info(f'Train Loss: {train_loss:.4f}, Val Loss: {val_loss:.4f}')
        
        # Save best model
        if val_loss < best_val_loss:
            best_val_loss = val_loss
            torch.save(model.state_dict(), model_save_path)
            logger.info('Saved new best model')

if __name__ == '__main__':
    # Training configuration
    config = {
        'data_dir': 'data/training',
        'model_save_path': 'models/context_cnn.pth',
        'num_epochs': 50,
        'batch_size': 32,
        'learning_rate': 0.001
    }
    
    # Create necessary directories
    os.makedirs('data/training', exist_ok=True)
    os.makedirs('models', exist_ok=True)
    
    # Train model
    train_model(**config) 