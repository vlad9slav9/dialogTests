from playwright.sync_api import Page
from playwright.sync_api import expect

class CreateDocumentPage():
    def __init__(self, page: Page):
        self.page = page

        self._outgoing_document_creation_tab = self.page.get_by_role("tab", name="Создание документа (Исходящий (Автотест))")




    def assert_outgoing_document_creation_tab_visible(self):
        expect(self._outgoing_document_creation_tab).to_be_visible()
