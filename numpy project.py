"""
Student Performance Analysis (Interactive Version)
--------------------------------------------------
Demonstrates advanced use of NumPy and Pandas with user input, analysis, and visualization.
Only requires this single .py file to run.
"""

import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt

# 1️⃣ Get user input
print("=== Student Performance Analysis ===")
try:
    num_students = int(input("Enter number of students to generate (e.g. 50): "))
    subjects_input = input("Enter subjects separated by commas (e.g. Maths,Physics,Business): ")
except ValueError:
    print("Invalid input. Please enter numbers where needed.")
    exit()

subjects = [s.strip().capitalize() for s in subjects_input.split(",") if s.strip()]
if len(subjects) == 0:
    print("You must enter at least one subject.")
    exit()

# 2️⃣ Generate synthetic data
np.random.seed(42)
names = [f"Student_{i+1}" for i in range(num_students)]

data = {"Name": names}
for subject in subjects:
    mean = np.random.randint(55, 75)
    std_dev = np.random.randint(8, 15)
    data[subject] = np.random.normal(loc=mean, scale=std_dev, size=num_students).clip(0, 100)

df = pd.DataFrame(data)

# 3️⃣ Add derived columns
df["Average"] = df[subjects].mean(axis=1)
df["Grade"] = pd.cut(
    df["Average"],
    bins=[0, 50, 60, 70, 80, 100],
    labels=["F", "D", "C", "B", "A"]
)

# 4️⃣ Show summary
print("\n=== Basic Statistics ===")
print(df.describe(numeric_only=True), "\n")

print("=== Grade Distribution ===")
print(df["Grade"].value_counts().sort_index(), "\n")

# 5️⃣ Ask user what to visualize
print("Visualization options:")
print("1. Grade Distribution Bar Chart")
print("2. Subject Correlation Heatmap")
print("3. Top 5 Students by Average")
choice = input("Choose a visualization (1/2/3): ")

if choice == "1":
    plt.figure(figsize=(8, 5))
    df["Grade"].value_counts().sort_index().plot(kind="bar", color="skyblue")
    plt.title("Grade Distribution")
    plt.xlabel("Grade")
    plt.ylabel("Number of Students")
    plt.tight_layout()
    plt.show()

elif choice == "2":
    plt.figure(figsize=(7, 6))
    corr = df[subjects + ["Average"]].corr()
    plt.imshow(corr, cmap="coolwarm", interpolation="none")
    plt.colorbar()
    plt.xticks(range(len(corr)), corr.columns, rotation=45)
    plt.yticks(range(len(corr)), corr.columns)
    plt.title("Subject Correlation Heatmap")
    plt.tight_layout()
    plt.show()

elif choice == "3":
    top_students = df.nlargest(5, "Average")[["Name", "Average", "Grade"] + subjects]
    print("\n=== Top 5 Students ===")
    print(top_students.to_string(index=False))
else:
    print("No visualization selected.")

# 6️⃣ Save results
save = input("\nSave dataset to CSV? (y/n): ").lower()
if save == "y":
    filename = "student_performance.csv"
    df.to_csv(filename, index=False)
    print(f"✅ Data saved to {filename}")

print("\nAnalysis complete. 🎉")
print("Thank you for using the Student Performance Analysis tool!")