from rest_framework_simplejwt import serializers

FORBIDDEN_WORDS = [
    'дурак',
    'криптовалюта',
    'биткоин',
    'наркотики',
    'убийство',
]


class ForbiddenWordsValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, attrs):
        value = attrs.get(self.field)
        if value and any(word in value for word in FORBIDDEN_WORDS):
            raise serializers.ValidationError(f'Недопустимые слова в {self.field}')


class YoutubeUrlValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, attrs):
        url = attrs.get(self.field)
        if url and not url.startswith('https://www.youtube.com/watch?v='):
            raise serializers.ValidationError('Недопустимая ссылка на видео')
