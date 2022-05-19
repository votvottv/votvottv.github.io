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
      let computedStyle = window.getComputedStyle(this);
      this.style.height = computedStyle.height;
      this.style.width = computedStyle.width;

      this.style.textAlign = 'center';

      let uncopied_span = this.querySelector('.onion-url-span-uncopied');
      uncopied_span.style.display = 'none';

      let copied_span = this.querySelector('.onion-url-span-copied');
      copied_span.style.display = 'inline-block';

      let onion_lock = this.querySelector('.onion-url-lock');
      onion_lock.style.display = 'none';

      // set the background color
      let original_bg = this.style.backgroundColor;
      let original_color = this.style.color;
      this.style.backgroundColor = url_copied_bg;
      this.style.color = 'white';

      // bind `this` to a name so we can use it in the setTimeout callback
      let currentElement = this;
      let revert = function() {
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
let nextDisplay;
let languageDropdown;

window.addEventListener('load', () => {
  nextDisplay = 'block';
  languageDropdown = document.querySelector('#language-dropdown');
})

function showLanguageSelect() {
  console.log('show');
  const dropdown = document.getElementById('language-dropdown');
  dropdown.style.display = 'block';
}
function hideLanguageSelect() {
  console.log('hide');
  const dropdown = document.getElementById('language-dropdown');
  dropdown.style.display = 'none';
}
function clickHandler() {
  console.log('test');
  let nextDisplay_ = window.getComputedStyle(languageDropdown).display;
  languageDropdown.style.display = nextDisplay;
  nextDisplay = nextDisplay_;
}
