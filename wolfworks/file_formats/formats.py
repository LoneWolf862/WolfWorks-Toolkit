FILE_FORMATS = {
    "json": {
        "name": "JSON",
        "full_name": "JavaScript Object Notation",
        "extensions": [".json"],
        "category": "Structured Data",
        "storage": "Text",
        "human_readable": True,
        "supports_comments": False,
        "common_uses": [
            "Configuration",
            "APIs",
            "Data interchange",
        ],
    },

    "jsonc": {
        "name": "JSONC",
        "full_name": "JSON with Comments",
        "extensions": [".jsonc"],
        "category": "Structured Data",
        "storage": "Text",
        "human_readable": True,
        "supports_comments": True,
        "common_uses": [
            "Configuration",
            "Development tools",
            "Human-edited structured data",
        ],
    },

    "yaml": {
        "name": "YAML",
        "full_name": "YAML Ain't Markup Language",
        "extensions": [".yaml", ".yml"],
        "category": "Structured Data",
        "storage": "Text",
        "human_readable": True,
        "supports_comments": True,
        "common_uses": [
            "Configuration",
            "Automation",
            "Infrastructure",
        ],
    },

    "xml": {
        "name": "XML",
        "full_name": "Extensible Markup Language",
        "extensions": [".xml"],
        "category": "Structured Data",
        "storage": "Text",
        "human_readable": True,
        "supports_comments": True,
        "common_uses": [
            "Data interchange",
            "Configuration",
            "Documents",
        ],
    },

    "csv": {
        "name": "CSV",
        "full_name": "Comma-Separated Values",
        "extensions": [".csv"],
        "category": "Tabular Data",
        "storage": "Text",
        "human_readable": True,
        "supports_comments": False,
        "common_uses": [
            "Spreadsheets",
            "Data export",
            "Tabular datasets",
        ],
    },

    "tsv": {
        "name": "TSV",
        "full_name": "Tab-Separated Values",
        "extensions": [".tsv"],
        "category": "Tabular Data",
        "storage": "Text",
        "human_readable": True,
        "supports_comments": False,
        "common_uses": [
            "Tabular datasets",
            "Data interchange",
            "Data export",
        ],
    },

    "ini": {
        "name": "INI",
        "full_name": "Initialization File",
        "extensions": [".ini"],
        "category": "Configuration",
        "storage": "Text",
        "human_readable": True,
        "supports_comments": True,
        "common_uses": [
            "Application configuration",
            "System configuration",
            "Legacy software",
        ],
    },

    "toml": {
        "name": "TOML",
        "full_name": "Tom's Obvious Minimal Language",
        "extensions": [".toml"],
        "category": "Configuration",
        "storage": "Text",
        "human_readable": True,
        "supports_comments": True,
        "common_uses": [
            "Application configuration",
            "Development tools",
            "Project configuration",
        ],
    },

    "sqlite": {
        "name": "SQLite",
        "full_name": "SQLite Database",
        "extensions": [".sqlite", ".sqlite3", ".db"],
        "category": "Database",
        "storage": "Binary",
        "human_readable": False,
        "supports_comments": False,
        "common_uses": [
            "Embedded databases",
            "Application storage",
            "Local structured data",
        ],
    },

    "xlsx": {
        "name": "XLSX",
        "full_name": "Microsoft Excel Open XML Workbook",
        "extensions": [".xlsx"],
        "category": "Spreadsheet",
        "storage": "Archive / XML",
        "human_readable": False,
        "supports_comments": False,
        "common_uses": [
            "Spreadsheets",
            "Engineering data",
            "Reports",
        ],
    },

    "nbt": {
        "name": "NBT",
        "full_name": "Named Binary Tag",
        "extensions": [".nbt", ".dat"],
        "category": "Structured Data",
        "storage": "Binary",
        "human_readable": False,
        "supports_comments": False,
        "common_uses": [
            "Hierarchical binary data",
            "Game data",
            "Minecraft data",
        ],
    },

    "reg": {
        "name": "REG",
        "full_name": "Windows Registry Export",
        "extensions": [".reg"],
        "category": "Configuration",
        "storage": "Text",
        "human_readable": True,
        "supports_comments": True,
        "common_uses": [
            "Windows Registry export",
            "Registry configuration",
            "System administration",
        ],
    },
}