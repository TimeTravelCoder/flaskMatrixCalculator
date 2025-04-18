from flask import Flask, request, render_template
from matrix_calculator import parse_element, calculate_matrix_results
from markupsafe import Markup

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            m = int(request.form['rows'])
            n = int(request.form['cols'])
            matrix = []
            errors = []

            # 验证行数和列数是否为正整数
            if m <= 0 or n <= 0:
                return render_template('index.html', error=Markup("行数和列数必须为正整数！"))

            for i in range(m):
                row = []
                for j in range(n):
                    elem = request.form.get(f'matrix[{i}][{j}]', '0').strip()
                    try:
                        row.append(parse_element(elem))
                    except Exception as e:
                        errors.append(f"行{i + 1}列{j + 1}: 无效输入 '{elem}'")
                matrix.append(row)

            if errors:
                return render_template('index.html', error=Markup("<br>".join(errors)))

            matrix_tuple = tuple(tuple(row) for row in matrix)
            results = calculate_matrix_results(matrix_tuple)
            return render_template('index.html', results=results)

        except Exception as e:
            return render_template('index.html', error=Markup(f"系统错误: {str(e)}"))

    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=12345)
    