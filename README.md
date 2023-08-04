# Virtual-Career-Advisor
## An LLM-Powered Career Assistant
Instructions:** Select your desired area of focus and provide information for the virtual career assistant about the role you are seeking. The virtual career assistant will respond in the format requested (e.g., by writing a cover letter). Virtual Career Assistant is a ***tech demo*** and should not be relied upon solely for information, only quick help when other sources are unavailable. Virtual Career Assistant may provide incorrect, or even offensive responses, depending on the prompt. By continuing, you understand that you will verify all outputs with the proper individuals (e.g., CRC) before relying on this information for career advice and that you understand the risks involved in the potential responses.

**Setting up:**
1. (Recommended) Created a new virtual Python environment
2. Download the `VirtualCareerAdvisor.py` file to your base directory
3. Download the back-end server, which can be found here: https://github.com/oobabooga/text-generation-webui
4. Run the back-end server in API mode
5. Download a viable model and follow the back-end server github instructions to load it (recommended model: https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGML)
6. Update `VirtualCareerAdvisor.py` to reference the server address as host (e.g., localhost:5005)
7. Run `pip install gradio` , `pip install requests`, and `pip install asyncio`
8. Run the `VirtualCareerAdvisor.py` file and open the web browser
