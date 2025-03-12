import asyncio
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from BoneStructureLoader import BoneStructureLoader
from CSControl import CSControl


class BodyMovementRandomForestClassifier:
    def __init__(self, mocap):
        self.bone_structure = BoneStructureLoader(mocap)
        self.csgo_control = CSControl()
        self.X = []  # Características
        self.y = []  # Etiquetas
        self.current_pose = None  # Para rastrear la pose actual
        self.last_pose = None  # Para rastrear la última pose detectada
    async def run(self):
        print("Conectando con CS:GO...")
        await self._connect_to_csgo()                               # Conectar con CSGO via telnet

        print("Iniciando recolección de datos de entrenamiento...")
        await self._collect_training_data()                          # Recolectar los datos de entrenamiento

        print("Entrenando modelo de clasificación...")
        self._train_classifier()                                     # Entrenar el modelo

        print("Iniciando control del juego en tiempo real...")
        await self._collect_and_control()  # Empezar a controlar el juego en tiempo real

    async def _connect_to_csgo(self):
        connected = await self.csgo_control.connect()
        if not connected:
            print(
                "No se pudo conectar a CS:GO. El juego debe estar en ejecución con el puerto Telnet habilitado.")
            return

    def _get_relevant_bone_positions(self):
        """Obtiene el vector de posición de los puntos relevantes."""
        bone_names = [
            "Spine",
            "LeftShoulder", "LeftUpperArm", "LeftLowerArm", "LeftHand",
            "RightShoulder", "RightUpperArm", "RightLowerArm", "RightHand"
        ]

        return tuple(
            bone if bone else (0, 0, 0)
            for bone in map(self.bone_structure.get_bone_position, bone_names)
        )

    def _get_relevant_bone_rotations(self):
        """Obtiene el vector de rotación de los puntos relevantes."""
        bone_names = [
            "Spine",
            "LeftShoulder", "LeftUpperArm", "LeftLowerArm", "LeftHand",
            "RightShoulder", "RightUpperArm", "RightLowerArm", "RightHand"
        ]

        return tuple(
            bone if bone else (1, 0, 0, 0)
            for bone in map(self.bone_structure.get_bone_rotation, bone_names)
        )

    def _store_data(self, label):
        """Almacena los datos de una observación con su etiqueta"""
        (
            spine_position,
            left_shoulder_position, left_upper_arm_position, left_lower_arm_position, left_hand_position,
            right_shoulder_position, right_upper_arm_position, right_lower_arm_position, right_hand_position

        ) = self._get_relevant_bone_positions()

        (
            spine_rotation,
            left_shoulder_rotation, left_upper_arm_rotation, left_lower_arm_rotation, left_hand_rotation,
            right_shoulder_rotation, right_upper_arm_rotation, right_lower_arm_rotation, right_hand_rotation

        ) = self._get_relevant_bone_rotations()

        # Añadir los puntos como características (X) y la etiqueta (y)
        self.X.append(np.hstack([
            spine_position,
            left_shoulder_position, left_upper_arm_position, left_lower_arm_position, left_hand_position,
            right_shoulder_position, right_upper_arm_position, right_lower_arm_position, right_hand_position,
            spine_rotation,
            left_shoulder_rotation, left_upper_arm_rotation, left_lower_arm_rotation, left_hand_rotation,
            right_shoulder_rotation, right_upper_arm_rotation, right_lower_arm_rotation, right_hand_rotation
        ]))
        self.y.append(label)

    def _train_classifier(self):
        """Entrena el clasificador RandomForest"""
        X = np.array(self.X)
        y = np.array(self.y)

        # Dividir los datos en entrenamiento y prueba
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Entrenar el modelo
        self.clf = RandomForestClassifier(n_estimators=50, max_depth=10, random_state=42)
        self.clf.fit(X_train, y_train)

        # Evaluar el modelo
        accuracy = self.clf.score(X_test, y_test)
        print(f"Precisión del modelo: {accuracy:.2f}")

    async def _ask_for_pose(self, pose_name):
        """Pide al usuario que realice una pose específica y almacena los datos"""
        print(f"Por favor, realiza la pose: {pose_name}")
        await asyncio.sleep(3)  # Espera 3 segundos para que el usuario haga la pose

        # Almacenar los datos de la pose
        for _ in range(10):  # Capturar múltiples muestras para cada pose
            self._store_data(pose_name)
            await asyncio.sleep(0.2)

        print(f"Pose '{pose_name}' almacenada correctamente.")

    async def _collect_training_data(self):
        """Recolecta los datos de entrenamiento para varias poses"""
        poses = ["avanzar", "retroceder", "girar_izquierda", "girar_derecha", "disparar", "apuntar", "neutral"] #, "agacharse", "saltar"]

        # Añadimos una pose "neutral" para cuando el usuario no está haciendo ningún movimiento

        for pose in poses:
            await self._ask_for_pose(pose)  # Espera que el usuario haga la pose y la almacena
            await asyncio.sleep(1)  # Espera entre poses

        print("Datos de entrenamiento recolectados correctamente.")

    def _predict_pose(self):
        """Predice la pose en base a los datos actuales"""
        (
            spine_position,
            left_shoulder_position, left_upper_arm_position, left_lower_arm_position, left_hand_position,
            right_shoulder_position, right_upper_arm_position, right_lower_arm_position, right_hand_position

        ) = self._get_relevant_bone_positions()

        (
            spine_rotation,
            left_shoulder_rotation, left_upper_arm_rotation, left_lower_arm_rotation, left_hand_rotation,
            right_shoulder_rotation, right_upper_arm_rotation, right_lower_arm_rotation, right_hand_rotation

        ) = self._get_relevant_bone_rotations()

        features = np.hstack([
            spine_position,
            left_shoulder_position, left_upper_arm_position, left_lower_arm_position, left_hand_position,
            right_shoulder_position, right_upper_arm_position, right_lower_arm_position, right_hand_position,
            spine_rotation,
            left_shoulder_rotation, left_upper_arm_rotation, left_lower_arm_rotation, left_hand_rotation,
            right_shoulder_rotation, right_upper_arm_rotation, right_lower_arm_rotation, right_hand_rotation
        ]).reshape(1, -1)

        prediction = self.clf.predict(features)
        return prediction[0]  # Devuelve la etiqueta de la pose predicha

    async def _execute_pose_action(self, pose_name):
        """Ejecuta la acción correspondiente en CS:GO dependiendo de la pose detectada"""
        if pose_name == "apuntar" and pose_name != self.last_pose:
            await self.csgo_control.aim()
            self.last_pose = pose_name
            return True

        if pose_name != "apuntar":
            match pose_name:
                case "avanzar":
                    await self.csgo_control.move_forward()
                case "retroceder":
                    await self.csgo_control.move_backwards()
                case "girar_izquierda":
                    await self.csgo_control.move_left()
                case "girar_derecha":
                    await self.csgo_control.move_right()
                case "agacharse":
                    await self.csgo_control.crouch()
                case "saltar":
                    await self.csgo_control.jump()
                case "disparar":
                    await self.csgo_control.shoot()
                case "neutral":
                    pass
                case _:
                    print(f"Acción '{pose_name}' no reconocida.")

            self.last_pose = pose_name
        return True

    async def _collect_and_control(self):
        """Recolecta los datos y ejecuta las acciones en CS:GO en tiempo real"""
        print("Iniciando control por movimiento. Presiona Ctrl+C para detener.")
        try:
            while True:
                pose_name = self._predict_pose()                    # Obtener la predicción de la pose actual

                if pose_name != self.current_pose:
                    print(f"Pose detectada: {pose_name}")
                    self.current_pose = pose_name

                await self._execute_pose_action(pose_name)          # Ejecutar la acción correspondiente en CS:GO
        except KeyboardInterrupt:
            print("\nDetención solicitada. Cerrando conexiones...")
        finally:
            await self.csgo_control.close_connection()
            print("Control por movimiento finalizado.")