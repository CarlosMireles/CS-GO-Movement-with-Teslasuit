from teslasuit_sdk.ts_mapper import TsBone2dIndex


class BoneStructureLoader:
    def __init__(self, mocap):
        self.mocap = mocap
        self.skeleton_data = self.mocap.get_skeleton_data_on_ready()
        if not self.skeleton_data:
            raise KeyError("No se puede obtener los datos del esqueleto.")
        
    def _load_bone(self, bone):
        selected_bone = self.skeleton_data.get(getattr(TsBone2dIndex, bone, None))
        if not selected_bone:
            self.debug_print(f"Hubo un error al cargar el hueso: {bone} ")
            return None
        return selected_bone
    
    def get_bone_position(self, bone):
        return (
            self._load_bone(bone).position.x,
            self._load_bone(bone).position.y,
            self._load_bone(bone).position.z
        )

    def get_bone_rotation(self, bone):
        return (
            self._load_bone(bone).rotation.w,
            self._load_bone(bone).rotation.x,
            self._load_bone(bone).rotation.y,
            self._load_bone(bone).rotation.z
        )

    @staticmethod
    def debug_print(message):
        print(f"[DEBUG] {message}")
