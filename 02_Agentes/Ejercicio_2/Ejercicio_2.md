### Asistente virtual de voz

- **Performance:** porcentaje de comandos reconocidos correctamente (idealmente arriba de 90%), tiempo de respuesta menor a 1-2 segundos, tareas completadas sin que el usuario tenga que repetir el comando, satisfacción reportada en reseñas de la app.
- **Environment:** parcialmente observable, ya que no tiene forma de saber todo el contexto del usuario (si está solo, con ruido de fondo, etc.); estocástico por el ruido y los acentos; secuencial, porque una respuesta puede depender de lo que se dijo antes en la conversación; dinámico, ya que el usuario puede interrumpir o cambiar de tema en cualquier momento.
- **Actuators:** bocina para responder por voz, pantalla para mostrar resultados si el dispositivo tiene, enviar comandos a otros aparatos conectados (luces, música, termostato), realizar llamadas o mandar mensajes de texto.
- **Sensors:** micrófono, botón o palabra de activación ("Hey Siri", "Alexa"), acceso a contactos y calendario vía API, conexión a internet para buscar información.

### Robot aspirador doméstico

- **Performance:** porcentaje del área limpiada por sesión, tiempo que tarda en terminar, consumo de batería, número de veces que se atora o choca con algo.
- **Environment:** parcialmente observable, porque solo detecta lo que tiene enfrente o a su alcance; mezcla de determinista y estocástico (el mapa de la casa es fijo pero los muebles se mueven, hay mascotas, etc.); secuencial, ya que su ruta depende de qué zonas ya limpió; dinámico, porque las personas y mascotas se mueven mientras el robot trabaja.
- **Actuators:** motores de las ruedas para desplazarse, motor de succión, cepillos giratorios, mecanismo que lo regresa solo a la base para cargar.
- **Sensors:** sensores infrarrojos de proximidad, sensor de caída para no rodar por las escaleras, cámara o láser para mapear el espacio, sensor de nivel de batería.

### Sistema de recomendación de streaming

- **Performance:** tasa de clics sobre lo recomendado, minutos de reproducción generados, retención de suscriptores mes a mes, qué tan variado es el catálogo que se le muestra al usuario (no repetir siempre lo mismo).
- **Environment:** parcialmente observable, porque el sistema no sabe realmente qué quiere ver el usuario, solo infiere; estocástico, ya que los gustos cambian y hay ruido en los datos; secuencial, porque el historial de lo visto afecta las siguientes recomendaciones; dinámico, porque el catálogo y las tendencias cambian todo el tiempo.
- **Actuators:** mostrar la lista ordenada de sugerencias, mandar notificaciones push, cambiar la miniatura o portada que se muestra de cada título, reproducir automáticamente el siguiente episodio.
- **Sensors:** historial de reproducción, calificaciones y "me gusta" que deja el usuario, tiempo que pasa viendo algo antes de dejarlo, búsquedas que hace dentro de la app.

### Vehículo autónomo en ciudad

- **Performance:** cero colisiones (la métrica más importante), tiempo total del trayecto, respeto a los límites de velocidad y señales de tránsito, qué tan brusca o suave es la conducción.
- **Environment:** parcialmente observable, por oclusiones de otros autos, clima o edificios; estocástico, ya que el comportamiento de peatones y otros conductores no se puede predecir del todo; secuencial y dinámico, porque el tráfico y los semáforos cambian constantemente mientras el vehículo avanza.
- **Actuators:** acelerador, freno, volante/dirección, luces direccionales, bocina.
- **Sensors:** cámaras alrededor del vehículo, LIDAR, radar, GPS, sensores de velocidad en las ruedas.

### Agente de trading algorítmico en bolsa

- **Performance:** retorno sobre la inversión, ratio de Sharpe, pérdida máxima tolerada (drawdown), qué tan rápido ejecuta las órdenes (la latencia importa mucho aquí).
- **Environment:** parcialmente observable, porque no se conoce toda la información del mercado ni lo que van a hacer otros agentes; estocástico; secuencial, ya que las decisiones anteriores afectan el portafolio actual; dinámico, los precios cambian en cuestión de milisegundos.
- **Actuators:** enviar órdenes de compra o venta, ajustar el tamaño de una posición, cancelar órdenes que ya no convienen, mandar una alerta a un operador humano si algo se sale de lo normal.
- **Sensors:** feed de precios en tiempo real, volumen de operaciones, noticias financieras vía API, indicadores técnicos calculados a partir del historial de precios.

### Sistema de diagnóstico médico asistido por IA

- **Performance:** sensibilidad y especificidad del diagnóstico (sobre todo minimizar falsos negativos), tiempo que tarda en dar un resultado, qué tanto coincide con el diagnóstico de un especialista humano.
- **Environment:** parcialmente observable, ya que no siempre están todos los síntomas o estudios disponibles; estocástico, porque una misma enfermedad se manifiesta distinto en cada paciente; más bien episódico, cada caso se analiza de forma bastante independiente del anterior; combina datos discretos (síntomas) y continuos (valores de laboratorio).
- **Actuators:** generar un reporte con el posible diagnóstico y su nivel de confianza, sugerir estudios adicionales, marcar el caso como urgente para que un médico lo revise antes.
- **Sensors:** historial clínico electrónico, resultados de laboratorio, imágenes médicas (rayos X, resonancias), signos vitales y síntomas reportados por el paciente.

### Dron de inspección de infraestructura

- **Performance:** porcentaje del área inspeccionada por vuelo, autonomía de batería usada, precisión al detectar daños como grietas o corrosión, inspecciones completadas sin que un operador tenga que intervenir.
- **Environment:** parcialmente observable, por la resolución de cámara y ángulos ciegos; estocástico, por el viento y el clima; secuencial, la ruta de vuelo depende de lo que ya se inspeccionó; dinámico, las condiciones climáticas pueden cambiar a media inspección.
- **Actuators:** motores/hélices para volar, cámara con zoom y estabilizador (gimbal), modo de retorno automático a la base, luces de señalización.
- **Sensors:** cámara de alta resolución, GPS, altímetro, sensores de proximidad para evitar choques, sensor de viento y batería.

### Agente jugador de ajedrez

- **Performance:** porcentaje de partidas ganadas, rating ELO alcanzado, profundidad de búsqueda por jugada, tiempo usado por movimiento (sobre todo en partidas con reloj).
- **Environment:** totalmente observable, el tablero completo siempre es visible; determinista; secuencial; discreto, tanto las posiciones como los movimientos posibles son un conjunto finito y contable.
- **Actuators:** mover una pieza (en pantalla si es digital, con un brazo robótico si es físico), declarar jaque o jaque mate, pausar/reanudar el reloj de la partida.
- **Sensors:** estado actual del tablero, reloj de la partida, último movimiento realizado por el oponente.
