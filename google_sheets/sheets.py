import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from loguru import logger

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']


class Sheet:
    def __init__(self):
        self.SPREADSHEET_ID = os.environ.get('SPREADSHEET_ID')
        self.credentials = None

    async def auth(self):
        if os.path.exists('token.json'):
            self.credentials = Credentials.from_authorized_user_file('token.json', SCOPES)
        if not self.credentials or not self.credentials.valid:
            if self.credentials and self.credentials.expired and self.credentials.refresh_token:
                self.credentials.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
                self.credentials = flow.run_local_server(port=0)
            with open('token.json', 'w') as token:
                token.write(self.credentials.to_json())

    async def get_workers(self, tg_id: int | str | None = None):
        await self.auth()
        try:
            service = build("sheets", "v4", credentials=self.credentials)
            sheet = service.spreadsheets()
            result = (
                sheet.values()
                .get(spreadsheetId=self.SPREADSHEET_ID, range='Workers')
                .execute()
            )
            if tg_id:  # if we are searching for exact worker
                for el in result['values']:
                    if str(el[0]) == str(tg_id):
                        return el
            return result['values']
        except HttpError as e:
            logger.error(f'Error by getting the connection to cheet -> \n{e}')


if __name__ == '__main__':
    sheet = Sheet()
    print(
        sheet.get_workers()
    )
