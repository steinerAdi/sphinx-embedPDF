function generateHTML(tag, tagFeatures = "", text = "") {
  if (tagFeatures) {
    features = " " + tagFeatures;
  }
  else {
    features = "";
  }

  return `<${tag}${features}>${text}</${tag}>`;
}


function getPageFromParams() {
  params = new URLSearchParams(window.location.search);
  page = params.get("Page");
  return page;
}


function addPDFTag(id, link, relativOutDir = "", styleSettings = "", additionalClass = "", pageMode = "none", zoom = "auto") {
  var element = document.getElementById(id);
  var page = getPageFromParams();
  pageString = ""
  if (page) {
    pageString = `&page=${page}`
  }

  zoomString = `&zoom=${zoom}`

  element.innerHTML = generateHTML(tag = "iframe", tagFeatures = `class="embedpdf ${additionalClass}" src="${relativOutDir}_static/pdfjs/web/viewer.html?file=${link}#pagemode=${pageMode}${pageString}${zoomString}" allow="fullscreen" style="${styleSettings}"`);
}