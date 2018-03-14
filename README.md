# snips-record-personal-hotword

This repo contains the script aimed at recording the 3 samples required a personal hotword model. 
It also contains the instructions to test your model before moving it into your assistant. To be ale to follow the instructions, you first have to [install the snips platform](https://github.com/snipsco/snips-platform-documentation/wiki/1.-Setup-the-Snips-Voice-Platform).

## 1. Clone the repository
Clone the repo (install git before if needed).

```bash
sudo apt-get install git
git clone https://github.com/snipsco/snips-record-personal-hotword.git
cd snips-record-personal-hotword/
```

⚠ If you have set up two factor authentication for git, you're likely to face the following issue:
```bash
remote: Invalid username or password.
fatal: Authentication failed for 'https://github.com/snipsco/snips-record-personal-hotword.git/'
```
You will need to [create a personal access token directly on github](https://help.github.com/articles/creating-a-personal-access-token-for-the-command-line/) and use it in place of your password.

## 2. Install dependencies
Use the following command to install the repository dependencies
```bash
sudo apt-get install python-numpy python-pyaudio python-soundfile
```

## 3. Record the 3 samples

Enter the following command to record your 3 hotword samples.

```bash
python script_recording.py your_hotword_name
```

**Note 1**: if you encounter errors because your microphone is not available, this might be because it is currently used by `snips-audio-server`. 
```bash
IOError: [Errno -9996] Invalid input device (no default output device)
```
Stop it before launching the previous script by running:
```bash
sudo systemctl stop snips-audio-server
```

The prompt will then guide you through the different steps. **We insist that the environment must 
be as quiet as possible to ensure the quality of your model.**

**Note 2**: you might encounter some warnings (`ALSA...` and/or `jack server...`) at each step, you ignore them.

This script also performs some postprocessing on your samples, in order to remove silence at the beginning and the end of each record. 
For this postprocessing to perform well, you have to be sure not to make any noise between the 
"recording..." and the "finished recording" messages in the prompt for each hotword (the duration between those two messages should be 2 seconds, 
which lets you time to pronounce your hotword). 

Once you are finished, take note of the place your model has been saved in the last prompt message (this will be the `path_to_your_model` in the next step). You are now ready to test and adjust its sensitivity.

## 3. Test your model and adjust its sensitivity

In order to test you model run the following command (if you stopped `snips-audio-server` at the previous step, restart it by running `sudo systemctl start snips-audio-server`).

```bash
sudo systemctl stop snips-hotword; snips-hotword --model <path_to_your_model>=<sensitivity>
```

where `sensitivity` is a number between 0 and 1 that allows you to adjust the model sensitivity (the higher the sensitivity the higher the false alarm rate, e.g cases where it is triggered when it shouldn't).
 and `path_to_your_model` it the path to your model. By default the sensibility is set to `0.5`. You can play with different values of the sensitivity to find the best value for your model.

Note that you can run several models simultaneously, to do so just declare them one after the other in the command line:

```bash
snips-hotword --model <path_to_your_model_1>=<sensitivity_1> --model <path_to_your_model_2>=<sensitivity_2>
```

## 4. Update your assistant configuration to run your personal model

Once you are happy with your model, move the model directory (containing the 3 waves and the `config.json` file) to `/etc/snips/`.

If you haven't done it yet, create a `snips` folder in `/etc`. Please note that this is a distinct location from `/usr/share/snips/` where your assistant is located.
```bash
sudo mkdir /etc/snips/
```

and then move the personal hotword in the right place:
```bash
sudo mv <path_to_your_model> /etc/snips/
```

Then update the `/etc/snips.toml` file by updating the `model` entry your model in the `[snips-hotword]` section:

```toml
model = ["<path_to_your_model_1>=<sensitivity_1>", "<path_to_your_model_2>=<sensitivity_2>"]
```
Please note that `path_to_your_model` has been updated since you moved it around - it is now in `/etc/snips/` 

**Important**: If you want the universal hotword model attached to your assistant to run simultaneously, add its path to the model entry: `/usr/share/snips/assistant/custom_hotword`
Note that if you do not provide `sensivity` the model will take 0.5 by default.

Last but not least, restart your assistant's hotword by running:

```bash
sudo systemctl start snips-hotword
```