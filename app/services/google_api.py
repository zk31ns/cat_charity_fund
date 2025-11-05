from datetime import datetime

from aiogoogle import Aiogoogle

from app.core.config import settings

FORMAT = '%Y/%m/%d %H:%M:%S'


async def create_spreadsheets(wrapper_services: Aiogoogle) -> str:
    """Создает новую Google Таблицу для отчета.

    Returns:
        str: ID созданной таблицы.

    """
    now_date_time = datetime.now().strftime(FORMAT)
    service = await wrapper_services.discover('sheets', 'v4')
    spreadsheet_body = {
        'properties': {
            'title': f'Отчёт QRKot на {now_date_time}',
            'locale': 'ru_RU'
        },
        'sheets': [{
            'properties': {
                'sheetType': 'GRID',
                'sheetId': 0,
                'title': 'Отчёт по проектам',
                'gridProperties': {
                    'rowCount': 100,
                    'columnCount': 4
                }
            }
        }]
    }
    return (
        await wrapper_services.as_service_account(
            service.spreadsheets.create(json=spreadsheet_body)
        )
    )['spreadsheetId']


async def set_user_permissions(
    spreadsheetid: str,
    wrapper_services: Aiogoogle
) -> None:
    """Предоставляет права доступа к таблице.

    Args:
        spreadsheetid: ID таблицы для предоставления прав.
        wrapper_services: Объект для работы с Google API.

    """
    permissions_body = {
        'type': 'user',
        'role': 'writer',
        'emailAddress': settings.email
    }
    service = await wrapper_services.discover('drive', 'v3')
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheetid,
            json=permissions_body,
            fields='id'
        )
    )


async def update_spreadsheets_value(
    spreadsheetid: str,
    projects: list,
    wrapper_services: Aiogoogle
) -> None:
    """Заполняет таблицу данными о проектах.

    Args:
        spreadsheetid: ID таблицы для обновления.
        projects: Список проектов для отображения.
        wrapper_services: Объект для работы с Google API.

    """
    now_date_time = datetime.now().strftime(FORMAT)
    service = await wrapper_services.discover('sheets', 'v4')
    table_values = [
        ['Отчёт от', now_date_time],
        ['Топ проектов по скорости закрытия'],
        ['Название проекта', 'Время сбора', 'Описание']
    ]
    for project in projects:
        days_to_close = (project.close_date - project.create_date).days
        new_row = [
            project.name,
            str(days_to_close),
            project.description
        ]
        table_values.append(new_row)

    update_body = {
        'majorDimension': 'ROWS',
        'values': table_values
    }
    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheetid,
            range='A1:E30',
            valueInputOption='USER_ENTERED',
            json=update_body
        )
    )
