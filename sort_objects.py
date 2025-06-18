def process_objects(objects):
    return [obj['label'] for obj in sorted(objects, key=lambda x: x['score'], reverse=True)]
