from flask import Flask, render_template, request, redirect, url_for, flash, session
app = Flask(__name__)
import ast
app.secret_key = 'holaMundoCruel'

def actualizarDatos():
    """
    Esta funcion por medio de la base de datos del programa
    recupera la infromacion que se encuentra ahi al retornar una lista con todos los usuarios
    """
    listaUsuarios=[]
    archivo=open("baseDeDatos.txt","r")
    if archivo.readline()=="":
        listaUsuarios=[]
    else:
        with open("baseDeDatos.txt","r")as f:
                listaUsuarios=ast.literal_eval(f.read())
    return listaUsuarios


def leerVuelos():
    """
    Esta funcion por medio de los datos de vuelos, crea una lista donde se contiene toda
    la informacionde cada vuelo para poder ser manejada por el programa
    """
    global aerolineas, llegadas, salidas, comidas, numEscalas1, horasSalida, horasLlegada
    archivo=open("infoVuelos.txt",mode="r")
    listaVuelo=[]
    for line in archivo:
        linea=line[:2]+" "+line[2:]
        linea2=linea.split()
        if linea2[6].isdigit()==True:
            linea2.insert(6,"hi")
            aerolinea=linea2[0]
            numeroVuelo=linea2[1]
            salida=linea2[2]
            horaSalida=linea2[3]
            llegada=linea2[4]
            horaLLegada=linea2[5]
            comida=" "
            numEscalas=linea2[7]
            tipoDeAvion=linea2[8]
            diccionario={"aerolinea":aerolinea,"numeroVuelo":numeroVuelo,
                         "salida":salida,"horaSalida":horaSalida,"llegada":llegada,
                         "horaLlegada":horaLLegada,"comida":comida,"numEscalas":numEscalas,
                         "tipoDeAvion":tipoDeAvion}
            listaVuelo.append(diccionario)
        elif linea2[6].isdigit()==False:
            aerolinea=linea2[0]
            numeroVuelo=linea2[1]
            salida=linea2[2]
            horaSalida=linea2[3]
            llegada=linea2[4]
            horaLLegada=linea2[5]
            comida=linea2[6]
            numEscalas=linea2[7]
            tipoDeAvion=linea2[8]
            diccionario={"aerolinea":aerolinea,"numeroVuelo":numeroVuelo,
                         "salida":salida,"horaSalida":horaSalida,"llegada":llegada,
                         "horaLlegada":horaLLegada,"comida":comida,"numEscalas":numEscalas,
                         "tipoDeAvion":tipoDeAvion}
            listaVuelo.append(diccionario)
            
            
    aerolineas=[]
    salidas=[]
    llegadas=[]
    comidas=[]
    numEscalas1=[]
    horasSalida=[]
    horasLlegada=[]
    contador=0
    while contador<len(listaVuelo):
        if listaVuelo[contador]["aerolinea"] in aerolineas:
            pass
        else:
            aerolineas.append(listaVuelo[contador]["aerolinea"])
                
        if listaVuelo[contador]["salida"] in salidas:
             pass
        else:
            salidas.append(listaVuelo[contador]["salida"])
            
        if listaVuelo[contador]["llegada"] in llegadas:
             pass
        else:
            llegadas.append(listaVuelo[contador]["llegada"])
            
        if listaVuelo[contador]["comida"] in comidas:
             pass
        else:
            comidas.append(listaVuelo[contador]["comida"])
            
        if listaVuelo[contador]["numEscalas"] in numEscalas1:
             pass
        else:
            numEscalas1.append(listaVuelo[contador]["numEscalas"])

        if listaVuelo[contador]["horaSalida"] in horasSalida:
             pass
        else:
            horasSalida.append(listaVuelo[contador]["horaSalida"])

        if listaVuelo[contador]["horaLlegada"] in horasLlegada:
             pass
        else:
            horasLlegada.append(listaVuelo[contador]["horaLlegada"])
            
        contador+=1
    for i in comidas:
        if i=="hi":
            comidas.remove("hi")
    return listaVuelo

@app.route("/iniciarSesion", methods=["GET","POST"])
def iniciarSesion():
    """
    Esta funcion crea la pestaña del login y recive la informacion de esta, para auenticar
    al usuario, ademas de redirijirlo a la pagina principal si este atenticado al
    pasar la comprobacion, o a la creacion
    de cuenta si el usuario lo decide
    """
    if request.method == "POST":
        listaUsuarios=actualizarDatos()
        ID=request.form["iniciarSesion"]
        contraseña=request.form["contraseña"]
        contador=0
        n=False
        while contador<len(listaUsuarios):
            if listaUsuarios[contador]["ID"]==ID and listaUsuarios[contador]["contraseña"]==contraseña:
                n=True
                session["usuario"]=listaUsuarios[contador]["ID"]+" "+str(contador)
                return redirect(url_for("paginaPrincipal"))
            contador+=1
        if n==False:
            flash("nombre de usuario o contraseña incorrectos")
            return redirect(url_for("iniciarSesion"))
            
    return render_template("login.html", title="iniciarSesion")

