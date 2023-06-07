
function championSearch() {
    //array de elementos en los que buscar
    let championList = document.getElementsByClassName("champion")
    let input = document.getElementById("championKey");
    //valor del input
    let filter = input.value.toUpperCase();
    for (let i = 0; i < championList.length; i++) {
        //champion name
        let champion = championList[i].getElementsByTagName("input")[0].value;
        //comparar si existe en cada uno de estos
        championList[i].style.display = (champion.toUpperCase().indexOf(filter) > -1) ? "" : "none"; 
    }
}