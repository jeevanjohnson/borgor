def string_to_key(s: str) -> str:
    """
    Makes a string into a valid key
    meant for things like 
    ```py
    self.__dict__[string_to_key(str)] = value
    ```
    """
    new_str = ''
    for i, char in enumerate(s):
        if i == 0:
            new_str += char.lower()
        elif char == 'I' and s[i+1] == 'D':
            new_str += '_i'
        elif char == 'D' and s[i-1] == 'I':
            new_str += 'd'
        elif char == 'H' and s[i+1] == 'P':
            new_str += '_h'
        elif char == 'P' and s[i-1] == 'H':
            new_str += 'p'
        elif char.isupper():
            new_str += f'_{char.lower()}'
        else:
            new_str += char
    
    return new_str

def isdecimal(s: str) -> bool:
    s = s.replace('.', '', 1)
    if '.' in s:
        return False
    
    return s.isdecimal()