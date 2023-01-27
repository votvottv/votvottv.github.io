'use strict';

document.addEventListener('DOMContentLoaded', function() {
  // if the browser doesn't have clipboard APIs, we want the same behavior as no js at all
  if (!navigator.clipboard) { return; }

  // We can't use lektor variables in JS files, so we use a data attribute to get the background color
  let url_copied_bg = document.querySelector('.onion-url-container[data-urlbg]').dataset.urlbg;

  // hide onion URLs, show the "copy" text
  document.querySelectorAll('.onion-url-span').forEach(function(el) { el.style.display = 'none'; });
  document.querySelectorAll('.onion-url-span-uncopied').forEach(function(el) { el.style.display = 'inline-block'; });

  document.querySelectorAll('.onion-url-desktop, .onion-url-mobile').forEach(function(onion_link) {
    onion_link.addEventListener('click', function(event) {
      event.preventDefault();
      navigator.clipboard.writeText(this.href);

      // set up the button's style for the "copied" text

      // we want the button to stay the same size with the new text
      var computedStyle = window.getComputedStyle(this);
      this.style.height = computedStyle.height;
      this.style.width = computedStyle.width;

      this.style.textAlign = 'center';

      var uncopied_span = this.querySelector('.onion-url-span-uncopied');
      uncopied_span.style.display = 'none';

      var copied_span = this.querySelector('.onion-url-span-copied');
      copied_span.style.display = 'inline-block';

      var onion_lock = this.querySelector('.onion-url-lock');
      onion_lock.style.display = 'none';

      // set the background color
      var original_bg = this.style.backgroundColor;
      var original_color = this.style.color;
      this.style.backgroundColor = url_copied_bg;
      this.style.color = 'white';

      // bind `this` to a name so we can use it in the setTimeout callback
      var currentElement = this;
      const revert = function() {
        uncopied_span.style.display = 'inline-block';
        copied_span.style.display = 'none';
        onion_lock.style.display = '';
        currentElement.style.backgroundColor = original_bg;
        currentElement.style.color = original_color;
        currentElement.style.height = '';
        currentElement.style.width = '';
        currentElement.style.textAlign = '';
      };

      // and go back to normal in 2 seconds
      setTimeout(
        revert,
        2000
      );

    }, true);
  });
});

/* language selection handlers */
let languageDropdown;

window.addEventListener('load', function() {
  languageDropdown = document.querySelector('#language-dropdown');
});

function showLanguageSelect() {
  languageDropdown.style.display = 'block';
}
function hideLanguageSelect() {
  languageDropdown.style.display = 'none';
}
function clickHandler() {
  if (window.getComputedStyle(languageDropdown).display != 'block') {
    languageDropdown.style.display = 'block';
  } else {
    languageDropdown.style.display = 'none';
  }
}

// Set the "For your operating system" text to the user's actual OS name
window.addEventListener('DOMContentLoaded', function() {
  // maps a normalized navigator.platform substring to a user-friendly name
  // we'll iterate through the keys and check them as substrings
  const originalBrowserName = document.getElementById('browser-span').innerText;
  const browserSpan = document.getElementById('browser-span');
  const iOSBrowserName = document.getElementById('ios-browser-name').innerText;
  const platformList = [
    'ipad',
    'iphone',
    'linux',
    'x11',
    'mac',
    'windows',
  ];
  const iOSPlatforms = ['ipad', 'iphone'];
  const osSpan = document.getElementById('os-span');
  const platform = navigator.platform.toLowerCase();

  // we're using an old-school for here to get as much browser compatibility as possible.
  for (var index = 0; index < platformList.length; index++) {
    var name = platformList[index];
    if (platform.includes(name)) {
      osSpan.innerText = document.querySelector('[data-os-name~=' + name + ']').innerText;

      if (iOSPlatforms.includes(name)) {
        browserSpan.innerText = iOSBrowserName;
      } else {
        browserSpan.innerText = originalBrowserName;
      }
      break;
    }
  }
});
