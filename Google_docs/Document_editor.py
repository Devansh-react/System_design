from abc import ABC, abstractmethod


# Abstraction for document elements
class DocumentElement(ABC):
    @abstractmethod
    def render(self) -> str:
        pass


# Concrete implementation for text elements
class TextElement(DocumentElement):
    def __init__(self, text: str) -> None:
        self.text = text

    def render(self) -> str:
        return self.text


# Concrete implementation for image elements
class ImageElement(DocumentElement):
    def __init__(self, image_path: str) -> None:
        self.image_path = image_path

    def render(self) -> str:
        return f"[Image: {self.image_path}]"


# NewLineElement represents a line break in the document.
class NewLineElement(DocumentElement):
    def render(self) -> str:
        return "\n"


# TabSpaceElement represents a tab space in the document.
class TabSpaceElement(DocumentElement):
    def render(self) -> str:
        return "\t"


# Document class responsible for holding a collection of elements
class Document:
    def __init__(self) -> None:
        self.document_elements: list[DocumentElement] = []

    def add_element(self, element: DocumentElement) -> None:
        self.document_elements.append(element)

    # Renders the document by concatenating the render output of all elements.
    def render(self) -> str:
        result = ""
        for element in self.document_elements:
            result += element.render()
        return result


# Persistence abstraction
class Persistence(ABC):
    @abstractmethod
    def save(self, data: str) -> None:
        pass


# FileStorage implementation of Persistence
class FileStorage(Persistence):
    def __init__(self, filename: str = "document.txt") -> None:
        self.filename = filename

    def save(self, data: str) -> None:
        try:
            with open(self.filename, "w", encoding="utf-8") as out_file:
                out_file.write(data)
            print(f"Document saved to {self.filename}")
        except OSError:
            print("Error: Unable to open file for writing.")


# Placeholder DBStorage implementation
class DBStorage(Persistence):
    def save(self, data: str) -> None:
        # Save to DB (not implemented)
        pass


# DocumentEditor class managing client interactions
class DocumentEditor:
    def __init__(self, document: Document, storage: Persistence) -> None:
        self.document = document
        self.storage = storage
        self._rendered_document: str | None = None

    def add_text(self, text: str) -> None:
        self.document.add_element(TextElement(text))

    def add_image(self, image_path: str) -> None:
        self.document.add_element(ImageElement(image_path))

    # Adds a new line to the document.
    def add_new_line(self) -> None:
        self.document.add_element(NewLineElement())

    # Adds a tab space to the document.
    def add_tab_space(self) -> None:
        self.document.add_element(TabSpaceElement())

    def render_document(self) -> str:
        if self._rendered_document is None:
            self._rendered_document = self.document.render()
        return self._rendered_document

    def save_document(self) -> None:
        self.storage.save(self.render_document())


# Client usage example
if __name__ == "__main__":
    document = Document()
    persistence = FileStorage("document.txt")

    editor = DocumentEditor(document, persistence)

    # Simulate a client using the editor with common text formatting features.
    editor.add_text("Hello, world!")
    editor.add_new_line()
    editor.add_text("This is a real-world document editor example.")
    editor.add_new_line()
    editor.add_tab_space()
    editor.add_text("Indented text after a tab space.")
    editor.add_new_line()
    editor.add_image("picture.jpg")

    # Render and display the final document.
    print(editor.render_document())

    editor.save_document()