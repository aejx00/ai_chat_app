import os 
import argparse
import uberduck
import subprocess
from transformers import AutoTokenizer, AutoModelForCausalLM


# https://towardsdatascience.com/develop-a-conversational-ai-bot-in-4-simple-steps-1b57e98372e2

# uber duck config
if os.getcwd() == '/code':
    temp_files_path = os.path.join("core", "chat", "static", "audio")
else:
    temp_files_path = os.path.abspath(os.path.join("static", "audio"))
client = uberduck.UberDuck(os.getenv('UBERDUCKKEY'), os.getenv('UBERDUCKSEC'))
voices = uberduck.get_voices(return_only_names=True)
voices_cleaned = [sub.replace('-', '_') for sub in voices]

# model config
model_name = 'microsoft/DialoGPT-large'
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)


def infer_response(voice, speech):
    if voice not in voices:
        print('Invalid voice')
        return None
    if '-' in voice:
        voice_validation = voice.replace('-','_')
    else:
        voice_validation = voice
    audio_path = os.path.join(temp_files_path, (voice_validation + ".wav"))
    result = client.speak(speech, voice, file_path=audio_path, play_sound=False)
    return result


def bot_response(voice, speech):
    try:
        sample = infer_response(voice, speech)
        return True
    except:
        return False



def get_model_response(input_message):
    if input_message:
        user_input_ids = tokenizer.encode(input_message + tokenizer.eos_token, return_tensors='pt')
        # generated a response by the model
        bot_output_ids = model.generate(user_input_ids, pad_token_id=tokenizer.eos_token_id)
        # decode previous message to text
        start_of_bot_message = user_input_ids.shape[-1]
        bot_message = tokenizer.decode(bot_output_ids[:, start_of_bot_message:][0], skip_special_tokens=True)
        return bot_message
    else:
        return ""


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
   
    parser.add_argument("-i", "--interpret", 
        help="will interpret text and return string")
    parser.add_argument("-s", "--setup", action='store_true',
        help="will download model and validate ai pipeline")

    args = parser.parse_args()


    if args.interpret:
        voice = "batman"
        user_message = args.interpret
        model_result = get_model_response(user_message)
        voice_update = bot_response(voice, model_result)
        print(model_result, voice_update) # prints the decoded message
    elif args.setup:
        print("setting up ai pipeline")
        voice = "batman"
        user_message = 'Are you batman?'
        print(user_message)
        model_result = get_model_response(user_message)
        print(model_result) # prints the decoded message


