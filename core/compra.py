class Compra:
    def __init__(self, request):
        self.request = request
        self.session = request.session

        compra = self.session.get("compra")
        if not compra:
            self.session["compra"]={}
            self.compra = self.session["compra"]
        else:
            self.compra= compra

    def agregar(self,id_producto, producto, precio):
        id = str(id_producto)
        if id not in self.compra.keys():
            self.compra[id]={
                "id_producto" : id_producto,
                "nombre": producto,
                "precio": precio,
                "Unidades":1,

            }
        else:
            self.compra[id]["Unidades"]+=1
            self.compra[id]["precio"]+=precio

        print("ESTA ES LA COMPRA",self.session["compra"])
        
        self.guardar_compra()
    
    def guardar_compra(self):
        self.session["compra"] = self.compra
        self.session.modified = True

    def eliminar(self, id_producto):
        id = str(id_producto)
        if id in self.compra:
            del self.compra[id]
            self.guardar_compra()
    
    def restar(self, id_producto, precio):
        id = str(id_producto)
        if id in self.compra.keys():
            self.compra[id]["Unidades"]-=1
            self.compra[id]["precio"]-=precio
            
            self.guardar_compra()

            if self.compra[id]["Unidades"]<=0:
                self.eliminar(id_producto)
            
                self.guardar_compra()
        
    def limpiar (self):
        self.session["compra"]={}
        self.session.modified= True