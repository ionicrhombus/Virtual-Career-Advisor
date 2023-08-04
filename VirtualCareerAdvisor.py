import gradio as gr
import random
import time
import json
import requests
import asyncio
import sys

try:
	import websockets
except ImportError:
	print("Websockets package not found. Make sure it's installed.")

# For local streaming, the websockets are hosted without ssl - ws://
HOST = '192.168.68.93:5005'
URI = f'ws://{HOST}/api/v1/chat-stream'



async def predict(RequestType,JobTitle,ResumeCover):
	RequestType1=RequestType
	JobTitle1=JobTitle
	ResumeCover1=ResumeCover
	history={'internal': [], 'visible': []}
	if RequestType1 == "Resume":	
		inputs="Consider the following resume: [Begin Resume] " + ResumeCover1 + "[End Resume]. Your task is to rewrite the above resume and to suggest improvements as the candidate begins their job search to become a "+ JobTitle1+". When suggesting improvements to the resume, follow these guidelines: Be truthful and objective to the experience listed in the resume, Be specific rather than general, Rewrite items using STAR methodology (but do not mention STAR explicitly), Fix spelling and grammar errors (and be explicit on where they exist when you find them), Write to express not impress, Articulate and don't be flowery, Prefer active voice over passive voice, Do not include a summary about the candidate, Consider the candidate will be applying for a new role as a " + JobTitle1 +" and make sure to address specific requirements for that type of job."
		request = {
			'user_input': inputs,
			'max_new_tokens': 1000,
			'history': history,
			'mode': 'chat-instruct',  # Valid options: 'chat', 'chat-instruct', 'instruct'
			'character': 'VCA Resume Helper',
			'instruction_template': 'Llama-v2',  # Will get autodetected if unset
			# 'context_instruct': '',  # Optional
			'your_name': 'You',

			'regenerate': False,
			'_continue': False,
			'stop_at_newline': False,
			'chat_generation_attempts': 1,
			'chat-instruct_command': 'Continue the chat dialogue below. Write a single reply for the character "<|character|>".\n\n<|prompt|>',

			# Generation params. If 'preset' is set to different than 'None', the values
			# in presets/preset-name.yaml are used instead of the individual numbers.
			'preset': 'None',
			'do_sample': True,
			'temperature': 0.7,
			'top_p': 0.1,
			'typical_p': 1,
			'epsilon_cutoff': 0,  # In units of 1e-4
			'eta_cutoff': 0,  # In units of 1e-4
			'tfs': 1,
			'top_a': 0,
			'repetition_penalty': 1.18,
			'repetition_penalty_range': 0,
			'top_k': 40,
			'min_length': 0,
			'no_repeat_ngram_size': 0,
			'num_beams': 1,
			'penalty_alpha': 0,
			'length_penalty': 1,
			'early_stopping': False,
			'mirostat_mode': 0,
			'mirostat_tau': 5,
			'mirostat_eta': 0.1,

			'seed': -1,
			'add_bos_token': True,
			'truncation_length': 2048,
			'ban_eos_token': False,
			'skip_special_tokens': True,
			'stopping_strings': []
		}
	elif RequestType1== "Cover Letter":	
		inputs="Consider the following resume: [Begin resume] " + ResumeCover1 + "[End resume letter]. Your task is to write a cover letter based on the above resume and to provide a cover letter that is one page in length and a fit for their job search to become a "+ JobTitle1+". The cover letter should start with an address to the contact person. If no contact person is known, use a Dear Hiring Manager Format. After these, the cover letter should have an introductory paragraph establishing rapport and stating the applicants purpose, including the position and where the applicant learned of it. This paragraph should never directly say the word resume. The introductory paragraph should also grab the readers attention by mentioning relevant skills from the resume in a positive manner. After the introduction, the body paragraph should reference the skills demonstrated in the above resume and highlight only the most relevant qualifications, emphasizing how the applicant can make a contribution, focusing on the reader without starting every sentence with the word I. Finally, a closing paragraph should be written to reaffirm interest and request an interview. When writing the cover letter: Be truthful and objective to the experience listed in the resume, Be specific rather than general, Articulate and don't be flowery, Prefer active voice over passive voice, and Consider the candidate will be applying for a new role as a " + JobTitle1 +" and make sure to address specific requirements for that job title."
		request = {
			'user_input': inputs,
			'max_new_tokens': 1000,
			'history': {'internal': [], 'visible': []},
			'mode': 'chat-instruct',  # Valid options: 'chat', 'chat-instruct', 'instruct'
			'character': 'VCA Cover Letter Helper',
			'instruction_template': 'Llama-v2',  # Will get autodetected if unset
			# 'context_instruct': '',  # Optional
			'your_name': 'You',

			'regenerate': False,
			'_continue': False,
			'stop_at_newline': False,
			'chat_generation_attempts': 1,
			'chat-instruct_command': 'Continue the chat dialogue below. Write a single reply for the character "<|character|>".\n\n<|prompt|>',

			# Generation params. If 'preset' is set to different than 'None', the values
			# in presets/preset-name.yaml are used instead of the individual numbers.
			'preset': 'None',
			'do_sample': True,
			'temperature': 0.7,
			'top_p': 0.1,
			'typical_p': 1,
			'epsilon_cutoff': 0,  # In units of 1e-4
			'eta_cutoff': 0,  # In units of 1e-4
			'tfs': 1,
			'top_a': 0,
			'repetition_penalty': 1.18,
			'repetition_penalty_range': 0,
			'top_k': 40,
			'min_length': 0,
			'no_repeat_ngram_size': 0,
			'num_beams': 1,
			'penalty_alpha': 0,
			'length_penalty': 1,
			'early_stopping': False,
			'mirostat_mode': 0,
			'mirostat_tau': 5,
			'mirostat_eta': 0.1,

			'seed': -1,
			'add_bos_token': True,
			'truncation_length': 2048,
			'ban_eos_token': False,
			'skip_special_tokens': True,
			'stopping_strings': []
		}
	elif RequestType1== "Interview Prep":	
		inputs="Consider the following job title: "+ JobTitle1+". Provide me with some possible questions and preparation tactics for the interview for this role. Focus on both behavioral and technical questions (if applicable to the job title). Along with each question, provide some strategies for answering the question that may prove useful for the interview process."
		request = {
			'user_input': inputs,
			'max_new_tokens': 1000,
			'history': {'internal': [], 'visible': []},
			'mode': 'chat-instruct',  # Valid options: 'chat', 'chat-instruct', 'instruct'
			'character': 'VCA Interview Helper',
			'instruction_template': 'Llama-v2',  # Will get autodetected if unset
			# 'context_instruct': '',  # Optional
			'your_name': 'You',

			'regenerate': False,
			'_continue': False,
			'stop_at_newline': False,
			'chat_generation_attempts': 1,
			'chat-instruct_command': 'Continue the chat dialogue below. Write a single reply for the character "<|character|>".\n\n<|prompt|>',

			# Generation params. If 'preset' is set to different than 'None', the values
			# in presets/preset-name.yaml are used instead of the individual numbers.
			'preset': 'None',
			'do_sample': True,
			'temperature': 0.7,
			'top_p': 0.1,
			'typical_p': 1,
			'epsilon_cutoff': 0,  # In units of 1e-4
			'eta_cutoff': 0,  # In units of 1e-4
			'tfs': 1,
			'top_a': 0,
			'repetition_penalty': 1.18,
			'repetition_penalty_range': 0,
			'top_k': 40,
			'min_length': 0,
			'no_repeat_ngram_size': 0,
			'num_beams': 1,
			'penalty_alpha': 0,
			'length_penalty': 1,
			'early_stopping': False,
			'mirostat_mode': 0,
			'mirostat_tau': 5,
			'mirostat_eta': 0.1,

			'seed': -1,
			'add_bos_token': True,
			'truncation_length': 2048,
			'ban_eos_token': False,
			'skip_special_tokens': True,
			'stopping_strings': []
		}
	elif RequestType1== "Job Information":	
		inputs="Consider the following job title: "+ JobTitle1+". Provide me with a detailed description of the job role based on this job title and what jobs with this title tend to entail. Format your response as follows: Summary of the job, alternative names for the job role, typical minimum qualifications, any specific skills or technology proficiencies needed, useful certifications or preparation methods that can increase my chances of getting an interview for the job role, and a summary of a day in the life for a professional in the job role. and any related job roles that I might also be interested in."
		request = {
			'user_input': inputs,
			'max_new_tokens': 1000,
			'history': {'internal': [], 'visible': []},
			'mode': 'chat-instruct',  # Valid options: 'chat', 'chat-instruct', 'instruct'
			'character': 'VCA Job Overview',
			'instruction_template': 'Llama-v2',  # Will get autodetected if unset
			# 'context_instruct': '',  # Optional
			'your_name': 'You',

			'regenerate': False,
			'_continue': False,
			'stop_at_newline': False,
			'chat_generation_attempts': 1,
			'chat-instruct_command': 'Continue the chat dialogue below. Write a single reply for the character "<|character|>".\n\n<|prompt|>',

			# Generation params. If 'preset' is set to different than 'None', the values
			# in presets/preset-name.yaml are used instead of the individual numbers.
			'preset': 'None',
			'do_sample': True,
			'temperature': 0.7,
			'top_p': 0.1,
			'typical_p': 1,
			'epsilon_cutoff': 0,  # In units of 1e-4
			'eta_cutoff': 0,  # In units of 1e-4
			'tfs': 1,
			'top_a': 0,
			'repetition_penalty': 1.18,
			'repetition_penalty_range': 0,
			'top_k': 40,
			'min_length': 0,
			'no_repeat_ngram_size': 0,
			'num_beams': 1,
			'penalty_alpha': 0,
			'length_penalty': 1,
			'early_stopping': False,
			'mirostat_mode': 0,
			'mirostat_tau': 5,
			'mirostat_eta': 0.1,

			'seed': -1,
			'add_bos_token': True,
			'truncation_length': 2048,
			'ban_eos_token': False,
			'skip_special_tokens': True,
			'stopping_strings': []
		}
	#response = requests.post(URI, json=request)

	async with websockets.connect(URI, ping_interval=None) as websocket:
		await websocket.send(json.dumps(request))

		while True:
			incoming_data = await websocket.recv()
			incoming_data = json.loads(incoming_data)

			match incoming_data['event']:
				case 'text_stream':
					cur_message=incoming_data['history']['visible'][-1][1]
					yield cur_message
				case 'stream_end':
					return
