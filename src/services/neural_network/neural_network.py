from abc import ABC, abstractmethod

import aiohttp

from django.conf import settings


class NeualNetworkABC(ABC):
    """Абстрактный класс нейросети.

    Attributes:
        token (str): токен.
        url (str): url к API.
        system_prompt (str): описание ответов нейросети.
        temperature (float): коэффициент.
        max_tokens (int | None): максимальная длина ответа. По дефолту None.
    """

    token: str
    url: str
    system_prompt: str
    temperature: float
    max_tokens: int | None = None

    @classmethod
    @abstractmethod
    async def send(cls, message: str) -> str:
        """Запрос к нейросети.

        Args:
            message (str): сообщение к нейросети.

        Returns:
            str: ответ нейросети.
        """


class DeepSeekNeualNetworkBase(NeualNetworkABC):
    """Базовый класс нейросети DeepSeek."""

    @classmethod
    async def send(cls, message: str) -> str:
        """Запрос к нейросети.

        Args:
            message (str): сообщение к нейросети.

        Returns:
            str: ответ нейросети.
        """
        headers = {'Content-Type': 'application/json', 'Authorization': cls.token}
        payload = {
            'model': 'deepseek-chat',
            'messages': [{'role': 'system', 'content': cls.system_prompt}, {'role': 'user', 'content': message}],
            'temperature': cls.temperature,
        }
        if cls.max_tokens:
            payload['max_tokens'] = cls.max_tokens
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.post(cls.url, json=payload) as response:
                data = await response.json()
                return data['choices'][0]['message']['content']


class DeepSeekNeualNetworkPrairieDog(DeepSeekNeualNetworkBase):
    """Класс нейросети DeepSeek, отвечающей как луговая собачка.

    Attributes:
        token (str): токен.
        url (str): url к API.
        system_prompt (str): описание ответов нейросети.
        temperature (float): коэффициент.
        max_tokens (int): максимальная длина ответа.
    """

    token: str = settings.DEEPSEEK_TOKEN
    url: str = settings.DEEPSEEK_URL
    system_prompt: str = settings.DEEPSEEK_SYSTEM_PROMPT_PRAIRIE_DOG
    temperature: float = settings.DEEPSEEK_TEMPERATURE_PRAIRIE_DOG
    max_tokens: int = settings.DEEPSEEK_MAX_TOKENS_PRAIRIE_DOG
