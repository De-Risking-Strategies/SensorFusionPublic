# SensorFusion API 

# Import packages
import os
import argparse
import cv2
import numpy as np
import sys
import time
from threading import Thread
import importlib.util
from flask import Flask, jsonify, request, render_template

app = Flask(__name__)
app.config("DEBUG") = True
#############################
# Additional code goes here #
#############################
@app.route('/')
def home_page():
    example_embed='This string is from python'
    return render_template('index.html', embed=example_embed)


#########  run app  #########
app.run(debug=True)
