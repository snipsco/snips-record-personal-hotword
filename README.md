# snips-record-personal-hotword

This repo contains the script aimed at recording the samples required for a personal hotword model. To be able to follow the instructions, you first have to [install the snips platform](https://snips.gitbook.io/documentation/installing-snips) and [add an assistant](https://snips.gitbook.io/documentation/console/first-steps) to your device .

## 0. Personal hotword
The personal hotword allows you to define your own word to wake your assistant and initiate a conversation. To do so, the algorithm needs some samples of you saying this particular word. In this tutorial, a script will guide you through the recording of those samples and in a second part, we will show you how to test your model and incorporate it in your assistant.

**WARNING: In order for the model to perform well, the environment where you record your samples must be as quiet as possible so you must avoid place with background noise (music, tv, people speaking ...).**

## 1. Clone the repository

Connect to the pi by ssh:

```bash
ssh username@hostname
```

Clone the repo (install git before if needed).

```bash
sudo apt-get install git
git clone https://github.com/snipsco/snips-record-personal-hotword.git
cd snips-record-personal-hotword/
```

## 2. Install dependencies
Use the following command to install the repository dependencies

```bash
sudo apt-get install python-numpy python-pyaudio python-soundfile
```

## 3. Record the samples

Enter the following command to record your hotword samples (where you can put your own hotword name instead of `your_hotword_name`):

```bash
sudo systemctl stop snips-audio-server; python script_recording.py your_hotword_name
```
 
The prompt will then guide you through the different steps. **We insist that the environment must 
be as quiet as possible to ensure the quality of your model. Some checks are made in the script to ensure that your records are not too long neither to different one from another. If that happens you might see some WARNING message that will ask you to record more samples.**

**Note**: you might encounter some warnings (`ALSA...` and/or `jack server...`) at each step, you can ignore them.

This script also performs some postprocessing on your samples, in order to remove silence at the beginning and the end of each record. 
For this postprocessing to perform well, you have to be sure not to make any noise between the 
"recording..." and the "finished recording" messages in the prompt for each hotword (the duration between those two messages should be 2 seconds, 
which lets you time to pronounce your hotword). 

Once you are finished, take note of the place your model has been saved in the last prompt message (this will be the `path_to_your_model` in the next step). You are now ready to test and adjust its sensitivity.

## 4. Test your model and adjust its sensitivity

In order to test you model first run the following commands.

```bash
sudo systemctl stop snips-hotword; sudo systemctl stop snips-dialogue; sudo systemctl start snips-audio-server;
```

Then run the following one to launch the hotword detector:

```bash
snips-hotword --model <path_to_your_model>=<sensitivity>
```


where `sensitivity` is a number between 0 and 1 that allows you to adjust the model sensitivity (the higher the sensitivity the higher the false alarm rate, e.g cases where it is triggered when it shouldn't) and `path_to_your_model` it the path to your model. By default the sensibility is set to `0.5`. You can play with different values of the sensitivity to find the best value for your model (usually between `0.4` and `0.6`).

## 5. Update your assistant configuration to run your personal model

Once you are satisfied with your model, move the model directory (containing the waves and the `config.json` file) to `/etc/snips/` (still with your own `path_to_your_model`):

```bash
sudo mkdir -p /etc/snips/; sudo mv <path_to_your_model> /etc/snips/
```

Your model now has a new path which we denote `new_path_to_your_model`. Then edit the `/etc/snips.toml` file  with `sudo nano /etc/snips.toml` by updating the `model` entry in the `[snips-hotword]` section with the following line:

```toml
[snips-hotword]
model = ["<new_path_to_your_model>=<sensitivity>"]
```

Note that the `#` symbol must be erased in front on the model line.


 If you want to run several models simultaneously, you just have declare them one after the other in the model entry (`model = ["<new_path_to_your_model_1>=<sensitivity_1>", "<new_path_to_your_model_2>=<sensitivity_2>"]`)


**Important**: If you want the universal hotword model attached to your assistant to run simultaneously, add its path to the model entry: `/usr/share/snips/assistant/custom_hotword`.
Note that if you do not provide `sensivity` the model will take 0.5 by default.

Finally, restart your assistant's hotword by running:

```bash
sudo systemctl restart snips-hotword; sudo systemctl restart snips-dialogue
```
 You can then check that it works by running ```snips-watch -vvv``` (if not installed, run ```sudo apt-get install snips-watch```).
 
 
## Contributing

Please see the [Contribution Guidelines](https://github.com/snipsco/snips-record-personal-hotword/blob/master/CONTRIBUTING.md).

## Copyright

This library is provided by [Snips](https://www.snips.ai) as Open Source software. See [LICENSE](https://github.com/snipsco/snips-record-personal-hotword/blob/master/LICENSE) for more information.
