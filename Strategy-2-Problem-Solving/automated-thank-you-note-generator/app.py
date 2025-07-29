import streamlit as st
import pandas as pd
import openai
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')
SENDER_EMAIL = os.getenv('SENDER_EMAIL')

openai.api_key = OPENAI_API_KEY

st.title('Automated Thank-You Note Generator (MVP)')

uploaded_file = st.file_uploader('Upload guest list (CSV with Name, Email)', type=['csv'])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    if 'Name' not in df.columns or 'Email' not in df.columns:
        st.error('CSV must have Name and Email columns.')
    else:
        st.success(f'Loaded {len(df)} guests.')
        notes = []
        for i, row in df.iterrows():
            prompt = f"Write a warm, personal thank-you note to {row['Name']} for attending our wedding."
            response = openai.Completion.create(
                engine='text-davinci-003',
                prompt=prompt,
                max_tokens=60
            )
            note = response.choices[0].text.strip()
            notes.append(note)
        df['ThankYouNote'] = notes
        st.write('Review and edit notes:')
        edited_notes = []
        for i, row in df.iterrows():
            note = st.text_area(f"Note for {row['Name']} ({row['Email']})", value=row['ThankYouNote'], key=f'note_{i}')
            edited_notes.append(note)
        df['ThankYouNote'] = edited_notes
        if st.button('Send Thank-You Notes via Email'):
            if not SENDGRID_API_KEY or not SENDER_EMAIL:
                st.error('Missing SendGrid API key or sender email in .env file.')
            else:
                sent_count = 0
                for i, row in df.iterrows():
                    message = Mail(
                        from_email=SENDER_EMAIL,
                        to_emails=row['Email'],
                        subject='Thank You for Celebrating With Us!',
                        plain_text_content=row['ThankYouNote']
                    )
                    try:
                        sg = SendGridAPIClient(SENDGRID_API_KEY)
                        sg.send(message)
                        sent_count += 1
                    except Exception as e:
                        st.error(f"Failed to send to {row['Email']}: {e}")
                st.success(f'Sent {sent_count} thank-you notes!') 