# API

Base URL for local development: `http://localhost:8000`

## `GET /health`

Returns API status.

```json
{
  "status": "ok",
  "service": "salaar-ai-api"
}
```

## `POST /api/classify`

Request:

```json
{
  "message": "Mera phone kho gaya hai",
  "language_hint": "roman_urdu"
}
```

Response:

```json
{
  "detected_language": "roman_urdu",
  "domain": "lost_or_stolen_vehicle_device",
  "subcategory": "lost_phone",
  "confidence": 0.91,
  "emergency_level": "medium"
}
```

## `POST /api/chat`

Request:

```json
{
  "session_id": "optional-uuid",
  "message": "Mera phone kho gaya hai",
  "user_location": {
    "city": "Islamabad",
    "area": "G-10"
  }
}
```

Response:

```json
{
  "session_id": "uuid",
  "reply": "I can help with this...",
  "stage": "collecting_missing_info",
  "missing_fields": ["incident_type", "phone_model", "last_known_location"],
  "category": "lost_or_stolen_vehicle_device",
  "subcategory": "lost_phone",
  "detected_language": "roman_urdu",
  "follow_up_questions": ["Was it lost, stolen, or snatched?"],
  "sources": []
}
```

## `POST /api/voice-message`

Transcribes a browser-recorded voice message with Gemini, then processes the transcript through the normal chat flow.

Request:

```json
{
  "session_id": "optional-uuid",
  "audio_base64": "base64-audio-bytes",
  "mime_type": "audio/webm",
  "user_location": {
    "city": "Islamabad",
    "area": "G-10"
  }
}
```

Response:

```json
{
  "transcript": "Mera phone kho gaya hai",
  "chat": {
    "session_id": "uuid",
    "reply": "I can help with this...",
    "stage": "collecting_missing_info",
    "missing_fields": ["incident_type", "imei"],
    "category": "lost_or_stolen_vehicle_device",
    "subcategory": "lost_phone",
    "detected_language": "roman_urdu",
    "follow_up_questions": [],
    "sources": []
  }
}
```

## `POST /api/generate-report`

Request:

```json
{
  "session_id": "uuid"
}
```

Response contains the full report:

```json
{
  "report_id": "uuid",
  "session_id": "uuid",
  "summary": "Guidance for lost_phone.",
  "category": "lost_or_stolen_vehicle_device",
  "subcategory": "lost_phone",
  "issue_type": "Lost mobile phone report",
  "department": "Nearest police station...",
  "reporting_office": "Model Police Station Ramna",
  "report_recipient": "Station House Officer (SHO)",
  "required_documents": [],
  "complaint_draft": "...",
  "maps_link": "https://www.google.com/maps/search/...",
  "department_location": {
    "place_name": "Police Station ...",
    "address": "Street address from Google Places",
    "phone_number": "optional phone number from Google Places",
    "latitude": 33.123,
    "longitude": 73.123,
    "google_maps_place_id": "places/...",
    "maps_link": "https://maps.google.com/...",
    "notes": "Confirm office jurisdiction, phone number, and timings before visiting."
  },
  "timeline": "...",
  "escalation_steps": [],
  "sources_used": [],
  "disclaimer": "..."
}
```

## `GET /api/reports/{report_id}`

Returns a generated report from the in-memory demo store.

## `GET /api/departments`

Optional query filters:

- `city`
- `province`
- `category`

## `POST /api/feedback`

Request:

```json
{
  "complaint_id": "uuid",
  "rating": 5,
  "helpful": true,
  "comments": "Useful guidance"
}
```
