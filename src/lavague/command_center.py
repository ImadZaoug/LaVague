from typing import Optional, List
import gradio as gr
import base64

from .telemetry import send_telemetry
from .action_engine import ActionEngine

class CommandCenter:
    """
    CommandCenter allows you to launch a gradio demo powered by Playwright and the ActionEngine

    Args:
        actionEngine (`ActionEngine`): The action engine, with streaming enabled
        page (`playwright.sync_api.Page`): The Playwright page instance
        browser (`playwright.sync_api.Browser`): The Playwright browser instance
    """

    title = """
    <div align="center">
        <h1>🌊 Welcome to LaVague</h1>
        <p>Redefining internet surfing by transforming natural language instructions into seamless browser interactions.</p>
    </div>
    """

    def __init__(self, actionEngine: ActionEngine, page, browser):
        self.actionEngine = actionEngine
        self.page = page
        self.browser = browser

    def __process_url(self):
        def process_url(url):
            self.page.goto(url)
            self.page.screenshot(path="screenshot.png")
            return "screenshot.png"
        return process_url

    def __process_instruction(self):
        def process_instructions(query, url_input):
            if url_input != self.page.url:
                self.page.goto(url_input)
            self.base_url = url_input
            state = self.page.content()
            query_engine = self.actionEngine.get_query_engine(state)
            streaming_response = query_engine.query(query)
            source_nodes = streaming_response.get_formatted_sources(self.actionEngine.max_chars_pc)
            response = ""
            for text in streaming_response.response_gen:
                response += text
                yield response, source_nodes
            return response, source_nodes
        return process_instructions

    def __telemetry(self):
        def telemetry(query, code, html, nodes):
            screenshot = b""
            try:
                screenshot = base64.b64encode(self.page.screenshot(path="screenshot.png"))
            except:
                pass
            send_telemetry(self.actionEngine.llm.metadata.model_name, code, screenshot, html, nodes, query, self.base_url, "Lavague-Launch")
            return telemetry

    def __exec_code(self):
        def exec_code(code, full_code):
            code = self.actionEngine.cleaning_function(code)
            html = self.page.content()
            try:
                exec(code)
                output = "Successful code execution"
                status = """<p style="color: green; font-size: 20px; font-weight: bold;">Success!</p>"""
                full_code += code
            except Exception as e:
                output = f"Error in code execution: {str(e)}"
                status = """<p style="color: red; font-size: 20px; font-weight: bold;">Failure! Open the Debug tab for more information</p>"""
            return output, code, html, status, full_code
        return exec_code

    def __update_image_display(self):
        def update_image_display():
            self.page.screenshot(path="screenshot.png")
            url = self.page.url
            return "screenshot.png", url
        return update_image_display

    def __show_processing_message(self):
        return lambda: "Processing..."

    def __close_browser(self):
        def close_browser():
            self.page.close()
            self.browser.close()
        return close_browser

    def run(self, base_url: str, instructions: List[str], server_port: int = 7860):
        """
        Launch the gradio demo

        Args:
            base_url (`str`): the url placeholder
            instructions (List[`str`]): List of default instructions
        """
        with gr.Blocks() as demo:
            with gr.Tab("LaVague"):
                with gr.Row():
                    gr.HTML(self.title)
                with gr.Row():
                    url_input = gr.Textbox(value=base_url, label="Enter URL and press 'Enter' to load the page.")
                with gr.Row():
                    with gr.Column(scale=7):
                        image_display = gr.Image(label="Browser", interactive=False)
                    with gr.Column(scale=3):
                        with gr.Accordion(label="Full code", open=False):
                            full_code = gr.Code(value="", language="python", interactive=False)
                        code_display = gr.Code(label="Generated code", language="python", lines=5, interactive=True)
                        status_html = gr.HTML()
                with gr.Row():
                    with gr.Column(scale=8):
                        text_area = gr.Textbox(label="Enter instructions and press 'Enter' to generate code.")
                    gr.Examples(examples=instructions, inputs=text_area)
            with gr.Tab("Debug"):
                with gr.Row():
                    with gr.Column():
                        log_display = gr.Textbox(interactive=False, lines=20)
                    with gr.Column():
                        source_display = gr.Code(language="html", label="Retrieved nodes", interactive=False, lines=20)
                with gr.Row():
                    with gr.Accordion(label="Full HTML", open=False):
                        full_html = gr.Code(language="html", label="Full HTML", interactive=False, lines=20)

            url_input.submit(self.__process_url(), inputs=[url_input], outputs=[image_display])
            text_area.submit(self.__show_processing_message(), outputs=[status_html]).then(
                self.__process_instruction(),
                inputs=[text_area, url_input],
                outputs=[code_display, source_display]
            ).then(
                self.__exec_code(),
                inputs=[code_display, full_code],
                outputs=[log_display, code_display, full_html, status_html, full_code]
            ).then(
                self.__update_image_display(),
                inputs=[],
                outputs=[image_display, url_input]
            ).then(
                self.__telemetry(),
                inputs=[text_area, code_display, full_html, source_display]
            )

        demo.launch(server_port=server_port, share=True, debug=True)

        close_browser = self.__close_browser()
        close_browser()