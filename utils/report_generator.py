from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import getSampleStyleSheet


def generate_pdf_report(candidates, output_path):

    doc = SimpleDocTemplate(output_path)

    styles = getSampleStyleSheet()

    elements = []

    title = Paragraph(
        "HireSense AI - Candidate Shortlist Report",
        styles['Title']
    )

    elements.append(title)

    elements.append(Spacer(1, 20))

    for idx, candidate in enumerate(candidates):

        content = f"""
        <b>Rank:</b> #{idx + 1}<br/>

        <b>Name:</b> {candidate['name']}<br/>

        <b>Email:</b> {candidate['email']}<br/>

        <b>Phone:</b> {candidate['phone']}<br/>

        <b>Total Score:</b> {candidate['total_score']}<br/>

        <b>Recommendation:</b> {candidate['recommendation']}<br/>

        <b>Matched Skills:</b> {', '.join(candidate['matched_skills'])}<br/>

        <b>Skills Score:</b> {candidate['skills_score']}<br/>

        <b>Experience Score:</b> {candidate['experience_score']}<br/>

        <b>Education Score:</b> {candidate['education_score']}<br/>

        <b>Project Score:</b> {candidate['project_score']}<br/>

        <b>Communication Score:</b> {candidate['communication_score']}<br/>
        """

        para = Paragraph(
            content,
            styles['BodyText']
        )

        elements.append(para)

        elements.append(Spacer(1, 20))

    doc.build(elements)