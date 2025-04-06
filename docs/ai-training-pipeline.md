# AI Training Pipeline

## Overview
The AI training pipeline for the Raasid system is designed to ensure that the AI models are trained effectively to detect handball incidents with high accuracy. The pipeline covers data collection, preprocessing, model training, evaluation, and deployment. The goal of the pipeline is to maintain high performance, scalability, and accuracy in real-world football scenarios.

## Pipeline Stages
The AI training pipeline consists of several stages, each aimed at improving the model's accuracy and reliability. Below is a detailed description of each stage:

### 1. Data Collection
The first step in the training pipeline is data collection. The system relies on two main types of data sources:

- Synthetic Data: Generated through simulations to model various handball scenarios, including different player poses, ball trajectories, and rule violations.
- Real Match Data: Collected from actual football matches, providing ground truth data for training and testing the models. This data includes video footage and sensor data (e.g., impact force, ball contact duration).

The data is labeled to indicate whether a handball occurred, the context of the handball, and the intent behind the action (intentional or accidental).

### 2. Data Preprocessing
Data preprocessing is crucial for preparing the collected data for training. This step includes:

- Normalization: Scaling input data to a consistent range to ensure uniformity across different data types.
- Data Augmentation: Generating variations of the original data (e.g., rotating images, varying lighting conditions) to improve model generalization.
- Feature Engineering: Extracting relevant features from raw sensor data and video frames, such as limb angles, impact force, and handball context.

Preprocessing helps reduce noise and prepares the data for optimal model training.

### 3. Model Training
The training stage focuses on optimizing the models to detect handball incidents accurately. The key models trained in this pipeline are:

- Pose Estimation Model: Trained to detect hand positions and limb angles to assess the likelihood of a handball.
- Ball Contact Detection Model: Trained to analyze sensor data and determine the severity of ball contact.
- Event Context Classification Model: Trained to classify the handball incident as intentional or accidental, and assess rule violations.

Each model is trained using supervised learning techniques, with labeled data to guide the training process. The models are optimized using performance metrics like accuracy, precision, recall, and F1 score.

### 4. Model Evaluation
Model evaluation ensures that the trained models perform well in real-world scenarios. The evaluation stage includes:

- Cross-validation: A technique used to assess the model's generalization ability by testing it on different subsets of data.
- Performance Metrics: Metrics such as accuracy, precision, recall, F1 score, and confusion matrix are used to evaluate the models' performance.
- A/B Testing: Comparing different versions of models to select the best-performing one for deployment.

The goal is to ensure the models can make accurate handball decisions under varying conditions.

### 5. Model Tuning and Optimization
After the initial evaluation, the models may require further tuning and optimization to enhance performance:

- Hyperparameter Tuning: Adjusting model parameters, such as learning rate, batch size, and the number of layers, to improve accuracy.
- Model Regularization: Techniques like dropout and L2 regularization are applied to prevent overfitting and improve generalization.
- Ensemble Methods: Combining the predictions of multiple models to enhance decision-making accuracy.

Optimization ensures that the models perform well under real-time match conditions.

### 6. Model Deployment
Once the models are trained and optimized, they are deployed as part of the Raasid system:

- Model Integration: The trained models are integrated into the FastAPI backend, where they are called in real time to make decisions during matches.
- Containerization: The models are packaged into Docker containers to ensure consistency and portability across different environments.
- Scalability: The system is designed to scale, allowing multiple matches to be processed simultaneously.

Deployment ensures that the models can make real-time handball decisions during matches.

## Future Enhancements
The training pipeline will be enhanced in future iterations of the system:

- Continuous Learning: Implementing an online learning system to update the models with new data in real time, improving accuracy over time.
- Automated Data Labeling: Using semi-supervised learning and active learning techniques to automate the labeling of data, reducing the need for manual labeling.
- Model Versioning: Implementing a version control system for models to track changes and ensure reproducibility of results.

## Technology Used
- Training Frameworks: TensorFlow, Keras, and Scikit-learn for model training and optimization.
- Data Processing: Pandas, NumPy, and OpenCV for data manipulation and preprocessing.
- Model Deployment: FastAPI for real-time deployment, Docker for containerization.
- Version Control: Git for code versioning, Docker for model versioning.

## Getting Started
To set up the training pipeline locally, follow these steps:

1. Clone the repository and set up the environment:
   ```bash
   git clone https://github.com/vseel5/raasid-project
   cd raasid-project
   python -m venv raasid-env
   raasid-env\Scripts\activate  # On macOS/Linux: source raasid-env/bin/activate
   pip install -r requirements.txt
   ```

2. Train the models by running the following script:
   ```bash
   python train_models.py
   ```

3. Evaluate the models:
   ```bash
   python evaluate_models.py
   ```

4. Once the models are trained and evaluated, run the FastAPI backend to deploy the models:
   ```bash
   uvicorn api.main:app --reload
   ```

## License
This project is licensed under the MIT License – see the LICENSE file for details.

## Authors
- Aseel K. Rajab, Majd I. Rashid, Ali S. Alharthi
- [GitHub Profile](https://github.com/vseel5/raasid-project)

