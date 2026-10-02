from markupsafe import escape

def test_file_formats_page_loads(client):
    response = client.get(
        "/file-formats/"
    )

    assert response.status_code == 200


def test_file_formats_page_title(client):
    response = client.get(
        "/file-formats/"
    )

    assert b"File Formats" in response.data


def test_file_formats_page_lists_tools(client):
    response = client.get(
        "/file-formats/"
    )

    assert b"Format Reference" in response.data
    assert b"Data Inspector" in response.data
    assert b"JSON Tools" in response.data
    assert b"CSV / TSV Tools" in response.data
    assert b"Format Converter" in response.data
    
    
import pytest

from wolfworks.file_formats.formats import FILE_FORMATS


REQUIRED_FIELDS = {
    "name",
    "full_name",
    "extensions",
    "category",
    "storage",
    "human_readable",
    "supports_comments",
    "common_uses",
}


def test_file_format_database_not_empty():
    assert FILE_FORMATS


@pytest.mark.parametrize(
    "format_id,format_data",
    FILE_FORMATS.items(),
)
def test_file_format_has_required_fields(
    format_id,
    format_data,
):
    assert REQUIRED_FIELDS <= format_data.keys()


@pytest.mark.parametrize(
    "format_id,format_data",
    FILE_FORMATS.items(),
)
def test_file_format_extensions_are_valid(
    format_id,
    format_data,
):
    assert format_data["extensions"]

    for extension in format_data["extensions"]:
        assert extension.startswith(".")


@pytest.mark.parametrize(
    "format_id,format_data",
    FILE_FORMATS.items(),
)
def test_file_format_boolean_fields(
    format_id,
    format_data,
):
    assert isinstance(
        format_data["human_readable"],
        bool,
    )

    assert isinstance(
        format_data["supports_comments"],
        bool,
    )


@pytest.mark.parametrize(
    "format_id,format_data",
    FILE_FORMATS.items(),
)
def test_file_format_common_uses(
    format_id,
    format_data,
):
    assert format_data["common_uses"]

    assert all(
        isinstance(use, str)
        for use in format_data["common_uses"]
    )
    
def test_format_reference_page_loads(client):
    response = client.get(
        "/file-formats/reference/"
    )

    assert response.status_code == 200
    assert b"File Format Reference" in response.data


@pytest.mark.parametrize(
    "format_id,format_data",
    FILE_FORMATS.items(),
)
def test_reference_lists_formats(
    client,
    format_id,
    format_data,
):
    response = client.get(
        "/file-formats/reference/"
    )

    assert format_data["name"].encode() in response.data


@pytest.mark.parametrize(
    "format_id,format_data",
    FILE_FORMATS.items(),
)
def test_format_detail_pages_load(
    client,
    format_id,
    format_data,
):
    response = client.get(
        f"/file-formats/reference/{format_id}/"
    )

    assert response.status_code == 200

    assert (
        format_data["name"].encode()
        in response.data
    )

    assert (
        str(escape(format_data["full_name"])).encode()
        in response.data
    )


def test_unknown_format_returns_404(client):
    response = client.get(
        "/file-formats/reference/not-a-format/"
    )

    assert response.status_code == 404