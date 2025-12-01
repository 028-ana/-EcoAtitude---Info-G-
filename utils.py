# recompensas/utils.py
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle

def gerar_pdf_resgate(resgate):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        spaceAfter=30,
        textColor=colors.HexColor('#2e7d32')
    )
    
    # Content
    content = []
    
    # Title
    content.append(Paragraph("COMPROVANTE DE RESGATE - ECOATITUDE", title_style))
    content.append(Spacer(1, 20))
    
    # Resgate information
    resgate_data = [
        ['Código do Resgate:', resgate.codigo_resgate],
        ['Data do Resgate:', resgate.data_resgate.strftime('%d/%m/%Y %H:%M')],
        ['Usuário:', resgate.usuario.get_full_name() or resgate.usuario.username],
        ['Recompensa:', resgate.recompensa.nome],
        ['Pontos Utilizados:', str(resgate.recompensa.pontos_necessarios)],
        ['Status:', 'Disponível para retirada' if not resgate.utilizado else 'Já utilizado']
    ]
    
    table = Table(resgate_data, colWidths=[200, 300])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e8f5e8')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2e7d32')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
    ]))
    
    content.append(table)
    content.append(Spacer(1, 30))
    
    # Instructions
    instructions = [
        "INSTRUÇÕES PARA RETIRADA:",
        "1. Apresente este comprovante em um de nossos pontos parceiros",
        "2. O código deve ser válido e não utilizado anteriormente",
        "3. A retirada deve ser feita em até 30 dias",
        "4. Em caso de problemas, entre em contato com nosso suporte"
    ]
    
    for instruction in instructions:
        content.append(Paragraph(instruction, styles['Normal']))
        content.append(Spacer(1, 5))
    
    doc.build(content)
    pdf = buffer.getvalue()
    buffer.close()
    return pdf