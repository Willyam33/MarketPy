import api
import asyncio
import listen_to_dataset_arrival

if __name__ == '__main__':

    print("Lancement de l'API")
    # Launching API
    asyncio.run(api.launching_API())
    print("Retour de lancement de l'API")
    # Launching listening on new dataset arrival
    listen_to_dataset_arrival.listening()

