from rich.console import Console
from rich.markdown import Markdown

console = Console()

markdown_text = """
# Lorem Ipsum Dolor

**Sed do eiusmod tempor** incididunt ut labore et dolore magna aliqua. *Ut enim ad minim veniam*, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.

## Duis Aute Irure

Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.

### Curabitur Pretium

| Item | Status | Value | Notes |
| :--- | :---: | ---: | :--- |
| Alpha | Normal | 100 | N/A |
| Beta | Warn | 42 | Hello |
| Gamma | Error | 0 | Yee |
| Delta | Idle | 77 | Ashita |

A usefule [Link](./nothing)

```python
import random

def generate_lorem_ipsum(word_count=10):
    words = ["lorem", "ipsum", "dolor", "sit", "amet", "consectetur", "adipiscing", "elit"]
    sentence = []
    
    for _ in range(word_count):
        word = random.choice(words)
        sentence.append(word)
        
    return " ".join(sentence).capitalize() + "."

print(generate_lorem_ipsum(15))
```
"""

md = Markdown(markdown_text)

console.print(md)
