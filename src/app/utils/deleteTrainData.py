from Services.qdrant_client import client
from Services.ollama_mistral_service import OllamaService

def deleteTrainData(model):
        vn = OllamaService(config={'client': client, 'model': model})
        training_data = vn.get_training_data()
        if len(training_data.columns) != 0:
            for id_train in training_data['id']:
                training_data = vn.remove_training_data(id=id_train)