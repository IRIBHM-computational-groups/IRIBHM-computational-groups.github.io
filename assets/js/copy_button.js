function copyText(clicked_button) {
  /* Copy text into clipboard */
  navigator.clipboard.writeText(clicked_button.value);
}
