### the Bible: the greatest love letter we could ever recieve. ꣑ৎ

**Why I made _firstloved_**

- This project actually started when I was learning Python in the summer this year. I decided to make a simple Bible searching program to practice integrating RESTful APIs.

- As time went on, I realized that in my own day to day Bible studies using the YouVersion Bible app and many others, there were small features I didn't like, and increased friction - even if miniscule, towards opening my Bible and studying it.

- For instance, in the YouVersion app - you can't simply search up a specific passage and see it immediately. You can only see certain verses at a time or open up the entire book and find the passage you want yourself.

**Features**

- Right now, _firstloved_ is a fully working Bible, with 4 translation options (working on adding more!) that has a simple, easy to use interface. You can also create an account if you want to save passages or make notes.

- Now, you no longer need to open tons of tabs (as I always had to) just to read your Bible. With an in-app Bible buddy powered by Claude that reads your current open passage for context, you now have definitions, clarifications and insight right at your fingertips.

- Of course, we can't rely on AI to understand scripture. I also included links to my favourite Bible commentary platform, Enduring Word every time you search a passage. ☺︎

**Tech stack**

- Written entirely in **Python** using the **Streamlit** framework, with plain **CSS** for custom styling. User authentication and data stored using **Supabase**.
- Powered by Claude using **Anthropic API**, and gets Bible information from https://bible-api.com/
- Containerized with **Docker** and deployed on **Render** using **Cloudflare** for the custom domain.

**Check it out - live at *https://firstloved.cc*!**

**Currently working on:**

- Lots of bugs, just to name a few:

  - Want to kep user logged in after refreshing (and maybe even their current chat conversation / state)
  - Order the saved verses better (in order of book)
  - Can only search max. 2 chapters at a time (seems like an API issue)

- UI/UX: customizing Streamlit design has been a learning curve! Going to keep it like this for now, and slowly iterate as I dive more into it.

- Community features. This has been the ultimate goal of creating a Bible app from the beginning, but has yet to be brought to fruition!

This project is open source, I'm also _open to collaborate and open to feedback!_

Thanks for stopping by. Hope you get to open your letter today, have a good one ♡
