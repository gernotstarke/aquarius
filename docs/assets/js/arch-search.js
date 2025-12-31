/**
 * Architecture Search - Client-side search using Lunr.js
 */
(function() {
  'use strict';

  var searchIndex = null;
  var searchData = null;
  var searchInput = null;
  var resultsContainer = null;

  // Initialize search when DOM is ready
  document.addEventListener('DOMContentLoaded', init);

  function init() {
    searchInput = document.getElementById('arch-search-input');
    resultsContainer = document.getElementById('arch-search-results');

    if (!searchInput || !resultsContainer) {
      return; // Search elements not on this page
    }

    // Load search index
    loadSearchIndex();

    // Set up event listeners
    searchInput.addEventListener('input', debounce(performSearch, 200));
    searchInput.addEventListener('focus', function() {
      if (searchInput.value.length >= 2) {
        resultsContainer.style.display = 'block';
      }
    });

    // Close results when clicking outside
    document.addEventListener('click', function(e) {
      if (!searchInput.contains(e.target) && !resultsContainer.contains(e.target)) {
        resultsContainer.style.display = 'none';
      }
    });

    // Keyboard navigation
    searchInput.addEventListener('keydown', handleKeyboard);
  }

  function loadSearchIndex() {
    fetch('/search.json')
      .then(function(response) {
        return response.json();
      })
      .then(function(data) {
        searchData = data;
        searchIndex = lunr(function() {
          this.ref('url');
          this.field('title', { boost: 10 });
          this.field('content');
          this.field('adr_number', { boost: 5 });

          data.forEach(function(doc) {
            this.add(doc);
          }, this);
        });
      })
      .catch(function(err) {
        console.error('Failed to load search index:', err);
      });
  }

  function performSearch() {
    var query = searchInput.value.trim();

    if (query.length < 2) {
      resultsContainer.style.display = 'none';
      resultsContainer.innerHTML = '';
      return;
    }

    if (!searchIndex) {
      resultsContainer.innerHTML = '<div class="arch-search-loading">Index wird geladen...</div>';
      resultsContainer.style.display = 'block';
      return;
    }

    try {
      // Add wildcard for partial matching
      var results = searchIndex.search(query + '*');
      displayResults(results, query);
    } catch (e) {
      // If lunr query syntax error, try simple search
      try {
        var results = searchIndex.search(query);
        displayResults(results, query);
      } catch (e2) {
        resultsContainer.innerHTML = '<div class="arch-search-no-results">Keine Ergebnisse</div>';
        resultsContainer.style.display = 'block';
      }
    }
  }

  function displayResults(results, query) {
    if (results.length === 0) {
      resultsContainer.innerHTML = '<div class="arch-search-no-results">Keine Ergebnisse für "' + escapeHtml(query) + '"</div>';
      resultsContainer.style.display = 'block';
      return;
    }

    var html = '<ul class="arch-search-list">';

    // Limit to top 10 results
    results.slice(0, 10).forEach(function(result, index) {
      var doc = findDoc(result.ref);
      if (doc) {
        var icon = getTypeIcon(doc);
        var statusBadge = doc.adr_status ? getStatusBadge(doc.adr_status) : '';

        html += '<li class="arch-search-item' + (index === 0 ? ' selected' : '') + '" data-url="' + escapeHtml(doc.url) + '">';
        html += '<a href="' + escapeHtml(doc.url) + '">';
        html += '<span class="arch-search-icon">' + icon + '</span>';
        html += '<span class="arch-search-title">' + highlightMatch(doc.title, query) + '</span>';
        html += statusBadge;
        html += '</a>';
        html += '</li>';
      }
    });

    html += '</ul>';

    if (results.length > 10) {
      html += '<div class="arch-search-more">' + (results.length - 10) + ' weitere Treffer...</div>';
    }

    resultsContainer.innerHTML = html;
    resultsContainer.style.display = 'block';

    // Add click handlers
    resultsContainer.querySelectorAll('.arch-search-item').forEach(function(item) {
      item.addEventListener('click', function(e) {
        if (e.target.tagName !== 'A') {
          window.location.href = item.dataset.url;
        }
      });
    });
  }

  function findDoc(url) {
    for (var i = 0; i < searchData.length; i++) {
      if (searchData[i].url === url) {
        return searchData[i];
      }
    }
    return null;
  }

  function getTypeIcon(doc) {
    if (doc.type === 'adr') {
      return '<i class="fas fa-file-alt"></i>';
    }
    return '<i class="fas fa-file"></i>';
  }

  function getStatusBadge(status) {
    var statusClass = 'adr-status-' + status.toLowerCase();
    var icons = {
      'accepted': '<i class="fas fa-check-circle"></i>',
      'akzeptiert': '<i class="fas fa-check-circle"></i>',
      'proposed': '<i class="fas fa-question-circle"></i>',
      'vorgeschlagen': '<i class="fas fa-question-circle"></i>',
      'deprecated': '<i class="fas fa-exclamation-triangle"></i>',
      'veraltet': '<i class="fas fa-exclamation-triangle"></i>',
      'superseded': '<i class="fas fa-arrow-right"></i>',
      'ersetzt': '<i class="fas fa-arrow-right"></i>',
      'rejected': '<i class="fas fa-times-circle"></i>',
      'abgelehnt': '<i class="fas fa-times-circle"></i>'
    };
    var icon = icons[status.toLowerCase()] || '';
    return '<span class="arch-search-status ' + statusClass + '">' + icon + '</span>';
  }

  function highlightMatch(text, query) {
    if (!text) return '';
    var escaped = escapeHtml(text);
    var regex = new RegExp('(' + escapeRegex(query) + ')', 'gi');
    return escaped.replace(regex, '<mark>$1</mark>');
  }

  function handleKeyboard(e) {
    var items = resultsContainer.querySelectorAll('.arch-search-item');
    var selected = resultsContainer.querySelector('.arch-search-item.selected');
    var index = Array.prototype.indexOf.call(items, selected);

    switch (e.key) {
      case 'ArrowDown':
        e.preventDefault();
        if (index < items.length - 1) {
          if (selected) selected.classList.remove('selected');
          items[index + 1].classList.add('selected');
        }
        break;
      case 'ArrowUp':
        e.preventDefault();
        if (index > 0) {
          if (selected) selected.classList.remove('selected');
          items[index - 1].classList.add('selected');
        }
        break;
      case 'Enter':
        e.preventDefault();
        if (selected) {
          window.location.href = selected.dataset.url;
        }
        break;
      case 'Escape':
        resultsContainer.style.display = 'none';
        searchInput.blur();
        break;
    }
  }

  function debounce(func, wait) {
    var timeout;
    return function() {
      var context = this, args = arguments;
      clearTimeout(timeout);
      timeout = setTimeout(function() {
        func.apply(context, args);
      }, wait);
    };
  }

  function escapeHtml(text) {
    var div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
  }

  function escapeRegex(string) {
    return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  }

})();
