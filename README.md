# School Help Guide — AI Assistant

**IBM SkillsBuild AI Experiential Learning Lab**

**Team:** Tech Orbit

**School:** California State University, Dominguez Hills (CSUDH)

School Help Guide is an AI assistant that helps college students find school services such as financial aid, tutoring, and academic advising.

## What It Does

Students can type a question about what they need help with. The assistant uses school information to help them find the right office.

It can provide office locations, contact information, official websites, and next steps when that information is available.

For academic advising, the assistant can ask students about their college or major before recommending a Student Success Center.

If a question is about a service that is not included in the project, the assistant directs students to the official CSUDH website.

## Supported Services

1. Financial Aid Office
2. Toro Learning & Testing Center (TLTC)
3. Academic Advising through Student Success Centers

## Technology Used

The project was developed with IBM Bob and Python.

It uses IBM watsonx.ai with the IBM Granite 4 H Small model to answer student questions.

The school information is stored in `school_data.json`. The assistant is instructed to use this information rather than inventing school contact details.

## Project Files

- `assistant.py` — Main Python program
- `school_data.json` — CSUDH school service information
- `requirements.txt` — Required Python packages
- `env.example` — Example configuration settings
- `.gitignore` — Files that should not be uploaded
- `README.md` — Project instructions

## How to Run the Project

**Step 1:** Install Python.

**Step 2:** Open the project folder in a terminal and install the required packages:

```bash
python -m pip install -r requirements.txt
```

**Step 3:** Make a copy of `env.example` and name it `.env`.

In `.env`, enter your IBM Cloud API key and the Project ID from your IBM watsonx.ai project.

Keep your API key private. Never upload `.env` to GitHub.

**Step 4:** Run the assistant:

```bash
python assistant.py
```

**Step 5:** Type a question when `You:` appears.

Type `quit` or `exit` to stop the program.

## Example Conversation

**Student:** I need help paying for school.

**Assistant:** You can contact the CSUDH Financial Aid Office for help.

**Office:** Financial Aid Office

**Location:** Toro Welcome & Information Center, Welch Hall 245

**Phone:** (310) 243-3691

**Email:** finaid@csudh.edu

**Website:** https://www.csudh.edu/financial-aid/contact-us/

**Next step:** Contact the Financial Aid Office or visit the official website for more information.

## Future Improvements

In the future, I would like to add more school services and improve how the assistant answers different student questions.

This project is a working prototype created for the IBM SkillsBuild AI Experiential Learning Lab.