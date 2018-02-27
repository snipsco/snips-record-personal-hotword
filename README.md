# snips-record-personal-hotword

This repo contains the script aimed at recording the 3 samples required a personal hotword model. 
It also contains the instructions to test your model before moving it into your assistant. To be ale to follow the instructions, you first have to install the snips platform (see the documentation at https://github.com/snipsco/snips-platform-documentation/wiki/1.-Setup-the-Snips-Voice-Platform).

## 1. Clone the repository that contains the script and postprocessing utils

Clone the repo (install git before if needed).

```sudo apt-get install git```
```git clone https://github.com/snipsco/snips-record-personal-hotword.git```

Install the required python packages. If you have `pip` installed you can use `pip install -r requirements.txt`. However we recommend to use the following command.

```sudo apt-get install python-numpy python-pyaudio python-soundfile```


## 2. Record the 3 samples

Enter the following command to record your 3 hotword samples.

```python script_recording your_hotword_name```

**Note**: if you encounter errors becouse your microphone is not availale, this might be because it is currently used y `snips-audio-server`. If yes, stop it efore lauching the previous script y running `sudo systemctl stop snips-audio-server`.

The prompt will then guide you through the different steps. **We insist that the environment must 
be as quiet as possible to ensure the quality of your model.**
This script also performs some postprocessing on your samples, in order to remove silence at the beginning and the end of each record. 
For this postprocessing to perform well, you have to be sure not to make any noise between the 
"recording..." and the "finished recording" messages in the prompt for each hotword (the duration between those two messages should be 2 seconds, 
which lets you time to pronounce your hotword). 

Once you are finished, take note of the place your model has been saved in the last prompt message (this will be the `path_to_your_model` in the next step). You are now ready to test and adjust its sensitivity.

## 3. Test your model and adjust its sensitivity

In order to test you model run the following command (if you stopped `snips-audio-server` at the previous step, restart it by running `sudo systemctl start snips-audio-server`).

```sudo systemctl stop snips-hotword; snips-hotword -- --model path_to_your_model=sensitivity```

where `sensitivity` is an integer between 0 and 1 that allows you to adjust the model sensitivity (the higher the sensitivity the higher the number of false positive).
 and `path_to_your_model` it the path to your model. By default the sensibility is set to `0.5`. You can play with different values of the sensitivity to find the best value for your model.

Note that you can run several models simultaneously, to do so just declare them one after the other in the command line:

```snips-hotword --model path_to_your_model_1=sensitivity_1 --model path_to_your_model_2=sensitivity_2```

## 4. Update your assistant configuration to run your personal model

Once you are happy with your model, move the model directory (containing the 3 waves and the `config.json` file) to `/etc/snips/`.

Then update the `etc/snips.toml` file by updating the `model` entry your model to the `[snips-hotword]` section:

```
model = ["path_to_your_model_1=sensitivity_1", "path_to_your_model_2=sensitivity_2"]
```

**Important**:If you want the universal hotword model provided y snips simultaneously, don't forget to add the path to the model in the array above. If you have an assistant, the path to the universal model is ususally `/usr/share/snips/assistant/custom_hotword`.
Note that if you do not provide `sensivity` the model will take 0.5 by default.

Finally, restart your assistant's hotword y runing:

```sudo systemctl start snips-hotword```


