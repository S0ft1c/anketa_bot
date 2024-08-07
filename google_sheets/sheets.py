import asyncio
import os

from dotenv import load_dotenv
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from loguru import logger

from sqlite_database import DB

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']


class Sheet:
    def __init__(self):
        load_dotenv()
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

    def clear_sheets(self, service):
        sheets = service.spreadsheets().get(spreadsheetId=self.SPREADSHEET_ID).execute().get('sheets', [])
        requests = [{'deleteSheet': {'sheetId': sheet['properties']['sheetId']}} for sheet in sheets[1:]]
        if not requests:
            return
        if requests:
            batch_update_request = {'requests': requests}
            service.spreadsheets().batchUpdate(spreadsheetId=self.SPREADSHEET_ID, body=batch_update_request).execute()

    # Функция для добавления новых данных в таблицу
    def add_sheet(self, service, spreadsheet_id, title, values):
        try:
            # Добавляем новый лист

            body = {
                "requests": {
                    "addSheet": {
                        "properties": {
                            "title": title
                        }
                    }
                }
            }

            response = service.spreadsheets().batchUpdate(spreadsheetId=self.SPREADSHEET_ID, body=body).execute()

            # Преобразуем значения в формат, понятный для Google Sheets API
            headers = list(values[0].keys())
            rows = [headers] + [[row[h] for h in headers] for row in values]

            # Обновляем значения на новом листе
            data = {
                # 'majorDimension': 'ROWS',
                'values': rows
            }
            service.spreadsheets().values().update(
                spreadsheetId=self.SPREADSHEET_ID,
                range=f'{title}',
                valueInputOption='RAW',
                body=data
            ).execute()
        except Exception as e:
            logger.error(f'Error in adding sheet {title}: {e}')

    async def write_all_to_google_table(self):
        try:
            # Загрузите учетные данные
            await self.auth()
            service = build('sheets', 'v4', credentials=self.credentials)

            spreadsheet_id = 'your_spreadsheet_id'

            async with DB() as db:
                admin_logs = await db.select_all_admin_logs()
                admin_reviews = await db.select_all_admin_reviews()
                inworks = await db.select_all_inworks()
                orders = await db.select_all_orders()
                workers = await db.get_all_workers(rated=False)

            # Очистите все листы в таблице
            self.clear_sheets(service)

            # Добавьте данные в таблицу
            self.add_sheet(service, spreadsheet_id, 'Admin_Logs', admin_logs)
            self.add_sheet(service, spreadsheet_id, 'Admin_Reviews', admin_reviews)
            self.add_sheet(service, spreadsheet_id, 'Inworks', inworks)
            self.add_sheet(service, spreadsheet_id, 'Orders', orders)
            self.add_sheet(service, spreadsheet_id, 'Workers', workers)

        except Exception as e:
            logger.error(f'Error in write_all_to_google_table -> {e}')


if __name__ == '__main__':
    sheet = Sheet()
    asyncio.run(
        sheet.write_all_to_google_table()
    )
