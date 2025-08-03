$(document).ready(() => {
    $("#year").text(new Date().getFullYear());
});

$(".wizard-img").on("click", function () {
    const currentSrc = $(this).attr("src");
    if (currentSrc.includes("wizard1.png")) {
     $(this).attr("src", "/static/images/wizard2.png");
} else {
    $(this).attr("src", "/static/images/wizard1.png");
}
});

