# Bank_Management

# Apna Bank - Banking System with Face Recognition Admin Authentication

## Overview
Apna Bank is a simple banking application that provides a secure interface for both administrators and regular users. The system includes face recognition technology for administrator authentication and standard password protection for regular user accounts.

## Features

### User Features
- **Account Creation**: New users can create accounts with a username and password
- **Balance Checking**: Users can check their current account balance
- **Deposits**: Users can deposit money into their accounts
- **Withdrawals**: Users can withdraw money with proper PIN verification
- **Password Management**: Users can change their passwords

### Admin Features
- **Secure Access**: Face recognition technology for admin authentication
- **User Management**: Administrators can view all registered users and their details

## Technical Components

### Face Recognition System
- Uses OpenCV and LBPH (Local Binary Patterns Histograms) Face Recognizer
- Face data collection and model training capabilities
- Real-time face detection and recognition for admin login

### Data Management
- User data stored in CSV format for simplicity
- Secure PIN verification for sensitive operations

## Project Structure
```
.
├── bank2.py               # Main banking application
├── user.csv               # User data storage
├── dataset/               # Face samples storage directory
│   └── admin.*.jpg        # Admin face samples
├── trainer.yml            # Trained face recognition model
└── new.ipynb              # Jupyter notebook with face recognition setup code
```

## Setup and Installation

### Prerequisites
- Python 3.x
- Required libraries:
  - pandas
  - numpy
  - matplotlib
  - opencv-python (cv2)
  - pillow (PIL)

```bash
pip install pandas numpy matplotlib opencv-python pillow
```

### Face Recognition Setup
1. Run the save_faces.py script to collect admin face samples:
   ```python
   # This will capture 30 images of your face for training
   # Code available in new.ipynb
   ```

2. Train the face recognition model:
   ```python
   # This will create trainer.yml file used for recognition
   # Code available in new.ipynb
   ```

## Usage

### Starting the Application
Run the main application file:
```bash
python bank2.py
```

### Main Menu Options
1. **Admin Login (Face Unlock)**: Access administrative features using face recognition
2. **User Login**: Regular user login with username and password
3. **Create Account**: Create a new user account
4. **Exit**: Exit the application

### User Menu Options
1. **Check Balance**: View current account balance
2. **Deposit**: Add funds to account
3. **Withdraw**: Remove funds from account (requires PIN verification)
4. **Change Password**: Update account password
5. **Logout**: Return to main menu

## Security Features
- Face recognition for admin access
- PIN verification for withdrawals
- Password protection for all accounts

## Future Enhancements
- Money transfer functionality between accounts
- Transaction history tracking
- Enhanced security measures
- Web or mobile interface

## Contributing
Feel free to fork this repository and submit pull requests with any enhancements.

## License
[Your License Choice]

---

*This project was created for educational purposes and demonstrates basic banking functionalities along with face recognition security.*
