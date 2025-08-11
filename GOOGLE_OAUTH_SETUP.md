# Google OAuth Setup for Nakhrali Fashion

This guide will help you set up Google OAuth authentication for the Nakhrali Fashion e-commerce website.

## Prerequisites

1. A Google Cloud Platform account
2. Access to the Google Cloud Console

## Steps to Set Up Google OAuth

### 1. Create a Google Cloud Project

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Note down the Project ID as you'll need it later

### 2. Configure OAuth Consent Screen

1. In the Google Cloud Console, navigate to **APIs & Services > OAuth consent screen**
2. Select the appropriate user type (External or Internal)
3. Fill in the required information:
   - App name: Nakhrali Fashion
   - User support email: your-email@example.com
   - Developer contact information: your-email@example.com
4. Add the following scopes:
   - `./auth/userinfo.email`
   - `./auth/userinfo.profile`
5. Add your domain to the authorized domains list
6. Save and continue

### 3. Create OAuth Client ID

1. In the Google Cloud Console, navigate to **APIs & Services > Credentials**
2. Click **Create Credentials** and select **OAuth client ID**
3. Select **Web application** as the application type
4. Add a name for your OAuth client (e.g., "Nakhrali Fashion Web Client")
5. Add the following authorized JavaScript origins:
   - `http://localhost:3000` (for development)
   - `https://your-production-domain.com` (for production)
6. Add the following authorized redirect URIs:
   - `http://localhost:3000/auth/google/callback` (for development)
   - `https://your-production-domain.com/auth/google/callback` (for production)
7. Click **Create**
8. Note down the **Client ID** and **Client Secret**

### 4. Configure Environment Variables

#### Backend (.env)

```
# Add these to your existing backend/.env file
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
GOOGLE_REDIRECT_URI=http://localhost:3000/auth/google/callback
```

#### Frontend (.env)

```
# Add this to your frontend/.env file
GOOGLE_CLIENT_ID=your-google-client-id
```

## Testing the Integration

1. Start both the backend and frontend servers
2. Navigate to the login page
3. Click on the "Sign in with Google" button
4. You should be redirected to Google's authentication page
5. After successful authentication, you should be redirected back to the application and logged in

## Troubleshooting

- If you encounter CORS issues, make sure your frontend domain is properly configured in the Google Cloud Console
- Check the backend logs for any authentication errors
- Verify that the redirect URI exactly matches what's configured in the Google Cloud Console
- Ensure that the Google OAuth API is enabled in your Google Cloud project

## Security Considerations

- Never commit your Client Secret to version control
- Use environment variables for sensitive information
- Implement proper token validation on the backend
- Consider using HTTPS even in development for secure OAuth flows