@app.route("/crearCuenta", methods=["GET","POST"])
def crearCuenta():
    """
    Esta funcion crea la pestaña de crear cuenta y permite que el usuario se involucre en
    la base de datos del sistema, ademas de redirigir al usuario al inicio de sesion despues
    de haberse registrado
    """
    leerVuelos()
    global aerolineas
    print(aerolineas)
    if request.method == "POST":
        listaUsuarios=actualizarDatos()
        ID=request.form["nombreUsuario"]
        contraseña=request.form["contraseña"]
        preferencias=request.form.getlist("aerolineas")
        usuario={"ID":ID,"contraseña":contraseña,"preferencias":preferencias,"historial":[]}            
        contador=0
        n=False
        while contador<len(listaUsuarios):
            if listaUsuarios[contador]["ID"]==ID:
                flash("el nombre de usuario ya esta en uso")
                n=True
                return redirect(url_for("crearCuenta"))
                break
            contador+=1
        if n==False:
            listaUsuarios.append(usuario)
            archivo=open("baseDeDatos.txt", mode="w")
            archivo.write(str(listaUsuarios))
            archivo.close()
            return redirect(url_for("iniciarSesion"))
        
        
    return render_template("crearCuenta.html", title="crearCuenta", aerolineas=aerolineas)

@app.route("/", methods=["GET","POST"])
def paginaPrincipal():
    """
    Esta funcion crea la pestaña de crear cuenta y funciona como punto de partida para dar
    inicio a las diferentes actividades que puede hacer el usuario en el programa(reservarVuelo,
    iniciar sesion o cerrar sesion y consultar informacion del usuario)
    """
    listaUsuarios=actualizarDatos()
    if request.method == "POST":
        if request.form['boton'] == "Reserva tu vuelo":
            if "usuario" in session: 
                return redirect(url_for("reservarVuelo"))
            else:
                flash("Debe iniciar sesion")
                return redirect(url_for("paginaPrincipal"))
        if request.form['boton'] == "Informacion del usuario":
            if "usuario" in session: 
                return redirect(url_for("infoUsuario"))
            else:
                flash("Debe iniciar sesion")
                return redirect(url_for("paginaPrincipal"))
        if request.form['boton'] == "Cerrar sesion":
            session.pop("usuario",None)
            return redirect(url_for("iniciarSesion"))
        if request.form['boton'] == "Iniciar sesion":
           return redirect(url_for("iniciarSesion"))
    return render_template("paginaPrincipal.html", title="paginaPrincipal", session=session)

@app.route("/reservarVuelo", methods=["GET","POST"])
def reservarVuelo():
    """
    Esta funcion crea la pestaña de reservas de vuelo y recive la informacion del usuario en
    cuanto a preferencias para la reserva, para asi generar los resultados que podrian ser de
    interes para este a la hora de separar un vuelo
    """
    listaVuelos=leerVuelos()
    listaUsuarios=actualizarDatos()
    global llegadas, salidas, comidas, numEscalas1, resultado, horasLlegada, horasSalida, llegada, salida
    resultado=[]
    if request.method == "POST":
        salida=request.form["salidas"]
        llegada=request.form["llegadas"]
        comida=request.form["comidas"]
        numEscalas=request.form["numEscalas"]
        considerarAero=request.form["considerarAero"]
        horaLlegada=request.form["horaLlegada"]
        horaSalida=request.form["horaSalida"]
        posibilidades=[]
        aux=[]
        for i in listaVuelos:
            if i["salida"]== salida and i["llegada"]== llegada:
                posibilidades.append(i)
                resultado.append("")
        if considerarAero=="si":
            usuario=session["usuario"].split()
            aerolineas=listaUsuarios[int(usuario[1])]["preferencias"]
            for i in posibilidades:
                contador=0
                if i["comida"]==comida:
                    contador+=1
                if i["horaLlegada"]==horaLlegada:
                    contador+=1
                if i["horaSalida"]==horaSalida:
                    contador+=1
                if i["numEscalas"]==numEscalas:
                    contador+=1
                for x in aerolineas:
                    if x in i["aerolinea"]:
                        contador+=1
                aux.append(contador)
                i["contador"]=contador
            aux.sort(reverse=True)
            for i in posibilidades:
                indice=aux.index(i["contador"])
                aux[indice]="a"
                resultado[indice]=i
        if considerarAero=="no":
            for i in posibilidades:
                contador=0
                if i["comida"]==comida:
                    contador+=1
                if i["numEscalas"]==numEscalas:
                    contador+=1
                if i["horaLlegada"]==horaLlegada:
                    contador+=1
                if i["horaSalida"]==horaSalida:
                    contador+=1
                aux.append(contador)
                i["contador"]=contador
            aux.sort(reverse=True)
            for i in posibilidades:
                indice=aux.index(i["contador"])
                aux[indice]="a"
                resultado[indice]=i
        return redirect(url_for("resultados"))                          
    return render_template("reservaVuelo.html", title="reservarVuelo", llegadas=llegadas,
                           salidas=salidas, comidas=comidas, numEscalas1=numEscalas1,
                           resultado=resultado, horasSalida=horasSalida,
                           horasLlegada=horasLlegada)

