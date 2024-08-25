import requests
from bs4 import BeautifulSoup
import pandas as pd
import smtplib
from email.mime.text import MIMEText
import os

from Banner.banner import Banner

def scrape_vulnerabilities(url):
    try:
        # Make an HTTP request to the target URL
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad status codes
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the URL: {e}")
        return None
    
    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Example: Assuming vulnerabilities are listed in a table
    vulnerabilities = []
    table = soup.find('table', {'id': 'vulnerability-table'})
    
    if table:
        rows = table.find_all('tr')
        for row in rows[1:]:  # Skip the header row
            cols = row.find_all('td')
            cve_id = cols[0].text.strip()
            description = cols[1].text.strip()
            severity = cols[2].text.strip()
            affected_products = cols[3].text.strip()
            
            vulnerabilities.append({
                'CVE ID': cve_id,
                'Description': description,
                'Severity': severity,
                'Affected Products': affected_products
            })
    
    return vulnerabilities

def send_email(subject, body, to_email):
    from_email = "your_email@example.com"  # Replace with your email
    password = "your_password"  # Replace with your password

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email

    with smtplib.SMTP_SSL('smtp.example.com', 465) as server:  # Replace with your SMTP server
        server.login(from_email, password)
        server.sendmail(from_email, to_email, msg.as_string())

if __name__ == "__main__":
    # Display the banner
    banner = Banner()
    banner.display()

    # Prompt user to enter URLs
    urls = []
    while True:
        url = input("Enter a URL to scrape for vulnerabilities (or type 'done' to finish): ")
        if url.lower() == 'done':
            break
        urls.append(url)
    
    all_critical_vulnerabilities = []

    for url in urls:
        print(f"Scraping {url}...")
        vulnerabilities = scrape_vulnerabilities(url)
        
        if vulnerabilities:
            # Filter for critical and high-severity vulnerabilities
            critical_vulnerabilities = [v for v in vulnerabilities if v['Severity'] in ['Critical', 'High']]
            
            if critical_vulnerabilities:
                all_critical_vulnerabilities.extend(critical_vulnerabilities)
                print(f"Added vulnerabilities from {url}.")

    # Save the data to a CSV file
    if all_critical_vulnerabilities:
        file_exists = os.path.isfile('critical_vulnerabilities_report.csv')
        df = pd.DataFrame(all_critical_vulnerabilities)
        df.to_csv('critical_vulnerabilities_report.csv', index=False, mode='a', header=not file_exists)
        print("Critical vulnerabilities report saved as 'critical_vulnerabilities_report.csv'.")

        # Prepare email body and send notification
        body = "New critical vulnerabilities found:\n\n" + "\n".join(str(v) for v in all_critical_vulnerabilities)
        send_email("Critical Vulnerabilities Report", body, "recipient@example.com")  # Replace with recipient email
        print("Notification email sent.")
    else:
        print("No critical vulnerabilities found.")
