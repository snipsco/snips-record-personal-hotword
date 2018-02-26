# snips-record-personal-hotword

This repo contains the script aimed at recording the 3 samples required a personal hotword model. 
It also contains the instructions to test your model before moving it into your assistant.

## Clone the repository that contains the script and postprocessing utils

```git clone git@github.com:snipsco/snips-record-personal-hotword.git```

## Record the 3 samples

First be sure that your device has the required package installed (see the `requirements.txt` file). If not, you can run the following command: 

```pip install -r requirements.txt```

Then, just enter the following command to record your 3 hotword samples:

```python script_recording your_hotword_name```

The prompt will then guide you through the different steps. We insist that the environment must 
be as quiet as possible to ensure the quality of your model.
This script also performs some postprocessing on your samples, in order to remove silence at the beginning and the end of each record. 
For this postprocessing to perform well, you have to be sure not to make any noise between the 
"recording..." and the "finished recording" messages in the prompt for each hotword (the duration between those two messages should be 2 seconds, 
which lets you time to pronounce your hotword). 

Once you are finished, take note of the place your model has been saved (last prompt message). You are now ready to test and adjust it.

## Test your model and adjust its sensitivity

In order to test you model run the following command: 

```snips-hotword -- --model path_to_your_model=sensitivity```

where `sensitivity` is an integer between 0 and 1 that allows you to adjust the model sensitivity (the higher the sensitivity the higher the number of false positive).
By default the sensibility is set to `0.5`. You can play with different values of the sensitivity to find the best value for your model.

## Update your assistant configuration to run your personal model

Once you are happy with your model, move the model directory (containing the 3 waves and the `config.json` file) to `/etc/snips/`.

Then update the `etc/snips.toml` file by adding to the `[snips-hotword]` section:

```
base base base
```

