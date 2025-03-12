import os
import sys
import asyncio
from BodyMovementRandomForestClassifier import BodyMovementRandomForestClassifier
from LoadTeslaSuit import LoadTeslaSuit


# Agregar la API de Teslasuit al path del sistema
ts_api_path = os.getenv('TESLASUIT_PYTHON_API_PATH')
if not ts_api_path:
    raise EnvironmentError("La variable TESLASUIT_PYTHON_API_PATH no está definida.")
sys.path.append(ts_api_path)


async def main():
    tesla_suit = LoadTeslaSuit()
    mocap = tesla_suit.get_mocap()
    mocap.start_streaming()

    body_movement_classifier = BodyMovementRandomForestClassifier(mocap=mocap)

    try:
        await body_movement_classifier.run()
    except KeyboardInterrupt:
        print("\nPrograma interrumpido por el usuario.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        mocap.stop_streaming()
        print("Programa finalizado.")

if __name__ == "__main__":
    asyncio.run(main())
