from pybtex.database.input import bibtex

from markdown_generators import generate_publications_markdown
from markdown_templates import (
    publication_markdown_template,
    talk_and_presentation_markdown_template,
)

# %%
configs = {
    "book": {
        "venuekey": "publisher",
        "venue-pretext": "In the proceedings of ",
        "collection": {"name": "publications", "permalink": "/publication/"},
        "markdown_generator": generate_publications_markdown,
        "markdown_template": publication_markdown_template,
    },
    "journal": {
        "venuekey": "journal",
        "venue-pretext": "",
        "collection": {"name": "publications", "permalink": "/publication/"},
        "markdown_generator": generate_publications_markdown,
        "markdown_template": publication_markdown_template,
    },
    "article": {
        "venuekey": "journal",
        "venue-pretext": "",
        "collection": {"name": "talks", "permalink": "/talks/"},
        "markdown_generator": generate_publications_markdown,
        "markdown_template": talk_and_presentation_markdown_template,
    },
}

# %%
def generate_markdown(bibtex_file):
    parser = bibtex.Parser()
    bibdata = parser.parse_file(bibtex_file)

    for bib_id in bibdata.entries:

        # BibLatex 'Item Type', e.g. @book or @article
        # Can be managed with the 'Item Type' field in Zotero
        bib_item_type = bibdata.entries.get(bib_id).type

        # Contents of the BibLatex Entry
        bib_item_fields = bibdata.entries.get(bib_id).fields

        # Authors are separately extracted by bibtex.Parser()
        bib_item_persons = bibdata.entries.get(bib_id).persons

        if bib_item_type not in configs:
            print()
            print()
            print(
                f"Warning. The bibitem type '{bib_item_type}' is not implemented yet. No Markdown page was generated for:"
            )
            print()
            print(bib_item_fields)
            print()
            continue

        # Get Item type for current BibLatex Entry
        config_item = configs.get(bib_item_type)

        # Generate Markdown page based on Item Type
        config_item.get("markdown_generator")(
            bib_item_fields, bib_item_persons, config_item
        )


# %%
generate_markdown(bibtex_file="./zotero_export_clmb.bib")

# %%
