"""Sanction Letter Generator Agent - Creates PDF loan approval documents."""
from typing import Dict, Any
from datetime import datetime, timedelta
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_JUSTIFY
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib import colors
from pathlib import Path
from utils.helpers import generate_loan_account_number, generate_reference_number


class SanctionLetterGenerator:
    """Sanction Letter Generator for creating PDF loan approval documents."""
    
    def __init__(self):
        self.output_dir = Path(__file__).parent.parent / "generated_documents"
        self.output_dir.mkdir(exist_ok=True)
    
    async def generate_sanction_letter(
        self,
        customer_data: Dict[str, Any],
        loan_details: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generate a professional PDF sanction letter.
        
        Args:
            customer_data: Customer information
            loan_details: Approved loan details
            
        Returns:
            Result with file path and download URL
        """
        try:
            # Validate required customer data
            required_customer_fields = ['customer_id', 'name', 'email', 'phone', 'address']
            missing_customer = [f for f in required_customer_fields if not customer_data.get(f)]
            if missing_customer:
                return {
                    "success": False,
                    "message": f"❌ Cannot generate sanction letter: Missing customer data ({', '.join(missing_customer)})",
                    "file_path": None
                }
            
            # Validate required loan details
            required_loan_fields = ['loan_amount', 'tenure_months', 'interest_rate', 'monthly_emi']
            missing_loan = [f for f in required_loan_fields if not loan_details.get(f)]
            if missing_loan:
                return {
                    "success": False,
                    "message": f"❌ Cannot generate sanction letter: Missing loan details ({', '.join(missing_loan)})",
                    "file_path": None
                }
            
            # Generate unique identifiers
            loan_account_number = generate_loan_account_number()
            reference_number = generate_reference_number("SL")
            sanction_date = datetime.now()
            disbursement_date = sanction_date + timedelta(days=2)
            
            # Create filename
            filename = f"sanction_letter_{customer_data['customer_id']}_{sanction_date.strftime('%Y%m%d')}.pdf"
            filepath = self.output_dir / filename
            
            # Create PDF
            doc = SimpleDocTemplate(
                str(filepath),
                pagesize=A4,
                rightMargin=72,
                leftMargin=72,
                topMargin=72,
                bottomMargin=72
            )
            
            # Container for content
            story = []
            styles = getSampleStyleSheet()
            
            # Custom styles
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=16,
                textColor=colors.HexColor('#1a365d'),
                spaceAfter=12,
                alignment=TA_CENTER,
                fontName='Helvetica-Bold'
            )
            
            heading_style = ParagraphStyle(
                'CustomHeading',
                parent=styles['Heading2'],
                fontSize=12,
                textColor=colors.HexColor('#2c5282'),
                spaceAfter=6,
                fontName='Helvetica-Bold'
            )
            
            body_style = ParagraphStyle(
                'CustomBody',
                parent=styles['BodyText'],
                fontSize=10,
                alignment=TA_JUSTIFY,
                spaceAfter=12
            )
            
            # Header
            story.append(Paragraph("TATA CAPITAL LIMITED", title_style))
            story.append(Paragraph("Personal Loan Division", styles['Normal']))
            story.append(Spacer(1, 0.2 * inch))
            
            # Reference and date
            ref_date_data = [
                ['Reference No:', reference_number, 'Date:', sanction_date.strftime('%d %B %Y')]
            ]
            ref_table = Table(ref_date_data, colWidths=[1.5*inch, 2*inch, 1*inch, 1.5*inch])
            ref_table.setStyle(TableStyle([
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('FONTNAME', (0, 0), (0, 0), 'Helvetica-Bold'),
                ('FONTNAME', (2, 0), (2, 0), 'Helvetica-Bold'),
            ]))
            story.append(ref_table)
            story.append(Spacer(1, 0.3 * inch))
            
            # Customer details
            story.append(Paragraph(f"<b>To,</b><br/>{customer_data['name']}<br/>{customer_data['address']}", body_style))
            story.append(Spacer(1, 0.2 * inch))
            
            # Subject
            story.append(Paragraph(
                f"<b>Subject: Sanction of Personal Loan - ₹{loan_details['loan_amount']:,.0f}</b>",
                heading_style
            ))
            story.append(Spacer(1, 0.2 * inch))
            
            # Salutation
            story.append(Paragraph(f"Dear {customer_data['name'].split()[0]},", body_style))
            
            # Approval message
            approval_text = f"""We are pleased to inform you that your application for a Personal Loan has been 
<b>approved</b>. This sanction is based on your credit profile, income assessment, and our internal 
credit policies. We congratulate you on this approval and look forward to serving you."""
            story.append(Paragraph(approval_text, body_style))
            story.append(Spacer(1, 0.2 * inch))
            
            # Loan details heading
            story.append(Paragraph("<b>LOAN SANCTION DETAILS</b>", heading_style))
            story.append(Spacer(1, 0.1 * inch))
            
            # Loan details table
            total_payment = loan_details['monthly_emi'] * loan_details['tenure_months']
            total_interest = total_payment - loan_details['loan_amount']
            
            loan_data = [
                ['Parameter', 'Details'],
                ['Loan Account Number', loan_account_number],
                ['Sanctioned Amount', f"₹{loan_details['loan_amount']:,.0f}"],
                ['Loan Tenure', f"{loan_details['tenure_months']} months ({loan_details['tenure_months']//12} years {loan_details['tenure_months']%12} months)"],
                ['Interest Rate (Annual)', f"{loan_details['interest_rate']:.2f}% per annum"],
                ['Processing Fee', '₹0 (Waived - Special Offer)'],
                ['Monthly EMI', f"₹{loan_details['monthly_emi']:,.0f}"],
                ['Total Interest Payable', f"₹{total_interest:,.0f}"],
                ['Total Amount Payable', f"₹{total_payment:,.0f}"],
                ['Expected Disbursement Date', disbursement_date.strftime('%d %B %Y')],
            ]
            
            loan_table = Table(loan_data, colWidths=[2.7*inch, 3.3*inch])
            loan_table.setStyle(TableStyle([
                # Header row styling
                ('BACKGROUND', (0, 0), (1, 0), colors.HexColor('#2c5282')),
                ('TEXTCOLOR', (0, 0), (1, 0), colors.whitesmoke),
                ('FONTNAME', (0, 0), (1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (1, 0), 11),
                ('ALIGN', (0, 0), (1, 0), 'CENTER'),
                
                # Data rows styling
                ('BACKGROUND', (0, 1), (0, -1), colors.HexColor('#e6f2ff')),
                ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
                ('ALIGN', (0, 1), (0, -1), 'LEFT'),
                ('ALIGN', (1, 1), (1, -1), 'RIGHT'),
                ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
                ('FONTNAME', (1, 1), (1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 10),
                
                # Highlight important rows
                ('BACKGROUND', (0, 6), (1, 6), colors.HexColor('#fff4e6')),  # Monthly EMI
                ('BACKGROUND', (0, 8), (1, 8), colors.HexColor('#fff4e6')),  # Total Payable
                ('FONTNAME', (0, 6), (1, 6), 'Helvetica-Bold'),
                ('FONTNAME', (0, 8), (1, 8), 'Helvetica-Bold'),
                
                # Borders and spacing
                ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#cbd5e0')),
                ('PADDING', (0, 0), (-1, -1), 10),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ]))
            story.append(loan_table)
            story.append(Spacer(1, 0.3 * inch))
            
            # Terms and conditions
            story.append(Paragraph("<b>TERMS AND CONDITIONS</b>", heading_style))
            story.append(Spacer(1, 0.15 * inch))
            
            terms_intro = "This loan sanction is subject to the following terms and conditions:"
            story.append(Paragraph(terms_intro, body_style))
            story.append(Spacer(1, 0.1 * inch))
            
            terms = [
                ("Validity", "This sanction is valid for 30 days from the date of this letter. Please complete the documentation within this period."),
                ("Disbursement", "Loan disbursement is subject to submission of required KYC documents, signing of loan agreement, and completion of all formalities."),
                ("EMI Deduction", "EMI will be auto-debited from your registered bank account on the 5th of every month. Please ensure sufficient balance."),
                ("Prepayment", "No prepayment charges after 6 months from disbursement date. Partial or full prepayment allowed."),
                ("Late Payment", "Late payment charges of 2% per month (24% p.a.) will apply on overdue amounts. Please ensure timely payment."),
                ("Insurance", "The loan is covered under our credit insurance scheme (optional). Details will be provided during documentation."),
                ("Documentation", "Required documents: PAN Card, Aadhaar Card, Address Proof, Bank Statements (last 6 months), and Salary Slips (last 3 months)."),
            ]
            
            term_style = ParagraphStyle(
                'TermBody',
                parent=styles['BodyText'],
                fontSize=9,
                alignment=TA_JUSTIFY,
                spaceAfter=8,
                leftIndent=15
            )
            
            for i, (title, description) in enumerate(terms, 1):
                term_text = f"<b>{i}. {title}:</b> {description}"
                story.append(Paragraph(term_text, term_style))
            
            story.append(Spacer(1, 0.3 * inch))
            
            # Next steps
            story.append(Paragraph("<b>NEXT STEPS</b>", heading_style))
            story.append(Spacer(1, 0.1 * inch))
            
            next_steps_text = """Our dedicated relationship manager will contact you within <b>24 hours</b> to guide you through the 
documentation process. Please keep your KYC documents ready. The loan amount will be disbursed directly 
to your registered bank account within <b>48 hours</b> of document verification and agreement signing."""
            story.append(Paragraph(next_steps_text, body_style))
            story.append(Spacer(1, 0.25 * inch))
            
            # Contact information box
            contact_data = [
                ['Customer Support', '1800-209-8800 (Toll Free)'],
                ['Email Support', 'support@tatacapital.com'],
                ['Website', 'www.tatacapital.com'],
                ['Working Hours', 'Monday to Saturday, 9:00 AM - 6:00 PM']
            ]
            
            contact_table = Table(contact_data, colWidths=[2*inch, 4*inch])
            contact_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f7fafc')),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                ('ALIGN', (0, 0), (0, -1), 'LEFT'),
                ('ALIGN', (1, 0), (1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e0')),
                ('PADDING', (0, 0), (-1, -1), 8),
            ]))
            story.append(contact_table)
            story.append(Spacer(1, 0.3 * inch))
            
            # Closing
            closing_text = """We thank you for choosing <b>Tata Capital</b> as your financial partner. We are committed to 
providing you with the best service and support throughout your loan journey."""
            story.append(Paragraph(closing_text, body_style))
            story.append(Spacer(1, 0.3 * inch))
            
            # Signature
            story.append(Spacer(1, 0.3 * inch))
            story.append(Paragraph("<b>Warm Regards,</b>", body_style))
            story.append(Spacer(1, 0.6 * inch))
            
            signature_data = [
                ['_____________________________'],
                ['<b>Authorized Signatory</b>'],
                ['Tata Capital Limited'],
                ['Personal Loan Division']
            ]
            
            signature_table = Table(signature_data, colWidths=[3*inch])
            signature_table.setStyle(TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 1), (0, 1), 'Helvetica-Bold'),
                ('FONTNAME', (0, 0), (0, 0), 'Helvetica'),
                ('FONTNAME', (0, 2), (0, 3), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('LINEABOVE', (0, 1), (0, 1), 1, colors.black),
            ]))
            story.append(signature_table)
            
            # Build PDF
            doc.build(story)
            
            return {
                "success": True,
                "message": f"""✅ Sanction Letter Generated Successfully!

📄 Your loan sanction letter has been created.

Key Details:
• Loan Account: {loan_account_number}
• Reference: {reference_number}
• Amount: ₹{loan_details['loan_amount']:,.0f}
• EMI: ₹{loan_details['monthly_emi']:,.0f}
• Disbursement Date: {disbursement_date.strftime('%d %B %Y')}

The sanction letter is ready for download. Our team will contact you within 24 hours for documentation.

🎉 Congratulations on your loan approval!""",
                "file_path": str(filepath),
                "filename": filename,
                "loan_account_number": loan_account_number,
                "reference_number": reference_number,
                "next_agent": None
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Error generating sanction letter: {str(e)}",
                "next_agent": None
            }
