import sys


def read_input_file(filename):
    with open(filename, 'r', encoding='utf-8-sig') as file:
        lines = file.readlines()

    u, m = map(int, lines[0].split())
    data = []
    for line in lines[1:]:
        values = list(map(int, line.split()))
        data.append(values)

    return u, m, data


def count_inversions(arr):
    def merge_and_count(arr, temp_arr, left, mid, right):
        i, j, k = left, mid + 1, left
        inv_count = 0

        while i <= mid and j <= right:
            if arr[i] <= arr[j]:
                temp_arr[k] = arr[i]
                i += 1
            else:
                temp_arr[k] = arr[j]
                inv_count += (mid - i + 1)
                j += 1
            k += 1

        while i <= mid:
            temp_arr[k] = arr[i]
            i += 1
            k += 1

        while j <= right:
            temp_arr[k] = arr[j]
            j += 1
            k += 1

        for i in range(left, right + 1):
            arr[i] = temp_arr[i]

        return inv_count

    def merge_sort_and_count(arr, temp_arr, left, right):
        inv_count = 0
        if left < right:
            mid = (left + right) // 2
            inv_count += merge_sort_and_count(arr, temp_arr, left, mid)
            inv_count += merge_sort_and_count(arr, temp_arr, mid + 1, right)
            inv_count += merge_and_count(arr, temp_arr, left, mid, right)
        return inv_count

    return merge_sort_and_count(arr, arr.copy(), 0, len(arr) - 1)


def calculate_similarity(u, m, data, x):
    reference_order = {movie: rank for rank, movie in enumerate(data[x - 1][1:])}
    similarities = []

    for user in data:
        if user[0] == x:
            continue

        try:
            user_order = [reference_order[movie] for movie in user[1:]]
        except KeyError:
            print(f"Помилка: Невідповідність у вподобаннях користувача {user[0]}")
            continue

        print(f"Користувач {user[0]}: {user_order}")  # Діагностика
        inversions = count_inversions(user_order)
        print(f"Інверсії для {user[0]}: {inversions}")  # Діагностика
        similarities.append((user[0], inversions))

    return sorted(similarities, key=lambda pair: pair[1])


def write_output_file(output_filename, x, similarities):
    with open(output_filename, 'w') as file:
        file.write(f"{x}\n")
        for user, score in similarities:
            file.write(f"{user} {score}\n")


def main():
    if len(sys.argv) != 3:
        print("Usage: python script.py input_filename user_x")
        return

    input_filename = sys.argv[1]
    try:
        x = int(sys.argv[2])
    except ValueError:
        print("Помилка: x має бути цілим числом")
        return

    u, m, data = read_input_file(input_filename)
    if not (1 <= x <= u):
        print("Помилка: x виходить за межі кількості користувачів")
        return

    output_filename = input_filename.replace('.txt', '_output.txt')
    similarities = calculate_similarity(u, m, data, x)
    write_output_file(output_filename, x, similarities)
    print(f"Output saved to {output_filename}")


if __name__ == "__main__":
    main()
