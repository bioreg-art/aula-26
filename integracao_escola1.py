import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
from mysql.connector import Error



# 1) Cursos (ids gerados: 1, 2, 3)
cursos = [
    # (nome_curso, carga_horaria, turno)
    ('Informática',    800,  'Manhã'),
    ('Administração',  1000, 'Noite'),
    ('Enfermagem',     1200, 'Tarde'),
]

# 2) Alunos (ids gerados: 1 a 10) — o último campo é o id_curso (FK)
# 1 = Informática, 2 = Administração, 3 = Enfermagem
alunos = [
    # (nome, cpf, data_nascimento, email, telefone, data_matricula, id_curso)
    ('Ana Souza',      '11122233344', '2005-03-14', 'ana@email.com',     '21999990001', '2026-02-01', 1),  # id 1
    ('Bruno Lima',     '22233344455', '2004-07-22', 'bruno@email.com',   '21999990002', '2026-02-01', 1),  # id 2
    ('Carla Mendes',   '33344455566', '2003-11-05', 'carla@email.com',   '21999990003', '2026-02-03', 2),  # id 3
    ('Diego Ferreira', '44455566677', '2006-01-30', 'diego@email.com',   '21999990004', '2026-02-05', 3),  # id 4
    ('Joana Ribeiro',  '55566677788', '2005-04-21', 'joana@email.com',   '21999990005', '2026-02-07', 1),  # id 5
    ('Lucas Martins',  '66677788899', '2004-09-10', 'lucas@email.com',   '21999990006', '2026-02-07', 1),  # id 6
    ('Mariana Costa',  '77788899900', '2003-12-02', 'mariana@email.com', '21999990007', '2026-02-10', 3),  # id 7
    ('Pedro Alves',    '88899900011', '2006-06-18', 'pedro@email.com',   '21999990008', '2026-02-10', 2),  # id 8
    ('Rafaela Nunes',  '99900011122', '2005-08-25', 'rafaela@email.com', '21999990009', '2026-02-12', 3),  # id 9
    ('Thiago Rocha',   '10120230344', '2004-02-14', 'thiago@email.com',  '21999990010', '2026-02-12', 1),  # id 10
]

# 3) Disciplinas (ids gerados: 1 a 6) — o último campo é o id_curso (FK)
disciplinas = [
    # (nome_disciplina, carga_horaria, id_curso)
    ('Lógica de Programação', 80, 1),  # id 1
    ('Banco de Dados',        60, 1),  # id 2
    ('Gestão Financeira',     60, 2),  # id 3
    ('Marketing',             40, 2),  # id 4
    ('Anatomia',              80, 3),  # id 5
    ('Farmacologia',          60, 3),  # id 6
]

# 4) Notas — cada aluno recebe nota nas disciplinas do seu curso
notas = [
    # (id_aluno, id_disciplina, nota, data_avaliacao)
    # Informática (alunos 1, 2, 5, 6, 10 | disciplinas 1 e 2)
    (1, 1, 8.5, '2026-06-30'), (1, 2, 9.0, '2026-06-30'),
    (2, 1, 7.0, '2026-06-30'), (2, 2, 6.5, '2026-06-30'),
    (5, 1, 9.5, '2026-06-30'), (5, 2, 8.0, '2026-06-30'),
    (6, 1, 6.0, '2026-06-30'), (6, 2, 7.5, '2026-06-30'),
    (10, 1, 8.0, '2026-06-30'), (10, 2, 8.5, '2026-06-30'),
    # Administração (alunos 3, 8 | disciplinas 3 e 4)
    (3, 3, 7.5, '2026-06-30'), (3, 4, 8.0, '2026-06-30'),
    (8, 3, 6.5, '2026-06-30'), (8, 4, 9.0, '2026-06-30'),
    # Enfermagem (alunos 4, 7, 9 | disciplinas 5 e 6)
    (4, 5, 9.0, '2026-06-30'), (4, 6, 8.5, '2026-06-30'),
    (7, 5, 7.0, '2026-06-30'), (7, 6, 6.0, '2026-06-30'),
    (9, 5, 8.5, '2026-06-30'), (9, 6, 9.5, '2026-06-30'),
]