async def print_response_stream(RequestType,JobTitle,ResumeCover,history):
	cur_len = 0
	async for new_history in predict(RequestType,JobTitle,ResumeCover,history):
		cur_message = new_history[0][cur_len:]
		cur_len += len(cur_message)
		print(cur_message, end='')
		sys.stdout.flush()

theme = gr.themes.Base(primary_hue=gr.themes.Color(c100="#dbeafe", c200="#bfdbfe", c300="#93c5fd", c400="#0073ff", c50="#eff6ff", c500="#3b82f6", c600="#2563eb", c700="#1d4ed8", c800="#1e40af", c900="#002f56", c950="#005bbb"),secondary_hue=gr.themes.Color(c100="#dbeafe", c200="#bfdbfe", c300="#93c5fd", c400="#60a5fa", c50="#eff6ff", c500="#3b82f6", c600="#2563eb", c700="#1d4ed8", c800="#1e40af", c900="#761919", c950="#b91818"),
).set(
	button_primary_background_fill='*primary_950',
	button_primary_background_fill_dark='*primary_950',
	button_primary_background_fill_hover='*primary_900',
	button_primary_background_fill_hover_dark='*primary_900',
	button_secondary_background_fill='*secondary_950',
	button_secondary_background_fill_dark='*secondary_950',
	button_secondary_background_fill_hover='*secondary_900',
	button_secondary_background_fill_hover_dark='*secondary_900',)

   
