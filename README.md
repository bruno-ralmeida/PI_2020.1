# <h1> Projeto Integrado 2020/1 </h1>
<h3>Especificações</h3>
<h3> Banco de dados: SQLite. </h3>
<h3> Django versão 3.0.5. </h3>

<h3> Para iniciar o servidor do projeto: </h3>
*É necessário instalar o Django.

<code> pip install Django </code>
<p> - Abrir o projeto no terminal e inserir o seguinte comando: </p>
<code> python manage.py runserver </code>

<h3> Para visuliazar a pagina de administrador (Django admin)</h3>
Incluir um super usuário: <br>
<b> Linha de comando:<b>
<code> python manage.py createsuperuser </code> <br>
URL de acesso:
<code> localhost:8000/admin </code>


<p> Se incluir uma classe em arquivo <b> models.py </b> é necessário informar no arquivo <b> admin.py </b> para que seja possível visualizar no Django admin. </p>

<h1> Estrutura de pastas </h1>

<ul>
    <p> * Pasta de configurações do projeto.</p>
    <li> <b> _projeto_2020_01 </b></li> 
    <p> * Pasta de apps do projeto,onde está separado cada módulo e funções de cada classe.</p>
    <li> <b> app </b>
        <ul>
            <li>atendente</li>
            <li>consulta_exame</li>
            <li>exames</li>
            <li>medicos</li>
            <li>paciente</li>
            <li>usuarios</li>
        </ul>
    </li> 
    <p> * Pasta para armazenar fotos e pdfs do projeto.</p>
    <li><b> media </b></li> 
    <p> * Pasta de arquivos estáticos (JS,CSS,IMAGES).</p>
    <li><b> static </b></li>
    <p> * Pasta de arquivos HTML que seram mostrados para o usuário.</p>
    <li><b> templates </b></li>
</ul>


<h6>ATENÇÃO</h6>
<p> Caso seja necessário alterar a estrutura de pasta, sempre verificar o arquivo <code> settings.py </code> do projeto</p>
