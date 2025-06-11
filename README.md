# Efficient-Traffic-Controlling-System-using-Fuzzy-Logic

This project was developed as a mini project for the course **Fuzzy Logic and Neural Network** during my B.tech.

### 👨‍💻 Developed By:
- **Krishanu Dev Sarma (ECB18006)**

---

## 📌 Project Overview

Traffic congestion is a major problem in urban areas. This project presents a **fuzzy logic-based intelligent traffic light controller**, which takes real-time inputs such as the number of waiting and incoming vehicles, and outputs the optimal wait time using fuzzy inference.

The system consists of:
- **Fuzzification** of crisp inputs (number of waiting and incoming cars)
- **Rule-based inference** using fuzzy logic
- **Defuzzification** to generate a crisp output (wait time in seconds)

---

## 🔧 Technologies Used

- **Python**
- scikit-fuzzy
- NumPy
- Matplotlib (for optional visualization)

---

## 📂 Folder Structure

| Folder           | Purpose                                                   |
|------------------|-----------------------------------------------------------|
| Codes/         | Contains all Python scripts divided into modules          |
| Results/       | Example simulation outputs and visualizations             |
| requirements.txt| Python dependencies list                                 |

---

## 🚀 How to Run

1. Clone the repository:
```bash
git clone https://github.com/KrishanuDevSarma/Efficient-Traffic-Controlling-System-using-Fuzzy-Logic.git
cd fuzzy-traffic-control
```
2. Install dependencies:
```bash
pip install -r requirements.txt
```
3. Run the controller:
```bash
python Codes/Model/fuzzy_traffic_controller.py
```
