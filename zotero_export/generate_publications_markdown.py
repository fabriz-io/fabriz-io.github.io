# %%
import html
import os
import re
from datetime import datetime
from string import Template

from pybtex.database.input import bibtex

# %% Markdown Templates

publication_markdown_template = Template(
    (
        "---\n"
        f"title: '$title'\n"
        f"collection: 'publications'\n"
        f"permalink: '/publication/$html_filename'\n"
        f"date: $pub_date\n"
        f"venue: '$venue'\n"
        f"paperurl: '$paperurl'\n"
        f"citation: '$citation'\n"
        "---\n\n"
        "This is a Test\n"
        f'[Access paper here]($paperurl){{:target="_blank"}}\n'
    )
)

talk_and_presentation_markdown_template = Template(
    (
        "---\n"
        f"title: '$title'\n"
        f"collection: 'publications'\n"
        f"permalink: '/publication/$html_filename'\n"
        f"date: $pub_date\n"
        f"venue: '$venue'\n"
        f"paperurl: '$paperurl'\n"
        f"citation: '$citation'\n"
        "---\n\n"
    )
)


# %%


def generate_publications_markdown(bib_item_fields, bib_item_persons, config_item):
    """Generates Markdown files for being HTML rendered."""

    def generate_citation(bib_persons, title, venue):
        """Generated the citation out of the publications meta data."""
        citation = ""

        for author in bib_persons.get("author"):
            citation += " " + author.first_names[0] + " " + author.last_names[0] + ", "

        citation += (
            '"'
            + html.escape(title.replace("{", "").replace("}", "").replace("\\", ""))
            + '."'
        )

        citation = citation + " " + html.escape(venue)
        citation = citation + ", " + pub_year + "."

        return citation

    pub_year = str(bib_item_fields.get("year"))

    # Apparently months can come in different formats in biblatex
    pub_month = "01"
    pub_day = "01"
    for month_formatting in ["%b", "%B", "%m"]:
        try:
            month_string = str(bib_item_fields.get("month"))
            pub_month = f"{datetime.datetime.strptime(month_string, month_formatting).month:02d}"
            break
        except:
            continue

    pub_date = "-".join([pub_year, pub_month, pub_day])

    # strip out {} as needed (some bibtex entries that maintain formatting)
    clean_title = (
        bib_item_fields["title"]
        .replace("{", "")
        .replace("}", "")
        .replace("\\", "")
        .replace(" ", "-")
    )
    title = html.escape(clean_title)

    url_slug = re.sub("\\[.*\\]|[^a-zA-Z0-9_-]", "", clean_title)
    url_slug = url_slug.replace("--", "-")

    md_filename = os.path.basename(
        (pub_date + "-" + url_slug + ".md").replace("--", "-")
    )
    html_filename = (pub_date + "-" + url_slug).replace("--", "-")

    collection = config_item.get("collection")
    paperurl = bib_item_fields.get("url")
    permalink = collection.get("permalink") + html_filename
    venue_pretext = config_item.get("venue-pretext")

    # The venuekey is important for identification
    venuekey = config_item.get("venuekey")

    venue = venue_pretext + bib_item_fields.get(venuekey).replace("{", "").replace(
        "}", ""
    ).replace("\\", "")

    citation = generate_citation(bib_item_persons, title, venue)

    markdown_template = config_item.get("markdown_template")

    markdown_string = markdown_template.substitute(
        title=title,
        html_filename=html_filename,
        pub_date=pub_date,
        venue=html.escape(venue),
        paperurl=paperurl,
        citation=citation,
    )

    collection_name = collection.get("name")
    collections_folder = f"../_{collection_name}"

    os.makedirs(collections_folder, exist_ok=True)

    with open(os.path.join(collections_folder, md_filename), "w") as f:
        f.write(markdown_string)


# %%

configs = {
    "book": {
        "venuekey": "publisher",
        "venue-pretext": "In the proceedings of ",
        "collection": {"name": "publications", "permalink": "/publication/"},
        "markdown_generator": generate_publications_markdown,
        "markdown_template": publikation_markdown_template,
    },
    "journal": {
        "venuekey": "journal",
        "venue-pretext": "",
        "collection": {"name": "publications", "permalink": "/publication/"},
        "markdown_generator": generate_publications_markdown,
        "markdown_template": publikation_markdown_template,
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
            print(bib_item_fields)
            print("Warning. This type of bibitem is not being handled yet.")
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
