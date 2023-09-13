# WalkieJr - A Cute Discord Bot

![Chino with twintails  GochiUsa](https://github.com/Ravediff/WalkieJr/assets/117040786/96e501c8-dd73-4890-ad68-403ad31ce03c)



## Table of Contents

- [Description](#description)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Description

WalkieJr is a charming Discord bot created to perform a variety of simple tasks, making your Discord server more fun and informative. With WalkieJr, you can easily:

- **Scrape Movie Info:** Get details about your favorite movies.
- **Post Meme GIFs:** Share hilarious GIFs with your server members.
- **Retrieve Random Quotes:** Inspire and entertain with random quotes.
- **Search Discord User Info:** Quickly find information about Discord users.

This bot is designed to enhance your Discord experience with a touch of cuteness and usefulness.

## Features

- **Movie Info:** Retrieve detailed information about movies, including title, release date, cast, and more.
- **Meme GIFs:** Share amusing GIFs from the internet to brighten up your server.
- **Random Quotes:** Get inspired or entertained with a collection of random quotes.
- **User Info:** Look up information about Discord users in your server.

## Installation

To host the WalkieJr Discord bot, follow these steps:

**Prerequisites:**
- Python 3.7 or higher installed on your system.

1. Clone the repository to your local machine:

```bash
$ git clone https://github.com/yourusername/WalkieJr.git
$ cd WalkieJr
```

Create a Python virtual environment (optional but recommended):
bash
$ python -m venv venv
$ source venv/bin/activate   # On Windows, use: venv\Scripts\activate

Install the required Python packages:
```bash
$ pip install -r requirements.txt
```

Create a Discord bot and obtain its token:

Visit the Discord Developer Portal.
Create a new application and navigate to the "Bot" tab.
Click "Add Bot" to create a bot user.
Under the "TOKEN" section, click "Copy" to copy your bot token.
paste your bot token in the main.py:


Set up a SQLite database (included in Python's standard library) for storing data.

Run the bot using the following command:

```bash
$ python bot.py
```

Optionally, if you want to use the Flask-based web interface (if applicable), navigate to the web directory and run:

```bash
$ python app.py
```
Your WalkieJr Discord bot should now be up and running on your server. You can invite it to your Discord server and start using its features!

Note: Make sure to configure the bot's permissions correctly in your Discord server to allow it to perform the desired actions.

If you encounter any issues or have questions, feel free to reach out for assistance.


## Usage

Once WalkieJr is added to your Discord server, you can start using its features with simple commands. Here are some examples:

- To get movie info: `!movie <movie_name>`
- To post a meme GIF: `!meme`
- To retrieve a random quote: `!quote`
- To search for Discord user info: `!userinfo <username>`

[Insert any additional usage instructions or command details as needed.]

## Contributing

We welcome contributions to improve WalkieJr! If you'd like to contribute, please follow these guidelines:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and commit them.
4. Create a pull request to submit your changes.

We appreciate your help in making WalkieJr even better!

## License

This project is licensed under the GNU Public License, Version 3.0 (GPL-3.0) - see the [LICENSE](LICENSE) file for details.

---

Feel free to customize this README further to suit your project's unique needs. If you have any additional sections or details to include, please do so. Good luck with your WalkieJr Discord bot!