@app.route("/resultados", methods=["GET","POST"])
def resultados():
    """
    Esta funcion crea la pestaña que muestra los resultados de la busqueda del usuario,
    para asi recivir la desicion del usuario sobre su ultima eleccion de reserva. Ademas de esto,
    existe la posibilidad de mostrar la animacion del vuelo
    """
    listaUsuarios=actualizarDatos()
    global resultado
    if request.method == "POST":
        vuelo=request.form["vuelo"]
        usuario=session["usuario"].split()
        listaUsuarios[int(usuario[1])]["historial"].append(vuelo)
        archivo=open("baseDeDatos.txt", mode="w")
        archivo.write(str(listaUsuarios))
        archivo.close()
        return redirect(url_for("paginaPrincipal"))
        
        
    return render_template("posiblesVuelos.html", title="resultados",resultado=resultado)


@app.route("/animacion", methods=["GET","POST"])
def animacion():
    """
    Esta funcion crea la pestaña de la animacion a partir de los datos recividos anteriormente
    """
    coordenadas=[]
    global llegada, salida
    archivo=open("coordenadas.txt", mode="r")
    aux1=[]
    aux2=[]
    for i in archivo:
        linea=i.split()
        if linea[0]==salida:
            aux1.append(linea[0])
            aux1.append(linea[2])
            aux1.append(linea[3])
            coordenadas.insert(0,aux1)
        if linea[0]==llegada:
            aux2.append(linea[0])
            aux2.append(linea[2])
            aux2.append(linea[3])
            coordenadas.insert(1,aux2)
    print(coordenadas)
    salidax=coordenadas[0][1]
    saliday=coordenadas[0][2]
    llegadax=coordenadas[1][1]
    llegaday=coordenadas[1][2]
    
        
    return render_template("animacion.html", title="resultados",salidax=salidax, saliday=saliday,
                           llegadax=llegadax, llegaday=llegaday)


@app.route("/infoUsuario", methods=["GET","POST"])
def infoUsuario():
    """
    Esta funcion crea la pestaña que muestra la informacion del usuario como tambien
    el historial de vuelos. Ademas de esto, se le da la posibilidad al usuario de
    borrar el historial y de cambiar su informacion
    """
    listaUsuarios=actualizarDatos()
    usuario=session["usuario"].split()
    indice=int(usuario[1])
    if request.method == "POST":
        if request.form['boton'] == "Borrar historial":
            listaUsuarios[indice]["historial"]=[]
            archivo=open("baseDeDatos.txt", mode="w")
            archivo.write(str(listaUsuarios))
            archivo.close()
            return redirect(url_for("infoUsuario"))
            
        if request.form['boton'] == "Cambiar informacion":
            return redirect(url_for("cambiarInfo"))
        
    return render_template("informacionUsuario.html", title="informacionUsuario",
                           listaUsuarios=listaUsuarios,indice=indice)


@app.route("/cambiarInfo", methods=["GET","POST"])
def cambiarInfo():
    """
    Esta funcion crea la pestaña de cambiar informacion y permite que el usuario cambie
    su ID, contraseña y preferencias, conservando su historial de vuelos
    """
    leerVuelos()
    global aerolineas
    listaUsuarios=actualizarDatos()
    usuario=session["usuario"].split()
    indice=int(usuario[1])
    if request.method == "POST":
        nombreUsuario=request.form["nombreUsuario"]
        contraseña=request.form["contraseña"]
        contraseña2=request.form["contraseña2"]
        nuevasAerolineas=request.form.getlist("aerolineas")
        if contraseña==listaUsuarios[indice]["contraseña"]:
            aux=[]
            for i in listaUsuarios:
                aux.append(i["ID"])
            if nombreUsuario in aux:
                flash("Nombre de usuario en uso")
                return redirect(url_for("cambiarInfo"))
            else:
                listaUsuarios[indice]["ID"]=nombreUsuario
                listaUsuarios[indice]["contraseña"]=contraseña2
                listaUsuarios[indice]["preferencias"]=nuevasAerolineas
                session["usuario"]=nombreUsuario+" "+str(indice)
                archivo=open("baseDeDatos.txt", mode="w")
                archivo.write(str(listaUsuarios))
                archivo.close()
                return redirect(url_for("infoUsuario"))
        elif contraseña!=listaUsuarios[indice]["contraseña"]:
            flash("Contraseña incorrecta")
            return redirect(url_for("cambiarInfo"))
            
            
        
    return render_template("cambiarInfo.html", title="informacionUsuario",
                           aerolineas=aerolineas)


if __name__=="__main__":
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(debug=True)
