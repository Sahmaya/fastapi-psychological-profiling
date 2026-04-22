"""
159.352 Assignment 1: Online Psychological Profiling
Sahmaya Anderson-Edwards, 24012404
"""

from fastapi import FastAPI, Depends, Form, HTTPException, status
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from typing import Annotated
import httpx

app = FastAPI()
security = HTTPBasic()

STUDENT_ID = "Inserted Student ID"
OMDB_KEY = "Inserted OMDB KEY"

# stored data 
form_data = {}
profile_data = {}
pet_images = {}


def check_creds(credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
    if credentials.username != STUDENT_ID or credentials.password != STUDENT_ID:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Bad credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials


@app.get("/")
async def index(credentials: Annotated[HTTPBasicCredentials, Depends(check_creds)]):
    with open("index.html") as f:
        html = f.read()
    return HTMLResponse(content=html)


@app.get("/form")
async def get_form(credentials: Annotated[HTTPBasicCredentials, Depends(check_creds)]):
    with open("psycho.html") as f:
        html = f.read()
    return HTMLResponse(content=html)


@app.post("/submit")
async def submit(
    credentials: Annotated[HTTPBasicCredentials, Depends(check_creds)],
    name: Annotated[str, Form()],
    gender: Annotated[str, Form()],
    birthyear: Annotated[str, Form()],
    birthplace: Annotated[str, Form()],
    residence: Annotated[str, Form()],
    question1: Annotated[str, Form()],
    question2: Annotated[str, Form()],
    question3: Annotated[str, Form()],
    question4: Annotated[str, Form()],
    question5: Annotated[str, Form()],
    question6: Annotated[str, Form()],
    question7: Annotated[str, Form()],
    question8: Annotated[str, Form()],
    question9: Annotated[str, Form()],
    question10: Annotated[str, Form()],
    question11: Annotated[str, Form()],
    question12: Annotated[str, Form()],
    question13: Annotated[str, Form()],
    question14: Annotated[str, Form()],
    question15: Annotated[str, Form()],
    question16: Annotated[str, Form()],
    question17: Annotated[str, Form()],
    question18: Annotated[str, Form()],
    question19: Annotated[str, Form()],
    question20: Annotated[str, Form()],
    job: Annotated[str, Form()],
    message: Annotated[str, Form()] = "",
    pets: Annotated[list[str], Form()] = [],
):
    # store everything in module-level 
    form_data.update({
        "name": name,
        "gender": gender,
        "birthyear": birthyear,
        "birthplace": birthplace,
        "residence": residence,
        "questions": {
            f"question{i}": locals()[f"question{i}"] for i in range(1, 21)
        },
        "job": job,
        "pets": pets,
        "message": message
    })
    return JSONResponse(content={"message": "Form has been submitted"})


@app.get("/analyze")
async def analyze(credentials: Annotated[HTTPBasicCredentials, Depends(check_creds)]):
    if not form_data:
        return JSONResponse(content={"message": "No form data yet. Submit the form first"})

    questions = form_data.get("questions", {})

    # score the quetion traits 
    extraversion = (int(questions.get("question1", 1)) +
                    int(questions.get("question8", 1)) +
                    (6 - int(questions.get("question14", 1))) +
                    (6 - int(questions.get("question16", 1)))) / 4

    conscientiousness = (int(questions.get("question2", 1)) +
                         int(questions.get("question10", 1)) +
                         (6 - int(questions.get("question5", 1))) +
                         (6 - int(questions.get("question12", 1))) +
                         (6 - int(questions.get("question15", 1)))) / 5

    openness = (int(questions.get("question3", 1)) +
                int(questions.get("question7", 1)) +
                int(questions.get("question11", 1))) / 3

    agreeableness = (int(questions.get("question4", 1)) +
                     int(questions.get("question20", 1)) +
                     (6 - int(questions.get("question9", 1))) +
                     (6 - int(questions.get("question17", 1))) +
                     (6 - int(questions.get("question18", 1)))) / 5

    neuroticism = ((6 - int(questions.get("question6", 1))) +
                   int(questions.get("question13", 1)) +
                   int(questions.get("question19", 1))) / 3

    job = form_data.get("job", "")
    career_comments = {
        "ceo": f"Your conscientiousness score of {conscientiousness:.1f}/5 and extraversion of {extraversion:.1f}/5 {'make you a natural fit for the boardroom' if conscientiousness > 3 and extraversion > 3 else 'suggest you might want to work on your leadership presence before taking the corner office'}.",
        "astronaut": f"Openness {openness:.1f}/5 and neuroticism {neuroticism:.1f}/5 — {'your curiosity and cool head are astronaut material' if openness > 3 and neuroticism < 3 else 'space is unforgiving and your profile suggests you might prefer to admire it from Earth'}.",
        "doctor": f"Agreeableness {agreeableness:.1f}/5 and conscientiousness {conscientiousness:.1f}/5 — {'your caring and reliable nature suits medicine well' if agreeableness > 3 and conscientiousness > 3 else 'a good bedside manner requires patience — something your scores suggest you might want to develop'}.",
        "model": f"Extraversion {extraversion:.1f}/5 — {'you were born for the spotlight' if extraversion > 3.5 else 'the camera loves confidence, and your profile suggests you might prefer life behind the lens'}.",
        "rockstar": f"Extraversion {extraversion:.1f}/5 and openness {openness:.1f}/5 — {'you have the personality for the stage' if extraversion > 3 and openness > 3 else 'even the greatest rockstars started somewhere — keep working on that stage presence'}.",
        "garbage": f"Conscientiousness {conscientiousness:.1f}/5 — {'an underrated but essential role, and your reliable nature is perfect for it' if conscientiousness > 3 else 'even refuse collection requires reliability — your scores suggest this might actually be a stretch'}.",
    }
    career_assessment = career_comments.get(job, "No assessment available for that career.")

    if openness > 3.5:
        movie_titles = ["Inception", "2001: A Space Odyssey", "Eternal Sunshine of the Spotless Mind"]
    elif extraversion > 3.5:
        movie_titles = ["The Grand Budapest Hotel", "Ferris Bueller's Day Off", "Guardians of the Galaxy"]
    elif conscientiousness > 3.5:
        movie_titles = ["The Martian", "Whiplash", "Schindler's List"]
    elif agreeableness > 3.5:
        movie_titles = ["Forrest Gump", "The Secret Life of Walter Mitty", "About Time"]
    else:
        movie_titles = ["Fight Club", "No Country for Old Men", "There Will Be Blood"]

    movies = []
    async with httpx.AsyncClient() as client:
        for title in movie_titles:
            resp = await client.get(f"http://www.omdbapi.com/?apikey={OMDB_KEY}&t={title}")
            if resp.status_code == 200:
                data = resp.json()
                if data.get("Response") == "True":
                    movies.append({
                        "title": data.get("Title"),
                        "year": data.get("Year"),
                        "plot": data.get("Plot"),
                        "poster": data.get("Poster"),
                        "imdbRating": data.get("imdbRating"),
                    })

    pets = form_data.get("pets", [])
    images = {}

    async with httpx.AsyncClient() as client:
        for pet in pets:
            if pet == "dog":
                resp = await client.get("https://dog.ceo/api/breeds/image/random")
                if resp.status_code == 200:
                    images["dog"] = resp.json().get("message")
            elif pet == "cat":
                resp = await client.get("https://api.thecatapi.com/v1/images/search")
                if resp.status_code == 200:
                    data = resp.json()
                    if data:
                        images["cat"] = data[0].get("url")
            elif pet == "duck":
                resp = await client.get("https://random-d.uk/api/v2/random")
                if resp.status_code == 200:
                    images["duck"] = resp.json().get("url")

    profile_data.update({
        "name": form_data.get("name"),
        "traits": {
            "extraversion": round(extraversion, 2),
            "conscientiousness": round(conscientiousness, 2),
            "openness": round(openness, 2),
            "agreeableness": round(agreeableness, 2),
            "neuroticism": round(neuroticism, 2),
        },
        "career_assessment": career_assessment,
        "movies": movies,
    })
    pet_images.update(images)

    return JSONResponse(content={"message": "Analysis complete. Click 'View Profile' to see your results"})


@app.get("/view/input")
async def view_input(credentials: Annotated[HTTPBasicCredentials, Depends(check_creds)]):
    if not form_data:
        return JSONResponse(content={"message": "No data yet"})
    return JSONResponse(content=form_data)


@app.get("/view/profile")
async def view_profile(credentials: Annotated[HTTPBasicCredentials, Depends(check_creds)]):
    if not form_data:
        return JSONResponse(content={"message": "No data yet"})
    return JSONResponse(content={"profile": profile_data, "pet_images": pet_images})
