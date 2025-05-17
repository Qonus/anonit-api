from presidio_analyzer import AnalyzerEngine
from presidio_analyzer.nlp_engine import NlpEngineProvider
from presidio_anonymizer import AnonymizerEngine, OperatorConfig
from langdetector import detect_lang

configuration = {"nlp_engine_name":"spacy", "models":[{"lang_code":'ru', "model_name":"ru_core_news_sm"}]}
ru_nlp = AnalyzerEngine(
    nlp_engine=NlpEngineProvider(nlp_configuration=configuration).create_engine(), 
    supported_languages = ['ru']
)

configuration = {"nlp_engine_name":"spacy", "models":[{"lang_code":'en', "model_name":"en_core_web_sm"}]}
en_nlp = AnalyzerEngine(
    nlp_engine=NlpEngineProvider(nlp_configuration=configuration).create_engine(), 
    supported_languages = ['en']
)

anonymizer = AnonymizerEngine()

def anonymize(text: str):
    lang = 'en' if detect_lang(text) == 'en' else 'ru'
    print(lang)
    
    results = (en_nlp if lang == 'en' else ru_nlp).analyze(text=text, language=lang)
    
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
    print(anonymize(text))

if (__name__ == "__main__"):
    main()