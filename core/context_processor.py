def total_compra(request):
    total=0
    if "compra" in request.session.keys():
            for key, value in request.session["compra"].items():
                if value["precio"]==None:   
                     value["precio"] = 0
                total += int(value["precio"])
     # Guardar el total de la compra en la sesión
    request.session['total_compra'] = total

    if request.session['total_compra'] == None:
         total = 0


    return {"total_compra": total}