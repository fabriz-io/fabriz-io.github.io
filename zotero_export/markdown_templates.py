from string import Template

journal_citation_template = Template('$authors, "$title". $venue, $pub_year.')

publication_markdown_template = Template(
    (
        "---\n"
        f"title: '$title'\n"
        f"collection: 'publications'\n"
        f"permalink: '/publication/$_id'\n"
        f"date: $pub_date\n"
        f"venue: '$venue'\n"
        f"paperurl: '$paperurl'\n"
        f"citation: '$citation'\n"
        f"filepath: '$filepath'\n"
        "---\n\n"
        f'[Access paper here]($paperurl){{:target="_blank"}}\n'
    )
)

talk_and_presentation_markdown_template = Template(
    (
        "---\n"
        f"title: '$title'\n"
        f"collection: 'talks'\n"
        f"permalink: '/talks/$id'\n"
        f"venue: '$venue'\n"
        f"date: $pub_date\n"
        f"url: '$url'\n"
        f"location: '$location'\n"
        "---\n\n"
    )
)
