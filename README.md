# snips-record-personal-hotword

This repo contains the script aimed at recording the 3 samples required a personal hotword model. 
It also contains the instructions to test your model before moving it into your assistant.

## Record the 3 samples

First be sure that your device has the required package installed (see the `requirements.txt` file). If not, you can run the following command: 

```pip install -r requirements.txt```

Then, just enter the following command to record your 3 hotword samples.

```python script_recording your_hotword_name```

The prompt will then guide you through the different steps. We insist that the environment must 
be as quiet as possible to ensure the quality of your model.
This script also performs some postprocessing on your samples, in order to remove silence at the beginning and the end of each record. 
For this postprocessing to perform well, you have to be sure not to make any noise between the 
"recording..." and the "finished recording" messages in the prompt for each hotword (the duration between those two messages should be 2 seconds, 
which lets you time to pronounce your hotword).

## Validate your recordings (optional)

## Test your model and adjust its sensitivity

## Update your assistant configuration to run your personal model

