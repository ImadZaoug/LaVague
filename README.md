# LaVague: Integrating Playwright and Gemini LLM

This README file outlines the changes made to the LaVague project to integrate the Playwright web automation library and add support for the Gemini LLM API alongside the existing APIs.

## Playwright Integration

To enable web automation using Playwright instead of Selenium, the following changes were made to the LaVague codebase:

### `defaults.py`

- Added a new function `default_get_playwright_driver()` to launch a Playwright browser instance and create a new context and page.

### `utils.py`

- Updated the `load_action_engine()` function to accept a `get_driver` argument, which can be used to pass the `default_get_playwright_driver` function or any other custom driver initialization function.

### `command_center.py`

- Modified the `CommandCenter` class to accept the Playwright `page` and `browser` instances instead of the Selenium `driver`.
- Updated the `__process_url()` and `__process_instruction()` methods to use the Playwright `page` instance for navigation and content retrieval.
- Added a new `__close_browser()` method to close the Playwright `page` and `browser` instances.
- Updated the `__telemetry()` method to capture screenshots using the Playwright `page` instance.
- Modified the `run()` method to create the Gradio components and connect them to the respective methods using the Playwright instances.

### `__init__.py`

- Updated the `build()` and `launch()` functions to use the `default_get_playwright_driver` function and handle the Playwright `page` and `browser` instances returned by `load_action_engine()`.
- Removed the code that extracted import statements from the Selenium driver initialization function, as it is no longer needed with Playwright.

### `main.py`

- Removed the code related to Selenium driver initialization and handling, as it is no longer needed with Playwright.

## Gemini LLM Integration

To add support for the Gemini LLM API alongside the existing APIs, a new file `gemini.py` was created in the folder containing the API codes:

```python
import os
from llama_index.llms.gemini import Gemini

class LLM(Gemini):
    def __init__(self):
        max_new_tokens = 512
        api_key = os.getenv("GOOGLE_API_KEY")
        if api_key is None:
            raise ValueError("GOOGLE_API_KEY environment variable is not set")
        else:
            super().__init__(api_key=api_key, max_tokens=max_new_tokens, temperature=0.0)
```

This file defines a class `LLM` that inherits from the `Gemini` class provided by the `llama_index` library. The `__init__` method initializes the Gemini LLM with the specified API key and configuration settings.

To use the Gemini LLM in the LaVague project, you can update the `defaults.py` file to import the `LLM` class from `gemini.py` and use it as the default LLM or provide an option to select the desired LLM during runtime.


## Gemini LLM Integration

Please note that you will need to set the `GOOGLE_API_KEY` environment variable with a valid API key to use the Gemini LLM. Additionally, ensure that the `llama_index` library is installed and up-to-date.

## Test


The file "quick_tour_using_playwright.ipynb" is intended for testing with the Playwright library, but the Docker container is not yet prepared.
