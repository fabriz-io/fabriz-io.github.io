from string import Template

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
