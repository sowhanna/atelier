import pefile

def script_extract(file_path):
    """Extrait 7 caractéristiques du fichier PE."""
    try:
        pe = pefile.PE(file_path)
        features = {
            "AddressOfEntryPoint": pe.OPTIONAL_HEADER.AddressOfEntryPoint,
            "MajorLinkerVersion": pe.OPTIONAL_HEADER.MajorLinkerVersion,
            "MajorImageVersion": pe.OPTIONAL_HEADER.MajorImageVersion,
            "MajorOperatingSystemVersion": pe.OPTIONAL_HEADER.MajorOperatingSystemVersion,
            "DllCharacteristics": pe.OPTIONAL_HEADER.DllCharacteristics,
            "SizeOfStackReserve": pe.OPTIONAL_HEADER.SizeOfStackReserve,
            "NumberOfSections": len(pe.sections),
        }
        return features
    except Exception as e:
        print(f"Erreur lors du traitement du fichier {file_path}: {e}")
        return None