try:

    #1)Conexão com o banco "escola"do XAMPP

    conexao = mysql.connector.connect(
    host='localhost',   #servidor local do XAMPP
    user='root',        #usuário padrão do XAMPP
    password='',        #senha vazia (padrão do XAMPP)
    database='escola',  #banco criado com o banco_escola.sql
    )

    if conexao.is_connected():
        print ("Conectado com sucesso!")

        cursor = conexao.cursor()

        insert = [
            ("cursos",
            "INSERT IGNORE INTO cursos (nome_curso, carga_horaria, turno)"
            "VALUES(%s, %s, %s)",
            cursos),
            ("alunos",
            "INSERT IGNORE INTO alunos"
            "(nome, cpf, data_nascimento, email, telefone, data_matricula, id_curso)"
            "VALUES(%s, %s, %s, %s, %s, %s, %s)",
            alunos),
            ("disciplinas",
             "INSERT IGNORE INTO disciplinas (nome_disciplina, carga_horaria, id_curso)"
             "VALUES (%s, %s, %s)",
            disciplinas),
            ("notas",
             "INSERT IGNORE INTO notas (id_aluno, id_disciplina, nota, data_avaliacao)"
             "VALUES (%s, %s, %s, %s)",
             notas),
             ]

        for tabela, sql, valores in insert:
            cursor.executemany(sql, valores)
            conexao.commit()
            print(f"{tabela}: {cursor.rowcount} linha(s) inserida(s)")

        consulta = """
            SELECT a.id_aluno, a.nome, c.nome_curso, c.turno,
            d.nome_disciplina, n.nota, n.data_avaliacao
            FROM notas n
            INNER JOIN alunos      a ON n.id_aluno = a.id_aluno
            INNER JOIN disciplinas d ON n.id_disciplina = d.id_disciplina
            INNER JOIN cursos      c ON a.id_curso      = c.id_curso
            ORDER BY c.nome_curso, a.nome, d.nome_disciplina
       """
        cursor.execute(consulta)

        df = pd.DataFrame(cursor.fetchall(), columns=cursor.column_names)

        df["nota"] = df['nota'].astype(float)

        print("\nDataFrame (notas + alunos + disciplinas + cursos):")
        print(df)

    df.to_csv("notas_alunos.csv", index=False, encoding="utf-8-sig")
    print("\nArquivo notas_alunos,csv gerado!")


                  
except Error  as e: 
    print(f"Erro ao conectar ou executar: {e}")

finally:
    if 'cursor' in locals():
        try:
            cursor.close()
        except Exception:
            pass
    if 'conexao' in locals () and conexao.is_connected():
        conexao.close()
        print("Conexão encerrada")

if 'df'in locals() and not df.empty:

    #Grafico 1: quantos alunos há em cada curso
    #nunque(conta cada aluno uma vez só (ele aparece uma vez por nota)
    alunos_por_curso = df.groupby("nome_curso")["id_aluno"].nunique().sort_values()

    # Gráfico 2: média de notas em cada disciplina
    media_por_disciplina = df.groupby("nome_disciplina")["nota"].mean().sort_values()

    # Uma figura com dois gráficos lado a lado
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))

    bars1 =ax1.barh(alunos_por_curso.index, alunos_por_curso.values, color="#2a7ab9")
    ax1.bar_label(bars1, padding=3)
    ax1.set_title("Alunos matriculados por curso")
    ax1.set_label("Quantidade de alunos")
    ax1.set_xlim(0, alunos_por_curso.max() +1)  #espaço para o rótulo

    bars2 = ax2.barh(media_por_disciplina.index, media_por_disciplina.values, color="#2a7ab9")
    ax2.bar_label(bars2, fmt="%.2f", padding=3)
    ax2.set_title("Media das notas por disciplina")
    ax2.set_label("Nota média(0 a 10)")
    ax2.set_xlim(0, 10.5)

    plt.tight_layout()
    plt.savefig("graficos_escola.png", dpi=150)   #salva a imagem
    plt.show()
        