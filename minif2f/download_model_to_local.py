from transformers import AutoModel, AutoTokenizer

# Model name from Hugging Face
model_name = "internlm/internlm2_5-step-prover"

# Download the model and tokenizer
model = AutoModel.from_pretrained(model_name,trust_remote_code=True)
tokenizer = AutoTokenizer.from_pretrained(model_name,trust_remote_code=True)

# Define the local directory where you want to save the model
save_directory = "/scratch/gpfs/st3812/models/internlm2_5-step-prover"

# Save the model and tokenizer locally
model.save_pretrained(save_directory)
tokenizer.save_pretrained(save_directory)

print(f"Model saved locally at: {save_directory}")