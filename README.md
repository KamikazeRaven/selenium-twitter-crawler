# selenium-twitter-crawler
This python program bypass the twitter API limitations and utilizes the library Selenium and Beautiful Soup to scrap tweet from twitter's website with the advanced search function. There is no need to log in your twitter account.

Twitter's API does not allow you to collect tweets older than 2 weeks. This program bypass that limitation by using selenium to manipulate twitter's website. Twitter allows people to search historical tweets on their website.

Please know that this is a very simple program that I specifically built for one of my project. I think it might be useful to twitter crawling in gernal, so I upload it here. This program won't be very user friendly.

To use this program, you need to have selenium, beautiful soup, and tqdm library installed. You can simply Google their names to find the instructions on how to install these libraries. You will also need to download a browser driver. I use Google Chrome. Agian, simply Google 'ChromeDriver' to find it.

You'll need to modify my code in order to make it work for you.
Put the path of your browser driver at "driver_path = ''"

Go down and locate the "#starting date" comment. Here, you can specify what date is your starting date.
One line down you'll find the place to set your stoping date.
then variable 'keyword1' and 'keyword2' are the keyword you want to search. You can just have one, or add more. One nice thing about Twitter website search is that it's not case sensitive.

This program might not work as expected on your machine. You can modify it to fit your needs.
