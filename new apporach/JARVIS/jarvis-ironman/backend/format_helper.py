"""
Helper method to format feature responses
Add this to jarvis_ai.py after the chat method
"""

def _format_feature_response(self, message: str, result: Dict) -> str:
    """Format feature execution result into a natural response"""
    message_lower = message.lower()
    
    # OCR Response
    if 'full_text' in result:
        text = result.get('full_text', '')
        word_count = result.get('total_words', 0)
        return f"I've extracted the text from the image. Found {word_count} words:\n\n{text}"
    
    # Image Generation Response
    if 'image_base64' in result or 'filepath' in result:
        filepath = result.get('filepath', 'generated image')
        return f"I've generated the image and saved it to: {filepath}"
    
    # PowerPoint Response
    if 'slides_count' in result:
        filename = result.get('filename', 'presentation')
        slides = result.get('slides_count', 0)
        return f"I've created a PowerPoint presentation with {slides} slides. Saved as: {filename}"
    
    # Web Scraping Response
    if 'data' in result and isinstance(result['data'], dict):
        title = result.get('title', 'the website')
        return f"I've scraped data from {title}. Found {len(result['data'])} data sections."
    
    # Object Detection Response
    if 'detections' in result:
        count = result.get('count', 0)
        if count > 0:
            objects = [d['class'] for d in result['detections']]
            return f"I detected {count} objects: {', '.join(objects)}"
        return "I didn't detect any objects in the image."
    
    # Screenshot Response
    if 'filepath' in result and 'screenshot' in message_lower:
        return f"Screenshot saved to: {result['filepath']}"
    
    # File Organization Response
    if 'organized' in result:
        total = sum(result['organized'].values())
        return f"I've organized {total} files by type."
    
    # Data Analysis Response
    if 'mean' in result:
        mean = result.get('mean', 0)
        std = result.get('std', 0)
        return f"Analysis complete. Mean: {mean:.2f}, Standard Deviation: {std:.2f}"
    
    # Generic success
    return "Task completed successfully!"
