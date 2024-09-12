import anthropic
import json
from system_prompt import get_system_prompt

class LearningChatbot:
    def __init__(self):
        self.client = anthropic.Anthropic()
        self.conversation_history = []
        self.learning_material = None

    def extract_progress(self, response):
        try:
            json_start = response.rfind('{"progress":')
            json_end = response.rfind('}') + 1
            json_str = response[json_start:json_end]
            progress_data = json.loads(json_str)
            return progress_data['progress']
        except:
            return None

    def update_progress_bar(self, progress_data):
        if progress_data:
            topic = progress_data['topic']
            percentage = progress_data['percentage']
            print(f"Progress in {topic}: {percentage}%")

    def parse_ai_response(self, ai_response):
        if isinstance(ai_response, list) and all(hasattr(block, 'text') for block in ai_response):
            ai_response = ' '.join(block.text for block in ai_response)
        
        while '{"progress":' in ai_response:
            start = ai_response.find('{"progress":')
            end = ai_response.find('}', start) + 1
            ai_response = ai_response[:start] + ai_response[end:]
        return ai_response

    def stream_ai_response(self, emit_response):
        full_response = ""
        system_prompt = get_system_prompt(self.learning_material)

        with self.client.messages.stream(
            model="claude-3-sonnet-20240229",
            max_tokens=4000,
            temperature=0.7,
            system=system_prompt,
            messages=self.conversation_history
        ) as stream:
            for text in stream.text_stream:
                emit_response(text)
                full_response += text

        return full_response

    def start_conversation(self, learning_material, emit_response):
        self.set_learning_material(learning_material)
        initial_user_message = {"role": "user", "content": f"Here's the learning material: {learning_material}\n\nLet's start our learning session. What's the first thing we should know about this topic?"}
        self.conversation_history = [initial_user_message]

        ai_response = self.stream_ai_response(emit_response)
        parsed_initial_response = self.parse_ai_response(ai_response)
        self.conversation_history.append({"role": "assistant", "content": ai_response})

        return {"response": parsed_initial_response, "conversation_history": self.conversation_history}

    def handle_user_message(self, user_input, conversation_history, learning_material, emit_response, emit_progress):
        self.learning_material = learning_material
        self.conversation_history = conversation_history

        # Add the new user message
        self.conversation_history.append({"role": "user", "content": user_input})

        # Ensure we keep the first user message and the most recent messages
        if len(self.conversation_history) > 10:  # Adjust this number as needed
            first_user_message = next((msg for msg in self.conversation_history if msg["role"] == "user"), None)
            self.conversation_history = [first_user_message] + self.conversation_history[-9:]

        ai_response = self.stream_ai_response(emit_response)
        ai_response_without_json = self.parse_ai_response(ai_response)

        self.conversation_history.append({"role": "assistant", "content": ai_response})

        # Add a progress check after each user interaction
        progress_response = self.get_progress()
        progress_data = self.extract_progress(progress_response)
        if progress_data:
            emit_progress(progress_data)

        return {
            "response": ai_response_without_json,
            "conversation_history": self.conversation_history
        }

    def run(self):
        self.start_conversation()

        while True:
            user_input = input("You: ")
            if user_input.lower() in ['exit', 'quit', 'bye']:
                break

            self.conversation_history.append({"role": "user", "content": user_input})

            ai_response = self.stream_ai_response()
            ai_response_without_json = self.parse_ai_response(ai_response)

            self.conversation_history.append({"role": "assistant", "content": ai_response})

            progress_data = self.extract_progress(ai_response)
            if progress_data:
                self.update_progress_bar(progress_data)

            if len(self.conversation_history) > 15:
                self.conversation_history = self.conversation_history[-15:]

        print("Conversation ended.")

    def set_learning_material(self, learning_material):
        self.learning_material = learning_material

    def get_progress(self):
        progress_query = {"role": "user", "content": "What's my current progress? Your response must end with a single newline character followed by a JSON object in this exact format:{\"progress\": {\"topic\": \"<topic name>\", \"percentage\": <number between 0 and 100>}}"}
        temp_conversation = self.conversation_history + [progress_query]
        
        progress_response = self.client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=100,
            messages=temp_conversation
        )

        print(progress_response.content[0].text)
        return progress_response.content[0].text

if __name__ == "__main__":
    chatbot = LearningChatbot()
    chatbot.run()

