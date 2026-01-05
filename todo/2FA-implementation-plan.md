# Implementation Plan: Two-Factor Authentication (2FA) for Admin Panel

## Overview
Implement Time-Based One-Time Password (TOTP) 2FA for admin panel security using Google Authenticator-compatible authenticator apps. 2FA will be mandatory for all ROOT users with backup recovery codes.

## User Requirements Summary
- **Method**: TOTP (Google Authenticator, Authy, Microsoft Authenticator compatible)
- **Enforcement**: Mandatory for all ROOT users
- **Migration**: Force setup on next login for existing admins
- **Recovery**: Generate 10 one-time backup codes

## Current System Analysis

### Existing Authentication Stack
- **Framework**: FastAPI 0.109.0 with JWT (HS256)
- **Password Hashing**: bcrypt via passlib
- **Database**: SQLite/Turso (libSQL) with SQLAlchemy ORM
- **Token Expiry**: 24 hours
- **User Model**: `/web/backend/app/models/user.py`
- **Auth Logic**: `/web/backend/app/auth.py`
- **Admin Login**: `/web/frontend/src/pages/admin/Login.tsx`

### User Roles
- **ROOT**: System administrator (requires 2FA)
- **PLANER**: Event planner (2FA optional in future)
- **OFFIZIELLER**: Judge/Official (2FA optional in future)

## Implementation Plan

### Phase 1: Backend - Database Schema Updates

**File**: `/web/backend/app/models/user.py`

Add new columns to `User` model:
```python
totp_secret = Column(String, nullable=True)  # Encrypted TOTP secret
totp_enabled = Column(Boolean, default=False)  # Is 2FA enabled?
totp_verified = Column(Boolean, default=False)  # Verified during login?
backup_codes = Column(Text, nullable=True)  # JSON array of hashed backup codes
created_at = Column(DateTime, default=datetime.utcnow)  # Already exists
totp_setup_at = Column(DateTime, nullable=True)  # When 2FA was enabled
```

**File**: `/web/backend/app/schemas/user.py`

Add Pydantic schemas:
```python
class UserTOTPSetup(BaseModel):
    secret: str
    qr_code: str  # Base64 encoded QR code image
    backup_codes: List[str]  # Plain text codes (show once)

class UserTOTPVerify(BaseModel):
    code: str  # 6-digit TOTP code

class UserBackupCodeVerify(BaseModel):
    code: str  # One of the 10 backup codes

class UserTOTPStatus(BaseModel):
    totp_enabled: bool
    totp_setup_at: Optional[datetime]
```

**Migration Script**: Create Alembic migration or add columns via SQLAlchemy

### Phase 2: Backend - TOTP Implementation

**New File**: `/web/backend/app/totp.py`

Create TOTP utility module:
```python
import pyotp
import qrcode
import io
import base64
from passlib.context import CryptContext

# Core functions:
- generate_totp_secret() -> str
- generate_qr_code(secret: str, username: str) -> str  # Base64 image
- verify_totp_code(secret: str, code: str) -> bool
- generate_backup_codes(count: int = 10) -> List[str]
- hash_backup_codes(codes: List[str]) -> str  # JSON of hashed codes
- verify_backup_code(hashed_codes: str, code: str) -> bool
```

**Dependencies to Add** (`requirements.txt`):
```
pyotp==2.9.0          # TOTP implementation
qrcode==7.4.2         # QR code generation
Pillow==10.2.0        # Image processing for QR codes
```

### Phase 3: Backend - Auth Flow Updates

**File**: `/web/backend/app/auth.py`

Update authentication dependency chain:

1. **Current**:
   ```
   get_current_user() → get_current_active_user() → get_current_admin_user()
   ```

2. **New (with 2FA)**:
   ```
   get_current_user() → get_current_active_user() → get_current_2fa_verified_user() → get_current_admin_user()
   ```

Add new functions:
```python
async def get_current_2fa_verified_user(current_user: User = Depends(get_current_active_user)):
    """Ensures ROOT users have verified 2FA in this session"""
    if current_user.role == "ROOT":
        if not current_user.totp_enabled:
            raise HTTPException(403, detail="2FA setup required")
        if not current_user.totp_verified:
            raise HTTPException(403, detail="2FA verification required")
    return current_user
```

