import re

class CleanDataHelper():
    @staticmethod
    def deleteMultipleWhiteSpaces(text):
        return re.sub('\s+', ' ', text).strip()