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
            showInLegend: true, 
            legendMarkerColor: "grey",
            legendText: "1 bloque",
            dataPoints: [      
                { y: data[0].getElementsByTagName("input").value, label: "Defensa" },
                { y: 4,  label: "Saudi" },
                { y: 3,  label: "Canada" },
                { y: 6,  label: "Iran" },
            ]
        }]
    });
    chart.render();
    
    }