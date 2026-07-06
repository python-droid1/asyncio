import asyncio
import httpx
import yagmail
import streamlit as st
# fyvk hmmo byvi immd

async def check_website(client, url):
    try:
        response = await client.get(url, timeout=5.0, follow_redirects=True)
        return url, response.status_code, "Healthy" if response.status_code == 200 else "Unhealthy"
    except Exception as e:
        return url, None, f"Failed: {str(e)}"

def send_email_sync(sender, password, receiver, subject, body):
    yag = yagmail.SMTP(sender, password)
    yag.send(to=receiver, subject=subject, contents=body)

async def send_email_async(sender, password, receiver, subject, body):
    await asyncio.to_thread(send_email_sync, sender, password, receiver, subject, body)

async def run_health_check(urls, email_config):
    async with httpx.AsyncClient() as client:
        tasks = [check_website(client, url) for url in urls]
        results = await asyncio.gather(*tasks)
    
    report_lines = []
    for url, status, msg in results:
        report_lines.append(f"URL: {url} | Status: {status} | Result: {msg}")
    
    email_body = "\n".join(report_lines)
    
    await send_email_async(
        email_config["sender"],
        email_config["password"],
        email_config["receiver"],
        "Website Health Check Report",
        email_body
    )
    return results

st.title("Async Website Health Checker")

urls_input = st.text_area("Enter URLs (one per line)", "https://www.google.com\nhttps://www.github.com")
sender_email = st.text_input("Sender Email (Gmail)")
app_password = st.text_input("App Password", type="password")
receiver_email = st.text_input("Receiver Email")

if st.button("Run Check"):
    url_list = [url.strip() for url in urls_input.split("\n") if url.strip()]
    
    if not url_list or not sender_email or not app_password or not receiver_email:
        st.error("Please fill in all fields.")
    else:
        config = {
            "sender": sender_email,
            "password": app_password,
            "receiver": receiver_email
        }
        
        with st.spinner("Checking websites and sending email..."):
            results = asyncio.run(run_health_check(url_list, config))
            
        st.success("Task completed!")
        for url, status, msg in results:
            st.write(f"**{url}**: {msg} (Status Code: {status})")


# ===============================
# with type hints 
# ===============================

import asyncio
from typing import List, Tuple, Dict, Optional
import httpx
import yagmail
import streamlit as st

async def check_website(client: httpx.AsyncClient, url: str) -> Tuple[str, Optional[int], str]:
    try:
        response: httpx.Response = await client.get(url, timeout=5.0, follow_redirects=True)
        return url, response.status_code, "Healthy" if response.status_code == 200 else "Unhealthy"
    except Exception as e:
        return url, None, f"Failed: {str(e)}"

def send_email_sync(sender: str, password: str, receiver: str, subject: str, body: str) -> None:
    yag: yagmail.SMTP = yagmail.SMTP(sender, password)
    yag.send(to=receiver, subject=subject, contents=body)

async def send_email_async(sender: str, password: str, receiver: str, subject: str, body: str) -> None:
    await asyncio.to_thread(send_email_sync, sender, password, receiver, subject, body)

async def run_health_check(urls: List[str], email_config: Dict[str, str]) -> List[Tuple[str, Optional[int], str]]:
    async with httpx.AsyncClient() as client:
        client: httpx.AsyncClient
        tasks = [check_website(client, url) for url in urls]
        results: List[Tuple[str, Optional[int], str]] = await asyncio.gather(*tasks)
    
    report_lines: List[str] = []
    for url, status, msg in results:
        report_lines.append(f"URL: {url} | Status: {status} | Result: {msg}")
    
    email_body: str = "\n".join(report_lines)
    
    await send_email_async(
        email_config["sender"],
        email_config["password"],
        email_config["receiver"],
        "Website Health Check Report",
        email_body
    )
    return results

st.title("Async Website Health Checker")

urls_input: str = st.text_area("Enter URLs (one per line)", "https://www.google.com\nhttps://www.github.com")
sender_email: str = st.text_input("Sender Email (Gmail)")
app_password: str = st.text_input("App Password", type="password")
receiver_email: str = st.text_input("Receiver Email")

if st.button("Run Check"):
    url_list: List[str] = [url.strip() for url in urls_input.split("\n") if url.strip()]
    
    if not url_list or not sender_email or not app_password or not receiver_email:
        st.error("Please fill in all fields.")
    else:
        config: Dict[str, str] = {
            "sender": sender_email,
            "password": app_password,
            "receiver": receiver_email
        }
        
        with st.spinner("Checking websites and sending email..."):
            results = asyncio.run(run_health_check(url_list, config))
            
        st.success("Task completed!")
        for url, status, msg in results:
            st.write(f"**{url}**: {msg} (Status Code: {status})")