demo=gr.Blocks(title="Virtual Career Assistant",theme=theme)
with demo:
	gr.Markdown(value="# Virtual Career Assistant")
	gr.Markdown(value="## An LLM-Powered Career Assistant")
	gr.Markdown(value="**Instructions:** Select your desired area of focus and provide information for the virtual career assistant about the role you are seeking. The virtual career assistant will respond in the format requested (e.g., by writing a cover letter). Virtual Career Assistant is a ***tech demo*** and should not be relied upon solely for information, only quick help when other sources are unavailable. Virtual Career Assistant may provide incorrect, or even offensive responses, depending on the prompt. By continuing, you understand that you will verify all outputs with the proper individuals (e.g., CRC) before relying on this information for career advice and that you understand the risks involved in the potential responses.")
	gr.Markdown(value="---")
	with gr.Column():
		with gr.Row():
			output=gr.TextArea(max_lines=40,label="Response")
		RequestType=gr.Dropdown(["Resume","Cover Letter","Interview Prep","Job Information"],label="What type of career help are you looking for?")
		JobTitle=gr.Textbox(label="What is the title of the job you are seeking?")
		ResumeCover=gr.TextArea(label="If applicable, paste your current resume here.")
		with gr.Row():
			clear=gr.ClearButton(variant="secondary",components=[output, RequestType,JobTitle,ResumeCover])
			btn=gr.Button(value="Send",variant="primary")
	btn.click(fn=predict,inputs=[RequestType,JobTitle,ResumeCover],outputs=output)
   
if __name__ == "__main__":
	demo.queue()
	demo.launch()