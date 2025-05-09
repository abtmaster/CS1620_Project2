import csv

def get_best_score(scores: list[int]) -> int:
    """
    Return the highest score
    """
    return max(scores)

def save_result(name: str, scores: list[int], final: int) -> None:
    """
    Save student name, scores, and final to CSV
    """
    file = open("grades.csv", "a", newline="")
    writer = csv.writer(file)
    writer.writerow([name] + scores + [final])
    file.close()
