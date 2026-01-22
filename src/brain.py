from llama_cpp import Llama # type: ignore

class DustinBrain:
    def __init__(self, model_path, system_prompt, context_size=2048):
        self.llm = Llama(
            model_path=model_path,
            n_ctx=context_size,
            n_gpu_layers=-1, 
            verbose=False
        )
        self.system_prompt = system_prompt

    def generate_response(self, chat_history):
        messages = [{"role": "system", "content": self.system_prompt}]
        messages.extend(chat_history)

        # FIX: Convert the list of dictionaries to a list of ChatCompletionRequestMessage
        chat_completion_messages = []
        for message in messages:
            chat_completion_message = {
                "role": message["role"],
                "content": message["content"]
            }
            chat_completion_messages.append(chat_completion_message)

        return self.llm.create_chat_completion(
            messages=chat_completion_messages,
            stream=True,
            temperature=0.7,
            max_tokens=1024
        )