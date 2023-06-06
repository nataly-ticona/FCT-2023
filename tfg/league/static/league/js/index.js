function championKey() {
    //array de elementos en los que buscar
    let list_champions = document.getElementsByClassName("list_champions")
    let input = document.getElementById("championKey");
    //valor del input
    let filter = input.value.toUpperCase();
    for (let i = 0; i < list_champions.length; i++) {
        //summoner name
        let champion = list_champions[i].getElementsByClassName("champions")[0];
        //comparar si existe en cada uno de estos
        list_champions.innerHTML += champion; 
    }
}