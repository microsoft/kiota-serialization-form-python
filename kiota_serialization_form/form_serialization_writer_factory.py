from kiota_abstractions.serialization import SerializationWriter, SerializationWriterFactory

from .form_serialization_writer import FormSerializationWriter


class FormSerializationWriterFactory(SerializationWriterFactory):
    """A factory that creates FormSerializationWriter instances.
    """

    def get_valid_content_type(self) -> str:
        """Gets the content type this factory creates serialization writers for.
        Returns:
            str: the content type this factory creates serialization writers for.
        """
        return "application/x-www-form-urlencoded"

    def get_serialization_writer(self, content_type: str) -> SerializationWriter:
        """Creates a new SerializationWriter instance for the given content type.
        Args:
            content_type (str): the content type to create a serialization writer for.
        Returns:
            SerializationWriter: A new SerializationWriter instance for the given content type.
        """
        if not content_type:
            raise TypeError("Content Type cannot be null")
        valid_content_type = self.get_valid_content_type()
        if valid_content_type.casefold() != content_type.casefold():
            raise TypeError(f"Expected {valid_content_type} as content type")

        return FormSerializationWriter()
