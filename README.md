# FastCare API

A FastAPI server with public endpoints for healthcare management system.

## Features

- **Patient Management**: CRUD operations for patient records
- **Appointment Management**: CRUD operations for appointments
- **RESTful API**: Full REST API with proper HTTP status codes
- **Auto-generated Documentation**: Interactive API docs with Swagger UI
- **CORS Support**: Cross-origin resource sharing enabled
- **Data Validation**: Pydantic models for request/response validation
- **Health Check**: Built-in health monitoring endpoint

## Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. Clone or download this project
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Server

```bash
python main.py
```

Or using uvicorn directly:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

The server will start on `http://localhost:8000`

## API Documentation

Once the server is running, you can access:

- **Interactive API Docs (Swagger UI)**: http://localhost:8000/docs
- **Alternative API Docs (ReDoc)**: http://localhost:8000/redoc

## Available Endpoints

### Root & Health
- `GET /` - Welcome message and API info
- `GET /health` - Health check endpoint
- `GET /stats` - API statistics

### Patients
- `GET /patients` - Get all patients
- `GET /patients/{patient_id}` - Get specific patient
- `POST /patients` - Create new patient
- `PUT /patients/{patient_id}` - Update patient
- `DELETE /patients/{patient_id}` - Delete patient

### Appointments
- `GET /appointments` - Get all appointments
- `GET /appointments/{appointment_id}` - Get specific appointment
- `POST /appointments` - Create new appointment
- `PUT /appointments/{appointment_id}` - Update appointment
- `DELETE /appointments/{appointment_id}` - Delete appointment

### Utility
- `GET /patients/{patient_id}/appointments` - Get appointments for specific patient

## Example Usage

### Creating a Patient

```bash
curl -X POST "http://localhost:8000/patients" \
     -H "Content-Type: application/json" \
     -d '{
       "name": "John Doe",
       "age": 35,
       "email": "john.doe@email.com",
       "phone": "+1234567890",
       "diagnosis": "Hypertension"
     }'
```

### Creating an Appointment

```bash
curl -X POST "http://localhost:8000/appointments" \
     -H "Content-Type: application/json" \
     -d '{
       "patient_id": 1,
       "doctor_name": "Dr. Smith",
       "appointment_date": "2024-01-15",
       "appointment_time": "14:30",
       "reason": "Follow-up consultation"
     }'
```

### Getting All Patients

```bash
curl -X GET "http://localhost:8000/patients"
```

## Data Models

### Patient
```json
{
  "id": 1,
  "name": "John Doe",
  "age": 35,
  "email": "john.doe@email.com",
  "phone": "+1234567890",
  "diagnosis": "Hypertension",
  "created_at": "2024-01-10T10:30:00"
}
```

### Appointment
```json
{
  "id": 1,
  "patient_id": 1,
  "doctor_name": "Dr. Smith",
  "appointment_date": "2024-01-15",
  "appointment_time": "14:30",
  "reason": "Follow-up consultation",
  "status": "scheduled",
  "created_at": "2024-01-10T10:30:00"
}
```

## Development

### Project Structure
```
Fastcare/
├── main.py              # Main FastAPI application
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

### Adding New Endpoints

1. Define Pydantic models for request/response validation
2. Create endpoint functions with appropriate HTTP methods
3. Add proper error handling with HTTPException
4. Update this README with new endpoint documentation

## Notes

- This is a demo application using in-memory storage
- In production, you should use a proper database (PostgreSQL, MongoDB, etc.)
- Add authentication and authorization for production use
- Implement proper logging and monitoring
- Add input validation and sanitization
- Consider rate limiting for public endpoints

## License

This project is open source and available under the MIT License.
