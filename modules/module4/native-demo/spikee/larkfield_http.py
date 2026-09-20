"""Minimal Spikee 0.9.1 connector: input JSON -> output text + event evidence."""
import requests
from spikee.templates.target import Target


class LarkfieldHTTP(Target):
    def get_description(self):
        return [], "Larkfield /chat: input in, output out"

    def get_available_option_values(self):
        return ["http://localhost:8089/chat"], False

    def process_input(self, input_text: str, system_message=None, target_options=None):
        response = requests.post(
            target_options or "http://localhost:8089/chat",
            json={"input": input_text}, timeout=120,
        )
        response.raise_for_status()
        data = response.json()
        return data["output"], {"events": data.get("events")}
