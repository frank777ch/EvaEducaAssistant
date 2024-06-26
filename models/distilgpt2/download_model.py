from transformers import AutoModelForCausalLM, AutoTokenizer

# Nombre del modelo
model_name = "distilgpt2"

# Descargar y cargar el modelo y el tokenizer
model = AutoModelForCausalLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Crear el directorio para guardar el modelo
model_path = "models/distilgpt2"
os.makedirs(model_path, exist_ok=True)

# Guardar el modelo y el tokenizer localmente
model.save_pretrained(model_path)
tokenizer.save_pretrained(model_path)

print(f"Modelo y tokenizer guardados en {model_path}")