from PIL import Image, ImageOps

def convert_to_ico(input_path, output_path):
    img = Image.open(input_path).convert("RGBA")
    datas = img.getdata()

    newData = []
    # Simple threshold for white/light background removal
    for item in datas:
        # Detectar blanco o muy claro (incluyendo artefactos de compresión)
        if item[0] > 230 and item[1] > 230 and item[2] > 230:
            newData.append((255, 255, 255, 0)) # Transparent
        else:
            newData.append(item)

    img.putdata(newData)
    
    # Crop to content (optional but good for icons)
    bbox = img.getbbox()
    if bbox:
        img = img.crop(bbox)
        
    # Resize to square canvas to keep aspect ratio
    max_dim = max(img.size)
    new_img = Image.new("RGBA", (max_dim, max_dim), (0, 0, 0, 0))
    offset = ((max_dim - img.size[0]) // 2, (max_dim - img.size[1]) // 2)
    new_img.paste(img, offset)
    
    # Resize to standard icon size (256x256) for high quality
    final_img = new_img.resize((256, 256), Image.Resampling.LANCZOS)
    
    final_img.save(output_path, format='ICO', sizes=[(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)])
    print(f"Icon saved to {output_path}")

if __name__ == "__main__":
    convert_to_ico("assets/final_logo_v2.png", "assets/rpc.ico")
