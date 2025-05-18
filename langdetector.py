from langdetect import detect

def detect_lang(text: str):
    try:
        return detect(text) 
    except:
        return 'en'

if __name__ == "__main__":
    text = input('Enter your text: ')
    print(detect_lang(text))