**JWT Token Updates**:
Add `totp_verified` claim to JWT payload:
```python
{
  "sub": "admin",
  "exp": 1234567890,
  "totp_verified": false  # New claim
}
```

### Phase 4: Backend - New API Endpoints

**File**: `/web/backend/app/routers/auth.py`

Add new authentication endpoints:

#### 1. Setup TOTP (First Time)
```
POST /api/auth/totp/setup
Headers: Authorization: Bearer <token>
Response: {
  secret: string,
  qr_code: string,  # Base64 PNG
  backup_codes: string[]  # Show once!
}
```

#### 2. Enable TOTP (Verify Setup)
```
POST /api/auth/totp/enable
Headers: Authorization: Bearer <token>
Body: { code: string }
Response: { success: bool, message: string }
```

#### 3. Verify TOTP During Login
```
POST /api/auth/totp/verify
Body: { username: string, password: string, code: string }
Response: { access_token: string, token_type: "bearer" }
```

#### 4. Verify Backup Code
```
POST /api/auth/totp/verify-backup
Body: { username: string, password: string, backup_code: string }
Response: { access_token: string, token_type: "bearer", warning: "Backup code used" }
```

#### 5. Get TOTP Status
```
GET /api/auth/totp/status
Headers: Authorization: Bearer <token>
Response: {
  totp_enabled: bool,
  totp_setup_at: string | null,
  requires_setup: bool
}
```

#### 6. Disable TOTP (Admin Self-Service)
```
POST /api/auth/totp/disable
Headers: Authorization: Bearer <token>
Body: { password: string, code: string }
Response: { success: bool }
```

#### 7. Reset User TOTP (Super Admin Function)
```
POST /api/users/{user_id}/reset-totp
Headers: Authorization: Bearer <token>
Response: { success: bool, message: "User must set up 2FA on next login" }
```

**Update Existing Login Endpoint**:
```
POST /api/auth/token
Body: { username: string, password: string }
Response:
  - If ROOT user WITHOUT 2FA: { access_token: string, requires_2fa_setup: true }
  - If ROOT user WITH 2FA: 403 "TOTP code required"
  - If non-ROOT: { access_token: string, token_type: "bearer" }
```

### Phase 5: Frontend - 2FA Setup Flow

**New File**: `/web/frontend/src/pages/admin/TOTPSetup.tsx`

Create TOTP setup page with:
- Display QR code for scanning with authenticator app
- Show text secret (manual entry option)
- Input field for verification code
- Display 10 backup codes (one-time view)
- Download/print backup codes button
- Warning: "Save these backup codes in a secure location"

**Flow**:
1. User logs in with username/password
2. If `requires_2fa_setup: true`, redirect to `/admin/totp-setup`
3. Call `POST /api/auth/totp/setup` to get QR code
4. Display QR code and backup codes
5. User scans QR code with Google Authenticator
6. User enters first TOTP code to verify
7. Call `POST /api/auth/totp/enable` with code
8. If verified, redirect to admin dashboard
9. Update token to include `totp_verified: true`

### Phase 6: Frontend - 2FA Login Flow

**Update File**: `/web/frontend/src/pages/admin/Login.tsx`

Add two-step login:

**Step 1: Username/Password**
```tsx
- Existing form (username + password)
- On submit: POST /api/auth/token
- If response has requires_2fa_setup: true → redirect to setup
- If 403 "TOTP code required" → show Step 2
- Otherwise: login successful
```

**Step 2: TOTP Verification**
```tsx
- Show 6-digit code input field
- "Use backup code instead" link
- On submit: POST /api/auth/totp/verify with username, password, code
- If successful: store token, redirect to dashboard
- If failed: show error "Invalid code"
```

**Backup Code Alternative**:
```tsx
- Modal/alternative form with backup code input
- POST /api/auth/totp/verify-backup
- Show warning: "This backup code is now invalid"
```

### Phase 7: Frontend - User Profile 2FA Management

**New File**: `/web/frontend/src/pages/admin/SecuritySettings.tsx`

Add security settings page accessible from admin profile:
- Display TOTP status (Enabled/Disabled)
- Button: "Disable 2FA" (requires password + current TOTP code)
- Button: "Regenerate Backup Codes" (generates new set, invalidates old)
- Last setup date display

**Navigation**: Add link in `AdminLayout.tsx` header or user dropdown

### Phase 8: Backend - Middleware & Security Enhancements

