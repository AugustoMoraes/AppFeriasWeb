from pathlib import Path
from typing import List

from sqlalchemy import create_engine, String, Boolean, Integer, select, ForeignKey
from  sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session, relationship

from werkzeug.security import generate_password_hash, check_password_hash

pasta_atual = Path(__file__).parent
PATH_TO_BD = pasta_atual / 'bd_usuarios.sqlite'

class Base(DeclarativeBase):
    pass

class UsuarioFerias(Base):
    __tablename__ = 'usuarios_ferias'

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(30))
    senha: Mapped[str] = mapped_column(String(128))
    email: Mapped[str] = mapped_column(String(30))
    acesso_gestor: Mapped[bool] = mapped_column(Boolean, default= False)
    inicio_na_empresa: Mapped[str] = mapped_column(String(30))
    eventos_ferias: Mapped[List['EventosFerias']] = relationship(
        back_populates='parent',
        lazy='subquery'
    )

    def __repr__(self):
        return f'Usuario({self.id=}, {self.nome=})'

    def define_senha(self, senha):
        self.senha = generate_password_hash(senha)

    def verifica_senha(self, senha):
        return check_password_hash(self.senha, senha)

class EventosFerias(Base):
    __tablename__ = 'eventos_ferias'

    id: Mapped[int] = mapped_column(primary_key=True)
    parent_id: Mapped[int] = mapped_column(ForeignKey('usuarios_ferias.id'))
    parent: Mapped['UsuarioFerias'] = relationship(lazy="subquery")
    inicio_ferias: Mapped[str] = mapped_column(String(30))
    fim_ferias: Mapped[str] = mapped_column(String(30))
    total_dias: Mapped[int] = mapped_column(Integer())


engine = create_engine(f'sqlite:///{PATH_TO_BD}')
Base.metadata.create_all(bind=engine)

#CRUD
def cria_usuarios(
        nome,
        senha,
        email,
        #acesso_gestor = False
        **kwargs
):
    with Session(bind=engine) as session:
        usuario = UsuarioFerias(
            nome = nome,
            email = email,
            #acesso_gestor = acesso_gestor
            **kwargs
        )
        usuario.define_senha(senha)
        session.add(usuario)
        session.commit()
def ler_todos_usuarios():
    with Session(bind=engine) as session:
        comando_sql = select(UsuarioFerias)
        usuarios = session.execute(comando_sql).fetchall()
        usuarios = [user[0] for user in usuarios]
        return usuarios

def ler_usuario_por_id(id):
    with Session(bind=engine) as session:
        comando_sql = select(UsuarioFerias).filter_by(id = id)
        usuario = session.execute(comando_sql).fetchall()
        return usuario[0][0]

def modifica_usuario(
        id,
        **kwargs):
    with Session(bind=engine) as session:
        comando_sql = select(UsuarioFerias).filter_by(id = id)
        usuarios = session.execute(comando_sql).fetchall()
        for usuario in usuarios:
            for key, value in kwargs.items():
                if key == 'senha':
                    usuario[0].define_senha(value)
                else:
                    setattr(usuario[0], key, value)

        session.commit()

def deleta_usuario(id):
    with Session(bind=engine) as session:
        comando_sql = select(UsuarioFerias).filter_by(id = id)
        usuarios = session.execute(comando_sql).fetchall()
        for usuario in usuarios:
            session.delete(usuario[0])

        session.commit()

if __name__ == '__main__':

    cria_usuarios(
        'Anna Maria',
        senha= 'annamaria',
        email = 'annao@gmail.com',
        # acesso_gestor= True,
        inicio_na_empresa = '2023-01-01'
    )
    # cria_usuarios(
    #     'Ryan Moraes',
    #     senha= 'ryanzinho',
    #     email = 'ryan@gmail.com',
    #     acesso_gestor= True,
    #     inicio_na_empresa = '2023-01-01'
    # )

    # usuarios = ler_todos_usuarios()
    #
    # usuario_0 = usuarios[0]
    # print(usuario_0.nome, usuario_0.email, usuario_0.senha)

    # usuario_augusto = ler_usuario_por_id(1)
    #
    # print(usuario_augusto.nome, usuario_augusto.email, usuario_augusto.senha)


    # modifica_usuario(id = 1, email= 'guto_moraes@gmail.com')
    # modifica_usuario2(id = 2, nome = 'Ryan Nonato Moraes', acesso_gestor = True, senha = 'ryan1234')


    # deleta_usuario(id = 5)
    # deleta_usuario(id=6)
    # deleta_usuario(id=7)

    # verificar se a senha está correta

    # usuario = ler_usuario_por_id(id = 1)
    # print(usuario.verifica_senha('dsadfAS'))