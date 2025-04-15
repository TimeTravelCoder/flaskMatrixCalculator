from functools import lru_cache
from sympy import Matrix, Rational, latex


def parse_element(elem):
    if '/' in elem:
        num, den = elem.split('/', 1)
        return Rational(num, den)
    try:
        return int(elem)
    except:
        return Rational(elem)


@lru_cache(maxsize=128)
def calculate_matrix_results(matrix_tuple):
    matrix = [list(row) for row in matrix_tuple]
    mat = Matrix(matrix)
    results = {}

    # 计算各项结果
    results['rank'] = mat.rank()
    results['is_square'] = mat.is_square
    if mat.is_square:
        # 直接将行列式转换为 LaTeX 格式
        results['det'] = latex(mat.det())
        results['charpoly'] = latex(mat.charpoly().as_expr())
        try:
            eigen = mat.eigenvects()
            results['eigen'] = [
                {
                    'value': latex(val.evalf(4)),
                    'multiplicity': mult,
                    'vectors': [latex(vec.normalized()) for vec in vectors]
                } for val, mult, vectors in eigen
            ]
        except Exception as e:
            results['eigen_error'] = str(e)

        # 计算矩阵的逆
        try:
            inv = mat.inv()
            results['inv'] = latex(inv)
        except Exception as e:
            results['inv_error'] = str(e)

        # 谱分解（假设矩阵可对角化）
        try:
            P, D = mat.diagonalize()
            results['spectral_P'] = latex(P)
            results['spectral_D'] = latex(D)
        except Exception as e:
            results['spectral_error'] = str(e)

        # LU 分解
        try:
            L, U, _ = mat.LUdecomposition()
            results['LU_L'] = latex(L)
            results['LU_U'] = latex(U)
        except Exception as e:
            results['LU_error'] = str(e)
    else:
        results['det'] = None
        results['inv'] = None
        results['spectral_P'] = None
        results['spectral_D'] = None
        results['LU_L'] = None
        results['LU_U'] = None

    # 计算 RREF 并转为 LaTeX
    rref = mat.rref()[0]
    results['rref'] = latex(rref)
    results['original'] = latex(mat)

    return results
    