**File**: `/web/backend/app/main.py`

Add rate limiting for 2FA endpoints:
```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

# Apply to sensitive endpoints:
@limiter.limit("5/minute")  # Max 5 attempts per minute
async def verify_totp_endpoint():
    ...
```

**Dependencies**:
```
slowapi==0.1.9  # Rate limiting
```

### Phase 9: Audit Logging

**File**: `/web/backend/app/models/audit_log.py` (NEW)

Create audit log model:
```python
class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    action = Column(String)  # "totp_enabled", "totp_disabled", "backup_code_used", "totp_failed", etc.
    ip_address = Column(String, nullable=True)
    user_agent = Column(String, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    details = Column(Text, nullable=True)  # JSON metadata
```

Log all security events:
- TOTP enabled
- TOTP disabled
- TOTP verification success
- TOTP verification failure (with counter)
- Backup code used
- Account lockout (after N failures)

### Phase 10: Account Lockout Protection

**File**: `/web/backend/app/models/user.py`

Add lockout fields:
```python
failed_totp_attempts = Column(Integer, default=0)
locked_until = Column(DateTime, nullable=True)
```

**Logic**:
- Lock account for 15 minutes after 5 failed TOTP attempts
- Reset counter on successful verification
- Show lockout time remaining in error message

### Phase 11: Mobile App Support (Future)

**Note**: Current plan focuses on web admin panel. Mobile app already has:
- Login screen: `/mobile/src/screens/LoginScreen.tsx`
- API client: `/mobile/src/api/client.ts`

**Future Enhancement**: Add TOTP verification step in mobile login flow when user role is ROOT.

---

## Implementation Order

### Sprint 1: Core Backend (Days 1-3)
1. ✅ Add database columns (user model updates)
2. ✅ Create TOTP utility module (`totp.py`)
3. ✅ Add pyotp, qrcode dependencies
4. ✅ Implement TOTP setup endpoint
5. ✅ Implement TOTP verify endpoint
6. ✅ Update JWT to include totp_verified claim
7. ✅ Update auth dependencies for 2FA check

### Sprint 2: Frontend Setup Flow (Days 4-5)
1. ✅ Create TOTP setup page (QR code display)
2. ✅ Update login page for two-step flow
3. ✅ Handle requires_2fa_setup redirect
4. ✅ Implement backup code display and download

### Sprint 3: Security & Polish (Days 6-7)
1. ✅ Add rate limiting on verification endpoints
2. ✅ Implement audit logging
3. ✅ Add account lockout after failed attempts
4. ✅ Create security settings page
5. ✅ Add "disable 2FA" functionality
6. ✅ Test existing admin user migration flow

### Sprint 4: Testing & Documentation (Day 8)
1. ✅ Write unit tests for TOTP functions
2. ✅ Write integration tests for auth flow
3. ✅ Test with Google Authenticator, Authy, Microsoft Authenticator
4. ✅ Update README with 2FA setup instructions
5. ✅ Create ADR document for 2FA architecture decision

---

## File Summary

### Files to Create (NEW):
1. `/web/backend/app/totp.py` - TOTP utility functions
2. `/web/backend/app/models/audit_log.py` - Audit log model
3. `/web/frontend/src/pages/admin/TOTPSetup.tsx` - Setup page
4. `/web/frontend/src/pages/admin/SecuritySettings.tsx` - 2FA management
5. `/web/backend/tests/test_totp.py` - Unit tests
6. `/documentation/architecture/adr/ADR-0XX-two-factor-authentication.md` - Architecture decision

### Files to Modify:
1. `/web/backend/app/models/user.py` - Add TOTP columns
2. `/web/backend/app/schemas/user.py` - Add TOTP schemas
3. `/web/backend/app/auth.py` - Update auth dependencies
4. `/web/backend/app/routers/auth.py` - Add TOTP endpoints
5. `/web/frontend/src/pages/admin/Login.tsx` - Two-step login
6. `/web/frontend/src/components/AdminLayout.tsx` - Add security settings link
7. `/web/backend/requirements.txt` - Add pyotp, qrcode, slowapi, Pillow
8. `/web/backend/app/main.py` - Add rate limiter

---

## Technical Decisions

