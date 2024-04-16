function setCursorPosition(position) {
  let range = document.createRange()
  let selection = window.getSelection()
  range.setStart(typingForm.firstElementChild, position);
  range.collapse(true)

  selection.removeAllRanges()
  selection.addRange(range)
}