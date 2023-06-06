function rankingSearch() {
    //array de elementos en los que buscar
    let itemsRanking = document.getElementsByClassName("ladder-item")
    let input = document.getElementById("searchBarRanking");
    //valor del input
    let filter = input.value.toUpperCase();
    for (let i = 0; i < itemsRanking.length; i++) {
        //summoner name
        let summonerName = itemsRanking[i].getElementsByClassName("ladder-item-summoner")[0].textContent;
        //summoner rank
        let summonerRank = itemsRanking[i].getElementsByClassName("ladder-item-ranking")[0].textContent;
        //comparar si existe en cada uno de estos
        itemsRanking[i].style.display = (summonerName.toUpperCase().indexOf(filter) > -1 || summonerRank.indexOf(filter) > -1) ? "" : "none"; 
    }
}