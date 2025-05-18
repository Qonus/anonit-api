from presidio_analyzer import PatternRecognizer, Pattern, AnalyzerEngine
from presidio_analyzer.nlp_engine import NlpEngineProvider
from presidio_anonymizer import AnonymizerEngine, OperatorConfig
from langdetector import detect_lang

configuration = {"nlp_engine_name":"spacy", "models": [
    {"lang_code":'en', "model_name":"en_core_web_sm"},
    {"lang_code":'ru', "model_name":"ru_core_news_sm"}
]}
analyzer = AnalyzerEngine(
    nlp_engine=NlpEngineProvider(nlp_configuration=configuration).create_engine(), 
    supported_languages = ['en', 'ru']
)
analyzer.registry.add_recognizer(PatternRecognizer(
    supported_entity="IBAN",
    patterns=[Pattern(name="IBAN", regex=r"\b[A-Z]{2}[0-9]{2}[A-Z0-9]{11,30}\b", score=0.85)],
    supported_language='ru',
    context=['iban'],
))
analyzer.registry.add_recognizer(PatternRecognizer(
    supported_entity="IBAN",
    patterns=[Pattern(name="IBAN", regex=r"\b[A-Z]{2}[0-9]{2}[A-Z0-9]{11,30}\b", score=0.85)],
    supported_language='en',
    context=['iban'],
))
analyzer.registry.add_recognizer(PatternRecognizer(
    supported_entity="GENERIC_ID",
    patterns=[
        Pattern(name="long_number", regex=r"\b\d{8,20}\b", score=0.5),
        Pattern(name="snils_like", regex=r"\b\d{3}-\d{3}-\d{3} \d{2}\b", score=0.7),
        Pattern(name="card_like", regex=r"\b\d{4} \d{4} \d{4} \d{4}\b", score=0.6),
    ],
    supported_language='ru',
    context=["id", "номер"],
))
analyzer.registry.add_recognizer(PatternRecognizer(
    supported_entity="GENERIC_ID",
    patterns=[
        Pattern(name="long_number", regex=r"\b\d{8,20}\b", score=0.5),
        Pattern(name="alphanum_id", regex=r"\b[A-Z]{2}[A-Z0-9]{6,30}\b", score=0.5),
        Pattern(name="snils_like", regex=r"\b\d{3}-\d{3}-\d{3} \d{2}\b", score=0.7),
        Pattern(name="card_like", regex=r"\b\d{4} \d{4} \d{4} \d{4}\b", score=0.6),
    ],
    supported_language='en',
    context=["id"],
))

anonymizer = AnonymizerEngine()

def analyze_text(text: str):
    lang = 'en' if detect_lang(text) == 'en' else 'ru'
    print(lang)
    
    return analyzer.analyze(text=text, language=lang)

def anonymize_text(text: str):
    results = analyze_text(text)
    
    operators = {}
    for res in results:
        if res.entity_type not in operators:
            operators[res.entity_type] = OperatorConfig(
                "replace", {"new_value": f"<{res.entity_type}>"})

    anonymized_result = anonymizer.anonymize(
        text=text, analyzer_results=results, operators=operators
    )
    return anonymized_result.text

def main():
    text = input('enter your text: ')
    print(anonymize_text(text))

if (__name__ == "__main__"):
    main()