import aspose.words as aw
import re

# doc = aw.Document("Test1.docx")


def convert(doc):
    doc.save("Output.html")

    with open("output.html", "r", encoding="utf-8") as file:
        html_string = file.read()
    html_string = re.sub(
        r'<meta name="generator" content="Aspose.Words for Python via .NET [^"]*" ?/?>', '', html_string)

    # Remove Aspose evaluation messages and links
    html_string = re.sub(
        r'<p[^>]*><span[^>]*>Created with an evaluation copy of Aspose\.Words\..*?</a></p>',
        '',
        html_string,
        flags=re.DOTALL
    )

    # Remove footer messages mentioning Aspose
    html_string = re.sub(
        r'<div[^>]*-aw-headerfooter-type:footer-primary[^>]*>.*?Created with Aspose\.Words[^<]*</span></p></div>',
        '',
        html_string,
        flags=re.DOTALL
    )

    # Clean up extra spaces or empty tags that may result from removal
    html_string = re.sub(r'\s*\n\s*', '\n', html_string)
    # Remove empty <p> tags
    html_string = re.sub(r'<p[^>]*>\s*</p>', '', html_string)
    html_string = re.sub(r'<div[^>]*>\s*</div>', '',
                         html_string)  # Remove empty <div> tags

    # Output the cleaned HTML string
    print(html_string)

    # Print the cleaned HTML
    # print(cleaned_html)
    # cleaned_html2 = re.sub(pattern2, "", cleaned_html)

    # print(cleaned_html)