### Why TOTP instead of SMS?
- **No recurring costs**: SMS requires paid API (Twilio ~$0.01/message)
- **Works offline**: TOTP doesn't need internet once set up
- **More secure**: SMS vulnerable to SIM swapping attacks
- **Industry standard**: Used by Google, GitHub, AWS, etc.
- **User preference**: User already mentioned using Google Authenticator

### Why Backup Codes?
- **Recovery mechanism**: If user loses phone/authenticator
- **Industry standard**: GitHub, Google, and other services use this pattern
- **Better UX**: Alternative to "contact support" recovery
- **One-time use**: Each code can only be used once, then invalidated

### Why Mandatory for ROOT?
- **Security-critical role**: ROOT users have full system access
- **User management power**: Can create/delete other admins
- **Data access**: Can view all user data
- **Low user count**: Only a few ROOT users, minimal friction
- **Compliance**: Many security frameworks require MFA for admin access

### JWT with totp_verified Claim
- **Stateless**: No session storage needed
- **Efficient**: Single token contains all auth state
- **Secure**: Signed with SECRET_KEY
- **Flexible**: Can verify 2FA per-request or per-session

### Database Storage
- **Encrypted TOTP secret**: Store hashed (bcrypt) not plaintext
- **Hashed backup codes**: Use same bcrypt as passwords
- **Nullable columns**: Allows gradual rollout, optional for non-ROOT

---

## Security Considerations

### Threats Mitigated:
- ✅ Stolen password attacks (TOTP provides second factor)
- ✅ Database breach (backup codes hashed, TOTP secret encrypted)
- ✅ Brute force (rate limiting + account lockout)
- ✅ Phishing (TOTP codes expire after 30 seconds)

### Remaining Considerations:
- ⚠️ QR code phishing: Users must verify they're on correct domain
- ⚠️ Backup code storage: Users must store codes securely (not in plaintext file)
- ⚠️ Secret key security: Ensure SECRET_KEY environment variable is strong
- ⚠️ Time synchronization: Server and client clocks must be reasonably in sync (±30s)

### Best Practices Implemented:
- 6-digit codes (standard TOTP)
- 30-second time window (standard)
- SHA-1 algorithm (TOTP standard, despite SHA-1 deprecation for other uses)
- 10 backup codes (GitHub standard)
- Account lockout after 5 failures (industry standard)
- Audit logging for compliance
- Rate limiting to prevent attacks

---

## User Experience Flow

### First-Time Setup (Existing Admin):
1. Admin logs in with username/password
2. Redirected to "Set Up Two-Factor Authentication" page
3. See QR code and instructions: "Scan this with Google Authenticator"
4. See manual entry key as alternative
5. Backup codes displayed: "Save these in a secure location - you won't see them again"
6. Download backup codes as text file
7. Enter first TOTP code from app to verify
8. Success! Redirected to admin dashboard

### Daily Login (After Setup):
1. Enter username and password
2. Page updates: "Enter the 6-digit code from your authenticator app"
3. Enter current TOTP code from Google Authenticator
4. Login successful → Admin dashboard

### Lost Device Recovery:
1. Enter username and password
2. Click "Use a backup code instead"
3. Enter one of the 10 backup codes
4. Login successful with warning: "Backup code used - you have X codes remaining"
5. Recommended: Go to Security Settings → Regenerate backup codes

### Disable 2FA (If Needed):
1. Go to Admin → Security Settings
2. Click "Disable Two-Factor Authentication"
3. Enter current password + current TOTP code
4. Confirm: "Are you sure? This will reduce your account security"
5. 2FA disabled
6. **Note**: Will be forced to re-enable on next login (since mandatory for ROOT)

---

## Testing Strategy

### Unit Tests:
- TOTP secret generation
- QR code generation
- TOTP code verification (with time drift)
- Backup code generation and hashing
- Backup code verification and invalidation

### Integration Tests:
- Full setup flow (API calls)
- Login with TOTP
- Login with backup code
- Failed login attempts and lockout
- Disable/re-enable 2FA

### Manual Testing:
- Test with Google Authenticator (Android/iOS)
- Test with Microsoft Authenticator
- Test with Authy
- Test time drift scenarios
- Test network interruptions
- Test rapid code entry (prevent replay)

### Browser Testing:
- Chrome, Firefox, Safari
- Mobile browsers (iOS Safari, Chrome Mobile)
- Check QR code scanning from mobile device

---

## Deployment Considerations

