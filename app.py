# -*- coding: utf-8 -*-
"""Copy of Untitled21.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/13w1XexDRQQ4OwdEPif6eGLYpS5fRsmCr
"""

import torch
import torch.nn as nn

# Create a simple linear regression model
class LinearRegressionModel(nn.Module):
    def __init__(self):
        super(LinearRegressionModel, self).__init__()
        self.linear = nn.Linear(1, 1)  # One input feature, one output

    def forward(self, x):
        return self.linear(x)

# Create some dummy data for training
x = torch.tensor([[1.0], [2.0], [3.0], [4.0]], dtype=torch.float32)  # Input data
y = torch.tensor([[2.0], [4.0], [6.0], [8.0]], dtype=torch.float32)  # Corresponding output data

# Instantiate the model
model = LinearRegressionModel()

# Define a loss function and an optimizer
criterion = nn.MSELoss()  # Mean Squared Error loss
optimizer = torch.optim.SGD(model.parameters(), lr=0.01)  # Stochastic Gradient Descent

# Training loop
for epoch in range(1000):
    # Forward pass
    y_pred = model(x)

    # Compute the loss
    loss = criterion(y_pred, y)

    # Backpropagation and optimization
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    if (epoch + 1) % 100 == 0:
        print(f'Epoch [{epoch + 1}/1000], Loss: {loss.item()}')

# Save the trained model to a .pth file
torch.save(model.state_dict(), 'linear_regression_model.pth')

print("Model saved to linear_regression_model.pth")

"""#------------------------------------------------------------------------"""

from flask import Flask, request, jsonify
import torch
import torch.nn as nn

app = Flask(__name__)

# Load your trained model
class RegressionModel(nn.Module):
    def __init__(self):
        super(RegressionModel, self).__init__()
        self.fc = nn.Linear(1, 1)

    def forward(self, x):
        return self.fc(x)

model = RegressionModel()
state_dict = torch.load('/home/abdullah/Documents/linear_regression_model.pth')
# Rename keys to match your model
state_dict['fc.weight'] = state_dict.pop('linear.weight')
state_dict['fc.bias'] = state_dict.pop('linear.bias')
model.load_state_dict(state_dict)
model.eval()

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        input_data = torch.tensor(data['input_data'], dtype=torch.float32)
        with torch.no_grad():
            prediction = model(input_data).item()
        return jsonify({"prediction": prediction})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)