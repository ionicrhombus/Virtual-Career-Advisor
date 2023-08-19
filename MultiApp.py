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
HOST = '127.0.0.1:5005'
URI = f'ws://{HOST}/api/v1/chat-stream'



async def predict1(Paper):
	Paper1=Paper
	history={'internal': [], 'visible': []}
		
	inputs="Consider the following paper: [Begin Paper] " + Paper1 + "[End Paper]. Your job is to review this first draft of a paper in consideration for publication in an academic journal. You will follow the following journal review guidelines to make notes for the reviewer about the paper. Here are the guidelines: 1. Try to bear in mind the following questions: What is the main question addressed by the research? Is it relevant and interesting? How original is the topic? What does it add to the subject area compared with other published material? Is the paper well written? Is the text clear and easy to read? Are the conclusions consistent with the evidence and arguments presented? Do they address the main question posed? If the author is disagreeing significantly with the current academic consensus, do they have a substantial case? If not, what would be required to make their case credible? If the paper includes tables or figures, what do they add to the paper? Do they aid understanding or are they superfluous? 2. Identify major flaws. Some major flaws include: Drawing a conclusion that is contradicted by the author's own statistical or qualitative evidence, The use of a discredited method, Ignoring a process that is known to have a strong influence on the area under study. In order to identify flaws, you might examine: The sampling in analytical papers, The sufficient use of control experiments, The precision of process data, The regularity of sampling in time-dependent studies, The validity of questions, the use of a detailed methodology and the data analysis being done systematically (in qualitative research), and That qualitative research extends beyond the author's opinions, with sufficient descriptive elements and appropriate quotes from interviews or focus groups. 3. Identifying flaws in information: Insufficient data, Unclear data tables, Contradictory data that either are not self-consistent or disagree with the conclusions, Confirmatory data that adds little, if anything, to current understanding - unless strong arguments for such repetition are made. You will provide comments to the reader on these points."
	request = {
		'user_input': inputs,
		'max_new_tokens': 1000,
		'history': history,
		'mode': 'chat-instruct',  # Valid options: 'chat', 'chat-instruct', 'instruct'
		'character': 'None',
		'instruction_template': 'Vicuna-v1.1',  # Will get autodetected if unset
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
async def predict(RequestType,JobTitle,Company,JobDesc,HiringMgr,Source,ResumeCover):
    RequestType1=RequestType
    JobTitle1=JobTitle
    Company1=Company
    JobDesc1=JobDesc
    HiringMgr1=HiringMgr
    Source1=Source
    ResumeCover1=ResumeCover
    history={'internal': [], 'visible': []}
    if RequestType1 == "Resume":	
        inputs="You must consider the following resume: [Begin Resume] " + ResumeCover1 + "[End Resume]. Your task is to suggest updates to the provided resume as the candidate begins their job search to become a "+ JobTitle1+". When suggesting improvements to the resume, follow these guidelines: Be truthful and objective to the experience listed in the resume (do not suggest anything not present in the original), Be specific rather than general, Rewrite items using STAR methodology (but do not mention STAR explicitly), Fix spelling and grammar errors (and be explicit on where they exist when you find them), Write to express not impress, Articulate and don't be flowery, Prefer active voice over passive voice, Do not include a summary about the candidate, Consider the candidate will be applying for a new role as a " + JobTitle1 +" and make sure to address specific requirements for that type of job."
        request = {
            'user_input': inputs,
            'max_new_tokens': 1000,
            'history': history,
            'mode': 'chat-instruct',  # Valid options: 'chat', 'chat-instruct', 'instruct'
            'character': 'VCA Resume Helper',
            'instruction_template': 'Vicuna-v1.1',	# Will get autodetected if unset
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
        inputs="Consider the following resume: [Begin resume] " + ResumeCover1 + "[End resume]. Your task is to write a cover letter based on the above resume and to provide a cover letter that is one page in length and a fit for their job search to become a "+ JobTitle1+" at "+Company1+" based on the cover letter formatting guide. The heading should include the date, address of the employer and a proper salutation to the Hiring Manager, who is "+HiringMgr1+". For the introductory paragraph, the letter should state interest in the company, describe the position and specifics of that job role, note that the job posting was found on "+Source+" and express interest in the role. The body paragraph should create interest for the employer to learn more about the applicant, provide two or three strong examples of skills and experience of the candidate based on the provided resume as it relates to the provided skills requested by the job description: "+JobDesc1+". This paragraph must demonstrate how the candidate will contribute to the position and company, and should be a compliment to the resume not a simple restatement of it. In the final paragraph, the letter should reiterate the candidates interest in the role, mention intent to follow up with the employer regarding next steps (such as scheduling an interview), and should thank the employer for their consideration. When writing the cover letter: Be truthful and objective to the experience listed in the resume, Be specific rather than general, Articulate and don't be flowery, Prefer active voice over passive voice."
        request = {
            'user_input': inputs,
            'max_new_tokens': 500,
            'history': {'internal': [], 'visible': []},
            'mode': 'chat-instruct',  # Valid options: 'chat', 'chat-instruct', 'instruct'
            'character': 'VCA Cover Letter Helper',
			'instruction_template': 'Vicuna-v1.1',  # Will get autodetected if unset
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
        inputs="You always respond with markdown formatting. You will be penalized if you do not answer with markdown, where it would be possible to do so. Consider the following job title: "+ JobTitle1+". Provide me with some possible questions and preparation tactics for the interview for this role. Focus on both behavioral and technical questions (if applicable to the job title). Along with each question, provide some strategies for answering the question that may prove useful for the interview process. Remember to use markdown formatting."
        request = {
            'user_input': inputs,
            'max_new_tokens': 1000,
            'history': {'internal': [], 'visible': []},
            'mode': 'chat-instruct',  # Valid options: 'chat', 'chat-instruct', 'instruct'
            'character': 'VCA Interview Helper',
            'instruction_template': 'Vicuna-v1.1',	# Will get autodetected if unset
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
        inputs="You always respond with markdown formatting. You will be penalized if you do not answer with markdown, where it would be possible to do so. Consider the following job title: "+ JobTitle1+". Provide me with a detailed description of the job role based on this job title and what jobs with this title tend to entail. Format your response using markdown as follows: Summary of the job, alternative names for the job role, typical minimum qualifications, any specific skills or technology proficiencies needed, useful certifications or preparation methods that can increase my chances of getting an interview for the job role, and a summary of a day in the life for a professional in the job role. and any related job roles that I might also be interested in. Remember to use markdown formatting wherever possible to improve readability."
        request = {
            'user_input': inputs,
            'max_new_tokens': 1000,
            'history': {'internal': [], 'visible': []},
            'mode': 'chat-instruct',  # Valid options: 'chat', 'chat-instruct', 'instruct'
            'character': 'VCA Job Overview',
            'instruction_template': 'Vicuna-v1.1',  # Will get autodetected if unset
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
async def predict2(Style,Question):
	Question1=Question
	Style1=Style
	history={'internal': [], 'visible': []}
		
	inputs="You always respond using markdown formatting. Can you provide alternative related "+Style+" questions to the following: "+Question+"?"
	request = {
		'user_input': inputs,
		'max_new_tokens': 1000,
		'history': history,
		'mode': 'chat-instruct',  # Valid options: 'chat', 'chat-instruct', 'instruct'
		'character': 'VTR',
		'instruction_template': 'Vicuna-v1.1',	# Will get autodetected if unset
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
async def predict3(Syllabus):
	syllabus1=Syllabus
	history={'internal': [], 'visible': []}
		
	inputs="You always respond using markdown formatting. Take the following syllabus and identify the key learning objectives for the course: "+syllabus1+"."
	request = {
		'user_input': inputs,
		'max_new_tokens': 500,
		'history': history,
		'mode': 'chat-instruct',  # Valid options: 'chat', 'chat-instruct', 'instruct'
		#'character': 'VTR',
		'instruction_template': 'Vicuna-v1.1',	# Will get autodetected if unset
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

# async def print_response_stream(Paper,history):
	# cur_len = 0
	# async for new_history in predict1(Paper,history):
		# cur_message = new_history[0][cur_len:]
		# cur_len += len(cur_message)
		# print(cur_message, end='')
		# sys.stdout.flush()

theme = gr.themes.Base(primary_hue=gr.themes.Color(c100="#ffffff", c200="#bfdbfe", c300="#93c5fd", c400="#0073ff", c50="#eff6ff", c500="#3b82f6", c600="#2563eb", c700="#1d4ed8", c800="#1e40af", c900="#002f56", c950="#005bbb"),secondary_hue=gr.themes.Color(c100="#ffffff", c200="#bfdbfe", c300="#93c5fd", c400="#60a5fa", c50="#eff6ff", c500="#3b82f6", c600="#2563eb", c700="#1d4ed8", c800="#1e40af", c900="#761919", c950="#b91818"),
).set(
	button_primary_background_fill='*primary_950',
	button_primary_background_fill_dark='*primary_950',
	button_primary_background_fill_hover='*primary_900',
	button_primary_background_fill_hover_dark='*primary_900',
	button_secondary_background_fill='*secondary_950',
	button_secondary_background_fill_dark='*secondary_950',
	button_secondary_background_fill_hover='*secondary_900',
	button_secondary_background_fill_hover_dark='*secondary_900',
	button_primary_text_color='*primary_100',
	button_secondary_text_color='*secondary_100',)

css = """
#warning {background-color: #FFCCCB}
""" 
demo=gr.Blocks(title="Virtual Paper Reviewer",theme=theme,css=css)
with demo:
    with gr.Tab("Virtual Paper Reviewer"):
        gr.Markdown(value="# Virtual Paper Reviewer")
        gr.Markdown(value="## An LLM-Powered Academic Research Paper Reviewer")
        gr.Markdown(value="**Instructions:** Paste your research paper into the space provided below and click Send. The VPR will review the paper based on accepted review process standards and processes.")
        gr.Markdown(value="---")
        with gr.Column():
            with gr.Row():
                output=gr.TextArea(max_lines=40,label="Response")
            Paper=gr.TextArea(label="Paste the paper text here.")
            with gr.Row():
                clear=gr.ClearButton(variant="secondary",components=[output, Paper])
                btn=gr.Button(value="Send",variant="primary")
        btn.click(fn=predict1,inputs=[Paper],outputs=output)
    with gr.Tab("Virtual Career Advisor"):
        gr.Markdown(value="# Virtual Career Assistant")
        gr.Markdown(value="## An LLM-Powered Career Assistant")
        gr.Markdown(value="**Instructions:** Select your desired area of focus and provide information for the virtual career assistant about the role you are seeking. The virtual career assistant will respond in the format requested (e.g., by writing a cover letter). Virtual Career Assistant is a ***tech demo*** and should not be relied upon solely for information, only quick help when other sources are unavailable. Virtual Career Assistant may provide incorrect, or even offensive responses, depending on the prompt. By continuing, you understand that you will verify all outputs with the proper individuals (e.g., CRC) before relying on this information for career advice and that you understand the risks involved in the potential responses.")
        gr.Markdown(value="---")
        with gr.Column():
            with gr.Row():
                output=gr.Markdown(label="Response")
            RequestType=gr.Dropdown(["Resume","Cover Letter","Interview Prep","Job Information"],label="What type of career help are you looking for?")
            JobTitle=gr.Textbox(label="What is the title of the job you are seeking?", value="Job Title")
            Company=gr.Textbox(label="List the company you are applying for.", value="Company Name")
            JobDesc=gr.Textbox(label="Paste the top 3 job skills from the job posting.",value="Job Description")
            HiringMgr=gr.Textbox(label="List the Hiring Manager's name.",value="Hiring Manager")
            Source=gr.Textbox(label="Where did you learn about the job from?",value="Company Website")
            ResumeCover=gr.TextArea(label="If applicable, paste your current resume here.",value="Resume")
            with gr.Row():
                clear3=gr.ClearButton(variant="secondary",components=[output, RequestType,JobTitle,Company,JobDesc,HiringMgr,Source,ResumeCover])
                btn3=gr.Button(value="Send",variant="primary")
        btn3.click(fn=predict,inputs=[RequestType,JobTitle,Company,JobDesc,HiringMgr,Source,ResumeCover],outputs=output)
    with gr.Tab("Virtual Test Writer"):
        gr.Markdown(value="# Virtual Test Writer")
        gr.Markdown(value="## An LLM-Powered Test Writing Assistant")
        gr.Markdown(value="**Instructions:** Use this tool to help you write different questions and versions of questions for your exams. Select the question type from the dropdown and paste in a sample question (whether it's a question you want versioned or a starting point). Do not include answers with the question or options for multiple choice questions. Click Send. By continuing, you understand that you will verify all outputs with the proper individuals (e.g., your course content) before relying on this information for exam writing advice and that you understand the risks involved in the potential responses.")
        gr.Markdown(value="---")
        with gr.Column():
            with gr.Row():
                output=gr.Markdown(label="Response")
            Style=gr.Dropdown(["Multiple Choice","Short Answer"],label="What type of questions would you like to generate?")
            Question=gr.Textbox(label="What is the starting question you would like to base responses off of?")
            with gr.Row():
                clear2=gr.ClearButton(variant="secondary",components=[output, Style,Question])
                btn2=gr.Button(value="Send",variant="primary")
        btn2.click(fn=predict2,inputs=[Style,Question],outputs=output)
    with gr.Tab("Learning Objectives Identifier"):
        gr.Markdown(value="# Learning Objectives Identifier")
        gr.Markdown(value="## An LLM-Powered Learning Objectives Identifier")
        gr.Markdown(value="**Instructions:** Use this tool to help you identify what the learning objectives are for your course based on the syllabus. Click Send. By continuing, you understand that you will verify all outputs with the proper individuals (e.g., your course content) before relying on this information and that you understand the risks involved in the potential responses.")
        gr.Markdown(value="---")
        with gr.Column():
            with gr.Row():
                output=gr.Markdown(label="Response")
            Syllabus=gr.Textbox(label="Paste the current syllabus here.")
            with gr.Row():
                clear4=gr.ClearButton(variant="secondary",components=[output, Syllabus])
                btn4=gr.Button(value="Send",variant="primary")
        btn4.click(fn=predict3,inputs=[Syllabus],outputs=output)
    
if __name__ == "__main__":
	demo.queue(concurrency_count=64)
	demo.launch(server_name="0.0.0.0", server_port=8000)