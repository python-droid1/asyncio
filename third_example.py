import asyncio

async def send_welcome_email(email):
    await asyncio.sleep(5)
    print(f"Notification: Welcome email successfully sent to {email}!")

async def handle_user_registration(email):
    print(f"Database: Saving {email} to the database...")
    await asyncio.sleep(0.5)
    print("Database: User saved successfully!")
    
    asyncio.create_task(send_welcome_email(email))
    
    print("Server response sent to user: HTTP 200 - Registration Successful!")

async def main():
    print("--- Simulation Started ---")
    await handle_user_registration("alex@example.com")
    print("Main: The user is already browsing the website now...")
    await asyncio.sleep(6)
    print("--- Simulation Ended ---")

asyncio.run(main())