import requests
from bs4 import BeautifulSoup
from tkinter import Tk, Label, Button, filedialog, Entry
from datetime import datetime, timedelta
import schedule
import time

class DomainScraper:
    def __init__(self, master):
        self.master = master
        master.title("Domain Scraper")

        self.label = Label(master, text="Choose a folder to save the text files")
        self.label.pack()

        self.choose_folder_button = Button(master, text="Choose Folder", command=self.choose_folder)
        self.choose_folder_button.pack()

        self.date_label = Label(master, text="Enter a date (YYYY-MM-DD):")
        self.date_label.pack()

        self.date_entry = Entry(master)
        self.date_entry.pack()

        self.scrape_button = Button(master, text="Start Scraping for Given Date", command=self.scrape_for_date)
        self.scrape_button.pack()

        self.scrape_today_button = Button(master, text="Start Scraping for Today", command=self.scrape)
        self.scrape_today_button.pack()

    def choose_folder(self):
        self.folder_selected = filedialog.askdirectory()
        print("Folder selected:", self.folder_selected)

    def scrape_for_date(self):
        target_date = self.date_entry.get()
        if not target_date:
            print("Date not specified!")
            return
        self.scrape(target_date=target_date)

    def scrape(self, target_date=None):
        if not hasattr(self, 'folder_selected'):
            print("Folder not selected!")
            return
        
        if not target_date:
            # Get the date two days before today in the format "YYYY-MM-DD"
            target_date = (datetime.now() - timedelta(days=2)).strftime("%Y-%m-%d")

        for i in range(1, 103):  # 102 subdomains
            url = f"https://newlyregddomains.com/{target_date}/{i}"
            response = requests.get(url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                domains = [tag.text for tag in soup.select('div.container div.whiteBox ul.list li a')]
                with open(f"{self.folder_selected}/{target_date}.txt", "a") as f:
                    f.write("\n".join(domains))
                    f.write("\n")
            else:
                print(f"Failed to retrieve the webpage for {url}")

        print(f"Scraping for {target_date} completed.")

def run_pending_tasks():
    schedule.run_pending()
    root.after(60000, run_pending_tasks)  # run again after 60 seconds

if __name__ == "__main__":
    root = Tk()
    my_scraper = DomainScraper(root)

    schedule.every().day.at("09:00").do(my_scraper.scrape)

    run_pending_tasks()  # Call function to start scheduling
    root.mainloop()
