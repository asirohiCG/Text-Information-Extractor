**Text information extraction endpoint:** /extract

**Current service port:** 8088
__________________________________
**Request structure:**
- header: Content-Type:application/json
- body:
```
{
  "language":"en",
  "description":"Description of the ticket"
}
```
Please notice that `language` field was added to support multi-language queries. This field is not mandatory, i.e. when not set, the `en` values is used by default.
__________________________________
**Response structure:**
- header: Content-Type:application/json
- body:
```
{
    [
        {
            "number": "INV-123",
            "number_score": "Unavailable",
            "date": "9th Jul 2019",
            "date_score": "Unavailable"
        },
        {
            "number": "SVC00000043223",
            "number_score": "Unavailable",
            "date": "10.12.2019",
            "date_score": "Unavailable"
        }
    ]
}
```
__________________________________
To launch the text information extraction service (which is actually a standalone ready-to-run application) run the main.py script in ticket_classifier directory using the virtual environment used for the AI HelpDesk. The server will be deployed on port 8088 (unless changed).

To get extraction result, make an HTTP request to `service-address:8084/extract` (e.g. `http://localhost:8088/extract` if deployed on local machine) with header Content-Type:application/json and request body (as JSON-formatted string).
Received result will be a JSON-formatted string containing list of tuples with invoice number, invoice date and their certainty scores (kept for legacy compliance)

## Start up the project

If the server is running without `Docker` it is recommended to start the server over conda to avoid admin restrictions to install `tensorflow` and `spacy` with pip.

## Use conda virtual environment
```
$ conda create -n text-ie --file requirements.txt
$ conda activate text-ie
```
## Create conda virtual env alternative via yml file
```
$ conda env create
```

## Install dependencies
```
$ conda install -c conda-forge spacy=2.2.3
```

## Start project
```
$ python main_tie.py
```