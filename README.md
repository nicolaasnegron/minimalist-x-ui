# Minimalist X Client

A lightweight desktop app built with Python and Tkinter for posting tweets via the X API.

### Updates

TBD...

## Local Installation

Before running the application, ensure you have Python installed on your machine. 
This application was built and tested with Python 3.12

### 1. Clone the repo

```
git clone https://github.com/nicolaasnegron/minimalist-x-ui.git
```

### 2. Navigate to the cloned repo:

```
cd minimalist-x-ui
```

### 3. Install pre-req(s):

```
pip install tweepy
```

## Configuration

To use this application, you must have an X Developer account and create a Project & App to generate API keys and tokens .

1. Set up your X Developer account, log in to the Developer Portal 
```
https://developer.twitter.com/en/portal/dashboard
```
2. Create a Project and an App
3. Retrieve your API Key, API Secret Key, Access Token, and Access Token Secret
3. Store these credentials as environment variables on your machine:

- For Windows:

  ```
  set X_API_KEY=your_api_key
  set X_API_SECRET=your_api_secret
  set X_ACCESS_TOKEN=your_access_token
  set X_ACCESS_SECRET=your_access_secret
  ```

- For macOS/Linux:

  ```
  export X_API_KEY=your_api_key
  export X_API_SECRET=your_api_secret
  export X_ACCESS_TOKEN=your_access_token
  export X_ACCESS_SECRET=your_access_secret
  ```

## Running the Application

To start the application, run the following command in the terminal:

```
python minimalist_x_ui.py
```

Replace `minimalist_x_ui.py` with the path to the script if necessary.

## Usage

### 1. **Composition**
Type your tweet in the text area.
### 2. **Publication**
Click the "Send Tweet" button to post your tweet.
### 3. **Confirmation**
Upon successful operation, a confirmation message will be temporarily displayed.
