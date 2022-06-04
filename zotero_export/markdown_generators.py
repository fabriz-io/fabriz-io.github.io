# %%
import datetime
import html
import json
import os
from string import Template

import dateutil
from slugify import slugify

# from markdown_generators import generate_publications_markdown
# from markdown_templates import (
#     publication_markdown_template,
#     talk_and_presentation_markdown_template,
# )

# from markdown_templates import publication_markdown_template


# %%


def generate_publications_markdown(bibitem, config_item):
    """Generates Markdown files for being HTML rendered.

    Args:
        bib_item: ...
        cofig_item: dictionary with specific format [Add description]
    """

    # String Template to be inserted into generated Markdown file.
    publication_markdown_template = Template(
        (
            "---\n"
            f"title: '$title'\n"
            f"collection: 'publications'\n"
            f"permalink: '/publication/$_id'\n"
            f"date: $date\n"
            f"venue: '$venue'\n"
            f"paperurl: '$paperurl'\n"
            f"citation: '$citation'\n"
            f"filepath: '$filepath'\n"
            "---\n\n"
            f'[PDF](https://fabriz-io.github.io/$filepath){{:target="_blank"}}\n'
        )
    )

    def generate_citation(creators, title, venue, pub_year):
        """Generates citation out of publications meta data."""

        citation = ""

        for author in creators:
            citation += (
                " " + author.get("firstName") + " " + author.get("lastName") + ", "
            )

        citation += (
            '"'
            + html.escape(title.replace("{", "").replace("}", "").replace("\\", ""))
            + '."'
        )

        citation = citation + " " + html.escape(venue)
        citation = citation + ", " + pub_year + "."

        return citation

    date = dateutil.parser.parse(bibitem.get("date"))

    pub_date = datetime.datetime.strftime(date, "%Y-%m-%d")

    pub_year = str(date.year)

    title = html.escape(bibitem.get("title"))

    url_slug = slugify(title)

    md_filename = os.path.basename(
        (pub_date + "-" + url_slug + ".md").replace("--", "-")
    )

    paperurl = bibitem.get("url")

    venuekey = config_item.get("venuekey")

    venue = bibitem.get(venuekey)

    creators = bibitem.get("creators")

    citation = generate_citation(creators, title, venue, pub_year)

    attachments = bibitem.get("attachments")

    filepath = [x.get("path") for x in attachments if ".pdf" in x.get("path")][0]

    markdown_string = publication_markdown_template.substitute(
        title=title,
        _id=url_slug,
        date=pub_date,
        venue=html.escape(venue),
        paperurl=paperurl,
        citation=citation,
        filepath=filepath,
    )

    collections_folder = "../_publications"

    os.makedirs(collections_folder, exist_ok=True)

    with open(os.path.join(collections_folder, md_filename), "w") as f:
        f.write(markdown_string)

    return markdown_string


def generate_markdown(bibtexjson_path, configs):
    with open(bibtexjson_path) as f:
        bibdata = json.load(f)

    bibdata_items = bibdata.get("items")

    for bibitem in bibdata_items:
        item_type = bibitem.get("itemType")

        if item_type not in configs.keys():
            print()
            print()
            print(
                f"Warning. The bibitem type '{item_type}' is not implemented yet. No Markdown page was generated for:"
            )
            print()
            print()
            continue

        config_item = configs.get(item_type)

        # Generate Markdown page based on Item Type
        try:
            markdown_string = config_item.get("markdown_generator")(
                bibitem, config_item
            )
            # print(markdown_string)
        except:
            print(bibitem.get("title"))
            print(
                "Error generating Markdown String. Probably some fields are missing in the bibitem."
            )
