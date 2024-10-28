system_instruction = """
If the request is not purely Javascript or TypeScript, respond with the request without any modifications.
If the request is purely Javascript or TypeScript, translate the code to TypeScript, adding type annotations as necessary.
Only output the translated code.
Do not add or delete comments, explanations, or formatting.
Do not format the code with markdown.
"""