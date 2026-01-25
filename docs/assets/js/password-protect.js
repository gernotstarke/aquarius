/**
 * Password Protection for Aquarius Architecture Section
 *
 * This script provides client-side password protection using SHA-256 hashing.
 * Note: This is NOT cryptographically secure - it's meant to deter casual access.
 * The password hash is stored in the page and can be extracted by determined users.
 *
 * For production use, consider server-side authentication.
 */
(function() {
  'use strict';

  // Configuration - set via data attributes on script tag or window.protectedPageConfig
  var config = window.protectedPageConfig || {};
  var STORAGE_KEY = config.storageKey || 'aquarius_arch_auth';
  var PASSWORD_HASH = config.passwordHash || '';
  var REDIRECT_URL = config.redirectUrl || '/';
  var MAX_ATTEMPTS = config.maxAttempts || 3;
  var LOCKOUT_DURATION = config.lockoutDuration || 300000; // 5 minutes in ms

  // Lockout tracking
  var LOCKOUT_KEY = STORAGE_KEY + '_lockout';
  var ATTEMPTS_KEY = STORAGE_KEY + '_attempts';

  /**
   * Compute SHA-256 hash of a string
   * @param {string} message - The string to hash
   * @returns {Promise<string>} - Hex-encoded hash
   */
  async function sha256(message) {
    var msgBuffer = new TextEncoder().encode(message);
    var hashBuffer = await crypto.subtle.digest('SHA-256', msgBuffer);
    var hashArray = Array.from(new Uint8Array(hashBuffer));
    var hashHex = hashArray.map(function(b) {
      return b.toString(16).padStart(2, '0');
    }).join('');
    return hashHex;
  }

  /**
   * Check if user is currently locked out
   * @returns {boolean}
   */
  function isLockedOut() {
    var lockoutUntil = parseInt(sessionStorage.getItem(LOCKOUT_KEY) || '0', 10);
    if (lockoutUntil > Date.now()) {
      return true;
    }
    // Clear expired lockout
    if (lockoutUntil > 0) {
      sessionStorage.removeItem(LOCKOUT_KEY);
      sessionStorage.removeItem(ATTEMPTS_KEY);
    }
    return false;
  }

  /**
   * Record a failed attempt and potentially trigger lockout
   */
  function recordFailedAttempt() {
    var attempts = parseInt(sessionStorage.getItem(ATTEMPTS_KEY) || '0', 10) + 1;
    sessionStorage.setItem(ATTEMPTS_KEY, attempts.toString());

    if (attempts >= MAX_ATTEMPTS) {
      sessionStorage.setItem(LOCKOUT_KEY, (Date.now() + LOCKOUT_DURATION).toString());
      return true; // Locked out
    }
    return false;
  }

  /**
   * Get remaining attempts
   * @returns {number}
   */
  function getRemainingAttempts() {
    var attempts = parseInt(sessionStorage.getItem(ATTEMPTS_KEY) || '0', 10);
    return Math.max(0, MAX_ATTEMPTS - attempts);
  }

  /**
   * Clear attempt counter (on successful auth)
   */
  function clearAttempts() {
    sessionStorage.removeItem(ATTEMPTS_KEY);
    sessionStorage.removeItem(LOCKOUT_KEY);
  }

  /**
   * Create and show the password modal
   */
  function showPasswordModal() {
    // Create overlay
    var overlay = document.createElement('div');
    overlay.id = 'password-protect-overlay';
    overlay.style.cssText = 'position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,0.85);z-index:10000;display:flex;align-items:center;justify-content:center;';

    // Create modal
    var modal = document.createElement('div');
    modal.style.cssText = 'background:#fff;padding:2rem;border-radius:8px;max-width:400px;width:90%;text-align:center;box-shadow:0 4px 20px rgba(0,0,0,0.3);';

    var remainingAttempts = getRemainingAttempts();

    modal.innerHTML =
      '<style>' +
      '.password-wrapper { position: relative; margin-bottom: 1rem; }' +
      '#password-input { width: 100%; padding: 0.75rem 2.5rem 0.75rem 1rem; font-size: 1rem; border: 2px solid #ddd; border-radius: 4px; box-sizing: border-box; }' +
      '.password-toggle-icon { position: absolute; top: 50%; right: 15px; transform: translateY(-50%); cursor: pointer; color: #777; }' +
      '</style>' +
      '<h2 style="margin:0 0 1rem;color:#333;font-size:1.5rem;">🔒 Geschützter Bereich</h2>' +
      '<p style="margin:0 0 1.5rem;color:#666;">Dieser Bereich ist nur für autorisierte Trainingsteilnehmer zugänglich.</p>' +
      '<form id="password-form">' +
      '<div class="password-wrapper">' +
      '<input type="password" id="password-input" placeholder="Passwort eingeben" autocomplete="current-password" />' +
      '<span id="toggle-password" class="password-toggle-icon"><i class="fas fa-eye"></i></span>' +
      '</div>' +
      '<div id="password-error" style="color:#dc3545;margin-bottom:1rem;display:none;"></div>' +
      '<button type="submit" style="width:100%;padding:0.75rem;font-size:1rem;background:#007bff;color:#fff;border:none;border-radius:4px;cursor:pointer;">Zugang anfordern</button>' +
      '</form>' +
      '<p style="margin:1rem 0 0;font-size:0.85rem;color:#999;">Verbleibende Versuche: <span id="attempts-count">' + remainingAttempts + '</span></p>' +
      '<a href="' + REDIRECT_URL + '" style="display:inline-block;margin-top:1rem;color:#666;text-decoration:none;font-size:0.9rem;">← Zurück zur Startseite</a>';

    overlay.appendChild(modal);
    document.body.appendChild(overlay);

    // Focus the input
    var input = document.getElementById('password-input');
    input.focus();

    // Handle password visibility toggle
    var togglePassword = document.getElementById('toggle-password');
    togglePassword.addEventListener('click', function() {
      var type = input.getAttribute('type') === 'password' ? 'text' : 'password';
      input.setAttribute('type', type);
      this.querySelector('i').classList.toggle('fa-eye');
      this.querySelector('i').classList.toggle('fa-eye-slash');
    });

    // Handle form submission
    var form = document.getElementById('password-form');
    form.addEventListener('submit', async function(e) {
      e.preventDefault();

      var password = input.value;
      var errorEl = document.getElementById('password-error');
      var attemptsEl = document.getElementById('attempts-count');

      if (!password) {
        errorEl.textContent = 'Bitte Passwort eingeben';
        errorEl.style.display = 'block';
        return;
      }

      try {
        var hash = await sha256(password);

        if (hash === PASSWORD_HASH) {
          // Success!
          sessionStorage.setItem(STORAGE_KEY, 'authenticated');
          clearAttempts();
          overlay.remove();
          document.body.style.overflow = '';
        } else {
          // Failed
          var lockedOut = recordFailedAttempt();

          if (lockedOut) {
            errorEl.textContent = 'Zu viele Fehlversuche. Bitte warten Sie 5 Minuten.';
            errorEl.style.display = 'block';
            input.disabled = true;
            form.querySelector('button').disabled = true;
          } else {
            var remaining = getRemainingAttempts();
            attemptsEl.textContent = remaining;
            errorEl.textContent = 'Falsches Passwort. Noch ' + remaining + ' Versuch(e).';
            errorEl.style.display = 'block';
            input.value = '';
            input.focus();
          }
        }
      } catch (err) {
        errorEl.textContent = 'Ein Fehler ist aufgetreten. Bitte versuchen Sie es erneut.';
        errorEl.style.display = 'block';
        console.error('Password check error:', err);
      }
    });

    // Prevent scrolling on body
    document.body.style.overflow = 'hidden';
  }

  /**
   * Show lockout message
   */
  function showLockoutMessage() {
    var overlay = document.createElement('div');
    overlay.style.cssText = 'position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,0.85);z-index:10000;display:flex;align-items:center;justify-content:center;';

    var modal = document.createElement('div');
    modal.style.cssText = 'background:#fff;padding:2rem;border-radius:8px;max-width:400px;width:90%;text-align:center;';

    var lockoutUntil = parseInt(sessionStorage.getItem(LOCKOUT_KEY) || '0', 10);
    var remainingMs = Math.max(0, lockoutUntil - Date.now());
    var remainingMin = Math.ceil(remainingMs / 60000);

    modal.innerHTML =
      '<h2 style="margin:0 0 1rem;color:#dc3545;">⏳ Zugang gesperrt</h2>' +
      '<p style="color:#666;">Zu viele fehlgeschlagene Anmeldeversuche.</p>' +
      '<p style="color:#666;">Bitte warten Sie noch <strong>' + remainingMin + ' Minute(n)</strong>.</p>' +
      '<a href="' + REDIRECT_URL + '" style="display:inline-block;margin-top:1rem;padding:0.75rem 1.5rem;background:#6c757d;color:#fff;text-decoration:none;border-radius:4px;">Zurück zur Startseite</a>';

    overlay.appendChild(modal);
    document.body.appendChild(overlay);
    document.body.style.overflow = 'hidden';
  }

  /**
   * Initialize password protection
   */
  function init() {
    // Check if already authenticated
    if (sessionStorage.getItem(STORAGE_KEY) === 'authenticated') {
      return; // Already authenticated, show page
    }

    // Check for lockout
    if (isLockedOut()) {
      showLockoutMessage();
      return;
    }

    // Show password prompt
    showPasswordModal();
  }

  // Run on DOM ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
