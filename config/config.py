import argparse


class BotConfig:
    def __init__(self, telegram_token: str, helper_username: str, bitrix_token: str, pg_link: str, owner_chat_id: str):
        self.TELEGRAM_TOKEN = telegram_token
        self.HELPER_USERNAME = helper_username
        self.BITRIX_TOKEN = bitrix_token
        self.PG_LINK = pg_link
        self.OWNER_CHAT_ID = owner_chat_id

    @classmethod
    def from_command_line(cls) -> 'BotConfig':
        parser = argparse.ArgumentParser(description='Конфигурация Telegram бота')

        parser.add_argument('--TELEGRAM_TOKEN', required=True, help='Токен Telegram бота')
        parser.add_argument('--HELPER_USERNAME', required=True, help='Username помощника (без @)')
        parser.add_argument('--BITRIX_TOKEN', required=True, help='Токен Bitrix API')
        parser.add_argument('--PG_LINK', required=True, help='Строка подключения к PostgreSQL')
        parser.add_argument('--OWNER_CHAT_ID', required=True, help='ID чата владельца')

        args = parser.parse_args()

        return cls(
            telegram_token=args.TELEGRAM_TOKEN,
            helper_username=args.HELPER_USERNAME,
            bitrix_token=args.BITRIX_TOKEN,
            pg_link=args.PG_LINK,
            owner_chat_id=args.OWNER_CHAT_ID
        )