# Introduction


# Installation
install the package 
```bash
pip install py-wininput
```


# Examples
## Send text
```python
import wininput.keyboard as kb
kb.send_text("hello world")
kb.send_text("안녕하세요 세계")
```

The above program produces the following output
```bash
hello world
안녕하세요 세계
```

## Send the virtual key

```python
import wininput.keyboard as kb
import wininput.common as common
kb.send_virtual_key(common.VK_A) # Send the 'a' chacter
kb.send_virtual_key(common.VK_RETURN) # Send the return character
```
The above program produces the following output
```bash 
a
<ENTER>
```


