var PDF_VIEWER = {
  // DEFAULT VALUES
  default: {
    startPage: 1,
    zoom: "page-fit",
    pageMode: "none",
    width: "100%"
  },

  // GENERATE THE PDF STARTING WITH A PATH AND THE URL PARAMS
  getSrcName: function (path, zoom = this.default.zoom, pagemode = this.default.pageMode) {
    params = new URLSearchParams(window.location.search);
    page = params.get("page");
    if (!page) {
      page = this.default.startPage;
    }
    return path + "#page=" + page + "&zoom=" + zoom + "&pagemode=" + pagemode + "&view=Fit";
  },

  // GENERATE THE STYLE WITH THE WIDTH AND THE CORRESPONDING RATIO
  getStyle: function (ratio, width = this.default.width) {
    return "width:" + width + "; aspect-ratio:" + ratio + ";";
  }
}

function generateHTML(tag, tagFeatures = "", text = "") {
  if (tagFeatures) {
    features = " " + tagFeatures;
  }
  else {
    features = "";
  }

  return `<${tag}${features}>${text}</${tag}>`;
}


function getPagefromParams() {
  params = new URLSearchParams(window.location.search);
  page = params.get("Page");
  return page;
}


function addPDFTag(id, link, styleSettings = "", additionalClass = "", pageMode = "none") {
  var element = document.getElementById(id);
  var page = getPagefromParams();
  pageString = ""
  if (page) {
    pageString = `&page=${page}`
  }

  element.innerHTML = generateHTML(tag = "iframe", tagFeatures = `class="embedpdf ${additionalClass}" title="Embedded PDF" src="/_static/pdfjs/web/viewer.html?file=${link}#pagemode=${pageMode}${pageString}" allow="fullscreen" style="${styleSettings}"`);
}