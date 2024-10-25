# user-stories-generator
Generador de historias de usuario estructurado en Gherkin usando LLaMA 3.

---------------------------------------------------------------------------------


Bajar el ejecutable:
```shell
curl -fsSL https://ollama.com/install.sh | sh
```

Iniciar servicio:
```shell
ollama serve
```

Bajar modelo:
```shell
ollama pull llama3
```

Para ver si el puerto utilizado por defecto está activo:
```shell
sudo lsof -i :11434
```

Cerrar el proceso:
```shell
kill -9 <PID>
```

Ver si llama3 está corriendo como servicio
```shell
systemctl list-units --type=service | grep ollama
```

Detener el servicio encontrado:
```shell
sudo systemctl stop ollama.service
```

Where to find the llama3 model:
```shell
/usr/share/ollama/.ollama/models/blobs/
```
