window.onload = function () {
    let data = document.getElementsByClassName("data-chart")
    var chart = new CanvasJS.Chart("chartContainer", {
        animationEnabled: true,
        theme: "dark1", // "light1", "light2", "dark1", "dark2"
        title:{
            text: "Estadisticas"
        },
        axisY: {
            title: ""
        },
        data: [{        
            type: "column",  
            showInLegend: false, 
            legendMarkerColor: "white",
            legendText: "",
            dataPoints: [      
                { y: Number(data[0].getElementsByTagName("input")[0].value), label: "Ataque" },
                { y: Number(data[0].getElementsByTagName("input")[1].value),  label: "Defensa" },
                { y: Number(data[0].getElementsByTagName("input")[2].value),  label: "Magia" },
                { y: Number(data[0].getElementsByTagName("input")[3].value),  label: "Dificultad" },
            ]
        }]
    });
    chart.render();
}
