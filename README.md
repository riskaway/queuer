# RiskAway Queuer Service

Queuer service to add risk points to the message queue

## API endpoints

### `/add/flood`

**PUT request** with the following body

```json
{
  "latitude": 1.44,
  "longitude": 2.33,
  "depth": "knee",
  "description": "flowing water"
}
```

**NOTE:**

- `description` field is optional
- `depth` should be one of the following:
  - ankle
  - knee
  - hip
  - chest
  - head

### `/add/earthquake`

**PUT request** with the following body

```json
{
  "latitude": 1.44,
  "longitude": 2.33,
  "intensity": "moderate"
}
```

**NOTE:**

- `description` field is optional
- `intensity` should be one of the following:
  - low
  - moderate
  - high
  - extreme

### `/add/hurricane`

**PUT request** with the following body

```json
{
  "latitude": 1.44,
  "longitude": 2.33,
  "intensity": "low"
}
```

**NOTE:**

- `description` field is optional
- `intensity` should be one of the following:
  - low
  - moderate
  - high
  - extreme

## Setup

```
$ pip install -r requirements.txt
```

## Run

```
$ uvicorn app:app --reload
```
