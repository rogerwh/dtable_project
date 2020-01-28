
function obtener_order_ajax_datatables(d) {
    if (d.order.length > 0) {
        var columna = d.columns[d.order[0].column].name

        var tipo_orden = d.order[0].dir
        if (tipo_orden == "desc") {
            tipo_orden = "-"
        } else {
            tipo_orden = ""
        }

        d.orden_columna = columna;
        d.tipo_orden = tipo_orden;

    }
    return d
}

function obtener_valor_busqueda_individual_datatables(d){
    d.busqueda_individual = []
    for (let key in d.columns) {
        if(d.columns[key].search.value && d.columns[key].searchable == true){
            columna = d.columns[key]
            d.busqueda_individual.push({"columna": columna.name, "valor_busqueda": columna.search.value})            
        }
    }
    d.busqueda_individual = JSON.stringify(d.busqueda_individual)
    return d
}