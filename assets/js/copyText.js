// copy text, requires tooltips enabled
const copyBtns = document.getElementsByClassName("text-copy");
Array.from(copyBtns).forEach(function(element) {
  element.addEventListener('click', copyText);
});
function copyText() {
  let copyIconId = this.id;
  let textToCopyId = this.getAttribute("data-copy");
  const textToCopy = document.getElementById(textToCopyId).innerText;
  // const textToCopy = textToCopyId.setSelectionRange();
  navigator.clipboard.writeText(textToCopy).then(function() {
    let tooltipElement = document.getElementById(copyIconId);
    let tooltip = bootstrap.Tooltip.getInstance(tooltipElement);
    setTimeout(() => { tooltip.hide(); }, 1000);
  }, function(err) {
    console.error('Async: Could not copy text: ', err);
  });
}