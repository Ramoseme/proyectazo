#importamos
from ursina import *#importamos ursina
from ursina.prefabs.first_person_controller import FirstPersonController #controles de movimiento

#tamaño ventana
app = Ursina(borderless=False) #opcion abrir y cerrar
random.seed(0) #semilla para ramdom
window.size = (1300, 900) #tamaño ventana

#definir el jugador
player = FirstPersonController()
player.collider = "box" #detecta colicion con player

#definir el cubo
class Cubo(Entity): #entidad
    def __init__(self, position=(0, 0, 0)):#posicion por defecto 0
        super().__init__( #llamamos a la entidad
            position=position,#definimos la posicion antes mencionada
            model="cube", #modelo de cubo
            scale=(1, 1), #escala en tupla
            origin_y=-0.5, #centro de origen, -.5 es el centro
            color=color.light_gray, #color cubo
            collider="box" #colisionador
        ) 

#aparecer arriba del cubo
player.position = Vec3(0, 2, 0) #encima del primer cubo
cubo_verde = Cubo(position=(0, 1, 0)) #Primer cubo
cubo_verde.color = color.green #color

#definimos el obstaculo
class Obstaculo(Entity):#entidad del cubo
    def __init__(self, position=(0, 0, 0), texture_path='brick.jpg'):#constructor, posicion y textura
        super().__init__( #llamo a la entidad
            position=position,#posicion
            model="cube",#modelo 
            scale=(1, 9, 1), #tamaño del obstaculo
            texture=texture_path,  # Escoge la textura personalizada aquí
            collider="box" #colisionador asignado al obstaculo
        )

#definicion obstaculos
obstaculo_speed = 0.1 #velocidad del obstaculo
obstaculo_direction = -1 #direccion de movimiento
obstaculo_generated = 0 #cantidad de obstaculos(resgistro)
obstaculos = [] #almacen de obstaculos

#escape para salir
def input(key):#representa la tecla
    if key == "escape": #se asegura que la tecla sea "escape"
        quit()#lo cierra

#logica

def update(): #actualiza dentro de la ventana
    global obstaculos, obstaculo_direction #variables globales(fuera de la funcion)

    if player.position.y <= -30: #detecta si el jugador se cae y reinicia
        player.position = Vec3(0, 25, 0) #posicion de reinicio

#bucle de los obstaculos
    for obstaculo in obstaculos:
        obstaculo.x += obstaculo_speed * obstaculo_direction #actualiza la posicion en el eje X

        if obstaculo.x > 8 or obstaculo.x < -7: #limites del obstaculo
            obstaculo_direction = -obstaculo_direction #invierte los valores para el cambio de posicion

        if player.intersects(obstaculo).hit:#verifica la interseccion (choque) con el jugador
            player.x += obstaculo_speed * obstaculo_direction #desplaza(empuja) al jugador hacia el lado que el obstaculo se mueva

# texto winner
    for cubo in cubos: #recorre todos los cubos generados
        if player.intersects(cubo).hit: #verifica que el jugador toque el bloque
            if cubo.color == color.green: #si el cubo es verde
                show_victory() #muestra el mensaje en la parte superior

#crear el texto 
def show_victory():
    victory_text = Text(text="¡Has ganado!", scale=2, origin=(0, 0), y=0.2, background=True)
    #origin=posicion del texto
    #y= alto del texto
    #background=Configurado en True para mostrar un fondo en el texto

#Mas obstaculos
def generate_obstaculo():
    global obstaculos, obstaculo_direction, obstaculo_generated #uso variables globales

    if obstaculo_generated < 10: #limite de obstaculos
        texture_path = '0s1s.jpg' #textura obstaculo
        obstaculo = Obstaculo(position=(random.randint(1, 6), 1, cubos[-1].z + 5), texture_path=texture_path)
        #crea obstaculos en posiciones aleatorias en eje X
        # toma en cuenta el ultimo obstaculo y crea otro en el eje z cada 5 bloques
        #y añade textura
        obstaculo_direction = -obstaculo_direction#invierte la direccion de movimiento
        obstaculos.append(obstaculo) #agrega el recien creado a la lista
        obstaculo_generated += 0  # contador de obstaculos

cubos = [] #amacenar mas cubos

#cantidad de bloques del camino
num_bloques = 30 #bloques en total del caminos

for z in range(num_bloques): #ciclo q se repite de 0 a 29
    cubo = Cubo(position=(random.randint(1, 6), 1, z)) #generacion y posicion de cubos randoms
    cubo.texture = load_texture('bloque7.jpg')#textura del cubo
    cubo.collider = "box" #colisionador
    cubos.append(cubo)#se añaden estos cubos a la lista

    if z % 5 == 0 and z > 0:#si Z es un múltiplo de 5 y mayor que 0 para determinar si debe generar un obstáculo
        generate_obstaculo()#si se cumple la condicion se llama a la funcion para generar otro obstaculo

cubos[-1].color = color.green#cambia el color del ultimo cubo

#fondo
Sky_texture = "cielo4.jpg"#tnombre de textura
Sky(texture=Sky_texture)#estable el fonfo(cielo)

#musica
music_path = 'USM.mp3'#nombre de musica
music = Audio(music_path, loop=True)#reproduce la cancion en bucle
music.volume = 0.7#volumen
music.play()#inicia el bucle(pone la cancion)

#ejecutar programa
app.run()
