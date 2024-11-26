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
        return path + "#page=" + page + "&zoom=" + zoom +"&pagemode="+pagemode + "&view=Fit";
    },

    // GENERATE THE STYLE WITH THE WIDTH AND THE CORRESPONDING RATIO
    getStyle: function (ratio, width = this.default.width) {
        return "width:" + width + "; aspect-ratio:" + ratio + ";";
    }
}