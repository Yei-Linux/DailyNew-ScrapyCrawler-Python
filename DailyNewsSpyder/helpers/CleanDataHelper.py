import re

class CleanDataHelper():
    @staticmethod
    def deleteMultipleWhiteSpaces(text):
        return re.sub('\s+', ' ', text).strip()

    @staticmethod
    def deleteIndexWikipedia(text):
        return re.sub(r'\[.*\]', '', text)

    @staticmethod
    def replaceStrangeCharacteres(text,currentValue,valueToReplace):
        return text.replace(currentValue,valueToReplace)
