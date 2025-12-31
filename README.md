# Sales Data Analytics System

Student Name: Varun Rishikesh Tiwari  
Student ID: bitsom_ba_25071293  
Date: December 2025  

## 📌 Project Overview
This project is a comprehensive Sales Data Analytics System built in Python. It processes raw, messy sales transaction logs, cleans and validates the data, enriches it with real-time product information from an external API (DummyJSON), and generates detailed business intelligence reports.

## 🚀 Key Features
 Robust Data Cleaning: Handles non-UTF-8 encoding, removes invalid characters (commas in numbers), and filters corrupt records.
 Data Validation: strictly validates transaction IDs, positive values, and required fields.
 Interactive Filtering: Allows users to filter data by Region and Transaction Amount via a console interface.
 API Integration: Fetches real-time product details (Category, Brand, Rating) from the [DummyJSON API](https://dummyjson.com/docs/products) to enrich sales data.
 Automated Reporting: Generates a professional `sales_report.txt` containing:
     Total Revenue & Average Order Value
     Region-wise Performance & Market Share
     Top 5 Best-Selling Products & Loyal Customers
     Daily Sales Trends & Peak Days
     API Enrichment Statistics

## 📂 Repository Structure

sales-analytics-system/
├── main.py                 # Entry point of the application
├── requirements.txt        # List of dependencies
├── README.md               # Project documentation
├── data/
│   ├── sales_data.txt          # Raw input data (provided)
│   └── enriched_sales_data.txt # Generated output with API data
├── output/
└── utils/
    ├── api_handler.py      # Handles DummyJSON API requests
    ├── data_processor.py   # Core analytics and logic
    ├── file_handler.py     # File I/O and data cleaning
    └── report_generator.py # Formats and writes the final report

I apologize if the previous version wasn't clear. Here is the complete and explicit README.md file, now fully detailed with step-by-step Setup and Run instructions.

You can save this exactly as README.md in your project root.

Markdown

# Sales Data Analytics System

**Student Name:** Varun Rishikesh Tiwari  
**Student ID:** bitsom_ba_25071293  
**Date:** December 2025  

## 📌 Project Overview
This project is a comprehensive **Sales Data Analytics System** built in Python. It is designed to process raw, messy sales transaction logs, clean and validate the data, enrich it with real-time product information from an external API (DummyJSON), and generate detailed business intelligence reports.

## 🚀 Key Features
* **Robust Data Cleaning:** Handles non-UTF-8 encoding, removes invalid characters (e.g., commas in numbers), and filters corrupt records.
* **Data Validation:** Strictly validates transaction IDs, positive values, and required fields.
* **Interactive Filtering:** Allows users to filter data by **Region** and **Transaction Amount** via a console interface.
* **API Integration:** Fetches real-time product details (Category, Brand, Rating) from the [DummyJSON API](https://dummyjson.com/docs/products) to enrich sales data.
* **Automated Reporting:** Generates a professional `sales_report.txt` containing revenue analysis, top products, customer insights, and daily trends.

## 📂 Repository Structure
```text
sales-analytics-system/
├── main.py                 # Entry point of the application
├── requirements.txt        # List of dependencies
├── README.md               # Project documentation
├── data/
│   ├── sales_data.txt          # Raw input data (provided)
│   └── enriched_sales_data.txt # Generated output with API data
├── output/
│   └── sales_report.txt        # Final text-based business report
└── utils/
    ├── api_handler.py      # Handles DummyJSON API requests
    ├── data_processor.py   # Core analytics and logic
    ├── file_handler.py     # File I/O and data cleaning
    └── report_generator.py # Formats and writes the final report

⚙️Setup & Installation

Follow these steps to set up the project environment on your local machine:

1. Clone or Download the Repository Ensure you have the folder sales-analytics-system containing all the files listed above.

2. Install Python Make sure you have Python 3.7 or higher installed. You can check this by running:

	python --version

3. Install Dependencies This project requires the requests library to communicate with the API. Open your terminal/command prompt in the project folder and run:

	pip install -r requirements.txt (Note: If you don't have pip installed, you can install the library manually using pip install requests)

▶️ How to Run the Application

1. Prepare the Data Ensure that your raw data file is located at data/sales_data.txt.
2. Execute the Script Run the main script from the root directory:

	python main.py

3. Follow On-Screen Prompts

	The system will read and clean the data.
	It will show you the available Regions and Price Ranges.
	It will ask: Do you want to filter data? (y/n)
		Enter n to process all data.
		Enter y to filter by specific Region or Amount.

4. View Results Once the process completes (usually in under 5 seconds), check the following files:

	Enriched Data: data/enriched_sales_data.txt (Contains combined Sales + API data).
	Final Report: output/sales_report.txt (Contains the full business analysis).

📝 License

This project is submitted for the Module 3: Python Programming assignment.