document.addEventListener("DOMContentLoaded", function () {
    const loader = document.getElementById("loader");
    loader.style.display = "block";
    
  
    window.addEventListener("load", function () {
      loader.style.display = "none";
      const header = document.getElementsByTagName("header");
    header.style.display= "none";
    const main = document.getElementsByTagName("main");
    main.style.display= "none";
    const footer = document.getElementsByTagName("footer");
    footer.style.display= "none";
    });


  });