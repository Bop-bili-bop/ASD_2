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


def sort_and_count_inv(arr):
    if len(arr) == 1:
        return arr, 0

    mid = len(arr) // 2
    left_part = arr[:mid]
    right_part = arr[mid:]

    L, x = sort_and_count_inv(left_part)
    R, y = sort_and_count_inv(right_part)
    merged, z = merge_and_count_split_inv(L, R)

    return merged, x + y + z


def merge_and_count_split_inv(L, R):
    n1, n2 = len(L), len(R)
    L_ext = L + [float('inf')]
    R_ext = R + [float('inf')]

    i = j = count = 0
    A = []

    for _ in range(n1 + n2):
        if L_ext[i] <= R_ext[j]:
            A.append(L_ext[i])
            i += 1
        else:
            A.append(R_ext[j])
            count += n1 - i
            j += 1

    return A, count


def calculate_similarity(u, m, data, x):
    user_index = x - 1
    order_x = list(range(m))
    order_x.sort(key=lambda j: data[user_index][j + 1])

    similarities = []

    for i in range(u):
        if i == user_index:
            continue

        user_order = [data[i][j + 1] for j in order_x]
        _, inversions = sort_and_count_inv(user_order)
        similarities.append((i + 1, inversions))

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
