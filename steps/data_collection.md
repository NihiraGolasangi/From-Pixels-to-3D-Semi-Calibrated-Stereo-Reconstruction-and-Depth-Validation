## Image Capture Setup

This section documents the stereo image collection process for reconstructing 3D scene geometry using epipolar constraints.

---

### **Hardware**
- **Device Used:** iPhone 12 Pro Max  
- **Lens Used:** Main wide-angle lens (5.1 mm focal length)  
- **Image Format:** Captured in `.HEIC`, converted to `.JPG`  
- **Zoom Setting:** 1.5× (confirmed no lens switch; focal length from EXIF = 5.1 mm)  
- **Resolution:** 4032 × 3024 px  

---

### 🎯 **Scene Description**
- **Type of Scene:** High-texture, non-repetitive printed poster with ruler taped below for scale.  
- **Lighting:** Indoor, uniform lighting (no shadows or specularities).  
- **Texture Quality:** High (no repeating patterns).  
  

---

### **Stereo Geometry**
- **Number of Views:** 2  
- **Baseline Distance:** 36 cm  
- **Camera Orientation:** Both images taken with phones placed on a stand with mild angular offset (~10–15°).  
- **Object Distance from Camera:** ~76 cm 

---

### **Capture Method**
1. Two images captured from slightly different positions (left and right) to create disparity.  
2. Camera settings were not changed between shots—no zoom or exposure adjustments.  
3. Baseline and object distances were measured using a physical tape for ground truth depth comparison.

---

###  **Scene Schematic**
*Below is a schematic illustration of the stereo setup with all annotated distances.*

![Stereo Setup Schematic](../images/Schematic.jpg)