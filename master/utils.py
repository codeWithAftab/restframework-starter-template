import json
import gzip

def compress_data(data):
    # Convert to JSON
    json_data = json.dumps(data, indent=2)
    # Convert to bytes
    encoded = json_data.encode('utf-8')
    # Compress
    compressed = gzip.compress(encoded)
    return compressed

# compressed_data = compress_data(data=data)
# print(compressed_data)

# decompressed = gzip.decompress(compressed_data)
# print(decompressed)