# %%
import shutil

from markdown_generators import *

configs = {
    "book": {
        "venuekey": "publisher",
        "venue-pretext": "In the proceedings of ",
        "collection": {"name": "publications", "permalink": "/publication/"},
        "markdown_generator": generate_publications_markdown,
    },
    "journalArticle": {
        "venuekey": "publicationTitle",
        "venue-pretext": "",
        "collection": {"name": "publications", "permalink": "/publication/"},
        "markdown_generator": generate_publications_markdown,
    },
    "conferencePaper": {
        "venuekey": "publicationTitle",
        "venue-pretext": "",
        "collection": {"name": "publications", "permalink": "/publication/"},
        "markdown_generator": generate_publications_markdown,
    },
    "presentation": {
        "venuekey": "meetingName",
        "venue-pretext": "",
        "collection": {"name": "talks", "permalink": "/talks/"},
        "markdown_generator": generate_talks_markdown,
    },
    # ______ Below this line items where newly added, format needs to be checked
    "bookSection": {
        "venuekey": "publisher",
        "venue-pretext": "In the proceedings of ",
        "collection": {"name": "publications", "permalink": "/publication/"},
        "markdown_generator": generate_publications_markdown,
    },
    "preprint": {
        "venuekey": "publisher",
        "venue-pretext": "",
        "collection": {"name": "publications", "permalink": "/publication/"},
        "markdown_generator": generate_publications_markdown,
    },
    "report": {
        "venuekey": "publisher",
        "venue-pretext": "",
        "collection": {"name": "publications", "permalink": "/publication/"},
        "markdown_generator": generate_publications_markdown,
    },
}


# %%

if __name__ == "__main__":
    bibtexjson_path = "./my_publication_new.json"

    generate_markdown(bibtexjson_path, configs)

    # Copys all files into root folder for public access.
    # filefolder = "../files"
    # shutil.rmtree(filefolder, ignore_errors=True)
    # # os.makedirs(filefolder, exist_ok=True)
    # shutil.copytree("./Exported Items/files", filefolder)

# %%
