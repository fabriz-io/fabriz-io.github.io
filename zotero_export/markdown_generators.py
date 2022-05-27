import datetime
import html
import os
import re


def generate_publications_markdown(bib_item_fields, bib_item_persons, config_item):
    """Generates Markdown files for being HTML rendered.

    Args:
        bib_item_fields: pybtex element holding fields of an BibLatex entry
        bib_item_persons: pybtex element holding authors of an BibLatex entry
        cofig_item: dictionary with specific format [Add description]
    """

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
    # permalink = collection.get("permalink") + html_filename
    venue_pretext = config_item.get("venue-pretext")

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
