import os
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from dotenv import load_dotenv

load_dotenv()

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = os.getenv("GOOGLE_SHEETS_CREDENTIALS")
SPREADSHEET_ID = os.getenv("GOOGLE_SHEET_ID")


class GoogleSheetService:
    @staticmethod
    def get_service():
        creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        service = build('sheets', 'v4', credentials=creds)
        return service.spreadsheets()

    @staticmethod
    def sheet_exists(sheet_name):
        """Check if the sheet exists in the spreadsheet."""
        service = GoogleSheetService.get_service()
        sheet_metadata = service.get(spreadsheetId=SPREADSHEET_ID).execute()
        sheets = sheet_metadata.get('sheets', [])
        return any(sheet['properties']['title'] == sheet_name for sheet in sheets)

    @staticmethod
    def create_sheet(sheet_name):
        """Create a new sheet if it doesn't exist."""
        service = GoogleSheetService.get_service()
        body = {
            'requests': [{
                'addSheet': {
                    'properties': {'title': sheet_name}
                }
            }]
        }
        service.batchUpdate(spreadsheetId=SPREADSHEET_ID, body=body).execute()

    @staticmethod
    def write_to_sheet(sheet_name, data):
        service = GoogleSheetService.get_service()
        if not GoogleSheetService.sheet_exists(sheet_name):
            GoogleSheetService.create_sheet(sheet_name)

        range_name = f"{sheet_name}!A1"
        body = {'values': data}

        service.values().update(
            spreadsheetId=SPREADSHEET_ID,
            range=range_name,
            valueInputOption='RAW',
            body=body
        ).execute()

        return {'message': 'Data written successfully'}

    @staticmethod
    def read_from_sheet(sheet_name):
        service = GoogleSheetService.get_service()
        range_name = f"{sheet_name}!A1:Z"
        result = service.values().get(spreadsheetId=SPREADSHEET_ID, range=range_name).execute()
        values = result.get('values', [])
        return values if values else {'message': 'No data found'}


class WriteSheetView(APIView):
    def post(self, request):
        sheet_name = request.data.get('sheet_name')
        data = request.data.get('data')
        if not sheet_name or not data:
            return Response({'error': 'sheet_name and data are required'}, status=status.HTTP_400_BAD_REQUEST)
        response = GoogleSheetService.write_to_sheet(sheet_name, data)
        return Response(response, status=status.HTTP_200_OK)


class ReadSheetView(APIView):
    def get(self, request):
        sheet_name = request.query_params.get('sheet_name')
        if not sheet_name:
            return Response({'error': 'sheet_name is required'}, status=status.HTTP_400_BAD_REQUEST)
        data = GoogleSheetService.read_from_sheet(sheet_name)
        return Response({'data': data}, status=status.HTTP_200_OK)
