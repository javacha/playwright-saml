

# Playwright SAML Login Automation

This project automates the SAML login process using [Playwright](https://playwright.dev/) and Python. It captures cookies after a successful login and uses them to make authenticated API requests.

## Features

- Automates the SAML login process in a browser.
- Captures cookies after successful login.
- Handles various errors gracefully, such as connection issues or timeouts.
- Uses the captured cookies to make authenticated API requests.

## Requirements

- Python 3.7 or higher
- [Playwright](https://playwright.dev/python/)
- Flask (for testing purposes)
- Requests library

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/playwright-saml.git
   cd playwright-saml
