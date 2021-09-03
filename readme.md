### Description
QuoteQuizz is a project for guessing quotes.

###Backend
#### Quote parsing
Quotes parser is launched by ``py manage.py startparser`` command, which parses a lot of html pages to get quote category, source (film, book, etc) and quote itself. Parser saves needed entities into database.
#### Questions generation
Questions generator is also launched by ``py manage.py generatequestions`` command. It generates a questions with four possible answers from same quote category, and saves them into database.
Other things, such as requests from front-end, are handled by Django mechanisms.

###Frontend
User can pick one of the categories (quotes from films, books, etc), and user sees question page, which has quote and four possible answers. Also page has 20-second timer (uses progressbar.js). When user picks one of questions or time runs out, AJAX request (uses JQuery) is sent to backend with info about question, so registered users could see statistics of correct/incorrect answers by category in their profile.