### Environment Variables:
```bash
# .env (backend)
SECRET_KEY=<strong-random-key>  # CRITICAL: Must be production-ready
DATABASE_URL=<database-connection>
TOTP_ISSUER="Aquarius Admin"  # Shows in authenticator app
```

### Database Migration:
```bash
# Run migration to add new columns
python -m alembic upgrade head

# Or use SQLAlchemy to add columns dynamically
```

### Dependency Installation:
```bash
pip install pyotp==2.9.0 qrcode==7.4.2 Pillow==10.2.0 slowapi==0.1.9
```

### Rollout Plan:
1. Deploy to staging environment first
2. Test with staging admin account
3. Deploy to production during low-traffic period
4. Monitor error logs for first 24 hours
5. Notify existing admins: "You will be prompted to set up 2FA on next login"

---

## Future Enhancements (Out of Scope)

### Phase 2 Features:
- Email OTP as backup method
- WebAuthn/FIDO2 support (security keys)
- Remember device for 30 days (reduce 2FA prompts)
- 2FA optional for PLANER role
- Admin dashboard showing 2FA adoption rate
- SMS OTP (if budget allows)

### Admin Tools:
- View all users' 2FA status
- Force 2FA reset for compromised accounts
- Bulk enable 2FA for multiple users
- 2FA compliance reporting

### Mobile App:
- Native TOTP setup flow for mobile judges
- Biometric unlock after 2FA verification
- Push notification 2FA (future alternative)

---

## Documentation Updates Required

### User Documentation:
1. **Admin Guide**: "Setting Up Two-Factor Authentication"
   - Step-by-step with screenshots
   - Recommended authenticator apps
   - How to use backup codes
   - What to do if device is lost

2. **Security Best Practices**:
   - Store backup codes securely (password manager)
   - Don't share TOTP codes
   - Use strong passwords in addition to 2FA

### Technical Documentation:
1. **ADR**: Architecture Decision Record for 2FA implementation
2. **API Documentation**: Update OpenAPI/Swagger with new endpoints
3. **Deployment Guide**: Migration steps for production
4. **Troubleshooting Guide**: Common 2FA issues and solutions

---

## Success Criteria

### Functional Requirements:
- ✅ ROOT users cannot access admin panel without 2FA
- ✅ TOTP setup flow works with Google Authenticator
- ✅ Login accepts valid TOTP codes
- ✅ Backup codes work for recovery
- ✅ Account locks after 5 failed attempts
- ✅ All security events are logged

### Security Requirements:
- ✅ TOTP secrets encrypted at rest
- ✅ Backup codes hashed (not plaintext)
- ✅ Rate limiting prevents brute force
- ✅ JWT includes 2FA verification status
- ✅ No bypasses for 2FA requirement

### Usability Requirements:
- ✅ Setup takes < 2 minutes
- ✅ Login with 2FA adds < 10 seconds
- ✅ Clear error messages for common issues
- ✅ Recovery mechanism (backup codes) available
- ✅ Works on mobile and desktop browsers

---

## Risk Mitigation

### Risk: Users Lock Themselves Out
- **Mitigation**: Backup codes, clear setup instructions, audit log for admin reset

### Risk: Time Synchronization Issues
- **Mitigation**: Accept ±1 time window (90 seconds total validity)

### Risk: QR Code Not Scannable
- **Mitigation**: Provide manual text entry option

### Risk: Lost Backup Codes
- **Mitigation**: Another ROOT admin can reset 2FA, or manual database update as last resort

### Risk: Performance Impact
- **Mitigation**: TOTP verification is fast (<1ms), minimal database overhead

---

## Estimated Effort

- **Backend Development**: 2-3 days
- **Frontend Development**: 2 days
- **Testing**: 1-2 days
- **Documentation**: 1 day
- **Total**: ~6-8 days for complete implementation

---

## Dependencies

### Python Packages (Backend):
```txt
pyotp==2.9.0          # TOTP algorithm implementation
qrcode==7.4.2         # QR code generation
Pillow==10.2.0        # Image library (required by qrcode)
slowapi==0.1.9        # Rate limiting middleware
```

### No Frontend Dependencies:
- QR codes rendered as Base64 images (no special libraries needed)
- Standard React form handling for TOTP input

---

This implementation follows industry best practices and provides a secure, user-friendly 2FA solution for the Aquarius admin panel.
